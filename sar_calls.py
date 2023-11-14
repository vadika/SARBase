from app import app, db
from flask import request, redirect, flash, render_template, url_for, jsonify
from flask_login import login_required, current_user
from dateutil import parser
from models import SARCall, Comment,  GPSTrack, SARCategory, SARStatus, User


@app.route('/create_sar', methods=['GET', 'POST'])
@login_required
def create_sar():
    categories = SARCategory.query.all()
    statuses = SARStatus.query.order_by('id').all()

    if request.method == 'POST':
        start_date = parser.parse(request.form.get('start_date'))
        category = request.form.get('category')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        status = request.form.get('status')
        title = request.form.get('title')
        # gpx_data_list = request.form.getlist('gpx_data[]')
        # gpx_color_list = request.form.getlist('gpx_color[]')

        # for data, color in zip(gpx_data_list, gpx_color_list):
        #     track = GPSTrack(data=data, color=color, sar_call=new_sar_call)
        #     db.session.add(track)

        new_sar_call = SARCall(
            start_date=start_date,
            category=category,
            latitude=latitude,
            longitude=longitude,
            search_manager_id=current_user.id,
            status=status,
            title=title,
            description=request.form.get('description'),
            description_hidden=request.form.get('description_hidden'),
            # gpx_data=gpx_data_list,
            # gpx_color_list=gpx_color_list,
        )
        db.session.add(new_sar_call)
        db.session.commit()
        flash('SAR call created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_sar.html', categories=categories, statuses=statuses)


@app.route('/list_sar')
@login_required
def list_sar():
    sar_calls = SARCall.query.join(User, SARCall.search_manager_id == User.id).join(SARCategory, SARCall.category == SARCategory.id).add_columns(SARCategory, User, SARCall).all()
    return render_template('list_sar.html', sar_calls=sar_calls)


@app.route('/edit_sar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sar(id):
    sar_call = SARCall.query.get_or_404(id)
    categories = SARCategory.query.all()
    statuses = SARStatus.query.order_by('id').all()

    if request.method == 'POST':
        sar_call.start_date = parser.parse(request.form.get('start_date'))
        if request.form.get('finish_date'):
            sar_call.finish_date = parser.parse(request.form.get('finish_date'))
        sar_call.category = request.form.get('category')
        sar_call.latitude = request.form.get('latitude')
        sar_call.longitude = request.form.get('longitude')
        sar_call.status = request.form.get('status')
        sar_call.result = request.form.get('result')
        sar_call.title = request.form.get('title')
        sar_call.description = request.form.get('description')
        sar_call.description_hidden = request.form.get('description_hidden')
        # sar_call.gpx_data = request.form.get('gpx_data')


        db.session.commit()
        flash('SAR call updated successfully!', 'success')
        return redirect(url_for('list_sar'))

    if sar_call.start_date:
        sar_call.start_date = sar_call.start_date.strftime('%Y-%m-%d')
    if sar_call.finish_date:
        sar_call.finish_date = sar_call.finish_date.strftime('%Y-%m-%d')

    return render_template('edit_sar.html', sar_call=sar_call,categories=categories, statuses=statuses)



@app.route('/sar_details/<int:id>')
def sar_details(id):
    sar = SARCall.query.get_or_404(id)  # Fetch the SARCall record or return 404
    return render_template('sar_details.html', sar=sar)



@app.route('/delete_sar/<int:id>')
@login_required
def delete_sar(id):
    sar_call = SARCall.query.get_or_404(id)
    db.session.delete(sar_call)
    db.session.commit()
    flash('SAR call record deleted successfully!', 'success')
    return redirect(url_for('list_sar'))


@app.route('/add_comment/<int:sar_call_id>', methods=['POST'])
@login_required
def add_comment(sar_call_id):
    text = request.form.get('text')
    gpx_file = request.files.get('gpx_file')
    gpx_data = gpx_file.read().decode("utf-8") if gpx_file else None
    comment = Comment(text=text, gpx_data=gpx_data, user_id=current_user.id, sar_call_id=sar_call_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('sar_details', id=sar_call_id))


@app.route('/edit_comment/<int:comment_id>', methods=['POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    # Permission checks...

    comment_text = request.form.get('comment')
    comment.text = comment_text
    db.session.commit()

    # return jsonify(success=True)  # or return relevant response
    return redirect(url_for('sar_details', id=comment.sar_call_id))

@app.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    # if current_user.id != comment.user_id and current_user.id != 1 and current_user.id != comment.sar_call.user_id:
    #     abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('sar_details', id=comment.sar_call_id))

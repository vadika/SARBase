from dateutil import parser
from flask import request, redirect, flash, render_template, url_for, jsonify, Response
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

from app import app, db
from models import SARCall, Comment, GPSTrack, SARCategory, SARStatus, User, Role, SARResult


@app.route('/create_sar', methods=['GET', 'POST'])
@login_required
def create_sar():
    categories = SARCategory.query.all()
    statuses = SARStatus.query.order_by('id').all()
    managers = User.query.join(Role).filter(or_(Role.name == 'search manager', Role.name == 'admin')).all()

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
            coordination_officer_id=current_user.id,
            status=status,
            title=title,
            description=request.form.get('description'),
            description_hidden=request.form.get('description_hidden'),
            search_officer_id=request.form.get('search_manager_id')
        )
        db.session.add(new_sar_call)
        db.session.commit()
        flash('SAR call created successfully!', 'success')
        return redirect(url_for('list_sar'))

    return render_template('create_sar.html', categories=categories, statuses=statuses, managers=managers)


@app.route('/list_sar')
def list_sar():
    is_logged_in = current_user.is_authenticated
    search_officer = aliased(User)
    coordination_officer = aliased(User)

    sar_calls = (SARCall.query
                 .outerjoin(search_officer, and_ (SARCall.search_officer_id == search_officer.id, SARCall.search_officer_id != None))
                 .join(coordination_officer, SARCall.coordination_officer_id == coordination_officer.id)
                 .join(SARCategory, SARCall.category == SARCategory.id)
                 .join(SARStatus, SARCall.status == SARStatus.id)
                 .add_columns(SARCategory, SARCall, SARStatus)
                 .all())

    return render_template('list_sar.html', sar_calls=sar_calls, is_logged_in=is_logged_in)


@app.route('/edit_sar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sar(id):
    sar_call = SARCall.query.get_or_404(id)
    categories = SARCategory.query.all()
    statuses = SARStatus.query.order_by('id').all()
    managers = User.query.join(Role).filter(or_(Role.name == 'search manager', Role.name == 'admin')).all()

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

        db.session.commit()
        flash('SAR call updated successfully!', 'success')
        return redirect(url_for('list_sar'))

    if sar_call.start_date:
        sar_call.start_date = sar_call.start_date.strftime('%Y-%m-%d')
    if sar_call.finish_date:
        sar_call.finish_date = sar_call.finish_date.strftime('%Y-%m-%d')

    return render_template('edit_sar.html', sar_call=sar_call, categories=categories, statuses=statuses,
                           managers=managers)


@app.route('/sar_details/<int:id>')
def sar_details(id):
    is_logged_in = current_user.is_authenticated
    search_officer = aliased(User)
    coordination_officer = aliased(User)

    sar = (SARCall.query
                 .outerjoin(search_officer,
                            and_(SARCall.search_officer_id == search_officer.id, SARCall.search_officer_id != None))
                 .join(coordination_officer, SARCall.coordination_officer_id == coordination_officer.id)
                 .join(SARCategory, SARCall.category == SARCategory.id)
                 .join(SARStatus, SARCall.status == SARStatus.id)
                 .outerjoin(SARResult, and_(SARCall.result == SARResult.id, SARCall.result != None))
                 .add_columns(SARCall, SARCategory, SARStatus, SARResult)
                 .filter(SARCall.id == id).first())

    comments = Comment.query.filter_by(sar_call_id=id).all()

    gpx_files = [id[0] for id in GPSTrack.query.with_entities(GPSTrack.id).filter_by(
        sar_call_id=id).all()]  # Fetch all GPX files for this SARCall
    comments_with_gpx = []

    for comment in comments:
        gpx_tracks = GPSTrack.query.filter_by(comment_id=comment.id).all()
        for track in gpx_tracks:
            comments_with_gpx.append({
                "id": track.id,
                "comment_id": comment.id,
                "name": track.file_name,
                "comment": track.gpx_name
            })

    print(sar)

    return render_template('sar_details.html', sar=sar, gpx_ids=gpx_files, comments_with_gpx=comments_with_gpx,is_logged_in=is_logged_in)


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
    comment = Comment(text=text, user_id=current_user.id, sar_call_id=sar_call_id)
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


@app.route('/upload_gpx', methods=['POST'])
@login_required
def upload_gpx():
    # Retrieve file and other data from the form
    file_name = request.form.get('gpxFileName')
    gpx_file = request.files.get('gpxFile')
    id = request.form.get('commentId')
    sar_id = request.form.get('sarId')

    # You need to implement logic to parse and store the GPX file
    # For example, read the file content
    gpx_data = gpx_file.read()

    # Create a new GPSTrack object and save it
    new_gpx_file = GPSTrack(comment_id=id, sar_call_id=sar_id, file_name=file_name, gpx_data=gpx_data)
    db.session.add(new_gpx_file)
    db.session.commit()

    return jsonify({'message': 'GPX file uploaded successfully'})


@app.route('/get_gpx/<int:gpx_id>')
def get_gpx(gpx_id):
    gpx_file = GPSTrack.query.get_or_404(gpx_id)
    return Response(gpx_file.gpx_data, mimetype='application/gpx+xml')

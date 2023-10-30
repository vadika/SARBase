from app import app, db
from flask import request, redirect, flash, render_template, url_for
from flask_login import login_required, current_user
from dateutil import parser
from models import SARCall
@app.route('/create_sar', methods=['GET', 'POST'])
@login_required
def create_sar():
    if request.method == 'POST':
        start_date = parser.parse(request.form.get('start_date'))
        finish_date = parser.parse(request.form.get('finish_date'))
        category = request.form.get('category')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        gpx_data = request.form.get('gpx_data')

        new_sar_call = SARCall(
            start_date=start_date,
            finish_date=finish_date,
            category=category,
            latitude=latitude,
            longitude=longitude,
            search_manager_id=current_user.id,
            gpx_data=gpx_data
        )
        db.session.add(new_sar_call)
        db.session.commit()
        flash('SAR call created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_sar.html')


@app.route('/list_sar')
@login_required
def list_sar():
    sar_calls = SARCall.query.all()
    return render_template('list_sar.html', sar_calls=sar_calls)


@app.route('/edit_sar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sar(id):
    sar_call = SARCall.query.get(id)
    if request.method == 'POST':
        sar_call.start_date = request.form.get('start_date')
        sar_call.finish_date = request.form.get('finish_date')
        sar_call.category = request.form.get('category')
        sar_call.latitude = request.form.get('latitude')
        sar_call.longitude = request.form.get('longitude')
        sar_call.gpx_data = request.form.get('gpx_data')
        db.session.commit()
        flash('SAR call updated successfully!', 'success')
        return redirect(url_for('list_sar'))
    return render_template('edit_sar.html', sar_call=sar_call)

@app.route('/delete_sar/<int:id>')
@login_required
def delete_sar(id):
    sar_call = SARCall.query.get(id)
    db.session.delete(sar_call)
    db.session.commit()
    flash('SAR call deleted successfully!', 'success')
    return redirect(url_for('list_sar'))


from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from dateutil import parser

from app import app, db
from models import SARCall, SARStatus, SARCategory, User, Role, SARResult


# This Python Flask module provides the functionality to list Search and Rescue (SAR) operations stored in the
# database. Routes included in this file: /list_sar A route that loads and returns the 'list_sar.html' template to
# display SAR operations. /update_sar_list A route that dynamically updates the SAR operations list based on user
# interactions such as filtering and sorting the list. The 'render_sar_list_template' function is a helper function
# that is used by these two routes to reduce code repetition. Functions: render_sar_list_template(template) A shared
# function for the '/list_sar' and '/update_sar_list' routes. It queries the database according to user's selected
# filters and sort orders, and renders the given template with the SAR operation data. It uses a SQLAlchemy query to
# obtain the SAR operation records. The records can be filtered by status and category, and can be sorted by date or
# by operation ID. Parameters: template (str): The name of the HTML template to render. Returns: A rendered Flask
# template, ready to be sent to the client's browser. This module uses a number of models from an imported models
# module: SARCall: A model representing a SAR operation. SARStatus: A model representing possible statuses of a SAR
# operation. SARCategory: A model representing possible categories of a SAR operation thus allowing classification.
# User: A model representing a logged-in user.

@app.route('/list_sar')
def list_sar():
    return render_sar_list_template('list_sar.html')


@app.route('/update_sar_list/')
def update_sar_list():
    return render_sar_list_template('dynamic-sar-list.html')


def render_sar_list_template(template):
    is_logged_in = current_user.is_authenticated
    search_officer = aliased(User)
    coordination_officer = aliased(User)
    categories = SARCategory.query.all()
    statuses = SARStatus.query.all()

    category_id = request.args.get('category')
    sort_order = request.args.get('sort')
    status_id = request.args.get('status')
    query = SARCall.query

    # Filter by status
    if status_id:
        query = query.filter_by(status=status_id)

    # Filter by category
    if category_id:
        query = query.filter_by(category=category_id)

    # Sorting
    if sort_order == 'date_asc':
        query = query.order_by(SARCall.start_date.asc())
    elif sort_order == 'date_desc':
        query = query.order_by(SARCall.start_date.desc())
    # add other sorting options if needed
    else:
        query = query.order_by(SARCall.id.desc())

    sar_calls = (query
                 .outerjoin(search_officer,
                            and_(SARCall.search_officer_id == search_officer.id, SARCall.search_officer_id is not None))
                 .join(coordination_officer, SARCall.coordination_officer_id == coordination_officer.id)
                 .join(SARCategory, SARCall.category == SARCategory.id)
                 .join(SARStatus, SARCall.status == SARStatus.id)
                 .add_columns(SARCategory, SARCall, SARStatus)
                 .all())

    return render_template(template, sar_calls=sar_calls, is_logged_in=is_logged_in,
                           categories=categories,
                           statuses=statuses)


@app.route('/create_sar', methods=['GET', 'POST'])
@login_required
def create_sar():
    categories = SARCategory.query.all()
    statuses = SARStatus.query.order_by('id').all()
    managers = User.query.join(Role).filter(or_(Role.name == 'search officer', Role.name == 'admin')).all()

    if request.method == 'POST':
        start_date = parser.parse(request.form.get('start_date'))
        category = request.form.get('category')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        status = request.form.get('status')
        title = request.form.get('title')

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


@app.route('/edit_sar/<int:sar_id>', methods=['GET', 'POST'])
@login_required
def edit_sar(sar_id):
    sar_call = SARCall.query.get_or_404(sar_id)
    categories = SARCategory.query.all()
    statuses = SARStatus.query.order_by('id').all()
    results = SARResult.query.all()
    search_officers = User.query.join(Role).filter(or_(Role.name == 'search officer', Role.name == 'admin')).all()
    coordination_officers = User.query.join(Role).filter(
        or_(Role.name == 'coordination officer', Role.name == 'admin')).all()

    if request.method == 'POST':
        sar_call.start_date = parser.parse(request.form.get('start_date'))
        if request.form.get('finish_date'):
            sar_call.finish_date = parser.parse(request.form.get('finish_date'))
        sar_call.category = request.form.get('category')
        sar_call.latitude = request.form.get('latitude')
        sar_call.longitude = request.form.get('longitude')
        sar_call.status = request.form.get('status')
        sar_call.result = request.form.get('result')
        if (request.form.get('latitude_found') and request.form.get('longitude_found')
                and request.form.get('latitude_found') != 'None' and request.form.get('longitude_found') != 'None'):
            sar_call.latitude_found = request.form.get('latitude_found')
            sar_call.longitude_found = request.form.get('longitude_found')
        sar_call.title = request.form.get('title')
        sar_call.description = request.form.get('description')
        sar_call.description_hidden = request.form.get('description_hidden')
        sar_call.search_officer_id = request.form.get('search_officer')
        sar_call.coordination_officer_id = request.form.get('coordination_officer')

        db.session.commit()
        flash('SAR call updated successfully!', 'success')
        return redirect(url_for('list_sar'))

    if sar_call.start_date:
        sar_call.start_date = sar_call.start_date.strftime('%Y-%m-%d')
    if sar_call.finish_date:
        sar_call.finish_date = sar_call.finish_date.strftime('%Y-%m-%d')

    return render_template('edit_sar.html', sar_call=sar_call, categories=categories, statuses=statuses,
                           coordination_officers=coordination_officers, results=results,
                           search_officers=search_officers)


@app.route('/delete_sar/<int:sar_id>')
@login_required
def delete_sar(sar_id):
    sar_call = SARCall.query.get_or_404(sar_id)
    db.session.delete(sar_call)
    db.session.commit()
    flash('SAR call record deleted successfully!', 'success')
    return redirect(url_for('list_sar'))

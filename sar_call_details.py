import os

from PIL import Image
from flask import request, redirect, flash, render_template, url_for, jsonify, Response, send_from_directory
from flask_login import login_required, current_user
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename

from app import app, db
from models import SARCall, Comment, GPSTrack, SARCategory, SARStatus, User, SARResult, FileAttachment
import base64

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
    comments_with_attachment = []

    for comment in comments:
        gpx_tracks = GPSTrack.query.filter_by(comment_id=comment.id).all()
        for track in gpx_tracks:
            comments_with_gpx.append({
                "id": track.id,
                "comment_id": comment.id,
                "name": track.file_name,
                "comment": track.gpx_name
            })

        attachments = FileAttachment.query.filter_by(comment_id=comment.id).all()
        for attachment in attachments:
            comments_with_attachment.append({
                "id": attachment.id,
                "comment_id": comment.id,
                "file_name": attachment.file_name,
                "file_type": attachment.file_type,
                "file_path": attachment.file_path,
                "is_image": attachment.is_image()
            })

    return render_template('sar_details.html', sar=sar,
                           gpx_ids=gpx_files,
                           comments_with_gpx=comments_with_gpx,
                           comments_with_attachment=comments_with_attachment,
                           is_logged_in=is_logged_in, filename_prefix=app.config['STORAGE_DIR'] + '/')


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

    # delete associated GPX files
    gpx_tracks = GPSTrack.query.filter_by(comment_id=comment.id).all()
    for track in gpx_tracks:
        db.session.delete(track)

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


@app.route('/delete_gpx/<int:gpx_id>/<int:sar_id>', methods=['GET'])
@login_required
def delete_gpx(gpx_id, sar_id):
    gpx_file = GPSTrack.query.get_or_404(gpx_id)
    db.session.delete(gpx_file)
    db.session.commit()
    flash('GPX file deleted successfully!', 'success')
    return redirect(url_for('sar_details', id=sar_id))


def custom_flask_response(data, status=200, headers=None, mimetype='application/json'):
    # TODO: fix filename encoding -- need to support unicode

    if headers is not None:
        new_headers = {}
        for key, value in headers.items():
            new_key = base64.b64encode(str(key).encode('utf-8'))
            new_value = base64.b64encode(str(value).encode('utf-8'))
            new_headers[new_key] = new_value
        headers = new_headers

    return Response(data, status=status, headers=headers, mimetype=mimetype)


@app.route('/get_gpx/<int:gpx_id>')
def get_gpx(gpx_id):
    gpx_file = GPSTrack.query.get_or_404(gpx_id)

    return custom_flask_response(gpx_file.gpx_data, mimetype='application/gpx+xml',
                    headers={'Content-Disposition': 'attachment;filename=' + gpx_file.file_name + '.gpx'})


@app.route('/save_track', methods=['POST'])
@login_required
def save_track():
    # Get the track data from the POST request
    track_data = request.form.get('track_data')  # Replace with the actual field name for the track data

    # Get the track name and comment from the POST request
    track_name = request.form.get('track_name')
    track_comment = request.form.get('track_comment')
    sar_id = request.form.get('sar_call_id')

    # Create a new Comment instance associated with the track and save it to the database
    new_comment = Comment(sar_call_id=sar_id, user_id=current_user.id, text=track_comment)

    db.session.add(new_comment)
    db.session.commit()

    # Create a new GPXTrack instance and save it to the database
    new_track = GPSTrack(comment_id=new_comment.id, sar_call_id=sar_id, file_name=track_name, gpx_data=track_data)
    db.session.add(new_track)
    db.session.commit()

    return jsonify(success=True, message="Track saved successfully")


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_thumbnail(input_path, output_path, base_width=150):
    img = Image.open(input_path)
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((base_width, h_size))
    img.save(output_path)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    sar_id = request.form.get('sarId')
    comment_id = request.form.get('commentId')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['STORAGE_DIR'], filename)
        file.save(file_path)
        # After saving the original file
        if file.content_type.startswith('image/'):
            thumbnail_path = os.path.join(app.config['STORAGE_DIR'], "thumbs", filename)
            create_thumbnail(file_path, thumbnail_path)
        file_type = file.content_type

        # Create a new file attachment record
        attachment = FileAttachment(file_name=filename, file_type=file_type, file_path=file_path, comment_id=comment_id)
        db.session.add(attachment)
        db.session.commit()
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('sar_details', id=sar_id))
        # return jsonify(success=True, message='File uploaded successfully')

    flash('File upload failed!', 'danger')
    return redirect(url_for('sar_details', id=sar_id))


@app.route('/delete_file/<int:attachment_id>', methods=['GET', 'POST'])
def delete_file(attachment_id):
    attachment = FileAttachment.query.get(attachment_id)
    sar_id = request.form.get('sarId')

    if attachment:
        try:
            os.remove(os.path.join(app.config['STORAGE_DIR'], attachment.file_name))
            try:
                os.remove(os.path.join(app.config['STORAGE_DIR'], 'thumbs', attachment.file_name))  # If a thumbnail exists
            except:
                flash('File thumbnail not deleted', 'danger')
            db.session.delete(attachment)
            db.session.commit()

            flash('File deleted successfully!', 'danger')
            return redirect(url_for('sar_details', id=sar_id))
        except Exception as e:
            return redirect(url_for('sar_details', id=sar_id))
    flash('File  not deleted', 'danger')
    return redirect(url_for('sar_details', id=sar_id))


@app.route('/download_attachment/<string:filename>')
@login_required
def download_attachment(filename):
    # Implement code to serve the attachment for download
    # You may use Flask's send_from_directory or send_file
    return send_from_directory(app.config['STORAGE_DIR'], filename)


@app.route('/download_thumb/<string:filename>')
@login_required
def download_thumb(filename):
    # Implement code to serve the attachment for download
    # You may use Flask's send_from_directory or send_file
    return send_from_directory(app.config['STORAGE_DIR'] + "/thumbs/", filename)

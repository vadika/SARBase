from app import app
from flask import render_template
from flask_login import login_required, current_user


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.full_name)

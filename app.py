from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

import models
import admin
import login
import sar_calls
import dashboard


@app.route('/')
def hello_world():  # put application's code here
    return  redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run()

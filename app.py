import os
from flask import Flask, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from sqlalchemy import MetaData


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


def get_locale():
    return session.get('language', request.accept_languages.best_match(['en', 'ru', 'et', 'lv', 'fi']))



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sarbaseuser:password@localhost/sarbaseapp'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://sarbaseuser:password@localhost/sarbaseapp')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel= Babel(app)
babel.init_app(app, locale_selector=get_locale)
db = SQLAlchemy(app, metadata=metadata)
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


@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    session['language'] = lang_code
    return redirect(request.referrer or url_for('dashboard'))




if __name__ == '__main__':
    app.run()

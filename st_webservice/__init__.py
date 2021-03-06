"""
The flask application package.
"""

import os
from flask import Flask
from st_webservice.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from celery import Celery
from st_webservice.config import config
from st_webservice.flask_util_js import FlaskUtilJs
from flask_s3 import FlaskS3

import flask_s3

fujs = FlaskUtilJs()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
lm = LoginManager()
s3 = FlaskS3()
lm.login_view = 'auth.login'
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    lm.init_app(app)
    fujs.init_app(app)
    s3.init_app(app)
    celery.conf.update(app.config)

    
    

    from st_webservice.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from st_webservice.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from st_webservice.main import bp as main_bp
    app.register_blueprint(main_bp)

    from st_webservice.model import bp as model_bp
    app.register_blueprint(model_bp)


    return app


import st_webservice.main.views, st_webservice.models
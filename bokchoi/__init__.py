import os
import psycopg2
from flask import Flask
from flask_s3 import FlaskS3
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# s3 = FlaskS3()

app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY_ID = os.environ.get('AWS_SECRET_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
S3_LOCATION = f'http://{AWS_STORAGE_BUCKET_NAME}/static/post_pics.s3.amazonaws.com/'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
app.config['SECRET_KEY'] = SECRET_KEY
app.config['FLASKS3_BUCKET_NAME'] = AWS_STORAGE_BUCKET_NAME
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Code Institute\\Project 4\\bokchoi\\bokchoi\\site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///C:\\Code Institute\\Project 4\\bokchoi\\bokchoi\\site.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from bokchoi import routes
import bokchoi.models

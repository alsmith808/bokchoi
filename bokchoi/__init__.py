import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Code Institute\\Project 4\\bokchoi\\bokchoi\\site.db'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# if __name__ == '__main__':
#     manager.run()

from bokchoi import routes
import bokchoi.models

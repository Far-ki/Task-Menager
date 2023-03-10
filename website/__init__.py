from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__,
            static_url_path='', 
            static_folder='./static',
            template_folder='./templates')
    app.config['SECRET_KEY'] = 'fsjkfsadassff'                          #admin - pswd database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/sampledb'


    db.init_app(app)
    from .models import User
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    return app



def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database')

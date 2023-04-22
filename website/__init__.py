from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

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

   

    from .models import User,Event
    from .views import views
    from .auth import auth
    from .event import event
    from .group import group
    from .panel import panel
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(event,url_prefix='/')
    app.register_blueprint(group,url_prefix='/')
    app.register_blueprint(panel,url_prefix='/')
    create_database(app)


    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database')



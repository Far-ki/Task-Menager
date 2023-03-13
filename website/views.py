from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User

views = Blueprint('views',__name__)


@views.route('/')
def home():
    # query the database for all users
    users = User.query.all() # <-- do wywalenia po zajeciach, bo rejestracja ogarnieta

    return render_template('home.html', users=users,user = current_user)



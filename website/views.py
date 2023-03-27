from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User

views = Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template('home.html',user = current_user)

@views.route('/calendar')
def calendar():
    return render_template('calendar.html',user = current_user)


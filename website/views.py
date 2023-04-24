from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import asc
from . import db
from .models import User,Group,Event
from datetime import datetime
from flask import jsonify
import json

views = Blueprint('views',__name__)


@views.route('/')
def home():
    if current_user.is_authenticated:
        personalTop5 = Event.query.filter_by(user_id=current_user.id).filter(Event.start >= datetime.today()).order_by(asc(Event.start)).limit(5).all()
        return render_template('home.html',user = current_user,personalTop5=personalTop5)
    else:
        return render_template('home.html',user=current_user)

@views.route('/calendar')
def calendar():
    return render_template('calendar.html',user = current_user)

@views.route('/groups')
def groups():
    user=current_user
    user_groups = current_user.groups
    return render_template('groups.html',user=user,user_groups=user_groups)




@views.route('/adminPanel')
@login_required
def view_admin_panel():
    group_id = request.args.get('group_id')
    group = Group.query.get(group_id)
    users = group.user.all()
    events = Event.query.filter_by(group_id=group_id).all()
    event_user = db.session.query(User.nickname, Event.title, Event.id).join(User.events).filter(Event.group_id == group_id).all()
    event_user_data = [{"nickname": result.nickname, "title": result.title, "id": result.id} for result in event_user]

    return render_template('adminPanel.html',user=current_user, group=group,users = users, events = events, event_user=event_user_data)


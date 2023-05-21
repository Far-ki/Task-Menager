from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import asc
from . import db

from .models import User,Group,Event,group_membership, Subtask, event_user
from datetime import datetime

from flask import jsonify
import json
views = Blueprint('views',__name__)


@views.route('/')
def home():
    if current_user.is_authenticated:
        subtasks = {}
        now = datetime.now()
        personalTop5 = Event.query.filter_by(user_id=current_user.id,group_id=None).filter(Event.start >= datetime.today()).order_by(asc(Event.start)).limit(5).all()
        for event in personalTop5:
            subtasks[event.id] = Subtask.query.filter_by(event_id=event.id).order_by(asc(Subtask.id)).all()
        return render_template('home.html',user = current_user,personalTop5=personalTop5,subtasks=subtasks,now=now)
    else:
        return render_template('home.html',user=current_user)

@views.route('/calendar')
def calendar():
    return render_template('calendar.html',user = current_user)

@views.route('/group_calendar')
def group_calendar():
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
    users_data = [{"nickname": result.nickname} for result in users]
    events = Event.query.filter_by(group_id=group_id).options(db.subqueryload(Event.subtasks)).all()
    event_user = db.session.query(User.nickname, Event.title, Event.id).join(User.events).filter(Event.group_id == group_id).all()
    event_user_data = [{"nickname": result.nickname, "title": result.title, "id": result.id} for result in event_user]
    my_id = current_user.id
    poss_admin = db.session.query(group_membership).filter_by(user_id=my_id).first()

    event_subtasks = {}
    
    # Loop through events and get subtasks for each event
    for event in events:
        subtasks = Subtask.query.filter_by(event_id=event.id).all()
        subtask_data = [subtask.as_dict() for subtask in subtasks]
        event_subtasks[event.id] = subtask_data

    print(event_subtasks)

    return render_template('adminPanel.html',user=current_user, group=group,users=users, events=events, event_user=event_user_data, poss_admin=poss_admin, users_data=users_data,event_subtasks=event_subtasks)

@views.route('/get_subtasks')
@login_required
def get_subtasks():
    event_id = request.args.get('event_id')
    event = Event.query.get(event_id)
    subtasks = event.subtasks
    subtask_data = [subtask.as_dict() for subtask in subtasks]
    return jsonify(subtask_data)

@views.route('/add_user_to_event', methods=['POST'])
def add_user_to_event():
  nickname = request.form['nickname']
  event_id = request.form['event_id']
  event_id = int(event_id)
  event = Event.query.get(event_id)

  if event is None:
    return jsonify({'success': False, 'error': 'Event not found'})

  user = User.query.filter_by(nickname=nickname).first()

  if user is None:
    return jsonify({'success': False, 'error': 'User not found'})

  event.user_events.append(user)
  db.session.commit()

  return jsonify({'success': True})


@views.route('/remove_user_from_event', methods=['POST'])
def remove_user_from_event():
  nickname = request.form['nickname']
  event_id = request.form['event_id']
  event_id = int(event_id)
  event = Event.query.get(event_id)

  if event is None:
    return jsonify({'success': False, 'error': 'Event not found'})

  user = User.query.filter_by(nickname=nickname).first()

  if user is None:
    return jsonify({'success': False, 'error': 'User not found'})

  event.user_events.remove(user)
  db.session.commit()

  return jsonify({'success': True})

@views.route('/update_subtask', methods=['POST'])
def update_subtask():
    subtask_id = request.json['id']
    is_completed = request.json['is_completed']
    subtask = Subtask.query.get(subtask_id)
    subtask.is_completed = is_completed
    db.session.commit()
    return jsonify({'message': 'Subtask updated successfully.'})
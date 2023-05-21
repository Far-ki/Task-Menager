from .models import Event
from flask import request,jsonify,Blueprint,redirect,url_for,render_template,flash
from . import db
from .models import Subtask,Event
from flask_login import login_user, login_required, logout_user, current_user
event = Blueprint('event', __name__)

@event.route('/events')
def events():
    events = Event.query.filter((Event.user_id == current_user.id) & (Event.group_id.is_(None))).all()
    return jsonify([event.as_dict() for event in events])

@event.route('/group_events')
def group_events():
    group_id = request.args.get('group_id')
    events = Event.query.filter_by(group_id=group_id).all()
    return jsonify([event.as_dict() for event in events])

@event.route('/events_add', methods=['POST'])
def create_event():
    event_title = request.form.get('event_title')
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    description = request.form.get('description')
    completed = request.form.get('is_completed')
    #user_id = 'completed' in request.form
    user_id = current_user.id
    group_id = request.form.get('g_id')
    
    if group_id:
        event = Event(title=event_title, start=date_from, end=date_to, user_id=user_id, group_id=group_id,description=description,completed=completed)
    else:
        event = Event(title=event_title, start=date_from, end=date_to, user_id=user_id,description=description,completed=completed)
        
    db.session.add(event)
    db.session.commit()
    flash('Task created!')

    if group_id:
        return redirect(url_for('views.group_calendar', group_id=group_id))
    else:
        return redirect(url_for('views.calendar'))



@event.route('/events_mod', methods=['POST'])
def update_event():
    group_id = request.form.get('g_id')
    event_id = request.form['event_id']
    event = Event.query.get_or_404(event_id)
    event.title = request.form.get('event_title')
    event.description = request.form.get('description')
    event.start = request.form.get('date_from')
    event.end = request.form.get('date_to')
    event.completed = request.form.get('is_completed')
    db.session.commit()
    if group_id:
        return redirect(url_for('views.group_calendar', group_id=group_id))
    else:
        return redirect(url_for('views.calendar'))


@event.route('/events_del', methods=['POST'])
def delete_event():
    try:
        group_id = request.form.get('g_id')
        event_id = request.form.get('event_id')
        event = Event.query.filter_by(id=event_id).first()

        db.session.query(Subtask).filter(Subtask.event_id == event_id).delete()
        #db.session.commit()
        db.session.delete(event)
        db.session.commit()
    except:
        flash('There is no such record','error')
    if group_id:
        return redirect(url_for('views.group_calendar', group_id=group_id))
    else:
        return redirect(url_for('views.calendar'))

@event.route('/create_subtask', methods=['POST'])
def create_subtask():
    title = request.form.get('subtask-title')
    description = request.form.get('subtask-description')
    event_id = request.form.get('event_id')
    event = Event.query.get_or_404(event_id)
    flash(event_id)

    subtask = Subtask(title=title, description = description, event_id = event_id)

    db.session.add(subtask)
    db.session.commit()

    return redirect(url_for('views.home'))
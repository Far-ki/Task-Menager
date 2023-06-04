from flask import request,jsonify,Blueprint,redirect,url_for,render_template,flash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Group,group_membership,User, event_user,Event,Subtask
from sqlalchemy import update, and_,asc
panel = Blueprint('panel', __name__)
from datetime import datetime



@panel.route('/adminPanel/kick', methods=['POST'])
@login_required
def kick_out_of_group():
    user_id = request.form.get("member_id") #id wyrzucanego
    group_id = request.form.get("some_id")

    user = User.query.filter_by(id=user_id).first() #wyrzucany user
    group = Group.query.filter_by(id=group_id).first()

    my_id = current_user.id

    selfcheck = db.session.query(group_membership).filter_by(user_id=my_id).first()
    if selfcheck.is_admin:
        admincheck = db.session.query(group_membership).filter_by(user_id=user_id).first()
        if admincheck.is_admin:
            flash("You can't kick yourself out of the group")
        else:
            db.session.query(event_user).filter(event_user.c.user_id == user_id).delete()
            group.user.remove(user)
            db.session.commit()
    else:
        flash("You are not an admin to do this!")
    
    return redirect(url_for('views.view_admin_panel',group_id = group_id))


@panel.route('/adminPanel/makeAdmin', methods = ['POST'])
@login_required
def make_admin():
    user_id = request.form.get("member_id")
    group_id = request.form.get("some_id")
    user = User.query.filter_by(id=user_id).first()
    group = Group.query.filter_by(id=group_id).first()

    my_id = current_user.id 

    selfcheck = db.session.query(group_membership).filter_by(user_id=my_id).first()
    if selfcheck.is_admin:
        admincheck = db.session.query(group_membership).filter_by(user_id=user_id).first()
        if admincheck.is_admin == False:
            db.session.query(group_membership).filter(and_(group_membership.c.group_id == group.id, group_membership.c.user_id == user.id)).update({group_membership.c.is_admin: True})
            db.session.commit()
        else:
            flash("Why are you trying to make this person an admin if he already is one")
    else:
        flash("You can't do this!")
    return redirect(url_for('views.view_admin_panel',group_id = group_id))


@panel.route('/adminPanel/showTasks', methods = ['POST'])
@login_required
def show_tasks():
    user_id = current_user.id
    user = User.query.get(user_id)
    group_id = request.form.get('group_id')
    group = Group.query.get(group_id)
    
    if current_user.is_authenticated:
        subtasks = {}
        now = datetime.now()
        personalTop5 = Event.query.filter_by(user_id=current_user.id,group_id=group_id,completed=0).filter(Event.start >= datetime.today()).order_by(asc(Event.start)).limit(5).all()
        for event in personalTop5:
            subtasks[event.id] = Subtask.query.filter_by(event_id=event.id).order_by(asc(Subtask.id)).all()
        return render_template('check.html',user = current_user,personalTop5=personalTop5,subtasks=subtasks,now=now,group = group)


@panel.route('/adminPanel/create_group_subtask', methods=['POST'])
def create_group_subtask():
    title = request.form.get('subtask-title')
    description = request.form.get('subtask-description')
    event_id = request.form.get('event_id')
    group_id = request.form.get('group_id')
    user = current_user

    event = Event.query.get_or_404(event_id)
    group = Group.query.get(group_id)

    subtask = Subtask(title=title, description=description, event_id=event.id)

    db.session.add(subtask)
    db.session.commit()

    subtasks = {}
    now = datetime.now()
    personalTop5 = Event.query.filter_by(user_id=current_user.id,group_id=group_id,completed=0).filter(Event.start >= datetime.today()).order_by(asc(Event.start)).limit(5).all()
    for event in personalTop5:
        subtasks[event.id] = Subtask.query.filter_by(event_id=event.id).order_by(asc(Subtask.id)).all()

    return render_template('check.html',user = user,personalTop5=personalTop5,subtasks=subtasks,now=now,group = group)



@panel.route('/group_history', methods=['POST'])
def group_history():
    if current_user.is_authenticated:
        group_id = request.form.get('group_id')
        group = Group.query.get(group_id)

        subtasks = {}
        now = datetime.now()
        events = Event.query.filter_by(group_id = group_id).filter(Event.completed == 1, Event.user_id==current_user.id).all()
        for event in events:
            subtasks[event.id] = Subtask.query.filter_by(event_id=event.id).order_by(asc(Subtask.id)).all()
        return render_template('group_history.html',user = current_user,events=events,subtasks=subtasks,now=now,group = group)



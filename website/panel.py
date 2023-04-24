from flask import request,jsonify,Blueprint,redirect,url_for,render_template,flash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Group,group_membership,User
from sqlalchemy import update, and_
panel = Blueprint('panel', __name__)




@panel.route('/adminPanel/kick', methods=['POST'])
@login_required
def kick_out_of_group():
    user_id = request.form.get("member_id")
    group_id = request.form.get("some_id")
    # flash(f'user id: {user_id} , group id: {group_id}')

    user = User.query.filter_by(id=user_id).first()
    group = Group.query.filter_by(id=group_id).first()

    my_id = current_user.id

    selfcheck = db.session.query(group_membership).filter_by(user_id=my_id).first()
    if selfcheck.is_admin:
        admincheck = db.session.query(group_membership).filter_by(user_id=user_id).first()
        if admincheck.is_admin:
            flash("You can't kick yourself out of the group")
        else:
            group.user.remove(user)
        # flash(f'{user} with id {user_id} has been deleted from the group')
            db.session.commit()
    else:
        flash("You are not an admin to do this!")
    
    return redirect(url_for('views.view_admin_panel',group_id = group_id))


@panel.route('/adminPanel/makeAdmin', methods = ['POST'])
@login_required
def make_admin():
    user_id = request.form.get("member_id")
    group_id = request.form.get("some_id")
    # flash(f'user id: {user_id} , group id: {group_id}')
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
from .models import Group,group_membership
from flask import request,jsonify,Blueprint,redirect,url_for,render_template,flash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random
import string
group = Blueprint('group', __name__)


def generate_group_code(length=6):
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(characters, k=length))
        return code



@group.route('/groups/create', methods=['POST'])
@login_required
def create_group():
    name = request.form.get('name')
    description = request.form.get('description')
    if not name: 
        flash("You haven't passed the name of your group", category='error')
        return redirect(url_for('views.groups'))
    group = Group(name=name, code=generate_group_code(),description = description)

    db.session.add(group)
    # current_user.groups.append(group)

    db.session.flush()
    ins = group_membership.insert().values(group_id=group.id, user_id=current_user.id, is_admin=True)
    db.session.execute(ins)
    db.session.commit()

    return redirect(url_for('views.groups'))


@group.route('/groups/join', methods=['POST'])
@login_required
def join_group():
    code = request.form.get('code')
    group = Group.query.filter_by(code=code).first()

    if not group:
        flash("Group code doesn't exist", category='error')
        return redirect(url_for('views.groups'))

    if group in current_user.groups:
        flash("You're already in this group", category='error')
        return redirect(url_for('views.groups'))

    current_user.groups.append(group)
    db.session.commit()

    flash(f"You've successfully joined the group '{group.name}'", category='success')
    return redirect(url_for('views.groups'))


@group.route('groups/leave_group')
@login_required
def leave_group():
    user = current_user
    group_id = request.args.get('group_id')
    group = Group.query.filter_by(id=group_id).first()
    user.groups.remove(group)
    db.session.commit()

    if group.user.count() == 0:
         db.session.delete(group)
         db.session.commit()
         
    flash(f'You have left the group {group.name}', 'success')
    return redirect(url_for('views.groups'))
from .models import Group
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

    group.members.append(current_user)
    group.admins.append(current_user)

    db.session.add(group)
    db.session.commit()

    return f'Created group "{group.name}" with code "{group.code}"', 201


@group.route('/groups/join', methods=['POST'])
@login_required
def join_group():
    code = request.form.get('code')
    if not code:
        return f'Missing group code {code}', 400
    group = Group.query.filter_by(code=code).first()

    if not group:
        return 'Invalid group code', 400

    group.members.append(current_user)

    db.session.commit()

    return f'Joined group "{group.name}" with code "{group.code}"', 200
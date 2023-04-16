from flask import request,jsonify,Blueprint,redirect,url_for,render_template,flash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Group,group_membership,User
panel = Blueprint('panel', __name__)




@panel.route('/adminPanel/kick')
@login_required
def kick_out_of_group():
    user = current_user


from .models import Task
from flask import request,jsonify,Blueprint,redirect,url_for,render_template,flash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
task = Blueprint('task', __name__)


# @task.route('/tasks', methods=['POST'])
# def create_task():
#     name = request.form['name']
#     description = request.form.get('description')
#     completed = 'completed' in request.form
#     task = Task(name=name, description=description, completed=completed)
#     db.session.add(task)
#     db.session.commit()
#     flash('Task created!')
#     return redirect(url_for('views.home'))

# @task.route('/tasks/update', methods=['POST'])
# def update_task():
#     task_id = request.form['id']
#     task = Task.query.get_or_404(task_id)

#     task.name = request.form['name']
#     task.description = request.form['description']
#     task.completed = 'completed' in request.form

#     db.session.commit()
#     return redirect(url_for('views.home'))

# @task.route('/tasks/delete', methods=['POST'])
# def delete_task():
#     try:
#         task_id = request.form.get('task_id')
#         task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
#         db.session.delete(task)
#         db.session.commit()
#     except:
#         flash('There is no such record','error')
#     return redirect(url_for('views.home'))


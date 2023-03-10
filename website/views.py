from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User

views = Blueprint('views',__name__)


@views.route('/')
def home():
    # query the database for all users
    users = User.query.all()

    # render the homepage template with the list of users
    return render_template('home.html', users=users)


@views.route('/Registration', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # get the email address from the form data
        email = request.form['email']

        # create a new User object with the email address
        new_user = User(email=email)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully!', category='success')
        return redirect(url_for('views.home'))

    # if the request method is GET, render the add user template
    return render_template('Registration.html')
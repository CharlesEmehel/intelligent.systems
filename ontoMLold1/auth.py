from flask import Blueprint, current_app as app
from . import db
from ontoML.forms import UserRegisterForm
from ontoML.forms import loginRegisterForm
from ontoML.forms import SPARQLQueryForm
from .models import User, Item
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint('main', __name__)

# ***Handles both GET and POST requests for user registration.***
@bp.route("/userRegister", methods=['GET', 'POST'])
def userRegister_page():
    form = UserRegisterForm()
    if form.validate_on_submit():
        created_user = User(username=form.username.data,
                             email_address=form.email_address.data,
                             password=form.password1.data, 
        )
        app.logger.info(f'Registration attempt for username: {created_user}')
        try:
            db.session.add(created_user)
            db.session.commit()
            login_user(created_user)
            flash(f"Account Created successfully! You have now created a user {created_user}", category='success')
            app.logger.info(f'User created successfully for username: {created_user}')
            return redirect(url_for('use_case_page'))
        except:
            flash(f'There was an issue adding user: {created_user}', category='danger')
            bp.logger.info(f'There was an issue adding user: {created_user}')
            
            return redirect(url_for('userRegister_page'))
    if form.errors != {}: # If errors occur on submit (if form errors are not empty in the dictionary)
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user:{err_msg}', category='danger') # send the category to base.html
            return render_template('userRegister.html', form=form)
    return render_template('userRegister.html', form=form)

# ***Handles  GET requests to display all registered users.***
@bp.route("/users")
@login_required
def users_page():
    try:
        users = User.query.all()
        return render_template('users.html', users=users)
    except:
        flash('No user database table found!', category='danger')
        return redirect(url_for('userRegister_page'))


# ***Handles both GET and POST requests for user login.***
@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    form = loginRegisterForm()
    try:
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'success! You are logged in as: {attempted_user.username}', category='success')
                app.logger.info(f'Login attempt for username: {attempted_user}')
                return redirect(url_for('home_page'))
            else:
                flash('Username and password do not match! Please try again', category='danger')
                app.logger.warning(f'Login failed: Invalid username or password for username: {attempted_user}')
    except SQLAlchemyError as e:
        flash('An error occurred while processing your request. Please try again later.', category='danger')
        
        # Log the error for further investigation
        bp.logger.info('Hello, logging!')
        bp.logger.error(f'SQLAlchemyError: {str(e)}')
    
    return render_template('login.html', form=form) # This passes the form object to render_template where form receives input and render to l


# ***Logs the user out and redirects to the login page.***
@bp.route("/logout")
def logout_page():
    app.logger.info(f'Logout attempt for username: {current_user.username}')
    logout_user()
    flash("You have been logout!", category='info')
    app.logger.info(f'Logout successful for username: {current_user.username}')
    return redirect(url_for('login_page'))

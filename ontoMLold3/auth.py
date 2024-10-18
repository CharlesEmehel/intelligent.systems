from flask import Blueprint, current_app as app, request, redirect, url_for, render_template, flash
from . import db
from .forms import UserRegisterForm, LoginRegisterForm, SPARQLQueryForm
from .models import User, Item
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from keycloak import KeycloakOpenID


auth_bp = Blueprint('auth', __name__)


# ***Handles both GET and POST requests for user registration.***
@auth_bp.route("/userRegister", methods=['GET', 'POST'])
def userRegister_page():
    form = UserRegisterForm()
    if form.validate_on_submit():
        created_user = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data
        )
        app.logger.info(f'Registration attempt for username: {created_user.username}')
        try:
            db.session.add(created_user)
            db.session.commit()
            login_user(created_user)
            flash(f"Account created successfully! You are now logged in as {created_user.username}", category='success')
            app.logger.info(f'User created successfully for username: {created_user.username}')
            return redirect(url_for('main.use_case_page'))
        except SQLAlchemyError as e:
            flash(f'There was an issue adding user: {created_user.username}', category='danger')
            app.logger.error(f'SQLAlchemyError: {str(e)}')
            return redirect(url_for('auth.userRegister_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg}', category='danger')
    return render_template('userRegister.html', form=form)

# ***Handles both GET and POST requests for user login.***
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginRegisterForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            app.logger.info(f'Login attempt for username: {attempted_user.username}')
            return redirect(url_for('main.ontology_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')
            app.logger.warning(f'Login failed: Invalid username or password for username: {form.username.data}')
    return render_template('login.html', form=form)

# ***Handles  GET requests to display all registered users.***
@auth_bp.route("/users")
@login_required
def users_page():
    try:
        users = User.query.all()
        return render_template('users.html', users=users)
    except SQLAlchemyError as e:
        flash('No user database table found!', category='danger')
        app.logger.error(f'SQLAlchemyError: {str(e)}')
        return redirect(url_for('auth.userRegister_page'))


# ***Logs the user out and redirects to the login page.***
@auth_bp.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    app.logger.info(f'Logout successful for current user')
    return redirect(url_for('auth.login_page'))

from flask import Blueprint, current_app as app, request, redirect, url_for, render_template, flash
from . import db
from .forms import UserRegisterForm, LoginRegisterForm, SPARQLQueryForm
from .models import User, Item
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
# from keycloak import KeycloakOpenID
# from flask_keycloak import Keycloak, requires_keycloak_role, KeycloakAdmin
import os

auth_bp = Blueprint('auth', __name__)

# Initialize Keycloak 
keycloak = Keycloak(
    server_url=os.getenv('KEYCLOAK_SERVER_URL'),
    client_id=os.getenv('KEYCLOAK_CLIENT_ID'),
    client_secret=os.getenv('KEYCLOAK_CLIENT_SECRET'),
    realm_name=os.getenv('KEYCLOAK_REALM'),
    verify=True  # Set to False if you don't have SSL setup
)

keycloak_openid = KeycloakOpenID(
        server_url=os.getenv('KEYCLOAK_SERVER_URL'),
        client_id=os.getenv('KEYCLOAK_CLIENT_ID'),
        realm_name=os.getenv('KEYCLOAK_REALM'),
        client_secret_key=os.getenv('KEYCLOAK_CLIENT_SECRET')
)

keycloak_admin = KeycloakAdmin(
    server_url=os.getenv('KEYCLOAK_SERVER_URL'),
    username=os.getenv('KEYCLOAK_ADMIN'),
    password=os.getenv('KEYCLOAK_ADMIN_PASSWORD'),
    realm_name=os.getenv('KEYCLOAK_REALM'),
    client_id=os.getenv('KEYCLOAK_CLIENT_ID'),
    client_secret=os.getenv('KEYCLOAK_CLIENT_SECRET')
)


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

# ***Handles keycloak login.***
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    return redirect(keycloak_openid.auth_url(redirect_uri='http://137.226.248.44:5001/auth/callback'))

   
# ***Handles Keycloak callback.***
@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token = keycloak_openid.token(redirect_uri='http://137.226.248.44:5001/auth/callback', code=code)
    userinfo = keycloak_openid.userinfo(token['access_token'])
    
    form = LoginRegisterForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if not attempted_user:
            attempted_user = User(username=userinfo['preferred_username'], email_address=userinfo['email'])
            db.session.add(attempted_user)
            db.session.commit()
            flash(f'Yu have been added to the database: {attempted_user.username}', category='success')
            app.logger.info(f'Login attempt for username: {attempted_user.username}')
        else: 
            flash('Username and password do not match! Please try again', category='danger')
            app.logger.warning(f'Login failed: Invalid username or password for username: {form.username.data}')
        login_user(attempted_user)
        flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
        app.logger.info(f'Login attempt for username: {attempted_user.username}')
        
        return redirect(url_for('main.home_page'))
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

from flask import Blueprint, current_app as app, request, redirect, url_for, render_template, flash, session
from . import db, oidc
from .forms import UserRegisterForm, LoginRegisterForm, SPARQLQueryForm
from .models import User, Item
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
import os

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
@oidc.require_login
def login_page():
    # check if the user is authenticated:
        return redirect(url_for('main.ontology_page.html'))
        # return render_template('main.ontology_page.html')

@app.route('/test')
def hello_world():
    if oidc.user_loggedin:
        return ('Hello, %s, <a href="/private">See private</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('preferred_username')
    else:
        return 'Welcome anonymous, <a href="/private">Log in</a>'    

@app.route('/private')
@oidc.require_login
def hello_me():
    """Example for protected endpoint that extracts private information from the OpenID Connect id_token.
       Uses the accompanied access_token to access a backend service.
    """

    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])

    username = info.get('preferred_username')
    email = info.get('email')
    user_id = info.get('sub')

    if user_id in oidc.credentials_store:
        try:
            from oauth2client.client import OAuth2Credentials
            access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
            print ('access_token=<%s>') % access_token
            headers = {'Authorization': 'Bearer %s' % (access_token)}
            # YOLO
            greeting = requests.get('http://localhost:8080/greeting', headers=headers).text
        except:
            print ("Could not access greeting-service")
            greeting = "Hello %s" % username
    

    return ("""%s your email is %s and your user_id is %s!
               <ul>
                 <li><a href="/">Home</a></li>
                 <li><a href="//localhost:8081/auth/realms/pysaar/account?referrer=flask-app&referrer_uri=http://localhost:5000/private&">Account</a></li>
                </ul>""" %
            (greeting, email, user_id))



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
    oidc.logout()
    # session.clear()
    # logout_url = oidc_client_secrets['issuer'] + '/protocol/openid-connect/logout' ############ http://localhost:8080/realms/smart/protocol/openid-connect/logout
    # flash("You have been logged out!", category='info')
    # app.logger.info(f'Logout successful for current user')
    return redirect(url_for('home.html'))

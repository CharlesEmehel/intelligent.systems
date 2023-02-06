from ontoML import app
from . import db
from ontoML.forms import UserRegisterForm
from ontoML.forms import loginRegisterForm
from ontoML.forms import SPARQLQueryForm
from .models import User, Item
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/userRegister", methods=['GET', 'POST'])
@login_required
def userRegister_page():
    form = UserRegisterForm()
    if form.validate_on_submit():
        created_user = User(username=form.username.data,
                             email_address=form.email_address.data,
                             password=form.password1.data
        )
        try:
            db.session.add(created_user)
            db.session.commit()
            flash('Account Created!', category='success')
            return redirect(url_for('user_page'))
        except:
            flash('There was an issue adding a user!', category='danger')
            return redirect(url_for('userRegister_page'))
    if form.errors != {}: # If errors occur on submit (if form errors are not empty in the dictionary)
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user:{err_msg}', category='danger') # send the category to base.html
            return render_template('userRegister.html', form=form)
    return render_template('userRegister.html', form=form)

@app.route("/users")
@login_required
def users_page():
    try:
        users = User.query.all()
        return render_template('users.html', users=users)
    except:
        flash('No user database table found!', category='danger')
        return redirect(url_for('userRegister_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = loginRegisterForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('info_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logout!", category='info')
    return redirect(url_for('home_page'))

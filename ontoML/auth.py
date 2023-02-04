from ontoML import app
from . import db
from ontoML.forms import UserRegisterForm
from ontoML.forms import loginRegisterForm
from ontoML.forms import SPARQLQueryForm
from .models import User, Item
from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/userRegister", methods=['GET', 'POST'])
def userRegister_page():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user_creation = User(username=form.username.data,
                             email_address=form.email_address.data,
                             password=form.password1.data
        )
        try:
            db.session.add(user_creation)
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

@app.route("/user")
def user_page():
    try:
        users = User.query.all()
        return render_template('user.html', users=users)
    except:
        flash('No user database table found!', category='danger')
        return redirect(url_for('userRegister_page'))


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = loginRegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', form=form)

@app.route("/logout")
def logout_page():
    return render_template('logout.html')

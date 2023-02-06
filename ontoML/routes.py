from ontoML import app
from ontoML import db
from ontoML.models import Item, Query, User
from ontoML.forms import EntityRegisterForm, SPARQLQueryForm, UserRegisterForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required



@app.route("/entityRegister", methods=['GET', 'POST'])
def entityRegister_page():
    form = EntityRegisterForm()
    if form.validate_on_submit():
        entity_creation = Item(entityname=form.entityname.data,
                               type=form.type.data,
                               locatedat=form.locatedat.data,
                               datecreated=form.datecreated.data,
                               modifiedat=form.datecreated.data,
                               entityversion=form.datecreated.data,
                               devicecategory=form.datecreated.data
        )
        try:
            db.session.add(entity_creation)
            db.session.commit()
            flash('Device Added!', category='success')
            return redirect(url_for('datamodel_page'))
        except:
            flash('There was an issue adding a device!', category='danger')
            return redirect(url_for('entityRegister_page'))
    if form.errors != {}: # If errors occur on submit (if form errors are not empty in the dictionary)
        for err_msg in form.errors.values():
            flash(f'There was an error in adding a device:{err_msg}', category='danger') # send the category to base.html
    return render_template('entityRegister.html', form=form)

@app.route("/sparqlquery", methods=['GET', 'POST'])
def sparqlquery_page():
    form = SPARQLQueryForm()
    if form.validate_on_submit():
        query_creation = Query(namespace=form.namespace.data,
                             querytext=form.querytext.data
        )
        try:
            db.session.add(query_creation)
            db.session.commit()
            flash('Query executing! please wait...!', category='success')
            return redirect(url_for('sparqlquery_page'))
        except:
            flash('There was an issue querying the namespace!', category='danger')
            return redirect(url_for('sparqlquery_page'))
    if form.errors != {}: # If errors occur on submit (if form errors are not empty in the dictionary)
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user:{err_msg}', category='danger') # send the category to base.html
    return render_template('sparqlQuery.html', form=form)


@app.route("/")
@app.route("/home")
@login_required
def home_page():
    return render_template('home.html')

@app.route("/namespaces")
def namespaces_page():
    return render_template('namespaces.html')

@app.route("/datamodel")
def datamodel_page():
    try:
        items = Item.query.all()
        return render_template('dataModel.html', items=items)
    except:
        flash('No item database table found!', category='danger')
        return redirect(url_for('entityRegister_page'))


@app.route("/ontology")
def ontology_page():
    return render_template('ontology.html')

@app.route("/API")
def api_page():
    return render_template('api.html')

@app.route("/api/timeseries")
@app.route("/timeseries")
def timeseries_page():
    return render_template('timeseries.html')
    #return render_template('timeseries.json')

@app.route("/profile/<username>") # browser: 127.0.0.1:5001/profile/charles
def profile_page(username):

    return render_template('profile.html', name=username)

@app.route("/delete/<int:id>")
def delete_page(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        flash('Account could not be deleted!', category='danger')
        return redirect(url_for('/home'))
    # return render_template('sparqlQuery.html', name=name)


@app.route("/info")
def info_page():
    return render_template('info.html')


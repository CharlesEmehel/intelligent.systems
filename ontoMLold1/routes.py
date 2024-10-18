from flask import Blueprint, create_app as app
from ontoML import db
from ontoML.models import Item, Query, User
from ontoML.forms import EntityRegisterForm, SPARQLQueryForm, UserRegisterForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required


bp = Blueprint('main', __name__)

# ***Handles both GET and POST requests for entity registration.***
@bp.route("/entityRegister", methods=['GET', 'POST'])
@login_required
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
            app.logger.info(f'Device created successfully : {entity_creation}')
            return redirect(url_for('main.datamodel_page'))
        except:
            flash('There was an issue adding a device!', category='danger')
            app.logger.info(f'There was an issue adding a device : {entity_creation}')
            return redirect(url_for('main.entityRegister_page'))
    if form.errors != {}: # If errors occur on submit (if form errors are not empty in the dictionary)
        for err_msg in form.errors.values():
            flash(f'There was an error in adding a device:{err_msg}', category='danger') # send the category to base.html
            app.logger.info(f'There was an issue adding a device : {entity_creation}')
    return render_template('entityRegister.html', form=form)


# ***Handles both GET and POST requests for sparql query.***
@bp.route("/sparqlquery", methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('main.sparqlquery_page'))
        except:
            flash('There was an issue querying the namespace!', category='danger')
            return redirect(url_for('main.sparqlquery_page'))
    if form.errors != {}: # If errors occur on submit (if form errors are not empty in the dictionary)
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user:{err_msg}', category='danger') # send the category to base.html
    return render_template('sparqlQuery.html', form=form)


# ***Handles both GET for returning to home.***
@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template('home.html')

@bp.route("/namespaces")
@login_required
def namespaces_page():
    return render_template('namespaces.html')

@bp.route("/datamodel")
@login_required
def datamodel_page():
    try:
        items = Item.query.all()
        return render_template('dataModel.html', items=items)
    except:
        flash('No item database table found!', category='danger')
        return redirect(url_for('entityRegister_page'))
    

# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/ontology")
@login_required
def ontology_page():
    return render_template('ontology.html')


# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/API")
@login_required
def api_page():
    return render_template('api.html')


# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/data")
@login_required
def data():
    return render_template('data.json')


# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/api/timeseries")
@bp.route("/timeseries")
@login_required
def timeseries_page():
    return render_template('timeseries.html')
    #return render_template('timeseries.json')
    
    
# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/profile/<username>") # browser: 127.0.0.1:5001/profile/charles
def profile_page(username):

    return render_template('profile.html', name=username)


# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/delete/<int:id>")
def delete_page(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash('Item has been deleted!', category='success')
        return redirect(url_for('datamodel_page'))
    except:
        flash('Item could not be deleted!', category='danger')
        return redirect(url_for('datamodel_page'))
    # return render_template('sparqlQuery.html', name=name)


# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/info")
@login_required
def use_case_page():
    return render_template('useCase.html')


# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/nifi_interface")
@login_required
def nifi_interface_page():
    pass

    return render_template('nifi.html')

# ***Handles both GET and POST requests for for ontology management.***
@bp.route("/run_script")
@login_required
def run_script():
    urlHandler = urllib.request.urlopen('https://sargon-n5geh.netlify.app/ontologies/Sargon.ttl')
    counts = dict()
    for line in urlHandler:
        words = line.decode().split()
        for word in words:
            counts[word] = counts.get(word, 0) + 1

    return render_template('result.html', counts=counts)


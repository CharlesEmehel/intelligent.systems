from flask import Blueprint, current_app as app, request, jsonify, redirect, url_for, render_template, flash
from .models import db, Item, Query, User
from .forms import EntityRegisterForm, SPARQLQueryForm, UserRegisterForm
from flask_login import login_required

bp = Blueprint('main', __name__)

# ***Handles both GET and POST requests for entity registration.***
@bp.route("/entityRegister", methods=['GET', 'POST'])
@login_required
def entityRegister_page():
    form = EntityRegisterForm()
    if form.validate_on_submit():
        entity_creation = Item(
            entityname=form.entityname.data,
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
            app.logger.info(f'Device created successfully: {entity_creation}')
            return redirect(url_for('main.datamodel_page'))
        except Exception as e:
            flash('There was an issue adding a device!', category='danger')
            app.logger.error(f'There was an issue adding a device: {e}')
            return redirect(url_for('main.entityRegister_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error in adding a device: {err_msg}', category='danger')
            app.logger.error(f'There was an issue adding a device: {err_msg}')
    return render_template('entityRegister.html', form=form)

# ***Handles both GET and POST requests for sparql query.***
@bp.route("/sparqlquery", methods=['GET', 'POST'])
@login_required
def sparqlquery_page():
    form = SPARQLQueryForm()
    if form.validate_on_submit():
        query_creation = Query(
            namespace=form.namespace.data,
            querytext=form.querytext.data
        )
        try:
            db.session.add(query_creation)
            db.session.commit()
            flash('Query executing! please wait...!', category='success')
            return redirect(url_for('main.sparqlquery_page'))
        except Exception as e:
            flash('There was an issue querying the namespace!', category='danger')
            app.logger.error(f'There was an issue querying the namespace: {e}')
            return redirect(url_for('main.sparqlquery_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg}', category='danger')
            app.logger.error(f'There was an issue creating a user: {err_msg}')
    return render_template('sparqlQuery.html', form=form)

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
    except Exception as e:
        flash('No item database table found!', category='danger')
        app.logger.error(f'No item database table found: {e}')
        return redirect(url_for('main.entityRegister_page'))

@bp.route("/ontology")
@login_required
def ontology_page():
    return render_template('ontology.html')

@bp.route("/API")
@login_required
def api_page():
    return render_template('api.html')

@bp.route("/data")
@login_required
def data():
    return render_template('data.json')

@bp.route("/api/timeseries")
@bp.route("/timeseries")
@login_required
def timeseries_page():
    return render_template('timeseries.html')

@bp.route("/profile/<username>")
def profile_page(username):
    return render_template('profile.html', name=username)

@bp.route("/delete/<int:id>")
def delete_page(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash('Item has been deleted!', category='success')
        return redirect(url_for('main.datamodel_page'))
    except Exception as e:
        flash('Item could not be deleted!', category='danger')
        app.logger.error(f'Item could not be deleted: {e}')
        return redirect(url_for('main.datamodel_page'))

@bp.route("/info")
@login_required
def use_case_page():
    return render_template('useCase.html')

@bp.route("/nifi_interface")
@login_required
def nifi_interface_page():
    return render_template('nifi.html')

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

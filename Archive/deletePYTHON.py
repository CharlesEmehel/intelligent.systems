import tempfile
import pathlib
import subprocess
​
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response, abort, send_file
)
​
from flask.views import View, MethodView
from wtforms import Form, BooleanField, StringField, IntegerField, SelectField, SelectMultipleField, validators,\
    DateField, MonthField, FieldList, FormField
from wtforms.widgets import HiddenInput
​
from management.models import *
from management.db import get_db
​
​
class CoffeeListsView(MethodView):
    init_every_request = False
​
    def get(self):
        lists = CrossList.query.all()
        return render_template("coffee_lists.html", lists=lists, list_form=CoffeeListForm())
​
    def post(self):
        f = CoffeeListForm(request.form)
        if f.validate():
            db = get_db()
            cl = CrossList(start=f.start.data, end=f.end.data)
            db.add(cl)
            db.flush()
            db.refresh(cl)
            people = Person.query.where(or_(Person.active, Person.on_lists)).all()
            for p in people:
                if p.coffee_rows > 0:
                    cle = CrossListEntry(cross_list_id=cl.cross_list_id, people_id=p.people_id, rows=p.coffee_rows, manual=False)
                    db.add(cle)
​
            db.commit()
            return self.get()
​
        abort(400)
​
​
class CrossListView(MethodView):
    init_every_request = False
​
    def _get_item(self, id):
        cl = CrossList.query.get(id)
        if cl is None:
            abort(404)
        return cl
​
    def get(self, id:int):
​
        cl = self._get_item(id)
        cle = CoffeeListEntriesForm(obj=cl)
        if request.args.get("print", False) is not False:
            tex = render_template('sheet.tex', cl=cl)
            with tempfile.TemporaryDirectory() as d:
                tex_file = pathlib.Path(d) / "sheet.tex"
                tex_file.write_text(tex)
                subprocess.run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", "sheet.tex"], cwd=d, check=True)
                subprocess.run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", "sheet.tex"], cwd=d, check=True)
                subprocess.run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", "sheet.tex"], cwd=d, check=True)
                print_file = pathlib.Path(d) / "sheet.pdf"
                return send_file(print_file)
        ncle = NewCoffeeEntryForm(cross_list_id=id)
        return render_template('coffee_list.html', cl=cl, cle=cle, ncle=ncle)
​
    def post(self, id:int):
        f = NewCoffeeEntryForm(request.form, cross_list_id=id)
        if f.validate():
            cle = CrossListEntry(cross_list_id=id, people_id=f.people_id.data, manual=True, checked=f.checked.data)
            db = get_db()
            db.add(cle)
            db.commit()
            return redirect(url_for("list", id=id), 303)
        f = CoffeeListEntriesForm(request.form)
        if f.validate():
            db = get_db()
            db_entries = CrossListEntry.query.where(CrossListEntry.cross_list_id == id).all()
            db_entries = {e.people_id: e for e in db_entries}
            p_ids = set(db_entries.keys())
            if p_ids != set(e.people_id.data for e in f.entries):
                abort(400)
            for e in f.entries:
                db_entry = db_entries[e.people_id.data]
                if db_entry.checked != e.checked.data:
                    db_entry.checked = e.checked.data
            db.commit()
            return redirect(url_for('list', id=id), 303)
​
        abort(400)
    def put(self, id:int):
        pass
​
    def delete(self, id:int):
        cl = self._get_item(id)
        db = get_db()
        db.delete(cl)
        db.commit()
        return '', 204
​
​
class CoffeeListForm(Form):
    start = DateField("Start", validators=[validators.InputRequired()])
    end = DateField("End", validators=[validators.InputRequired()])
​
​
class CoffeeEntryForm(Form):
    people_id = IntegerField("list_id", validators=[validators.InputRequired()], widget=HiddenInput())
    checked = IntegerField(validators=[validators.Optional(), validators.NumberRange(0, 1000)])
​
​
class NewCoffeeEntryForm(Form):
    people_id = SelectField("list_id", validators=[validators.InputRequired()], coerce=int)
    checked = IntegerField(validators=[validators.Optional(), validators.NumberRange(0, 1000)])
​
    def __init__(self, *args, **kwargs):
        cross_list_id = kwargs.pop("cross_list_id")
        super().__init__(*args, **kwargs)
        missing = Person.query.where(~Person.people_id.in_(
            select(CrossListEntry.people_id).where(CrossListEntry.cross_list_id == cross_list_id)
        )).order_by(Person.last_name, Person.first_name).all()
        self.people_id.choices = [(m.people_id, (m.last_name + ", " + m.first_name)) for m in missing]
​
​
class CoffeeListEntriesForm(Form):
    entries = FieldList(FormField(CoffeeEntryForm))
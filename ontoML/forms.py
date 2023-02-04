from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from ontoML.models import User, Item, Query


class UserRegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email address already exists! Please use your valid email address")

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class EntityRegisterForm(FlaskForm):

    def validate_entityname(self, entityname_to_check):
        item = Item.query.filter_by(entityname=entityname_to_check.data).first()
        if item:
            raise ValidationError("Entity name already exists! Please confirm the spelling or check the data model")

    entityname = StringField(label='Entity', validators=[Length(min=2, max=30), DataRequired()])
    type = StringField(label='Type', validators=[Length(min=2, max=30), DataRequired()])
    locatedat = StringField(label='Located At', validators=[Length(min=2, max=30), DataRequired()])
    datecreated = StringField(label='Date Created', validators=[Length(min=2, max=30), DataRequired()])
    modifiedat = StringField(label='Modified At', validators=[Length(min=2, max=30), DataRequired()])
    entityversion = StringField(label='Entity Version', validators=[Length(min=1, max=30), DataRequired()])
    devicecategory = StringField(label='Device Category', validators=[Length(min=2, max=30), DataRequired()])
    submit = SubmitField(label='Add Entity')


class SPARQLQueryForm(FlaskForm):

    def validate_entityname(self, namespace_to_check):
        query = Query.query.filter_by(namespace=namespace_to_check.data).first()
        if query:
            raise ValidationError("Entity name already exists! Please confirm the spelling or check the data model")
    namespace = StringField(label='Namespace', validators=[Length(min=2, max=30), DataRequired()])
    querytext = StringField(label='Query Text', validators=[Length(min=2, max=200), DataRequired()])
    submit = SubmitField(label='Run Query')


class loginRegisterForm(FlaskForm):
    username = StringField(label='User name:', validators=[DataRequired()])
    password = StringField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


    pass
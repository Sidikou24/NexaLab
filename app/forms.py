# pour définir les formulaires WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Optional

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', [validators.Length(min=10, max=15)])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

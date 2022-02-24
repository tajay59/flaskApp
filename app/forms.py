from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired

class ContactForm(FlaskForm):
    """ContactForm"""
    name        = StringField("Name",validators=[DataRequired()])
    email       = EmailField("E-mail",validators=[DataRequired(),Email()])
    subject     = StringField("Subject", validators=[DataRequired()])
    message     = TextAreaField("Message", validators=[DataRequired()]) 
    
    

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Navn', validators=[
        DataRequired(message='Navn er påkrevd'),
        Length(min=2, max=100, message='Navn må være mellom 2 og 100 tegn')
    ])
    
    email = EmailField('E-post', validators=[
        DataRequired(message='E-post er påkrevd'),
        Email(message='Ugyldig e-postadresse')
    ])
    
    phone = StringField('Telefon', validators=[
        Length(max=20, message='Telefonnummer kan ikke overstige 20 tegn')
    ])
    
    subject = StringField('Emne', validators=[
        DataRequired(message='Emne er påkrevd'),
        Length(min=2, max=200, message='Emne må være mellom 2 og 200 tegn')
    ])
    
    message = TextAreaField('Melding', validators=[
        DataRequired(message='Melding er påkrevd'),
        Length(min=5, max=1000, message='Melding må være mellom 5 og 1000 tegn')
    ])
    
    submit = SubmitField('Send melding')

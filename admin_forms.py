from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


class LoginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Passord', validators=[DataRequired()])
    submit = SubmitField('Logg inn')


class MenuItemForm(FlaskForm):
    name = StringField('Retnavn', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Beskrivelse', validators=[Optional(), Length(max=500)])
    price = StringField('Pris (NOK)', validators=[DataRequired(), Length(max=10)])
    category = SelectField('Kategori', 
                          choices=[('hovedretter', 'Hovedretter'), 
                                 ('ekstra', 'Ekstra'), 
                                 ('drikker', 'Drikker'), 
                                 ('catering', 'Catering')],
                          validators=[DataRequired()])
    image_filename = StringField('Bildefil (valgfritt)', validators=[Optional(), Length(max=100)])
    is_active = BooleanField('Aktiv', default=True)
    sort_order = IntegerField('Rekkefølge', default=0)
    submit = SubmitField('Lagre')


class RestaurantInfoForm(FlaskForm):
    phone = StringField('Telefonnummer', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-post', validators=[DataRequired(), Email(), Length(max=120)])
    address = TextAreaField('Adresse', validators=[DataRequired(), Length(max=200)])
    opening_hours = TextAreaField('Åpningstider', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Oppdater kontaktinfo')


class CreateAdminForm(FlaskForm):
    username = StringField('Brukernavn', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('E-post', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Passord', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Bekreft passord', 
                             validators=[DataRequired(), EqualTo('password', message='Passordene må være like')])
    submit = SubmitField('Opprett administrator')
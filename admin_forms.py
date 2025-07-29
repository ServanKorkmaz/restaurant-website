from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[DataRequired()])
    password = PasswordField('Passord', validators=[DataRequired()])
    remember_me = BooleanField('Husk meg')
    submit = SubmitField('Logg inn')


class CreateAdminForm(FlaskForm):
    username = StringField('Brukernavn', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-post', validators=[DataRequired(), Email()])
    password = PasswordField('Passord', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Bekreft passord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Opprett administrator')


class MenuItemForm(FlaskForm):
    name = StringField('Navn på rett', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Beskrivelse', validators=[Length(max=500)])
    price = StringField('Pris (NOK)', validators=[DataRequired()])
    category = SelectField('Kategori', choices=[
        ('hovedretter', 'Hovedretter'),
        ('ekstra', 'Ekstra'),
        ('drikker', 'Drikker'),
        ('catering', 'Catering')
    ], validators=[DataRequired()])
    image_filename = StringField('Bildenavn', validators=[Length(max=100)])
    sort_order = IntegerField('Rekkefølge', validators=[NumberRange(min=0, max=100)], default=10)
    is_active = BooleanField('Aktiv', default=True)
    submit = SubmitField('Lagre')


class RestaurantInfoForm(FlaskForm):
    phone = StringField('Telefonnummer', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-post', validators=[DataRequired(), Email(), Length(max=100)])
    address = TextAreaField('Adresse', validators=[DataRequired(), Length(max=200)])
    opening_hours = TextAreaField('Åpningstider', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Lagre endringer')
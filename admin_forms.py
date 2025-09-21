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
        ('alkohol', 'Alkoholholdige drikker'),
        ('catering', 'Catering')
    ], validators=[DataRequired()])
    image_filename = StringField('Bildenavn', validators=[Length(max=100)])
    sort_order = IntegerField('Rekkefølge', validators=[NumberRange(min=0, max=100)], default=10)
    is_active = BooleanField('Aktiv', default=True)
    submit = SubmitField('Lagre')


class CateringPackageForm(FlaskForm):
    name = StringField('Pakkenavn', validators=[DataRequired(), Length(max=100)])
    price_per_person = StringField('Pris per person (NOK)', validators=[DataRequired()])
    description = TextAreaField('Kort beskrivelse', validators=[Length(max=500)])
    items = TextAreaField('Inkluderte retter (en per linje)', validators=[DataRequired()])
    min_persons = IntegerField('Minimum antall personer', validators=[NumberRange(min=1)], default=10)
    allergens = StringField('Allergener (f.eks. 1,3,7)', validators=[Length(max=200)])
    best_for = StringField('Best egnet for', validators=[Length(max=200)])
    sort_order = IntegerField('Rekkefølge', validators=[NumberRange(min=0)], default=0)
    is_active = BooleanField('Aktiv', default=True)
    submit = SubmitField('Lagre')


class RestaurantInfoForm(FlaskForm):
    phone = StringField('Telefonnummer', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-post', validators=[DataRequired(), Email(), Length(max=100)])
    address = TextAreaField('Adresse', validators=[DataRequired(), Length(max=200)])
    opening_hours = TextAreaField('Åpningstider', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Lagre endringer')
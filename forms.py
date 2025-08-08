"""Form definitions for the application."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, DateField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError
import re

def norwegian_phone_validator(form, field):
    """Validate Norwegian phone number format."""
    if field.data:
        # Remove spaces and dashes
        phone = re.sub(r'[\s-]', '', field.data)
        # Check for valid Norwegian phone patterns
        if not re.match(r'^(\+47|47)?\d{8}$', phone):
            raise ValidationError('Ugyldig norsk telefonnummer. Bruk format: +47 12345678 eller 12345678')

class ContactForm(FlaskForm):
    """Contact form for customer inquiries."""
    name = StringField('Navn', validators=[
        DataRequired(message='Navn er påkrevd'),
        Length(min=2, max=100, message='Navn må være mellom 2 og 100 tegn')
    ])
    email = StringField('E-post', validators=[
        DataRequired(message='E-post er påkrevd'),
        Email(message='Ugyldig e-postadresse')
    ])
    phone = StringField('Telefon', validators=[
        Optional(),
        norwegian_phone_validator
    ])
    subject = StringField('Emne', validators=[
        DataRequired(message='Emne er påkrevd'),
        Length(min=3, max=200, message='Emne må være mellom 3 og 200 tegn')
    ])
    message = TextAreaField('Melding', validators=[
        DataRequired(message='Melding er påkrevd'),
        Length(min=10, max=2000, message='Melding må være mellom 10 og 2000 tegn')
    ])

class CateringInquiryForm(FlaskForm):
    """Catering inquiry form."""
    name = StringField('Kontaktperson', validators=[
        DataRequired(message='Navn er påkrevd'),
        Length(min=2, max=100)
    ])
    firma = StringField('Firma/Organisasjon', validators=[
        DataRequired(message='Firma er påkrevd'),
        Length(min=2, max=200)
    ])
    email = StringField('E-post', validators=[
        DataRequired(message='E-post er påkrevd'),
        Email(message='Ugyldig e-postadresse')
    ])
    phone = StringField('Telefon', validators=[
        DataRequired(message='Telefon er påkrevd'),
        norwegian_phone_validator
    ])
    antall_personer = IntegerField('Antall personer', validators=[
        DataRequired(message='Antall personer er påkrevd'),
        NumberRange(min=10, max=500, message='Vi leverer catering for 10-500 personer')
    ])
    dato = DateField('Ønsket dato', validators=[
        DataRequired(message='Dato er påkrevd')
    ], format='%Y-%m-%d')
    pakke = SelectField('Ønsket cateringpakke', choices=[
        ('', 'Velg pakke...'),
        ('menyforslag_1', 'Menyforslag 1 - 199 kr/pers'),
        ('menyforslag_2', 'Menyforslag 2 - 239 kr/pers'),
        ('menyforslag_3', 'Menyforslag 3 - 275 kr/pers'),
        ('menyforslag_4', 'Menyforslag 4 - 299 kr/pers'),
        ('menyforslag_5', 'Menyforslag 5 - 349 kr/pers'),
        ('menyforslag_6', 'Menyforslag 6 - 385 kr/pers'),
        ('spesialtilpasset', 'Spesialtilpasset meny')
    ], validators=[DataRequired(message='Velg en cateringpakke')])
    leveringsadresse = StringField('Leveringsadresse', validators=[
        DataRequired(message='Leveringsadresse er påkrevd'),
        Length(min=5, max=300)
    ])
    kommentar = TextAreaField('Spesielle ønsker/allergier', validators=[
        Optional(),
        Length(max=1000)
    ])

class LoginForm(FlaskForm):
    """Admin login form."""
    username = StringField('Brukernavn', validators=[
        DataRequired(message='Brukernavn er påkrevd')
    ])
    password = PasswordField('Passord', validators=[
        DataRequired(message='Passord er påkrevd')
    ])
    remember_me = BooleanField('Husk meg')

class MenuItemForm(FlaskForm):
    """Form for adding/editing menu items."""
    name = StringField('Navn', validators=[
        DataRequired(message='Navn er påkrevd'),
        Length(min=2, max=100)
    ])
    description = TextAreaField('Beskrivelse', validators=[
        Optional(),
        Length(max=500)
    ])
    price = StringField('Pris', validators=[
        DataRequired(message='Pris er påkrevd')
    ])
    category = SelectField('Kategori', choices=[
        ('hovedretter', 'Hovedretter'),
        ('ekstra', 'Ekstra'),
        ('drikker', 'Drikker'),
        ('catering', 'Catering')
    ], validators=[DataRequired()])
    image = FileField('Bilde', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Kun bildefiler tillatt')
    ])
    alt_text = StringField('Alternativ tekst for bilde', validators=[
        Optional(),
        Length(max=200)
    ])
    is_active = BooleanField('Aktiv')
    is_featured = BooleanField('Fremhevet på forsiden')
    sort_order = IntegerField('Sorteringsrekkefølge', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    allergens = StringField('Allergener (kommaseparert)', validators=[
        Optional(),
        Length(max=100)
    ])
    min_pax = IntegerField('Minimum antall personer (for catering)', validators=[
        Optional(),
        NumberRange(min=1)
    ])

class RestaurantInfoForm(FlaskForm):
    """Form for restaurant information."""
    address = TextAreaField('Adresse', validators=[
        DataRequired(message='Adresse er påkrevd'),
        Length(max=300)
    ])
    phone = StringField('Telefon', validators=[
        DataRequired(message='Telefon er påkrevd'),
        norwegian_phone_validator
    ])
    email = StringField('E-post', validators=[
        DataRequired(message='E-post er påkrevd'),
        Email(message='Ugyldig e-postadresse')
    ])
    opening_hours = TextAreaField('Åpningstider', validators=[
        DataRequired(message='Åpningstider er påkrevd'),
        Length(max=500)
    ])
    parking_info = TextAreaField('Parkeringsinformasjon', validators=[
        Optional(),
        Length(max=300)
    ])
    about_text = TextAreaField('Om oss', validators=[
        Optional(),
        Length(max=2000)
    ])
    facebook_url = StringField('Facebook URL', validators=[
        Optional(),
        Length(max=200)
    ])
    instagram_url = StringField('Instagram URL', validators=[
        Optional(),
        Length(max=200)
    ])
    tripadvisor_url = StringField('TripAdvisor URL', validators=[
        Optional(),
        Length(max=200)
    ])

class SearchForm(FlaskForm):
    """Search form for menu items."""
    query = StringField('Søk', validators=[
        Optional(),
        Length(max=100)
    ])
    category = SelectField('Kategori', choices=[
        ('alle', 'Alle kategorier'),
        ('hovedretter', 'Hovedretter'),
        ('ekstra', 'Ekstra'),
        ('drikker', 'Drikker')
    ])
    allergen_free = SelectField('Allergener', choices=[
        ('', 'Alle retter'),
        ('1', 'Glutenfri'),
        ('7', 'Laktosefri'),
        ('vegetar', 'Vegetar'),
        ('vegan', 'Vegansk')
    ])
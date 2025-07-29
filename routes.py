from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import ContactForm
import logging

@app.route('/')
def index():
    """Homepage with business introduction"""
    return render_template('index.html')

@app.route('/meny')
def menu():
    """Menu page displaying food and beverage offerings"""
    # Menu data structure
    menu_data = {
        'kaffe_drikker': [
            {'name': 'Espresso', 'price': '35', 'description': 'Klassisk italiensk kaffe'},
            {'name': 'Americano', 'price': '40', 'description': 'Espresso med varmt vann'},
            {'name': 'Cappuccino', 'price': '45', 'description': 'Espresso med dampet melk og melkeskum'},
            {'name': 'Latte', 'price': '45', 'description': 'Espresso med mye dampet melk'},
            {'name': 'Flat White', 'price': '48', 'description': 'Dobbel espresso med mikroskum'},
            {'name': 'Kaffe av dagen', 'price': '30', 'description': 'Dagens spesialkaffe'}
        ],
        'te_varme_drikker': [
            {'name': 'Earl Grey', 'price': '35', 'description': 'Klassisk bergamot-te'},
            {'name': 'Grønn te', 'price': '35', 'description': 'Frisk japansk sencha'},
            {'name': 'Kamille', 'price': '35', 'description': 'Beroligende urtete'},
            {'name': 'Varm sjokolade', 'price': '48', 'description': 'Rik sjokolade med pisket krem'},
            {'name': 'Chai latte', 'price': '45', 'description': 'Krydret te med dampet melk'}
        ],
        'kalde_drikker': [
            {'name': 'Is-kaffe', 'price': '45', 'description': 'Kald kaffe med is og melk'},
            {'name': 'Smoothie', 'price': '65', 'description': 'Daglig varierende fruktsmootie'},
            {'name': 'Fresh juice', 'price': '55', 'description': 'Fersk pressede juicer'},
            {'name': 'Mineralvann', 'price': '25', 'description': 'Norsk kildevann'},
            {'name': 'Brus', 'price': '30', 'description': 'Utvalg av lokale brusfabrikanter'}
        ],
        'mat': [
            {'name': 'Smørbrød', 'price': '85-120', 'description': 'Klassiske norske smørbrød med lokale ingredienser'},
            {'name': 'Salater', 'price': '95-140', 'description': 'Sesongbaserte salater med friske grønnsaker'},
            {'name': 'Supper', 'price': '110', 'description': 'Dagens hjemmelagde suppe med brød'},
            {'name': 'Kaker', 'price': '45-65', 'description': 'Hjemmelagde kaker og desserter'},
            {'name': 'Bakverk', 'price': '25-45', 'description': 'Ferske croissanter, muffins og wienerbrød'},
            {'name': 'Yoghurt med granola', 'price': '75', 'description': 'Naturell yoghurt med hjemmelaget granola'}
        ],
        'catering': [
            {'name': 'Møtecatering', 'price': 'Fra 150/pers', 'description': 'Kaffe, te og bakverk for møter'},
            {'name': 'Lunsjcatering', 'price': 'Fra 250/pers', 'description': 'Komplett lunsj med drikke'},
            {'name': 'Kurs og konferanse', 'price': 'Tilbud på forespørsel', 'description': 'Heldag catering for kurs og konferanser'},
            {'name': 'Private arrangement', 'price': 'Tilbud på forespørsel', 'description': 'Skreddersydde menyer for private fester'}
        ]
    }
    
    return render_template('menu.html', menu=menu_data)

@app.route('/kontakt', methods=['GET', 'POST'])
def contact():
    """Contact page with business information and contact form"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # In a real application, you would send an email or save to database
        # For now, we'll just log the message and show a success message
        logging.info(f"Contact form submission from {form.name.data} ({form.email.data})")
        logging.info(f"Subject: {form.subject.data}")
        logging.info(f"Message: {form.message.data}")
        
        flash('Takk for din henvendelse! Vi vil kontakte deg så snart som mulig.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

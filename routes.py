from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import ContactForm
import logging

@app.route('/')
def index():
    """Homepage with business introduction"""
    # Featured dishes to showcase on homepage
    featured_dishes = [
        {'name': 'Kylling m/ Cashewnøtter', 'image': 'kylling-cashew.jpg', 'price': '205'},
        {'name': 'Rød Karri m/ And', 'image': 'rod-karri-and.jpg', 'price': '245'},
        {'name': 'Pad Krapao', 'image': 'pad-krapao.jpg', 'price': '205'}
    ]
    return render_template('index.html', featured_dishes=featured_dishes)

@app.route('/meny')
def menu():
    """Menu page displaying food and beverage offerings"""
    # Menu data structure - Authentic dishes from Nawarat Thai Mat og Catering
    menu_data = {
        'hovedretter': [
            {'name': 'Kylling m/ Cashewnøtter & Ris', 'price': '205', 'description': 'Paprika, løk og hjemmelaget saus', 'image': 'kylling-cashew.jpg'},
            {'name': 'Rød Karri', 'price': '205', 'description': 'Kremet rød karri med rød karri pasta, ananas, tomat, fersk basilikum, paprika og kokosmelk. Velg mellom kylling, biff eller svin', 'image': 'rod-karri.jpg'},
            {'name': 'Paneng Kai', 'price': '205', 'description': 'Paprika, basilikum, sitronblad, rød chilipaste, kokosmelk og ris. Velg mellom kylling, scampi, svin og biff', 'image': 'paneng-kai.jpg'},
            {'name': 'Sweet Chili', 'price': '205', 'description': 'Paprika, løk, gulrot, ananas, ris og hjemmelaget saus. Velg mellom kylling, scampi, svin og biff', 'image': 'sweet-chili.jpg'},
            {'name': 'Stekt Ris', 'price': '205', 'description': 'Stekt ris med brokkoli, gulrot, løk, egg, østersaus og soyasaus. Velg mellom kylling, svin eller scampi', 'image': 'stekt-ris.jpg'},
            {'name': 'Rød Karri m/ And & Ris', 'price': '245', 'description': 'Ananas, paprika, basilikum, tomat og kokosmelk', 'image': 'rod-karri-and.jpg'},
            {'name': 'Kyllingsuppe m/ Ris', 'price': '205', 'description': 'Champignon, tomat, løk, sitronblad, sitrongress, lime og kokosmelk', 'image': 'kyllingsuppe.jpg'},
            {'name': 'Pad Krapao', 'price': '205', 'description': 'Bambus, holybasilikum, chili, hvitløk, østersaus og soyasaus. Velg mellom kylling, scampi og svin', 'image': 'pad-krapao.jpg'},
            {'name': 'Biff m/ Østersaus', 'price': '235', 'description': 'Brokkoli, gulrot, løk, ris og hjemmelaget saus', 'image': 'biff-ostersaus.jpg'},
            {'name': 'Wok', 'price': '205', 'description': 'Wok med paprika, løk, brokkoli, gulrot, hvitløk, soyasaus og østersaus. Velg mellom kylling, biff, svin eller scampi', 'image': 'wok.jpg'},
            {'name': 'Stekte Eggnudler m/ Kylling', 'price': '205', 'description': 'Eggnudler, grønnsaker, egg, edikk, soyasaus og østersaus', 'image': 'stekte-eggnudler.jpg'},
            {'name': 'Vårruller m/ Salat & Ris', 'price': '185', 'description': 'Glassnudler, kål, gulrot, løk, kyllinkjøttdeig, soyasaus og østersaus. Serveres med salat og ris', 'image': 'varruller.jpg'}
        ],
        'ekstra': [
            {'name': 'Vårull', 'price': '25', 'description': '1 stk vårull med glassnudler, kål, gulrot, løk, kyllinkjøttdeig, soyasaus og østersaus', 'image': None},
            {'name': 'Innbakt Scampi', 'price': '30', 'description': '1 stk fritert innbakt scampi', 'image': None},
            {'name': 'Ekstra Ris', 'price': '20', 'description': 'Ekstra ris til retten', 'image': None}
        ],
        'drikker': [
            {'name': 'Coca-Cola', 'price': '40', 'description': '0,5l Coca-Cola', 'image': None},
            {'name': 'Coca-Cola Zero', 'price': '40', 'description': '0,5l Coca-Cola Zero', 'image': None},
            {'name': 'Fanta', 'price': '40', 'description': '0,5l Fanta', 'image': None},
            {'name': 'Pepsi', 'price': '40', 'description': '0,5l Pepsi', 'image': None},
            {'name': 'Pepsi Max', 'price': '40', 'description': '0,5l Pepsi Max', 'image': None},
            {'name': 'Solo', 'price': '40', 'description': '0,5l Solo', 'image': None},
            {'name': 'Solo Super', 'price': '40', 'description': '0,5l Solo Super', 'image': None},
            {'name': 'Fanta Exotic', 'price': '40', 'description': '0,5l Fanta Exotic', 'image': None},
            {'name': 'Sprite', 'price': '40', 'description': '0,5l Sprite', 'image': None},
            {'name': 'Farris naturell', 'price': '40', 'description': '0,5l Farris naturell', 'image': None},
            {'name': 'Farris Lime', 'price': '40', 'description': '40 Farris Lime', 'image': None},
            {'name': 'Munkholm', 'price': '69', 'description': '0,33l', 'image': None},
            {'name': 'Mozell', 'price': '40', 'description': '0,5l', 'image': None}
        ],
        'catering': [
            {'name': 'Små catering', 'price': 'Fra 200/pers', 'description': 'Utvalg av våre populære retter for 10-20 personer'},
            {'name': 'Medium catering', 'price': 'Fra 180/pers', 'description': 'Utvidet meny for 20-50 personer med forretter'},
            {'name': 'Store arrangementer', 'price': 'Tilbud på forespørsel', 'description': 'Komplett buffet for over 50 personer'},
            {'name': 'Bedrift lunsjcatering', 'price': 'Fra 165/pers', 'description': 'Daglig leveranse til bedrifter'}
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

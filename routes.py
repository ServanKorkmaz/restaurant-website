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
    # Menu data structure - Authentic Thai dishes
    menu_data = {
        'forretter': [
            {'name': 'Satay Gai', 'price': '179', 'description': 'Grillede kyllingspyd med peanøttsaus og agurkrelish'},
            {'name': 'Tom Kha Gai', 'price': '149', 'description': 'Kremet kyllingsuppe med kokosnøtt, galanga og lime'},
            {'name': 'Tod Man Pla', 'price': '169', 'description': 'Friterte fiskekaker med søt chilisaus'},
            {'name': 'Larb Gai', 'price': '159', 'description': 'Krydret kyllingsalat med friske urter og ris'},
            {'name': 'Vegetar Vårruller', 'price': '139', 'description': '4 stk friterte vårruller med grønnsaker og søt chilisaus'}
        ],
        'hovedretter_kylling': [
            {'name': 'Pad Thai Gai', 'price': '219', 'description': 'Klassisk thailandsk wok med kylling, risnudler og tamarind'},
            {'name': 'Massaman Gai', 'price': '239', 'description': 'Mild curry med kylling, kokosnøtt, poteter og peanøtter'},
            {'name': 'Pad Kra Pao Gai', 'price': '229', 'description': 'Krydret kylling med thai-basilikum og stekt egg'},
            {'name': 'Gai Yang', 'price': '249', 'description': 'Marinert grillet kylling med sticky rice og jeaw bong'},
            {'name': 'Gaeng Keow Wan Gai', 'price': '239', 'description': 'Grønn curry med kylling, thailandske auberginer og basilikum'}
        ],
        'hovedretter_svin_storfe': [
            {'name': 'Pad See Ew Moo', 'price': '229', 'description': 'Wok med svinekjøtt, brede nudler og kinesisk brokkoli'},
            {'name': 'Gaeng Phed Neua', 'price': '259', 'description': 'Rød curry med storfekjøtt, bambuskonserves og thai-basilikum'},
            {'name': 'Laab Moo', 'price': '189', 'description': 'Nordthailandsk svinekjøttsalat med lime og chili'},
            {'name': 'Pad Kra Pao Moo', 'price': '219', 'description': 'Krydret svinekjøtt med thai-basilikum og stekt egg'}
        ],
        'sjomat': [
            {'name': 'Pad Thai Goong', 'price': '269', 'description': 'Pad Thai med store reker og tamarind'},
            {'name': 'Pla Rad Prik', 'price': '289', 'description': 'Fritert hel fisk med søt og sur chilisaus'},
            {'name': 'Tom Yum Goong', 'price': '179', 'description': 'Sur og krydret rekesupppe med sitrongress og lime'},
            {'name': 'Gaeng Som Pla', 'price': '249', 'description': 'Sur curry med fisk og grønnsaker'}
        ],
        'vegetar': [
            {'name': 'Pad Thai Jay', 'price': '199', 'description': 'Vegetarisk Pad Thai med tofu og grønnsaker'},
            {'name': 'Gaeng Keow Wan Jay', 'price': '219', 'description': 'Grønn vegetar curry med tofu og thailandske auberginer'},
            {'name': 'Pad Pak Ruam Mit', 'price': '189', 'description': 'Wok med blandede sesonggrønnsaker og soyasaus'},
            {'name': 'Som Tam Jay', 'price': '169', 'description': 'Vegetarisk papayasalat med tomater og grønne bønner'}
        ],
        'drikker': [
            {'name': 'Thai Iste', 'price': '65', 'description': 'Klassisk thai iste med kondensert melk'},
            {'name': 'Singha øl (0,33l)', 'price': '79', 'description': 'Thailandsk lager øl'},
            {'name': 'Chang øl (0,33l)', 'price': '79', 'description': 'Thailandsk lager øl'},
            {'name': 'Kokosnøttvann', 'price': '55', 'description': 'Fersk kokosnøtt'},
            {'name': 'Mineralvann', 'price': '39', 'description': 'Importert fra Thailand'},
            {'name': 'Brus (Coca-Cola)', 'price': '45', 'description': 'Diverse brus'}
        ],
        'catering': [
            {'name': 'Små catering', 'price': 'Fra 200/pers', 'description': 'Pad Thai, curry og ris for 10-20 personer'},
            {'name': 'Medium catering', 'price': 'Fra 180/pers', 'description': 'Utvidet meny for 20-50 personer med forretter'},
            {'name': 'Store arrangementer', 'price': 'Tilbud på forespørsel', 'description': 'Komplett buffet for over 50 personer'},
            {'name': 'Bedrift lunsjcatering', 'price': 'Fra 165/pers', 'description': 'Daglig leveranse til bedrifter'},
            {'name': 'Hjemmelaging', 'price': 'Fra 800/time', 'description': 'Vi kommer hjem til deg og lager autentisk thailandsk mat'}
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

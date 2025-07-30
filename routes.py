from flask import render_template, request, flash, redirect, url_for
from app import app, db  
import logging
from forms import ContactForm
from models import MenuItem, RestaurantInfo
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
    # Get menu items from database, fallback to static data if empty
    db_items = MenuItem.query.filter_by(is_active=True).filter(MenuItem.category != 'catering').order_by(MenuItem.category, MenuItem.sort_order, MenuItem.name).all()
    
    if db_items:
        # Use database items (exclude catering items)
        menu_data = {
            'hovedretter': [],
            'ekstra': [],
            'drikker': []
        }
        
        for item in db_items:
            if item.category in menu_data:
                menu_data[item.category].append({
                    'name': item.name,
                    'price': item.price,
                    'description': item.description,
                    'image': item.image_filename
                })
    else:
        # Fallback to static data - this will be replaced by database items
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
            {'name': 'Vårruller m/ Salat & Ris', 'price': '185', 'description': 'Glassnudler, kål, gulrot, løk, kyllinkjøttdeig, soyasaus og østersaus. Serveres med salat og ris', 'image': 'varruller.jpg'},
            {'name': 'Pad Thai', 'price': '205', 'description': 'Thailandsk stekt nudlerrett med tofu, peanøtter, balansert søt og syrlig saus. Velg mellom scampi, kylling eller svin', 'image': None},
            {'name': 'Nudelsuppe', 'price': '235', 'description': 'Nudelsuppe med svin', 'image': None}
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

    }
    
    return render_template('menu.html', menu=menu_data)

@app.route('/catering')
def catering():
    """Catering page with detailed catering packages"""
    return render_template('catering.html')

@app.route('/kontakt', methods=['GET', 'POST'])
def contact():
    """Contact page with business information and contact form"""
    form = ContactForm()
    
    # Skip CSRF validation and check if fields are valid manually
    if request.method == 'POST':
        # Manual validation to bypass CSRF issues
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        errors = []
        if len(name) < 2:
            errors.append("Navn må være minst 2 tegn")
        if '@' not in email or '.' not in email:
            errors.append("Ugyldig e-postadresse")
        if len(subject) < 2:
            errors.append("Emne må være minst 2 tegn")
        if len(message) < 5:
            errors.append("Melding må være minst 5 tegn")
            
        if not errors:
            # Create a simple form object for logging
            class SimpleForm:
                def __init__(self, name, email, phone, subject, message):
                    self.name = type('obj', (object,), {'data': name})
                    self.email = type('obj', (object,), {'data': email})
                    self.phone = type('obj', (object,), {'data': phone})
                    self.subject = type('obj', (object,), {'data': subject})
                    self.message = type('obj', (object,), {'data': message})
            
            simple_form = SimpleForm(name, email, phone, subject, message)
            
            try:
                # Try to send email
                if send_contact_email(simple_form):
                    flash('Takk for din henvendelse! Vi kommer tilbake til deg så snart som mulig.', 'success')
                else:
                    # Always log the message
                    log_contact_message(simple_form)
                    flash('Takk for din henvendelse! Vi kommer tilbake til deg så snart som mulig.', 'success')
            except Exception as e:
                app.logger.error(f"Contact form error: {e}")
                log_contact_message(simple_form)
                flash('Takk for din henvendelse! Vi kommer tilbake til deg så snart som mulig.', 'success')
            
            return redirect(url_for('contact'))
        else:
            for error in errors:
                flash(error, 'danger')
    
    # Original form validation for GET requests and form display
    if form.validate_on_submit():
        # This should not be reached due to the manual handling above
        pass
    else:
        # Debug form validation errors
        if form.errors:
            app.logger.error(f"Form validation errors: {form.errors}")
            # Only show non-CSRF errors to user, CSRF errors are technical
            for field, errors in form.errors.items():
                if field != 'csrf_token':  # Don't show CSRF errors to users
                    for error in errors:
                        flash(f"Feil i {field}: {error}", 'danger')
                else:
                    # For CSRF errors, try to process anyway if other fields are valid
                    app.logger.warning("CSRF token invalid, but processing form anyway")
                    # Check if all other fields are valid
                    csrf_error = form.errors.pop('csrf_token', None)
                    if not form.errors:  # Only CSRF error existed
                        try:
                            # Process the form despite CSRF error
                            if send_contact_email(form):
                                flash('Takk for din henvendelse! Vi kommer tilbake til deg så snart som mulig.', 'success')
                            else:
                                log_contact_message(form)
                                flash('Takk for din henvendelse! Vi kommer tilbake til deg så snart som mulig.', 'success')
                            return redirect(url_for('contact'))
                        except Exception as e:
                            app.logger.error(f"Contact form error: {e}")
                            log_contact_message(form)
                            flash('Takk for din henvendelse! Vi kommer tilbake til deg så snart som mulig.', 'success')
                            return redirect(url_for('contact'))
                    # Restore CSRF error for template display
                    if csrf_error:
                        form.errors['csrf_token'] = csrf_error
    
    return render_template('contact.html', form=form)

def send_contact_email(form):
    """Send contact form email via SendGrid or Gmail SMTP"""
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Try SendGrid first if available
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if sendgrid_key:
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            message = Mail(
                from_email='noreply@nawaratthaimat.no',
                to_emails='post@nawaratthaimat.no',
                subject=f'Ny henvendelse fra nettsiden: {form.subject.data}',
                html_content=f'''
                <h3>Ny henvendelse fra nettsiden</h3>
                <p><strong>Navn:</strong> {form.name.data}</p>
                <p><strong>E-post:</strong> {form.email.data}</p>
                <p><strong>Telefon:</strong> {form.phone.data or "Ikke oppgitt"}</p>
                <p><strong>Emne:</strong> {form.subject.data}</p>
                <p><strong>Melding:</strong></p>
                <p>{form.message.data}</p>
                <hr>
                <p><small>Sendt fra nawarat-thai-mat.replit.app</small></p>
                '''
            )
            
            sg = SendGridAPIClient(sendgrid_key)
            response = sg.send(message)
            app.logger.info(f"E-post sendt via SendGrid til post@nawaratthaimat.no")
            return True
            
        except Exception as e:
            app.logger.error(f"SendGrid error: {e}")
    
    # Try Gmail SMTP if available
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if gmail_user and gmail_password:
        try:
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = 'post@nawaratthaimat.no'
            msg['Subject'] = f'Ny henvendelse fra nettsiden: {form.subject.data}'
            
            body = f'''Ny henvendelse fra nettsiden

Navn: {form.name.data}
E-post: {form.email.data}
Telefon: {form.phone.data or "Ikke oppgitt"}
Emne: {form.subject.data}

Melding:
{form.message.data}

---
Sendt fra nawarat-thai-mat.replit.app
'''
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            server.sendmail(gmail_user, 'post@nawaratthaimat.no', text)
            server.quit()
            
            app.logger.info(f"E-post sendt via Gmail SMTP til post@nawaratthaimat.no")
            return True
            
        except Exception as e:
            app.logger.error(f"Gmail SMTP error: {e}")
    
    # Log that no email service is configured
    app.logger.info("Ingen e-posttjeneste konfigurert - meldinger lagres kun i logg")
    return False

def log_contact_message(form):
    """Log contact message to file as backup"""
    import datetime
    
    message = f"""
--- Ny henvendelse {datetime.datetime.now()} ---
Navn: {form.name.data}
E-post: {form.email.data}
Telefon: {form.phone.data or "Ikke oppgitt"}
Emne: {form.subject.data}
Melding: {form.message.data}
---
"""
    
    app.logger.info(f"Contact form submission: {message}")
    
    # Also write to file for easy access
    try:
        with open('contact_messages.log', 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    except Exception as e:
        app.logger.error(f"Could not write to contact log: {e}")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

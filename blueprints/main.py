"""Main blueprint for public-facing routes."""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models import MenuItem, RestaurantInfo
from forms import CateringInquiryForm
from utils.helpers import clean_description_and_extract_allergens
import logging

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage with focused hero and featured dishes."""
    # Get featured dishes from database or use defaults
    featured_dishes = []
    try:
        # Get top 6 dishes marked as featured or first 6 huvudretter
        dishes = MenuItem.query.filter_by(
            category='hovedretter', 
            is_active=True
        ).order_by(MenuItem.sort_order).limit(6).all()
        
        for dish in dishes:
            clean_desc, allergens = clean_description_and_extract_allergens(dish.description)
            featured_dishes.append({
                'name': dish.name,
                'price': dish.price,
                'description': clean_desc,
                'allergens': allergens,
                'image': dish.image_filename,
                'webp_image': dish.webp_filename if hasattr(dish, 'webp_filename') else None
            })
    except Exception as e:
        logging.error(f"Error loading featured dishes: {e}")
        # Fallback featured dishes
        featured_dishes = [
            {'name': '01. Kylling med cashewnøtter', 'price': '195', 'image': '01-kylling-cashew.jpg'},
            {'name': '07. Rød Karri m/ And', 'price': '205', 'image': '07-rod-karri-and.jpg'},
            {'name': '09. Pad Krapao', 'price': '195', 'image': '09-pad-krapao.jpg'}
        ]
    
    # Get restaurant info
    restaurant_info = {}
    try:
        info_items = RestaurantInfo.query.all()
        for item in info_items:
            restaurant_info[item.key] = item.value
    except:
        pass
    
    return render_template('index.html', 
                         featured_dishes=featured_dishes,
                         restaurant_info=restaurant_info)

@main_bp.route('/meny')
def menu():
    """Menu page with filtering and search capabilities."""
    # Get menu items from database
    try:
        db_items = MenuItem.query.filter_by(is_active=True).filter(
            MenuItem.category != 'catering'
        ).order_by(MenuItem.sort_order, MenuItem.id).all()
        
        menu_data = {
            'hovedretter': [],
            'ekstra': [],
            'drikker': []
        }
        
        for item in db_items:
            if item.category in menu_data:
                clean_desc, allergens = clean_description_and_extract_allergens(item.description)
                menu_data[item.category].append({
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'description': clean_desc,
                    'allergens': allergens,
                    'image': item.image_filename,
                    'webp_image': item.webp_filename if hasattr(item, 'webp_filename') else None,
                    'alt_text': item.alt_text if hasattr(item, 'alt_text') else item.name
                })
    except Exception as e:
        logging.error(f"Error loading menu: {e}")
        # Use fallback menu data
        menu_data = get_fallback_menu()
    
    return render_template('menu.html', menu=menu_data)

@main_bp.route('/catering')
def catering():
    """Catering page with packages and inquiry form."""
    # Get catering packages from database or use defaults
    packages = get_catering_packages()
    return render_template('catering.html', packages=packages)

@main_bp.route('/catering/foresporsel', methods=['POST'])
def catering_inquiry():
    """Handle catering inquiry form submission."""
    form = CateringInquiryForm()
    
    if form.validate_on_submit():
        # Process the inquiry (could send email, save to DB, etc.)
        flash('Takk for din forespørsel! Vi tar kontakt innen 24 timer.', 'success')
        
        # Log the inquiry
        logging.info(f"Catering inquiry from {form.firma.data}: {form.antall_personer.data} personer for {form.dato.data}")
        
        # Here you could send an email or save to database
        # For now, just redirect with success message
        return redirect(url_for('main.catering'))
    
    # If validation failed, return JSON response for AJAX handling
    if request.is_json:
        return jsonify({
            'success': False,
            'errors': form.errors
        }), 400
    
    flash('Vennligst sjekk skjemaet og prøv igjen.', 'error')
    return redirect(url_for('main.catering'))

@main_bp.route('/kontakt')
def contact():
    """Contact page with business information."""
    # Get restaurant info from database
    restaurant_info = {}
    try:
        info_items = RestaurantInfo.query.all()
        for item in info_items:
            restaurant_info[item.key] = item.value
    except:
        # Fallback info
        restaurant_info = {
            'address': 'Tordenskjolds gate 1, 2821 Gjøvik',
            'phone': '+47 61 17 77 71',
            'email': 'post@nawaratthaimat.no',
            'opening_hours': 'Tirsdag-Onsdag: 11:00-17:45\nTorsdag-Fredag: 11:00-19:45\nLørdag: 11:00-20:45\nSøndag: 12:00-19:45\nMandag: Stengt'
        }
    
    return render_template('contact.html', restaurant_info=restaurant_info)

@main_bp.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap for SEO."""
    from flask import Response, request
    from datetime import datetime
    
    base_url = request.url_root.rstrip('/')
    
    pages = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': '/meny', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': '/catering', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/kontakt', 'priority': '0.7', 'changefreq': 'monthly'},
    ]
    
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    
    for page in pages:
        xml_content += f'''
    <url>
        <loc>{base_url}{page['loc']}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>{page['changefreq']}</changefreq>
        <priority>{page['priority']}</priority>
    </url>'''
    
    xml_content += '\n</urlset>'
    
    return Response(xml_content, mimetype='text/xml')

@main_bp.route('/robots.txt')
def robots():
    """Generate robots.txt for SEO."""
    from flask import Response, request
    
    base_url = request.url_root.rstrip('/')
    content = f'''User-agent: *
Allow: /
Disallow: /admin/
Disallow: /static/admin/

Sitemap: {base_url}/sitemap.xml'''
    
    return Response(content, mimetype='text/plain')

def get_fallback_menu():
    """Return fallback menu data if database is unavailable."""
    return {
        'hovedretter': [
            {'name': '01. Kylling med cashewnøtter og ris', 'price': '195', 'description': 'Paprika, løk og hjemmelaget saus', 'allergens': '1,2,3,4,5,6,8', 'image': '01-kylling-cashew.jpg'},
            {'name': '02. Rød karri med kylling, svin eller biff og ris', 'price': '195', 'description': 'Bambus, paprika, basilikum, rød chilipasta og kokosmelk', 'allergens': '7', 'image': '02-rod-karri.jpg'},
            {'name': '03. Grønn karri med kylling, svin eller biff og ris', 'price': '195', 'description': 'Bambus, paprika, basilikum, grønn chilipasta og kokosmelk', 'allergens': '7', 'image': '03-gronn-karri.jpg'},
            {'name': '04. Paneng kai med kylling, svin, scampi eller biff og ris', 'price': '195', 'description': 'Paprika, basilikum, sitronblad, rød chilipasta og kokosmelk', 'allergens': '7', 'image': '04-paneng-kai.jpg'},
            {'name': '05. Sweet chili', 'price': '195', 'description': 'Paprika, løk, gulrot, ananas og hjemmelaget saus', 'allergens': '1,4,5', 'image': '05-sweet-chili.jpg'},
            {'name': '06. Stekt ris', 'price': '195', 'description': 'Brokkoli, gulrot, løk, egg, østersaus, gulrot og soyasaus', 'allergens': '1,2,4,5,6', 'image': '06-stekt-ris.jpg'},
            {'name': '07. Rød karri m/ And og Ris', 'price': '205', 'description': 'Ananas, paprika, basilikum, tomat og kokosmelk', 'allergens': '7', 'image': '07-rod-karri-and.jpg'},
            {'name': '08. Kyllingsuppe m/ Ris', 'price': '195', 'description': 'Champignon, tomat, løk, sitronblad, sitrongress, lime og kokosmelk', 'allergens': '', 'image': '08-kyllingsuppe.jpg'},
            {'name': '09. Pad Krapao', 'price': '195', 'description': 'Bambus, holy basilikum, chili, hvitløk, østersaus og soyasaus', 'allergens': '1,4,5', 'image': '09-pad-krapao.jpg'},
            {'name': '10. Biff m/ Østersaus', 'price': '215', 'description': 'Brokkoli, gulrot, løk, hjemmelaget saus', 'allergens': '1,4,5', 'image': '10-biff-ostersaus.jpg'},
            {'name': '11. Wok', 'price': '195', 'description': 'Paprika, løk, brokkoli, gulrot, hvitløk, soyasaus, østersaus', 'allergens': '1,2,4,5', 'image': '11-wok.jpg'},
            {'name': '12. Pad Thai', 'price': '195', 'description': 'Risnudler, egg, grønnsaker og hjemmelaget saus', 'allergens': '1,4,5,6', 'image': '12-pad-thai.jpg'},
            {'name': '13. Stekte Eggnudler m/ Kylling', 'price': '195', 'description': 'Eggnudler, grønnsaker, egg, edikk, soyasaus og østersaus', 'allergens': '1,4,5,6', 'image': '13-stekte-eggnudler.jpg'},
            {'name': '14. Vårruller m/ Salat & Ris', 'price': '195', 'description': 'Glassnudler, kål, gulrot, løk, kyllingkjøttdeig, soyasaus og østersaus', 'allergens': '1,4,5,8', 'image': '14-varruller.jpg'},
            {'name': '15. Kyllingklubber', 'price': '195', 'description': 'Med hjemmelaget marinade og ris', 'allergens': '1,4,5,6', 'image': '15-kyllingklubber.jpg'},
            {'name': '16. Innbakt Scampi', 'price': '195', 'description': 'Med salat og ris', 'allergens': '1,2,6', 'image': '16-innbakt-scampi.jpg'},
            {'name': '17. Mixed Tallerken', 'price': '195', 'description': '2 vårruller, 1 innbakt scampi og 1 innbakt kylling med salat og ris', 'allergens': '1,2,4,5,6,8', 'image': '17-mixed-tallerken.jpg'}
        ],
        'ekstra': [
            {'name': 'Vårruller pr stk', 'price': '25', 'description': '', 'image': None},
            {'name': 'Innbakt scampi pr stk', 'price': '30', 'description': '', 'image': None}
        ],
        'drikker': [
            {'name': 'Vann', 'price': '40', 'description': '', 'image': None},
            {'name': 'Brus', 'price': '40', 'description': '', 'image': None}
        ]
    }

def get_catering_packages():
    """Get catering packages from database or return defaults."""
    try:
        packages = MenuItem.query.filter_by(category='catering', is_active=True).order_by(MenuItem.sort_order).all()
        if packages:
            return [
                {
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'price': p.price,
                    'min_pax': getattr(p, 'min_pax', 10),
                    'features': getattr(p, 'features', [])
                } for p in packages
            ]
    except:
        pass
    
    # Fallback catering packages
    return [
        {
            'name': 'Menyforslag 1',
            'price': '199',
            'min_pax': 10,
            'description': 'Vårruller m/ sweet chili saus, Kylling m/ cashewnøtter, Stekt ris m/ grønnsaker',
            'features': ['3 retter', 'Vegetar-alternativ mulig', 'Inkludert bestikk']
        },
        {
            'name': 'Menyforslag 2',
            'price': '239',
            'min_pax': 10,
            'description': 'Kyllingsuppe, Rød karri m/ kylling, Pad Thai, Jasminris',
            'features': ['4 retter', 'Mild eller sterk', 'Allergitilpasning mulig']
        },
        {
            'name': 'Menyforslag 3',
            'price': '275',
            'min_pax': 10,
            'description': 'Tom Yum suppe, Grønn karri, Sweet & sour, Stekte nudler, Jasminris',
            'features': ['5 retter', 'Premium ingredienser', 'Dessert inkludert']
        },
        {
            'name': 'Menyforslag 4',
            'price': '299',
            'min_pax': 15,
            'description': 'Innbakt scampi, Paneng kai, Biff m/ østersaus, Pad Krapao, Stekt ris',
            'features': ['5 retter', 'Sjømat og kjøtt', 'Inkludert forrett']
        },
        {
            'name': 'Menyforslag 5',
            'price': '349',
            'min_pax': 15,
            'description': 'Mixed forrett, Rød karri m/ and, Wok m/ scampi, Pad Thai, Mango sticky rice',
            'features': ['5 retter + dessert', 'Premium and', 'Autentisk thai dessert']
        },
        {
            'name': 'Menyforslag 6',
            'price': '385',
            'min_pax': 20,
            'description': 'Komplett thai buffet med 8 retter inkludert forretter, hovedretter, ris og dessert',
            'features': ['8 retter total', 'Buffet-oppsett', 'Alt inkludert', 'Premium kvalitet']
        }
    ]
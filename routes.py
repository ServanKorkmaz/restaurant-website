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
    # Helper function to separate allergen info from description
    def clean_description_and_extract_allergens(desc):
        """Separate allergen info from description"""
        if not desc:
            return '', ''
        
        # Look for allergen patterns like "Allergener: 1,2,3"
        import re
        allergen_match = re.search(r'[.\s]*Allergener?:\s*([0-9,\s]+)', desc, re.IGNORECASE)
        if allergen_match:
            allergens = allergen_match.group(1).strip()
            # Remove allergen info from description
            clean_desc = re.sub(r'[.\s]*Allergener?:\s*[0-9,\s]+', '', desc, flags=re.IGNORECASE).strip().rstrip('.')
            return clean_desc, allergens
        return desc, ''
    
    # Get menu items from database, fallback to static data if empty
    db_items = MenuItem.query.filter_by(is_active=True).filter(MenuItem.category != 'catering').order_by(MenuItem.category, MenuItem.sort_order, MenuItem.name).all()
    
    if db_items and len([item for item in db_items if item.category == 'hovedretter']) > 0:
        # Use database items (exclude catering items)
        menu_data = {
            'hovedretter': [],
            'ekstra': [],
            'drikker': []
        }
        
        for item in db_items:
            if item.category in menu_data:
                clean_desc, allergens = clean_description_and_extract_allergens(item.description)
                menu_data[item.category].append({
                    'name': item.name,
                    'price': item.price,
                    'description': clean_desc,
                    'allergens': allergens or getattr(item, 'allergens', ''),
                    'image': item.image_filename
                })
    else:
        # Fallback to static data - this will be replaced by database items
        menu_data = {
        'hovedretter': [
            {'name': '01. Kylling med cashewnøtter og ris', 'price': '195', 'description': 'Paprika, løk og hjemmelaget saus', 'allergens': '1,2,3,4,5,6,8', 'image': '01-kylling-cashew.jpg'},
            {'name': 'Rød karri med kylling, svin eller biff og ris', 'price': '195', 'description': 'Bambus, paprika, basilikum, rød chilipasta og kokosmelk', 'allergens': '7', 'image': 'rod-karri.jpg'},
            {'name': 'Grønn karri med kylling, svin eller biff og ris', 'price': '195', 'description': 'Bambus, paprika, basilikum, grønn chilipasta og kokosmelk', 'allergens': '7', 'image': None},
            {'name': 'Paneng Kai med kylling, svin, scampi eller biff og ris', 'price': '195', 'description': 'Paprika, basilikum, sitronblad, rød chilipasta og kokosmelk', 'allergens': '7', 'image': 'paneng-kai.jpg'},
            {'name': 'Sweet chili med kylling, svin eller biff og ris', 'price': '195', 'description': 'Paprika, løk, gulrot, ananas og hjemmelaget saus', 'allergens': '1,4,5', 'image': 'sweet-chili.jpg'},
            {'name': 'Stekt ris med kylling, svin eller scampi', 'price': '195', 'description': 'Brokkoli, gulrot, løk, egg, østersaus, gulrot og soyasaus', 'allergens': '1,2,4,5,6', 'image': 'stekt-ris.jpg'},
            {'name': 'Rød karri med and og ris', 'price': '205', 'description': 'Ananas, paprika, basilikum, tomat og kokosmelk', 'allergens': '7', 'image': 'rod-karri-and.jpg'},
            {'name': 'Kylling suppe med ris', 'price': '195', 'description': 'Champignon, tomat, løk, sitronblad, sitrongress, lime og kokosmelk', 'allergens': '', 'image': 'kyllingsuppe.jpg'},
            {'name': 'Pad krapao med kylling, svin eller scampi og ris', 'price': '195', 'description': 'Bambus, holy basilikum, chili, hvitløk, østersaus og soyasaus', 'allergens': '1,4,5', 'image': 'pad-krapao.jpg'},
            {'name': 'Biff med østersaus', 'price': '215', 'description': 'Brokkoli, gulrot, løk, hjemmelaget saus', 'allergens': '1,4,5', 'image': 'biff-ostersaus.jpg'},
            {'name': 'Wok med kylling, biff, svin eller scampi', 'price': '195', 'description': 'Paprika, løk, brokkoli, gulrot, hvitløk, soyasaus, østersaus', 'allergens': '1,2,4,5', 'image': 'wok.jpg'},
            {'name': 'Pad Thai med kylling, svin eller scampi', 'price': '195', 'description': 'Risnudler, egg, grønnsaker og hjemmelaget saus', 'allergens': '1,4,5,6', 'image': None},
            {'name': 'Stekte eggnudler med kylling', 'price': '195', 'description': 'Eggnudler, grønnsaker, egg, edikk, soyasaus og østersaus', 'allergens': '1,4,5,6', 'image': 'stekte-eggnudler.jpg'},
            {'name': 'Vårruller med salat og ris', 'price': '195', 'description': 'Glassnudler, kål, gulrot, løk, kyllingkjøttdeig, soyasaus og østersaus', 'allergens': '1,4,5,8', 'image': 'varruller.jpg'},
            {'name': 'Kylling klubber med hjemmelaget marinade og ris', 'price': '195', 'description': '', 'allergens': '1,4,5,6', 'image': None},
            {'name': 'Innbakt scampi med salat og ris', 'price': '195', 'description': '', 'allergens': '1,2,6', 'image': None},
            {'name': 'Mixed tallerken med salat og ris', 'price': '195', 'description': '2 vårruller, 1 innbakt scampi og 1 innbakt kylling', 'allergens': '1,2,4,5,6,8', 'image': None}
        ],
        'ekstra': [
            {'name': 'Vårruller pr stk', 'price': '25', 'description': '', 'image': None},
            {'name': 'Innbakt scampi pr stk', 'price': '30', 'description': '', 'image': None}
        ],
        'drikker': [
            {'name': 'Vann', 'price': '40', 'description': '', 'image': None},
            {'name': 'Brus', 'price': '40', 'description': '', 'image': None}
        ],

    }
    
    return render_template('menu.html', menu=menu_data)

@app.route('/catering')
def catering():
    """Catering page with detailed catering packages"""
    return render_template('catering.html')

@app.route('/kontakt')
def contact():
    """Contact page with business information and mailto links"""
    return render_template('contact.html')

# Contact form functions removed since we now use mailto links

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

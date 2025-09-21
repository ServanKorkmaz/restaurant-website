from app import app, db
from models import CateringPackage

def init_catering_packages():
    """Initialize the 6 catering packages from the restaurant's menu"""
    
    packages = [
        {
            'name': 'Menyforslag 1',
            'price_per_person': '385 kr/pers',
            'description': 'Komplett buffet med norske og thailandske retter',
            'items': '''Laks og eggerøre
Karbonader med løk
Salat med dressing
Brød og smør
Potetsalat
Kyllingklubber i hjemmelaget marinade
Kylling med cashew nøtter
Vårruller''',
            'min_persons': 10,
            'allergens': '1,3,5,7,8',
            'best_for': 'Store selskap og bedriftsarrangementer',
            'sort_order': 1
        },
        {
            'name': 'Menyforslag 2 - Thai Tapas',
            'price_per_person': '365 kr/pers',
            'description': 'Variert utvalg av thailandske småretter',
            'items': '''Vårruller
Innbakt scampi
Kyllingklubber i hjemmelaget marinade
Hjemmelaget kyllingspyd med satay saus (peanøttsaus)
Innbakt kyllingfilet
Hjemmelaget dressing
Salat''',
            'min_persons': 10,
            'allergens': '1,2,3,5',
            'best_for': 'Cocktailparty og minglearrangementer',
            'sort_order': 2
        },
        {
            'name': 'Menyforslag 3',
            'price_per_person': '299 kr/pers',
            'description': 'Klassisk norsk og thai kombinasjon',
            'items': '''Laks og eggerøre
Karbonader med løk
Roastbeef m/ remulade
Stekte kyllingklubber i hjemmelaget marinade
Smør
Brød
Salat og hjemmelaget dressing''',
            'min_persons': 10,
            'allergens': '1,3,4,7,10',
            'best_for': 'Familiearrangementer og mindre selskap',
            'sort_order': 3
        },
        {
            'name': 'Menyforslag 4 - Spekemat',
            'price_per_person': '225 kr/pers',
            'description': 'Tradisjonell norsk spekemat',
            'items': '''Spekeskinke
Spekepølser
Eggerøre
Hjemmelaget potetsalat
Fruktfat
Flatbrød og smør''',
            'min_persons': 10,
            'allergens': '1,3,7',
            'best_for': 'Lunsj og uformelle sammenkomster',
            'sort_order': 4
        },
        {
            'name': 'Menyforslag 5 - Thai Mat',
            'price_per_person': '249 kr/pers',
            'description': 'Enkel thai-meny for mindre budsjetter',
            'items': '''Vårruller 2 stk pr pers
Kylling med cashew nøtter
Jasminris''',
            'min_persons': 10,
            'allergens': '1,5,8',
            'best_for': 'Enkle arrangementer og studentfester',
            'sort_order': 5
        },
        {
            'name': 'Menyforslag 6 - Thai Mat Deluxe',
            'price_per_person': '365 kr/pers',
            'description': 'Premium thai-buffet med varierte retter',
            'items': '''Vårruller
Stekte kyllingklubber i hjemmelaget marinade
Rød karri med kylling
Pad thai
Kylling med cashew nøtter
Jasminris''',
            'min_persons': 10,
            'allergens': '1,2,3,5,8',
            'best_for': 'Bryllup og store feiringer',
            'sort_order': 6
        }
    ]
    
    with app.app_context():
        # Check if packages already exist
        existing_count = CateringPackage.query.count()
        if existing_count > 0:
            print(f"Catering packages already exist ({existing_count} found). Skipping initialization.")
            return
        
        # Add all packages
        for package_data in packages:
            package = CateringPackage(**package_data)
            package.is_active = True
            db.session.add(package)
        
        db.session.commit()
        print(f"Successfully added {len(packages)} catering packages.")

if __name__ == '__main__':
    init_catering_packages()
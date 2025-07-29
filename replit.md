# Nawarat Thai Mat og Catering - Restaurant Website

## Overview

This is a Flask-based website for Nawarat Thai Mat og Catering, an authentic Thai restaurant and catering business in Gjøvik, Norway. The application provides a professional web presence with comprehensive Thai menu display, contact functionality, and business information. It's built with Flask as the web framework, Bootstrap for responsive design, and includes form handling for customer inquiries.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask
- **CSS Framework**: Bootstrap 5 with dark theme implementation
- **Icons**: Font Awesome 6.0.0 for consistent iconography
- **Typography**: Google Fonts (Playfair Display for headings, Inter for body text)
- **JavaScript**: Vanilla JavaScript with Bootstrap components
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Backend Architecture
- **Web Framework**: Flask (Python)
- **Form Handling**: Flask-WTF with WTForms for form validation
- **Session Management**: Flask sessions with configurable secret key
- **Middleware**: ProxyFix for proper header handling behind proxies
- **Logging**: Python's built-in logging configured for DEBUG level

### Application Structure
- **Single Module Design**: Centralized app creation with route imports
- **Separation of Concerns**: Routes, forms, and templates are separated into different files
- **Static Asset Management**: CSS and JavaScript files served through Flask's static file handling

## Key Components

### Core Application Files
- `app.py`: Flask application factory and configuration
- `routes.py`: URL route definitions and view functions
- `forms.py`: WTForms form definitions with Norwegian language validation
- `main.py`: Application entry point

### Templates
- `base.html`: Base template with navigation, Bootstrap integration, and common structure
- `index.html`: Homepage with hero section and business features
- `menu.html`: Menu display with categorized items and pricing
- `contact.html`: Contact form with validation and error handling

### Static Assets
- `custom.css`: Custom styling with Norwegian-themed color palette and animations
- `main.js`: Frontend JavaScript for navigation, animations, and form enhancements

## Data Flow

### Request Processing
1. User requests come through Flask routes
2. Routes render templates with context data (menu items, forms)
3. Static assets (CSS, JS) are served directly by Flask
4. Form submissions are processed with validation and feedback

### Menu Data Structure
- Menu items are defined as Python dictionaries within routes
- Categories include Thai appetizers, chicken dishes, pork & beef dishes, seafood, vegetarian options, drinks, and catering
- Each item contains authentic Thai dish names, Norwegian descriptions, and pricing in NOK
- Data is passed to templates for rendering with appropriate Thai cuisine iconography

### Form Processing
- Contact forms use Flask-WTF for CSRF protection
- Validation messages are displayed in Norwegian
- Form errors are handled gracefully with Bootstrap styling

## External Dependencies

### CDN Resources
- **Bootstrap CSS**: replit.com hosted Bootstrap with dark theme
- **Font Awesome**: CloudFlare CDN for icons
- **Google Fonts**: Typography resources

### Python Packages
- **Flask**: Web framework
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering
- **Werkzeug**: WSGI utilities and middleware

## Deployment Strategy

### Development Configuration
- Debug mode enabled for development
- Host set to '0.0.0.0' for container compatibility
- Port 5000 as default Flask development port
- Environment-based secret key configuration

### Production Considerations
- Secret key should be set via SESSION_SECRET environment variable
- Debug mode should be disabled in production
- ProxyFix middleware configured for reverse proxy deployment
- Logging configured for troubleshooting

### Container Ready
- Application listens on all interfaces (0.0.0.0)
- Static files served through Flask (suitable for single-container deployment)
- No database dependencies for simple deployment

## Norwegian Localization with Thai Restaurant Context

The application is fully localized for Norwegian users with authentic Thai restaurant content:
- All UI text in Norwegian with proper Thai dish names
- Form validation messages in Norwegian
- Norwegian business context (pricing in NOK, local business culture)
- Authentic Thai menu items with Norwegian descriptions
- Contact information for Nawarat Thai Mat og Catering (Tordenskjolds gate 1, 2821 Gjøvik)
- Operating hours: Tuesday-Wednesday 11:00-17:45, Thursday-Friday 11:00-19:45, Saturday 11:00-20:45, Sunday 12:00-19:45, closed Mondays

## Recent Changes (July 29, 2025)

✓ Updated restaurant identity from generic café to Nawarat Thai Mat og Catering
✓ Replaced menu with authentic dishes from real restaurant photos:
  - 14 hovedretter: Kylling m/ Cashewnøtter, Rød Karri, Paneng Kai, Sweet Chili, Stekt Ris, Rød Karri m/ And, Kyllingsuppe, Pad Krapao, Biff m/ Østersaus, Wok, Stekte Eggnudler m/ Kylling, Vårruller m/ Salat & Ris, Pad Thai, Nudelsuppe
  - 3 ekstra items: Vårull (25 NOK), Innbakt Scampi (30 NOK), Ekstra Ris (20 NOK)
  - 13 drikker: Full beverage menu with Coca-Cola, Pepsi, Solo, Fanta, etc. (40-69 NOK)
  - 4 catering options (removed Hjemmelaging service)
  - All prices now uniform yellow color across all sections
✓ Updated all contact information to match real restaurant (Tordenskjolds gate 1)
✓ Modified business description and features to reflect Thai cuisine focus
✓ Changed hero image from restaurant exterior to appetizing Cashew Chicken dish
✓ Updated operating hours to match actual restaurant schedule
✓ Improved multiple dish photos: Rød Karri m/ And, Kyllingsuppe, Pad Krapao, Wok
✓ Removed appetizer section, moved spring rolls to main dishes
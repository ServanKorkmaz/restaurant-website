# Gjøvik Kafe og Catering - Restaurant Website

## Overview

This is a Flask-based website for Gjøvik Kafe og Catering, a Norwegian café and catering business. The application provides a professional web presence with menu display, contact functionality, and business information. It's built with Flask as the web framework, Bootstrap for responsive design, and includes form handling for customer inquiries.

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
- Categories include coffee drinks, tea, cold beverages, food, and catering
- Each item contains name, price, and description fields
- Data is passed to templates for rendering

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

## Norwegian Localization

The application is fully localized for Norwegian users:
- All UI text in Norwegian
- Form validation messages in Norwegian
- Norwegian business context (pricing in NOK, local business culture)
- Norwegian typography and color scheme reflecting national identity
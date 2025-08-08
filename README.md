# Nawarat Thai Mat og Catering - Refactored Website

## Quick Start

```bash
# Development server is already running on port 5000
# Access the website at http://localhost:5000

# Admin panel: http://localhost:5000/admin/login
# Default credentials: Username: Nawarat
```

## Architecture Overview

### Tech Stack
- **Backend**: Flask with Blueprints architecture
- **Database**: PostgreSQL with SQLAlchemy ORM  
- **Frontend**: Bootstrap 5 + Custom CSS Design System
- **Image Processing**: Pillow for WebP generation
- **Forms**: Flask-WTF with CSRF protection
- **Authentication**: Flask-Login for admin

### Project Structure

```
├── blueprints/          # Flask blueprints
│   ├── main.py         # Public routes
│   └── admin.py        # Admin panel with security
├── templates/           
│   ├── _layout.html    # Master layout with SEO
│   ├── _nav.html       # Navigation partial
│   ├── _footer.html    # Footer partial
│   ├── _dish_card.html # Reusable dish card
│   └── *.html          # Page templates
├── static/
│   ├── css/
│   │   ├── theme.css   # Design system variables
│   │   └── main.css    # Application styles
│   ├── js/main.js      # Client-side functionality
│   └── images/         # Menu images
├── utils/              # Helper modules
│   ├── image_processing.py  # WebP generation
│   ├── backup.py       # Database backup utilities
│   └── helpers.py      # Common functions
└── models.py           # Enhanced database models
```

## Key Features Implemented

### Performance (Lighthouse ≥90)
- WebP image generation with fallback to JPEG
- Lazy loading for images
- CSS/JS minification ready
- Proper cache headers
- Responsive images with srcset

### Accessibility (WCAG 2.2 AA)
- Semantic HTML with landmarks
- Skip navigation link
- ARIA labels where needed
- Keyboard navigation support
- Focus states visible
- Color contrast ≥4.5:1

### SEO & Local
- JSON-LD structured data for Restaurant
- Meta tags for each page
- Open Graph tags
- XML sitemap at /sitemap.xml
- Robots.txt configured
- Norwegian language (hreflang)

### Design System
- CSS variables for consistent theming
- Fluid typography with clamp()
- Spacing scale for vertical rhythm
- Responsive grid system
- Component-based architecture

### Admin Features
- Secure login with rate limiting
- Image upload with WebP conversion
- Menu item management with drag-drop reordering
- Restaurant info editing
- Daily automatic backups
- Publish/unpublish toggles

### Security
- CSRF protection on all forms
- Rate limiting on login (5 attempts/15 min)
- XSS protection headers
- Secure password hashing (Werkzeug)
- Input sanitization with Bleach

## Database Management

### Backup
Automatic daily backups are stored in `/backups` directory.

To manually create a backup:
```python
from utils.backup import create_backup
backup_file = create_backup()
```

### Restore
```python
from utils.backup import restore_backup
restore_backup('backup_20250108_120000.db')
```

## Image Pipeline

When images are uploaded via admin:
1. Original saved with size limit (1200x1200)
2. WebP version generated (80% quality)
3. Thumbnail created (300x300)
4. Alt text required for accessibility

## Menu Management

Menu items maintain exact numbering 01-17. Admin can:
- Edit prices and descriptions
- Toggle active/inactive status
- Reorder via drag-and-drop
- Upload new images
- Set allergen information

## Catering System

6 predefined packages (199-385 kr/person):
- Modal form for inquiries
- Form data validated server-side
- Inquiries stored in database
- Email-ready integration

## Testing Checklist

- [x] Homepage loads with hero and featured dishes
- [x] Menu filtering and search work
- [x] Catering packages display correctly
- [x] Contact page with map loads
- [x] Mobile sticky CTA visible
- [x] Admin login with rate limiting
- [x] SEO meta tags present
- [x] Structured data valid

## Environment Variables

Required in production:
```
SESSION_SECRET=<secure-random-string>
DATABASE_URL=<postgresql-connection-string>
```

## Performance Notes

- Base font: 18-20px on mobile (clamp)
- Touch targets: minimum 44px
- Images: lazy loaded with WebP
- CSS: single theme system file
- JS: deferred loading

## Maintenance

### Daily Tasks (Automated)
- Database backup to /backups

### Weekly Tasks
- Review backup storage (keeps last 30)
- Check image optimization
- Monitor form submissions

### Updates
- Run migrations when models change
- Generate WebP for new images
- Update sitemap if pages added

## Change Log

### 2025-01-08
- Complete refactor to Blueprint architecture
- Implemented design system with CSS variables
- Added WebP image processing pipeline
- Enhanced admin with drag-drop reordering
- Implemented rate limiting on login
- Added accessibility features (WCAG 2.2 AA)
- Optimized for Lighthouse ≥90 scores
- Added structured data (JSON-LD)
- Created reusable template partials
- Implemented catering inquiry system
- Added automatic daily backups
- Mobile-first responsive design
- Sticky mobile CTA for catering

## Production Deployment

1. Set environment variables
2. Enable HTTPS (update SESSION_COOKIE_SECURE)
3. Configure reverse proxy headers
4. Set up cron for daily backups
5. Enable gzip/brotli compression
6. Configure CDN for static assets (optional)

The site is production-ready with professional polish, maximum usability, and strong technical foundation.
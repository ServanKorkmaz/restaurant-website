Nawarat Thai Mat og Catering  

Visit the website](https://nawaratthaimat.no/)

## About  
This is the official website for **Nawarat Thai Mat og Catering**, an authentic Thai restaurant in Gjøvik, Norway.  
It includes a dynamic menu, catering packages, contact details, and an admin dashboard for easy updates.  

## Features  
- Dynamic menu system with categories and images  
- Admin panel with CRUD operations and authentication  
- Catering package management  
- Responsive dark theme design (Bootstrap 5 + custom CSS)  
- Norwegian localization for all text and forms  

## Tech Stack  
- **Backend:** Flask (Python 3.11), Gunicorn  
- **Database:** PostgreSQL with SQLAlchemy  
- **Frontend:** Bootstrap 5, Jinja2 templates, custom CSS  
- **Authentication:** Flask-Login  
- **Forms:** Flask-WTF  

## Project Structure  
```
├── app.py              # Flask app factory
├── main.py             # Entry point
├── routes.py           # Public routes
├── admin_routes.py     # Admin routes
├── models.py           # Database models
├── forms.py            # Forms
├── templates/          # Jinja2 templates
├── static/css/         # Custom styling
└── static/images/      # Menu images
```

## Setup  
1. Clone the repository  
   ```
   git clone https://github.com/your-username/restaurant-website.git
   cd nawaratthaimat
   ```
2. Create and activate a virtual environment  
3. Install dependencies  
   ```
   pip install -r requirements.txt
   ```
4. Set environment variables  
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/nawaratdb
   SESSION_SECRET=your-secret
   ```
5. Run the app  
   ```
   flask run
   ```

## Contact  
- Address: Tordenskjolds gate 1, 2821 Gjøvik, Norway  
- Phone: +47 61 17 77 71  
- Email: post@nawaratthaimat.no  

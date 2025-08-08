"""Admin blueprint with enhanced security and functionality."""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import logging
import json
from functools import wraps
from collections import defaultdict
import time
import shutil
from PIL import Image
import io

from app import db
from models import User, MenuItem, RestaurantInfo
from forms import LoginForm, MenuItemForm, RestaurantInfoForm
from utils.image_processing import process_uploaded_image
from utils.backup import create_backup

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Simple rate limiting for login attempts
login_attempts = defaultdict(lambda: {'count': 0, 'last_attempt': 0})
RATE_LIMIT_ATTEMPTS = 5
RATE_LIMIT_WINDOW = 900  # 15 minutes in seconds

def rate_limit_check(ip_address):
    """Check if IP is rate limited."""
    now = time.time()
    attempts = login_attempts[ip_address]
    
    # Reset if outside window
    if now - attempts['last_attempt'] > RATE_LIMIT_WINDOW:
        attempts['count'] = 0
    
    attempts['last_attempt'] = int(now)
    attempts['count'] += 1
    
    if attempts['count'] > RATE_LIMIT_ATTEMPTS:
        return False
    return True

def admin_required(f):
    """Decorator to require admin access."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Du har ikke tilgang til denne siden.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login with rate limiting."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Check rate limiting
        ip_address = request.remote_addr
        if not rate_limit_check(ip_address):
            flash('For mange påloggingsforsøk. Prøv igjen om 15 minutter.', 'error')
            logging.warning(f"Rate limit exceeded for IP: {ip_address}")
            return render_template('admin/login.html', form=form)
        
        # Authenticate user
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            login_attempts[ip_address] = {'count': 0, 'last_attempt': 0}
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('admin.dashboard')
            
            logging.info(f"Admin login successful for user: {user.username}")
            return redirect(next_page)
        
        flash('Ugyldig brukernavn eller passord.', 'error')
        logging.warning(f"Failed login attempt for username: {form.username.data}")
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    """Admin logout."""
    logout_user()
    flash('Du er nå logget ut.', 'success')
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with statistics."""
    stats = {
        'total_dishes': MenuItem.query.filter_by(category='hovedretter').count(),
        'active_dishes': MenuItem.query.filter_by(category='hovedretter', is_active=True).count(),
        'catering_packages': MenuItem.query.filter_by(category='catering').count(),
        'last_backup': get_last_backup_time()
    }
    
    # Recent updates
    recent_items = MenuItem.query.order_by(MenuItem.updated_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_items=recent_items)

@admin_bp.route('/menu')
@admin_required
def menu_list():
    """List all menu items with management options."""
    category = request.args.get('category', 'hovedretter')
    items = MenuItem.query.filter_by(category=category).order_by(MenuItem.sort_order, MenuItem.id).all()
    
    return render_template('admin/menu_list.html', items=items, current_category=category)

@admin_bp.route('/menu/add', methods=['GET', 'POST'])
@admin_required
def menu_add():
    """Add new menu item with image processing."""
    form = MenuItemForm()
    
    if form.validate_on_submit():
        item = MenuItem()
        form.populate_obj(item)
        
        # Handle image upload
        if form.image.data:
            image_data = process_uploaded_image(form.image.data)
            if image_data:
                item.image_filename = image_data['original']
                item.webp_filename = image_data['webp']
                item.thumbnail_filename = image_data['thumbnail']
                item.alt_text = form.alt_text.data or item.name
        
        # Auto-assign sort order
        if not item.sort_order:
            max_order = db.session.query(db.func.max(MenuItem.sort_order)).filter_by(category=item.category).scalar()
            item.sort_order = (max_order or 0) + 1
        
        db.session.add(item)
        db.session.commit()
        
        flash(f'Menyelement "{item.name}" lagt til.', 'success')
        return redirect(url_for('admin.menu_list', category=item.category))
    
    return render_template('admin/menu_form.html', form=form, title='Legg til menyelement')

@admin_bp.route('/menu/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def menu_edit(id):
    """Edit menu item."""
    item = MenuItem.query.get_or_404(id)
    form = MenuItemForm(obj=item)
    
    if form.validate_on_submit():
        # Store old image filenames
        old_image = item.image_filename
        old_webp = getattr(item, 'webp_filename', None)
        old_thumb = getattr(item, 'thumbnail_filename', None)
        
        form.populate_obj(item)
        
        # Handle new image upload
        if form.image.data:
            image_data = process_uploaded_image(form.image.data)
            if image_data:
                item.image_filename = image_data['original']
                item.webp_filename = image_data['webp']
                item.thumbnail_filename = image_data['thumbnail']
                item.alt_text = form.alt_text.data or item.name
                
                # Clean up old images
                if old_image and old_image != item.image_filename:
                    try:
                        os.remove(os.path.join('static/images', old_image))
                        if old_webp:
                            os.remove(os.path.join('static/images', old_webp))
                        if old_thumb:
                            os.remove(os.path.join('static/images', old_thumb))
                    except:
                        pass
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Menyelement "{item.name}" oppdatert.', 'success')
        return redirect(url_for('admin.menu_list', category=item.category))
    
    return render_template('admin/menu_form.html', form=form, title='Rediger menyelement', item=item)

@admin_bp.route('/menu/<int:id>/toggle', methods=['POST'])
@admin_required
def menu_toggle(id):
    """Toggle menu item active status."""
    item = MenuItem.query.get_or_404(id)
    item.is_active = not item.is_active
    item.updated_at = datetime.utcnow()
    db.session.commit()
    
    status = 'aktivert' if item.is_active else 'deaktivert'
    flash(f'Menyelement "{item.name}" {status}.', 'success')
    
    if request.is_json:
        return jsonify({'success': True, 'is_active': item.is_active})
    
    return redirect(url_for('admin.menu_list', category=item.category))

@admin_bp.route('/menu/<int:id>/delete', methods=['POST'])
@admin_required
def menu_delete(id):
    """Delete menu item."""
    item = MenuItem.query.get_or_404(id)
    
    # Clean up images
    if item.image_filename:
        try:
            os.remove(os.path.join('static/images', item.image_filename))
            if hasattr(item, 'webp_filename') and item.webp_filename:
                os.remove(os.path.join('static/images', item.webp_filename))
            if hasattr(item, 'thumbnail_filename') and item.thumbnail_filename:
                os.remove(os.path.join('static/images', item.thumbnail_filename))
        except:
            pass
    
    db.session.delete(item)
    db.session.commit()
    
    flash(f'Menyelement "{item.name}" slettet.', 'success')
    
    if request.is_json:
        return jsonify({'success': True})
    
    return redirect(url_for('admin.menu_list', category=item.category))

@admin_bp.route('/menu/reorder', methods=['POST'])
@admin_required
def menu_reorder():
    """Reorder menu items via drag and drop."""
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({'success': False, 'error': 'Invalid data'}), 400
    
    try:
        for item_data in data['items']:
            item = MenuItem.query.get(item_data['id'])
            if item:
                item.sort_order = item_data['order']
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error reordering menu items: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/restaurant-info')
@admin_required
def restaurant_info():
    """Manage restaurant information."""
    info_items = RestaurantInfo.query.all()
    info_dict = {item.key: item.value for item in info_items}
    
    # Ensure default keys exist
    default_keys = ['address', 'phone', 'email', 'opening_hours', 'parking_info', 'about_text']
    for key in default_keys:
        if key not in info_dict:
            info_dict[key] = ''
    
    return render_template('admin/restaurant_info.html', info=info_dict)

@admin_bp.route('/restaurant-info/update', methods=['POST'])
@admin_required
def restaurant_info_update():
    """Update restaurant information."""
    form = RestaurantInfoForm()
    
    if form.validate_on_submit():
        for field_name, field in form._fields.items():
            if field_name not in ['csrf_token', 'submit']:
                # Update or create restaurant info entry
                info = RestaurantInfo.query.filter_by(key=field_name).first()
                if not info:
                    info = RestaurantInfo()
                info.key = field_name
                
                info.value = field.data
                info.updated_at = datetime.utcnow()
                db.session.add(info)
        
        db.session.commit()
        flash('Restaurantinformasjon oppdatert.', 'success')
    else:
        flash('Feil ved oppdatering. Sjekk skjemaet.', 'error')
    
    return redirect(url_for('admin.restaurant_info'))

@admin_bp.route('/backup/create', methods=['POST'])
@admin_required
def backup_create():
    """Create database backup."""
    try:
        backup_file = create_backup()
        flash(f'Backup opprettet: {backup_file}', 'success')
        return jsonify({'success': True, 'filename': backup_file})
    except Exception as e:
        logging.error(f"Backup creation failed: {e}")
        flash('Backup feilet. Se logg for detaljer.', 'error')
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/backup/download/<filename>')
@admin_required
def backup_download(filename):
    """Download backup file."""
    backup_dir = 'backups'
    filepath = os.path.join(backup_dir, secure_filename(filename))
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    
    flash('Backup-fil ikke funnet.', 'error')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/setup-admin', methods=['GET', 'POST'])
def setup_admin():
    """Initial admin setup (only if no admin exists)."""
    # Check if admin already exists
    admin_exists = User.query.filter_by(is_admin=True).first()
    
    if admin_exists:
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        username = request.form.get('username', 'Nawarat')
        password = request.form.get('password', 'nawarat2024')
        email = request.form.get('email', 'post@nawaratthaimat.no')
        
        # Create admin user
        admin = User()
        admin.username = username
        admin.email = email
        admin.is_admin = True
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        flash('Admin bruker opprettet. Du kan nå logge inn.', 'success')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/setup.html')

def get_last_backup_time():
    """Get the timestamp of the last backup."""
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        return None
    
    backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    if not backup_files:
        return None
    
    latest = max(backup_files, key=lambda f: os.path.getctime(os.path.join(backup_dir, f)))
    timestamp = os.path.getctime(os.path.join(backup_dir, latest))
    
    return datetime.fromtimestamp(timestamp)
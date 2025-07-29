from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User, MenuItem, RestaurantInfo
from admin_forms import LoginForm, MenuItemForm, RestaurantInfoForm, CreateAdminForm
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user)
            flash('Velkommen til admin-panelet!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Ugyldig brukernavn eller passord', 'error')
    
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
@admin_required
def logout():
    logout_user()
    flash('Du er nå logget ut', 'info')
    return redirect(url_for('index'))


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    menu_count = MenuItem.query.filter_by(is_active=True).count()
    total_items = MenuItem.query.count()
    return render_template('admin/dashboard.html', 
                         menu_count=menu_count, 
                         total_items=total_items)


@admin_bp.route('/menu')
@login_required
@admin_required
def menu_list():
    items = MenuItem.query.order_by(MenuItem.category, MenuItem.sort_order, MenuItem.name).all()
    return render_template('admin/menu_list.html', items=items)


@admin_bp.route('/menu/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            image_filename=form.image_filename.data if form.image_filename.data else None,
            is_active=form.is_active.data,
            sort_order=form.sort_order.data
        )
        db.session.add(item)
        db.session.commit()
        flash(f'Rett "{item.name}" er lagt til!', 'success')
        return redirect(url_for('admin.menu_list'))
    
    return render_template('admin/menu_form.html', form=form, title='Legg til ny rett')


@admin_bp.route('/menu/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    form = MenuItemForm(obj=item)
    
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        item.category = form.category.data
        item.image_filename = form.image_filename.data if form.image_filename.data else None
        item.is_active = form.is_active.data
        item.sort_order = form.sort_order.data
        db.session.commit()
        flash(f'Rett "{item.name}" er oppdatert!', 'success')
        return redirect(url_for('admin.menu_list'))
    
    return render_template('admin/menu_form.html', form=form, title=f'Rediger: {item.name}')


@admin_bp.route('/menu/delete/<int:id>')
@login_required
@admin_required
def delete_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    name = item.name
    db.session.delete(item)
    db.session.commit()
    flash(f'Rett "{name}" er slettet', 'info')
    return redirect(url_for('admin.menu_list'))


@admin_bp.route('/restaurant-info', methods=['GET', 'POST'])
@login_required
@admin_required
def restaurant_info():
    # Get current restaurant info
    phone = RestaurantInfo.query.filter_by(key='phone').first()
    email = RestaurantInfo.query.filter_by(key='email').first()
    address = RestaurantInfo.query.filter_by(key='address').first()
    hours = RestaurantInfo.query.filter_by(key='opening_hours').first()
    
    form = RestaurantInfoForm()
    
    if request.method == 'GET':
        # Pre-populate form with current values
        form.phone.data = phone.value if phone else '+47 61 17 77 71'
        form.email.data = email.value if email else 'post@nawaratthai.no'
        form.address.data = address.value if address else 'Tordenskjolds gate 1\n2821 Gjøvik\nNorge'
        form.opening_hours.data = hours.value if hours else 'Tir - Ons: 11:00 - 17:45\nTor - Fre: 11:00 - 19:45\nLørdag: 11:00 - 20:45\nSøndag: 12:00 - 19:45\nMandag: Stengt'
    
    if form.validate_on_submit():
        # Update or create restaurant info
        for key, value in [
            ('phone', form.phone.data),
            ('email', form.email.data),
            ('address', form.address.data),
            ('opening_hours', form.opening_hours.data)
        ]:
            info = RestaurantInfo.query.filter_by(key=key).first()
            if info:
                info.value = value
            else:
                info = RestaurantInfo(key=key, value=value)
                db.session.add(info)
        
        db.session.commit()
        flash('Restaurantinformasjon er oppdatert!', 'success')
        return redirect(url_for('admin.restaurant_info'))
    
    return render_template('admin/restaurant_info.html', form=form)


@admin_bp.route('/setup-admin', methods=['GET', 'POST'])
def setup_admin():
    # Only allow setup if no admin users exist
    if User.query.filter_by(is_admin=True).first():
        flash('Administrator eksisterer allerede', 'error')
        return redirect(url_for('admin.login'))
    
    form = CreateAdminForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Administrator opprettet! Du kan nå logge inn.', 'success')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/setup_admin.html', form=form)
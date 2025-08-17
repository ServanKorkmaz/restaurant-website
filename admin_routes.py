from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User, MenuItem, RestaurantInfo, CateringPackage
from admin_forms import LoginForm, MenuItemForm, RestaurantInfoForm, CreateAdminForm, CateringPackageForm
import json
from functools import wraps
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'is_admin', False):
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and getattr(user, 'is_admin', False):
            login_user(user, remember=form.remember_me.data)
            flash('Velkommen til admin-panelet!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Ugyldig brukernavn eller passord', 'error')
    
    return render_template('admin/login.html', form=form)


@admin_bp.route('/setup-admin', methods=['GET', 'POST'])
def setup_admin():
    # Check if admin already exists
    if User.query.filter_by(is_admin=True).first():
        flash('Administrator allerede opprettet', 'info')
        return redirect(url_for('admin.login'))
    
    form = CreateAdminForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = True
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Administrator opprettet! Du kan nå logge inn.', 'success')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/setup_admin.html', form=form)


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
        item = MenuItem()
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        item.category = form.category.data
        item.image_filename = form.image_filename.data if form.image_filename.data else None
        item.is_active = form.is_active.data
        item.sort_order = form.sort_order.data
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


@admin_bp.route('/menu/toggle/<int:id>')
@login_required
@admin_required
def toggle_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    item.is_active = not item.is_active
    db.session.commit()
    status = "aktivert" if item.is_active else "deaktivert"
    flash(f'Rett "{item.name}" er {status}!', 'success')
    return redirect(url_for('admin.menu_list'))


@admin_bp.route('/menu/delete/<int:id>')
@login_required
@admin_required
def delete_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    name = item.name
    db.session.delete(item)
    db.session.commit()
    flash(f'Rett "{name}" er slettet!', 'success')
    return redirect(url_for('admin.menu_list'))


@admin_bp.route('/catering')
@login_required
@admin_required
def catering_list():
    packages = CateringPackage.query.order_by(CateringPackage.sort_order, CateringPackage.name).all()
    return render_template('admin/catering_list.html', packages=packages)


@admin_bp.route('/catering/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_catering_package():
    form = CateringPackageForm()
    if form.validate_on_submit():
        package = CateringPackage()
        package.name = form.name.data
        package.price_per_person = form.price_per_person.data
        package.description = form.description.data
        package.items = form.items.data
        package.min_persons = form.min_persons.data
        package.allergens = form.allergens.data
        package.best_for = form.best_for.data
        package.sort_order = form.sort_order.data
        package.is_active = form.is_active.data
        db.session.add(package)
        db.session.commit()
        flash(f'Catering-pakke "{package.name}" er lagt til!', 'success')
        return redirect(url_for('admin.catering_list'))
    
    return render_template('admin/catering_form.html', form=form, title='Legg til ny catering-pakke')


@admin_bp.route('/catering/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_catering_package(id):
    package = CateringPackage.query.get_or_404(id)
    form = CateringPackageForm(obj=package)
    
    if form.validate_on_submit():
        package.name = form.name.data
        package.price_per_person = form.price_per_person.data
        package.description = form.description.data
        package.items = form.items.data
        package.min_persons = form.min_persons.data
        package.allergens = form.allergens.data
        package.best_for = form.best_for.data
        package.sort_order = form.sort_order.data
        package.is_active = form.is_active.data
        db.session.commit()
        flash(f'Catering-pakke "{package.name}" er oppdatert!', 'success')
        return redirect(url_for('admin.catering_list'))
    
    return render_template('admin/catering_form.html', form=form, title=f'Rediger: {package.name}')


@admin_bp.route('/catering/toggle/<int:id>')
@login_required
@admin_required
def toggle_catering_package(id):
    package = CateringPackage.query.get_or_404(id)
    package.is_active = not package.is_active
    db.session.commit()
    status = "aktivert" if package.is_active else "deaktivert"
    flash(f'Catering-pakke "{package.name}" er {status}!', 'success')
    return redirect(url_for('admin.catering_list'))


@admin_bp.route('/catering/delete/<int:id>')
@login_required
@admin_required
def delete_catering_package(id):
    package = CateringPackage.query.get_or_404(id)
    name = package.name
    db.session.delete(package)
    db.session.commit()
    flash(f'Catering-pakke "{name}" er slettet!', 'success')
    return redirect(url_for('admin.catering_list'))


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
        form.email.data = email.value if email else 'post@nawaratthaimat.no'
        form.address.data = address.value if address else 'Tordenskjolds gate 1\n2821 Gjøvik\nNorge'
        form.opening_hours.data = hours.value if hours else 'Tir - Ons: 11:00 - 17:45\nTor - Fre: 11:00 - 19:45\nLørdag: 11:00 - 20:45\nSøndag: 12:00 - 20:00\nMandag: Stengt'
    
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
                info = RestaurantInfo()
                info.key = key
                info.value = value
                db.session.add(info)
        
        db.session.commit()
        flash('Restaurantinformasjon er oppdatert!', 'success')
        return redirect(url_for('admin.restaurant_info'))
    
    return render_template('admin/restaurant_info.html', form=form)



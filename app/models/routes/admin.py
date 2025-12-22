from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app.extensions import database
from app.models.models.service import LaundryService
from app.models.models.order import ServiceOrder
from app.models.models.user import User

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

def karyawan_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('auth.login'))

        if not current_user.is_karyawan():
            flash('Anda tidak memiliki akses ke halaman ini. Hanya karyawan yang diizinkan.', 'danger')
            return redirect(url_for('main.index'))

        return function(*args, **kwargs)
    return decorated_function

@admin_blueprint.route('/dashboard')
@login_required
@karyawan_required
def dashboard():
    total_services = LaundryService.query.count()
    active_services = LaundryService.query.filter_by(is_active=True).count()
    total_users = User.query.count()
    total_orders = ServiceOrder.query.count()

    total_revenue = ServiceOrder.query.with_entities(ServiceOrder.total_price).all()
    total_revenue = sum(price[0] for price in total_revenue) if total_revenue else 0

    pending_orders = ServiceOrder.query.filter_by(status='pending').count()
    processing_orders = ServiceOrder.query.filter_by(status='processing').count()
    completed_orders = ServiceOrder.query.filter_by(status='ready').count() + ServiceOrder.query.filter_by(status='delivered').count()
    pending_revenue = ServiceOrder.query.filter_by(status='pending').with_entities(ServiceOrder.total_price).all()
    pending_revenue = sum(price[0] for price in pending_revenue) if pending_revenue else 0

    processing_revenue = ServiceOrder.query.filter_by(status='processing').with_entities(ServiceOrder.total_price).all()
    processing_revenue = sum(price[0] for price in processing_revenue) if processing_revenue else 0

    completed_revenue = ServiceOrder.query.filter(ServiceOrder.status.in_(['ready', 'delivered'])).with_entities(ServiceOrder.total_price).all()
    completed_revenue = sum(price[0] for price in completed_revenue) if completed_revenue else 0

    recent_services = LaundryService.query.order_by(LaundryService.created_at.desc()).limit(5).all()

    stats = {
        'total_services': total_services,
        'active_services': active_services,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'pending_revenue': pending_revenue,
        'processing_revenue': processing_revenue,
        'completed_revenue': completed_revenue
    }

    return render_template('admin/dashboard.html', stats=stats, recent_services=recent_services)

@admin_blueprint.route('/services')
@login_required
@karyawan_required
def manage_services():
    all_services = LaundryService.query.order_by(LaundryService.created_at.desc()).all()
    return render_template('admin/manage_service.html', services=all_services)

@admin_blueprint.route('/services/create', methods=['GET', 'POST'])
@login_required
@karyawan_required
def create_service():
    """
    CREATE: Menambah layanan baru.
    Form untuk input data layanan lengkap.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        unit = request.form.get('unit')
        duration = request.form.get('duration')
        image_url = request.form.get('image_url')
        
        # Validasi input
        if not all([name, description, price, unit]):
            flash('Nama, deskripsi, harga, dan satuan wajib diisi.', 'danger')
            return render_template('admin/edit_service.html', service=None)
        
        try:
            price = float(price)
            if price < 0:
                raise ValueError()
        except ValueError:
            flash('Harga harus berupa angka positif.', 'danger')
            return render_template('admin/edit_service.html', service=None)
        
        # Buat layanan baru
        try:
            new_service = LaundryService(
                name=name,
                description=description,
                price=price,
                unit=unit,
                duration=duration,
                image_url=image_url,
                is_active=True
            )
            
            database.session.add(new_service)
            database.session.commit()
            
            flash(f'Layanan "{name}" berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.manage_services'))
        except Exception as e:
            database.session.rollback()
            flash('Terjadi kesalahan saat menambahkan layanan. Silakan coba lagi.', 'danger')
            return render_template('admin/edit_service.html', service=None)
    
    return render_template('admin/edit_service.html', service=None)

@admin_blueprint.route('/services/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
@karyawan_required
def edit_service(service_id):
    """
    UPDATE: Mengubah data layanan yang sudah ada.
    Form pre-filled dengan data layanan saat ini.
    """
    service = LaundryService.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.description = request.form.get('description')
        service.price = float(request.form.get('price'))
        service.unit = request.form.get('unit')
        service.duration = request.form.get('duration')
        service.image_url = request.form.get('image_url')
        is_active = request.form.get('is_active')
        service.is_active = True if is_active == 'on' else False
        
        database.session.commit()
        
        flash(f'Layanan "{service.name}" berhasil diperbarui!', 'success')
        return redirect(url_for('admin.manage_services'))
    
    return render_template('admin/edit_service.html', service=service)

@admin_blueprint.route('/services/delete/<int:service_id>', methods=['POST'])
@login_required
@karyawan_required
def delete_service(service_id):
    """
    DELETE: Menghapus layanan dari database.
    Menggunakan hard delete.
    """
    service = LaundryService.query.get_or_404(service_id)
    service_name = service.name
    
    # Hard delete - hapus dari database
    database.session.delete(service)
    database.session.commit()
    
    flash(f'Layanan "{service_name}" berhasil dihapus!', 'success')
    return redirect(url_for('admin.manage_services'))

@admin_blueprint.route('/customers')
@login_required
@karyawan_required
def manage_customers():
    """
    Halaman manajemen pelanggan.
    Menampilkan daftar semua pelanggan dengan informasi lengkap.
    """
    customers = User.query.filter_by(role_id=2).order_by(User.created_at.desc()).all()  # role_id 2 = Customer
    return render_template('admin/manage_customers.html', customers=customers)

@admin_blueprint.route('/orders')
@login_required
@karyawan_required
def manage_orders():
    """
    Halaman manajemen pesanan untuk karyawan.
    Menampilkan semua pesanan dari semua pelanggan dengan opsi update status.
    """
    all_orders = ServiceOrder.query.order_by(ServiceOrder.order_date.desc()).all()
    return render_template('admin/manage_orders.html', orders=all_orders)

@admin_blueprint.route('/orders/update/<int:order_id>', methods=['POST'])
@login_required
@karyawan_required
def update_order_status(order_id):
    """
    UPDATE: Mengubah status pesanan.
    Hanya karyawan yang bisa mengubah status pesanan.
    """
    order = ServiceOrder.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    valid_statuses = ['pending', 'processing', 'ready', 'delivered', 'cancelled']
    if new_status not in valid_statuses:
        flash('Status pesanan tidak valid.', 'danger')
        return redirect(url_for('admin.manage_orders'))
    
    order.status = new_status
    database.session.commit()
    
    flash(f'Status pesanan #{order.id} berhasil diubah menjadi {new_status}.', 'success')
    return redirect(url_for('admin.manage_orders'))
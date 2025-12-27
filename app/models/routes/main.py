from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import database
from app.models.models.service import LaundryService
from app.models.models.order import ServiceOrder
from datetime import datetime
import random
import string

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    featured_services = LaundryService.query.filter_by(is_active=True).limit(6).all()
    return render_template('index.html', featured_services=featured_services)

@main_blueprint.route('/services')
def services():
    all_services = LaundryService.query.filter_by(is_active=True).all()
    return render_template('services.html', services=all_services)

@main_blueprint.route('/order/<int:service_id>', methods=['GET', 'POST'])
@login_required
def order(service_id):
    if current_user.is_karyawan():
        flash('Karyawan tidak dapat memesan layanan. Fitur pemesanan hanya untuk customer.', 'warning')
        return redirect(url_for('main.services'))

    service = LaundryService.query.get_or_404(service_id)

    if request.method == 'POST':
        quantity = request.form.get('quantity', type=int)
        notes = request.form.get('notes', '')
        pickup_address = request.form.get('pickup_address', '')
        delivery_address = request.form.get('delivery_address', '')

        if not quantity or quantity <= 0:
            flash('Jumlah harus lebih dari 0.', 'danger')
            return render_template('order.html', service=service)
        if not quantity or quantity <= 0:
            flash('Jumlah harus lebih dari 0.', 'danger')
            return render_template('order.html', service=service)

        if not pickup_address:
            flash('Alamat penjemputan wajib diisi.', 'danger')
            return render_template('order.html', service=service)
        if not delivery_address:
            flash('Alamat pengiriman wajib diisi.', 'danger')
            return render_template('order.html', service=service)
        total_price = service.price * quantity

        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

        while ServiceOrder.query.filter_by(order_number=order_number).first():
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

        new_order = ServiceOrder(
            order_number=order_number,
            user_id=current_user.id,
            service_id=service.id,
            quantity=quantity,
            total_price=total_price,
            notes=notes,
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            status='pending'
        )

        database.session.add(new_order)
        database.session.commit()

        flash('Pesanan berhasil dibuat! Kami akan segera memprosesnya.', 'success')
        return redirect(url_for('main.index'))

    return render_template('order.html', service=service)

@main_blueprint.route('/orders')
@login_required
def orders():
    if current_user.is_karyawan():
        all_orders = ServiceOrder.query.order_by(ServiceOrder.order_date.desc()).all()
        return render_template('orders.html', orders=all_orders, is_karyawan=True)
    else:
        user_orders = ServiceOrder.query.filter_by(user_id=current_user.id).order_by(ServiceOrder.order_date.desc()).all()
        return render_template('orders.html', orders=user_orders, is_karyawan=False)

@main_blueprint.route('/order/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """
    Route untuk customer membatalkan pesanan mereka sendiri.
    Hanya bisa membatalkan pesanan dengan status 'pending'.
    """
    if current_user.is_karyawan():
        flash('Karyawan tidak dapat membatalkan pesanan customer.', 'warning')
        return redirect(url_for('main.orders'))

    order = ServiceOrder.query.get_or_404(order_id)

    # Pastikan pesanan milik user yang sedang login
    if order.user_id != current_user.id:
        flash('Anda tidak memiliki akses untuk membatalkan pesanan ini.', 'danger')
        return redirect(url_for('main.orders'))

    # Hanya bisa membatalkan pesanan yang masih pending
    if order.status != 'pending':
        flash('Pesanan yang sudah diproses tidak dapat dibatalkan.', 'warning')
        return redirect(url_for('main.orders'))

    # Update status menjadi cancelled
    order.status = 'cancelled'
    database.session.commit()

    flash('Pesanan berhasil dibatalkan.', 'success')
    return redirect(url_for('main.orders'))

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/contact')
def contact():
    return render_template('contact.html')
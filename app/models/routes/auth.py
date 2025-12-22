from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import database
from app.models.models.user import User
from app.models.models.role import Role

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Menangani proses login pengguna.
    Melakukan validasi kredensial dan membuat session.
    """
    # Redirect jika sudah login
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Validasi input
        if not username or not password:
            flash('Username dan password harus diisi.', 'danger')
            return render_template('login.html')
        
        # Cari user di database
        user = User.query.filter_by(username=username).first()
        
        # Validasi kredensial
        if not user or not check_password_hash(user.password, password):
            flash('Username atau password salah. Silakan coba lagi.', 'danger')
            return render_template('login.html')
        
        # Login berhasil
        login_user(user, remember=remember)
        flash(f'Selamat datang, {user.full_name}! Login berhasil.', 'success')
        
        # Redirect ke halaman yang dituju sebelumnya atau dashboard
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        
        # Redirect berdasarkan role
        if user.is_karyawan():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.services'))
    
    return render_template('login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Menangani pendaftaran pengguna baru.
    Membuat akun dengan role User secara default.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        # Validasi input
        if not all([username, email, password, confirm_password, full_name]):
            flash('Semua field wajib diisi.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password minimal 6 karakter.', 'danger')
            return render_template('register.html')
        
        # Cek username dan email sudah terdaftar atau belum
        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar. Silakan gunakan username lain.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar. Silakan gunakan email lain.', 'danger')
            return render_template('register.html')
        
        # Dapatkan role Customer
        customer_role = Role.query.filter_by(name='Customer').first()
        
        # Buat user baru
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            full_name=full_name,
            phone=phone,
            role_id=customer_role.id
        )
        
        database.session.add(new_user)
        database.session.commit()
        
        flash('Registrasi berhasil! Silakan login dengan akun Anda.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    """
    Menangani proses logout pengguna.
    Menghapus session dan redirect ke halaman utama.
    """
    logout_user()
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('main.index'))
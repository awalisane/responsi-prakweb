# Sistem Manajemen Laundry Professional

## Deskripsi Proyek

Sistem Manajemen Laundry Professional adalah aplikasi web berbasis Flask yang dirancang untuk mengelola layanan laundry secara komprehensif. Aplikasi ini menyediakan fitur manajemen layanan, pesanan, dan sistem autentikasi berbasis role untuk Admin dan User.

## Fitur Utama

1. Autentikasi & Otorisasi
- Login & Logout: Sistem keamanan dengan password hashing menggunakan werkzeug.security
- Role-Based Access Control: 
  -Admin: Akses penuh untuk mengelola layanan, melihat pesanan, dan dashboard
  -User: Dapat melihat layanan dan melakukan pemesanan

2. Manajemen Layanan (CRUD)
- Create: Menambah layanan laundry baru dengan detail lengkap
- Read: Menampilkan daftar layanan dengan informasi komprehensif
- Update: Memperbarui informasi layanan yang sudah ada
- Delete: Menghapus layanan yang tidak diperlukan

3. Sistem Pemesanan
- User dapat melakukan pemesanan layanan laundry
- Tracking status pesanan
- Riwayat pesanan untuk setiap user

4. Database Relasional
- 4 tabel utama dengan relasi yang jelas:
  - `roles`: Menyimpan jenis role pengguna
  - `users`: Data pengguna dengan relasi ke roles
  - `laundry_services`: Katalog layanan laundry
  - `service_orders`: Pesanan dengan relasi ke users dan services



Backend
- python 3.8
- Flask 2.3.0**: Web framework
- Flask-SQLAlchemy**: ORM untuk database
- Flask-Login: Manajemen session dan autentikasi
- Werkzeug: Password hashing dan security

Database
- MySQL (Production)
- SQLite (Development/Demo)

Frontend
- HTML5 & Jinja2: Template engine
- Bootstrap 5.3: Framework CSS responsif
- Google Fonts: Poppins dan Inter
- Font Awesome 6: Icon library

Panduan Deployment

1. Setup Database Online

Opsi 1: Railway (PostgreSQL - Recommended)
1. Buat akun di [Railway.app](https://railway.app)
2. Buat project baru dan pilih "PostgreSQL"
3. Copy DATABASE_URL dari Railway dashboard

Opsi 2: Supabase (PostgreSQL - Free)
1. Buat akun di [Supabase.com](https://supabase.com)
2. Buat project baru
3. Pergi ke Settings > Database dan copy connection string

Opsi 3: PlanetScale (MySQL - Free)
1. Buat akun di [PlanetScale.com](https://planetscale.com)
2. Buat database baru
3. Copy connection string MySQL

### 2. Environment Variables

Buat file `.env` di root project:

```bash
# Copy dari .env.example
cp .env.example .env

# Edit .env dengan database URL yang didapat
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### 3. Migrasi Database

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan migrasi dari SQLite ke PostgreSQL
python migrate_db.py
```

### 4. Deploy Aplikasi

#### Railway Deployment:
1. Connect GitHub repository ke Railway
2. Set environment variables di Railway dashboard:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `FLASK_ENV=production`
3. Deploy otomatis

#### Manual Deployment:
```bash
# Install gunicorn untuk production
pip install gunicorn

# Jalankan aplikasi
gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

### 5. Testing Deployment

```bash
# Test koneksi database
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.models.models.user import User; print('Users:', User.query.count())"
```

## 📁 Struktur Proyek

```
project_laundry/
├── app/
│   ├── __init__.py              # Inisialisasi aplikasi Flask
│   ├── models/
│   │   ├── __init__.py
│   │   ├── role.py              # Model Role
│   │   ├── user.py              # Model User
│   │   ├── laundry_service.py   # Model Laundry Service
│   │   └── service_order.py     # Model Service Order
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Route autentikasi
│   │   ├── main.py              # Route utama
│   │   ├── services.py          # Route manajemen layanan
│   │   └── orders.py            # Route pesanan
│   ├── templates/
│   │   ├── base.html            # Template dasar
│   │   ├── index.html           # Halaman beranda
│   │   ├── login.html           # Halaman login
│   │   ├── register.html        # Halaman registrasi
│   │   ├── services/
│   │   │   ├── list.html        # Daftar layanan
│   │   │   ├── detail.html      # Detail layanan
│   │   │   ├── create.html      # Form tambah layanan
│   │   │   └── edit.html        # Form edit layanan
│   │   ├── orders/
│   │   │   ├── list.html        # Daftar pesanan
│   │   │   └── create.html      # Form pemesanan
│   │   └── dashboard.html       # Dashboard admin
│   └── static/
│       ├── css/
│       │   └── style.css        # Custom CSS
│       └── images/              # Gambar (dari CDN)
├── config.py                    # Konfigurasi aplikasi
├── run.py                       # Entry point aplikasi
├── requirements.txt             # Dependencies Python
└── README.md                    # Dokumentasi (file ini)
```

## Instalasi dan Penggunaan

### 1. Persiapan Virtual Environment

Virtual environment adalah isolated environment untuk Python yang memungkinkan instalasi package tanpa mempengaruhi sistem Python global. Hal ini penting untuk:
- Menghindari konflik dependency antar project
- Memudahkan deployment dengan requirements yang jelas
- Menjaga kebersihan sistem Python

#### Langkah-langkah Pembuatan Virtual Environment:

**a. Buka terminal/command prompt dan navigasi ke folder project**
```bash
cd path/to/project_laundry
```

**b. Buat virtual environment**

Di Windows:
```bash
python -m venv venv
```

Di Linux/Mac:
```bash
python3 -m venv venv
```

Perintah ini akan membuat folder bernama `venv` yang berisi salinan interpreter Python dan tools untuk mengelola package.

**c. Aktivasi virtual environment**

Di Windows:
```bash
venv\Scripts\activate
```

Di Linux/Mac:
```bash
source venv/bin/activate
```

Setelah aktivasi, Anda akan melihat `(venv)` di awal baris command prompt, menandakan virtual environment aktif.

### 2. Instalasi Dependencies

Setelah virtual environment aktif, install semua dependencies yang diperlukan:

```bash
pip install -r requirements.txt
```

File `requirements.txt` berisi daftar lengkap package Python yang dibutuhkan aplikasi beserta versinya, memastikan konsistensi environment di berbagai mesin.

### 3. Konfigurasi Database

**a. Untuk SQLite (Development)**

Tidak perlu konfigurasi tambahan, database akan dibuat otomatis saat pertama kali menjalankan aplikasi.

**b. Untuk MySQL (Production)**

Edit file `config.py` dan sesuaikan connection string:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/laundry_db'
```

Buat database di MySQL:
```sql
CREATE DATABASE laundry_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Inisialisasi Database

Jalankan perintah berikut untuk membuat tabel dan data awal:

```bash
python run.py
```

Aplikasi akan otomatis membuat:
- Struktur tabel database sesuai model
- Data role (Admin dan User)
- User admin default
- Sample data layanan dan pesanan

### 5. Menjalankan Aplikasi

Setelah database terinisialisasi, jalankan aplikasi:

```bash
python run.py
```

Aplikasi akan berjalan di: `http://127.0.0.1:5000`

### 6. Login Kredensial Default

**Admin:**
- Email: admin@laundry.com
- Password: admin123

**User Demo:**
- Email: user@laundry.com
- Password: user123

## Diagram Relasi Database

### Struktur Relasi

```
roles (1) ─────< (N) users
                        │
                        │ (1)
                        │
                        ∨
              (N) service_orders (N)
                        │
                        │ (N)
                        │
                        ∨
                        (1) laundry_services
```

### Penjelasan Relasi:

1. **roles → users** (One-to-Many)
   - Satu role dapat dimiliki oleh banyak users
   - Setiap user memiliki satu role
   - Foreign Key: `users.role_id` → `roles.id`

2. **users → service_orders** (One-to-Many)
   - Satu user dapat membuat banyak pesanan
   - Setiap pesanan dimiliki oleh satu user
   - Foreign Key: `service_orders.user_id` → `users.id`

3. **laundry_services → service_orders** (One-to-Many)
   - Satu layanan dapat dipesan berkali-kali
   - Setiap pesanan mengacu pada satu layanan
   - Foreign Key: `service_orders.service_id` → `laundry_services.id`

### Detail Tabel:

**Table: roles**
- `id` (Primary Key)
- `name` (VARCHAR) - Nama role (Admin, User)
- `description` (TEXT) - Deskripsi role

**Table: users**
- `id` (Primary Key)
- `email` (VARCHAR, UNIQUE) - Email pengguna
- `password_hash` (VARCHAR) - Password ter-hash
- `full_name` (VARCHAR) - Nama lengkap
- `phone` (VARCHAR) - Nomor telepon
- `role_id` (Foreign Key → roles.id)
- `created_at` (DATETIME)

**Table: laundry_services**
- `id` (Primary Key)
- `name` (VARCHAR) - Nama layanan
- `description` (TEXT) - Deskripsi layanan
- `price` (DECIMAL) - Harga per kg
- `duration_days` (INTEGER) - Durasi pengerjaan
- `image_url` (VARCHAR) - URL gambar layanan
- `is_active` (BOOLEAN) - Status aktif/tidak

**Table: service_orders**
- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `service_id` (Foreign Key → laundry_services.id)
- `weight_kg` (DECIMAL) - Berat cucian dalam kg
- `total_price` (DECIMAL) - Total harga
- `status` (VARCHAR) - Status pesanan
- `pickup_address` (TEXT) - Alamat penjemputan
- `notes` (TEXT) - Catatan tambahan
- `order_date` (DATETIME)
- `estimated_completion` (DATETIME)

## Fitur Keamanan

### 1. Password Hashing
- Menggunakan `werkzeug.security.generate_password_hash`
- Algoritma: PBKDF2 dengan SHA-256
- Salt otomatis untuk setiap password
- Tidak ada password plain text di database

### 2. Session Management
- Flask-Login untuk manajemen session
- Session timeout otomatis
- CSRF protection (bisa ditambahkan dengan Flask-WTF)

### 3. Role-Based Authorization
- Decorator `@admin_required` untuk route admin
- Pemeriksaan role di level aplikasi
- Redirect otomatis jika akses tidak sah

## Cara Pengujian Fitur

### 1. Testing CRUD Layanan (Admin)
1. Login sebagai admin
2. Akses menu "Kelola Layanan"
3. **Create**: Klik "Tambah Layanan", isi form, submit
4. **Read**: Lihat daftar layanan di halaman
5. **Update**: Klik "Edit" pada layanan, ubah data, submit
6. **Delete**: Klik "Hapus" pada layanan, konfirmasi

### 2. Testing Autentikasi
1. Akses halaman login
2. Masukkan kredensial yang salah → muncul pesan error
3. Masukkan kredensial yang benar → redirect ke dashboard
4. Klik logout → kembali ke halaman utama

### 3. Testing Otorisasi
1. Login sebagai user biasa
2. Coba akses URL admin langsung (misal: `/admin/services`)
3. Sistem akan redirect dengan pesan akses ditolak
4. Login sebagai admin → akses berhasil

### 4. Testing Responsiveness
1. Buka aplikasi di browser
2. Tekan F12 untuk developer tools
3. Toggle device toolbar
4. Cek tampilan di berbagai ukuran layar:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1200px+)

## Troubleshooting

### Error: "ModuleNotFoundError"
**Solusi**: Pastikan virtual environment aktif dan semua dependencies terinstall
```bash
pip install -r requirements.txt
```

### Error: "sqlalchemy.exc.OperationalError"
**Solusi**: 
- Cek koneksi database MySQL
- Pastikan database sudah dibuat
- Verifikasi username/password di config.py

### Error: "Address already in use"
**Solusi**: Port 5000 sudah digunakan, ubah port di run.py:
```python
app.run(debug=True, port=5001)
```

### Tampilan Tidak Responsif
**Solusi**: 
- Clear browser cache (Ctrl+Shift+Del)
- Hard reload (Ctrl+F5)
- Pastikan CDN Bootstrap dapat diakses

## Pengembangan Lebih Lanjut

### Fitur yang Dapat Ditambahkan:
1. **Payment Gateway**: Integrasi dengan Midtrans/Xendit
2. **Email Notification**: Notifikasi status pesanan via email
3. **Real-time Tracking**: WebSocket untuk tracking real-time
4. **Report & Analytics**: Dashboard statistik dan laporan
5. **Rating & Review**: Sistem ulasan layanan
6. **Multi-language**: Support bahasa Inggris
7. **API REST**: Untuk integrasi dengan mobile app

## Kontribusi dan Lisensi

Project ini dibuat untuk keperluan akademik Tugas Akhir Pengembangan Web dengan Flask.

### Teknologi Open Source yang Digunakan:
- Flask (BSD License)
- Bootstrap (MIT License)
- Font Awesome (Font Awesome Free License)
- Google Fonts (Apache License 2.0)

## Kontak dan Support

Untuk pertanyaan atau dukungan terkait aplikasi ini, silakan hubungi melalui:
- Email: support@laundry.com
- Repository: [Link GitHub jika ada]
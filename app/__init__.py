from flask import Flask
from flask_login import LoginManager
from config import Config
from .extensions import database, login_manager
from .models.models.role import Role
from .models.models.user import User
from .models.models.service import LaundryService
import logging

def create_app(config_class=Config):
    """
    Factory function untuk membuat instance aplikasi Flask.
    Pattern ini memungkinkan multiple instances dengan konfigurasi berbeda.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    @app.template_filter('number_format')
    def number_format(value):
        try:
            return f"{value:,.0f}".replace(',', '.')
        except (ValueError, TypeError):
            return value

    database.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu untuk mengakses halaman ini.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        from .models.models.user import User
        return User.query.get(int(user_id))

    from .models.routes import auth, main, admin
    app.register_blueprint(auth.auth_blueprint)
    app.register_blueprint(main.main_blueprint)
    app.register_blueprint(admin.admin_blueprint)
    
    with app.app_context():
        database.create_all()
        from werkzeug.security import generate_password_hash

        try:
            role_count = Role.query.count()
            if role_count == 0:
                karyawan_role = Role(name='Karyawan', description='Karyawan dengan akses penuh untuk mengelola sistem')
                customer_role = Role(name='Customer', description='Customer dengan akses terbatas untuk pemesanan')
                database.session.add_all([karyawan_role, customer_role])
                database.session.commit()

            karyawan_exists = User.query.filter_by(username='karyawan').first() is not None
            umi_exists = User.query.filter_by(username='umi').first() is not None

            if not karyawan_exists or not umi_exists:
                karyawan_role = Role.query.filter_by(name='Karyawan').first()
                customer_role = Role.query.filter_by(name='Customer').first()

                if karyawan_role and customer_role:
                    users_to_add = []

                    if not karyawan_exists:
                        karyawan_user = User(
                            username='karyawan',
                            email='karyawan@miyalaundry.com',
                            password=generate_password_hash('karyawan123'),
                            full_name='Karyawan Laundry',
                            phone='081234567890',
                            role_id=karyawan_role.id
                        )
                        users_to_add.append(karyawan_user)
                    
                    if not umi_exists:
                        # Membuat customer umi
                        customer1 = User(
                            username='umi',
                            email='umi@email.com',
                            password=generate_password_hash('umi123'),
                            full_name='Umi Santoso',
                            phone='081234567891',
                            role_id=customer_role.id
                        )
                        users_to_add.append(customer1)
                    
                    # Add more customers to reach 50+ users
                    customer_data = [
                        ('budi', 'budi@email.com', 'Budi Santoso', '081234567892'),
                        ('siti', 'siti@email.com', 'Siti Aminah', '081234567893'),
                        ('ahmad', 'ahmad@email.com', 'Ahmad Rahman', '081234567894'),
                        ('maya', 'maya@email.com', 'Maya Sari', '081234567895'),
                        ('doni', 'doni@email.com', 'Doni Kusuma', '081234567896'),
                        ('lisa', 'lisa@email.com', 'Lisa Putri', '081234567897'),
                        ('rudi', 'rudi@email.com', 'Rudi Hartono', '081234567898'),
                        ('nina', 'nina@email.com', 'Nina Wijaya', '081234567899'),
                        ('eko', 'eko@email.com', 'Eko Prasetyo', '081234567900'),
                        ('rini', 'rini@email.com', 'Rini Susanti', '081234567901'),
                        ('agus', 'agus@email.com', 'Agus Setiawan', '081234567902'),
                        ('tina', 'tina@email.com', 'Tina Marlina', '081234567903'),
                        ('yudi', 'yudi@email.com', 'Yudi Nugroho', '081234567904'),
                        ('sari', 'sari@email.com', 'Sari Dewi', '081234567905'),
                        ('andi', 'andi@email.com', 'Andi Firmansyah', '081234567906'),
                        ('wulan', 'wulan@email.com', 'Wulan Sari', '081234567907'),
                        ('dika', 'dika@email.com', 'Dika Pratama', '081234567908'),
                        ('ani', 'ani@email.com', 'Ani Wijaya', '081234567909'),
                        ('bagus', 'bagus@email.com', 'Bagus Setiawan', '081234567910'),
                        ('cici', 'cici@email.com', 'Cici Marlina', '081234567911'),
                        ('deni', 'deni@email.com', 'Deni Nugroho', '081234567912'),
                        ('ela', 'ela@email.com', 'Ela Dewi', '081234567913'),
                        ('fajar', 'fajar@email.com', 'Fajar Firmansyah', '081234567914'),
                        ('gita', 'gita@email.com', 'Gita Sari', '081234567915'),
                        ('hadi', 'hadi@email.com', 'Hadi Pratama', '081234567916'),
                        ('ina', 'ina@email.com', 'Ina Wijaya', '081234567917'),
                        ('joko', 'joko@email.com', 'Joko Setiawan', '081234567918'),
                        ('kiki', 'kiki@email.com', 'Kiki Marlina', '081234567919'),
                        ('luki', 'luki@email.com', 'Luki Nugroho', '081234567920'),
                        ('mira', 'mira@email.com', 'Mira Dewi', '081234567921'),
                        ('nando', 'nando@email.com', 'Nando Firmansyah', '081234567922'),
                        ('olga', 'olga@email.com', 'Olga Sari', '081234567923'),
                        ('pandu', 'pandu@email.com', 'Pandu Pratama', '081234567924'),
                        ('qiqi', 'qiqi@email.com', 'Qiqi Wijaya', '081234567925'),
                        ('raka', 'raka@email.com', 'Raka Setiawan', '081234567926'),
                        ('sasa', 'sasa@email.com', 'Sasa Marlina', '081234567927'),
                        ('toto', 'toto@email.com', 'Toto Nugroho', '081234567928'),
                        ('ulia', 'ulia@email.com', 'Ulia Dewi', '081234567929'),
                        ('vivi', 'vivi@email.com', 'Vivi Firmansyah', '081234567930'),
                        ('wawan', 'wawan@email.com', 'Wawan Sari', '081234567931'),
                        ('xena', 'xena@email.com', 'Xena Pratama', '081234567932'),
                        ('yaya', 'yaya@email.com', 'Yaya Wijaya', '081234567933'),
                        ('zaki', 'zaki@email.com', 'Zaki Setiawan', '081234567934'),
                        ('amin', 'amin@email.com', 'Amin Marlina', '081234567935'),
                        ('bela', 'bela@email.com', 'Bela Nugroho', '081234567936'),
                        ('candra', 'candra@email.com', 'Candra Dewi', '081234567937'),
                        ('dina', 'dina@email.com', 'Dina Firmansyah', '081234567938'),
                        ('erik', 'erik@email.com', 'Erik Sari', '081234567939'),
                        ('fani', 'fani@email.com', 'Fani Pratama', '081234567940'),
                        ('galih', 'galih@email.com', 'Galih Wijaya', '081234567941'),
                        ('hana', 'hana@email.com', 'Hana Setiawan', '081234567942'),
                        ('iman', 'iman@email.com', 'Iman Marlina', '081234567943'),
                        ('juna', 'juna@email.com', 'Juna Nugroho', '081234567944'),
                        ('kartika', 'kartika@email.com', 'Kartika Dewi', '081234567945'),
                        ('luna', 'luna@email.com', 'Luna Firmansyah', '081234567946'),
                        ('maman', 'maman@email.com', 'Maman Sari', '081234567947'),
                        ('nana', 'nana@email.com', 'Nana Pratama', '081234567948'),
                        ('opik', 'opik@email.com', 'Opik Wijaya', '081234567949'),
                        ('putri', 'putri@email.com', 'Putri Setiawan', '081234567950'),
                        ('qori', 'qori@email.com', 'Qori Marlina', '081234567951'),
                        ('rahman', 'rahman@email.com', 'Rahman Nugroho', '081234567952'),
                        ('siska', 'siska@email.com', 'Siska Dewi', '081234567953'),
                        ('tono', 'tono@email.com', 'Tono Firmansyah', '081234567954'),
                        ('umi2', 'umi2@email.com', 'Umi Sari', '081234567955'),
                        ('vika', 'vika@email.com', 'Vika Pratama', '081234567956'),
                        ('widi', 'widi@email.com', 'Widi Wijaya', '081234567957'),
                        ('yuni', 'yuni@email.com', 'Yuni Setiawan', '081234567958'),
                        ('zara', 'zara@email.com', 'Zara Marlina', '081234567959'),
                    ]
                    
                    for username, email, full_name, phone in customer_data:
                        if not User.query.filter_by(username=username).first():
                            customer = User(
                                username=username,
                                email=email,
                                password=generate_password_hash(f'{username}123'),
                                full_name=full_name,
                                phone=phone,
                                role_id=customer_role.id
                            )
                            users_to_add.append(customer)
                    
                    if users_to_add:
                        database.session.add_all(users_to_add)
                        database.session.commit()
                        print("Seed data berhasil dibuat")
                else:
                    print("Roles not found, skipping user seeding")
        except Exception as e:
            database.session.rollback()
            app.logger.error(f"Error saat seeding data: {e}")
        
        if LaundryService.query.count() == 0:
            # Membuat layanan laundry contoh
            services_data = [
                {
                    'name': 'Cuci Kering Reguler',
                    'description': 'Layanan cuci dan kering standar untuk pakaian sehari-hari. Proses pencucian menggunakan deterjen berkualitas dan pengeringan sempurna.',
                    'price': 5000.00,
                    'unit': 'per kg',
                    'duration': '2-3 hari',
                    'image_url': 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800'
                },
                {
                    'name': 'Cuci Kering Express',
                    'description': 'Layanan cuci dan kering kilat untuk kebutuhan mendesak. Pakaian selesai dalam waktu singkat dengan kualitas terjamin.',
                    'price': 8000.00,
                    'unit': 'per kg',
                    'duration': '1 hari',
                    'image_url': 'https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?w=800'
                },
                {
                    'name': 'Cuci Setrika Premium',
                    'description': 'Paket lengkap cuci, kering, dan setrika rapi. Cocok untuk pakaian kerja dan acara formal yang membutuhkan tampilan sempurna.',
                    'price': 7000.00,
                    'unit': 'per kg',
                    'duration': '3-4 hari',
                    'image_url': 'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800'
                },
                {
                    'name': 'Setrika Saja',
                    'description': 'Layanan khusus setrika untuk pakaian yang sudah bersih. Hasil rapi dan profesional dengan teknik setrika modern.',
                    'price': 3000.00,
                    'unit': 'per kg',
                    'duration': '1-2 hari',
                    'image_url': 'https://images.unsplash.com/photo-1489274495757-95c7c837b101?w=800'
                },
                {
                    'name': 'Cuci Sepatu',
                    'description': 'Perawatan khusus untuk sepatu dengan metode deep cleaning. Menghilangkan kotoran membandel dan bau tidak sedap.',
                    'price': 25000.00,
                    'unit': 'per pasang',
                    'duration': '3-5 hari',
                    'image_url': 'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=800'
                },
                {
                    'name': 'Cuci Karpet',
                    'description': 'Pembersihan karpet menyeluruh dengan peralatan profesional. Menghilangkan debu, tungau, dan noda membandel.',
                    'price': 15000.00,
                    'unit': 'per meter',
                    'duration': '5-7 hari',
                    'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'
                },
                {
                    'name': 'Cuci Boneka',
                    'description': 'Perawatan lembut untuk boneka kesayangan. Proses pencucian aman tanpa merusak bentuk dan warna boneka.',
                    'price': 20000.00,
                    'unit': 'per item',
                    'duration': '4-6 hari',
                    'image_url': 'https://images.unsplash.com/photo-1530325553241-4f6e7690cf36?w=800'
                },
                {
                    'name': 'Dry Clean Jas',
                    'description': 'Dry cleaning khusus untuk jas, blazer, dan pakaian formal. Menjaga kualitas kain dan bentuk pakaian tetap prima.',
                    'price': 35000.00,
                    'unit': 'per potong',
                    'duration': '5-7 hari',
                    'image_url': 'https://images.unsplash.com/photo-1594938291221-94f18cbb5660?w=800'
                },
                {
                    'name': 'Cuci Selimut',
                    'description': 'Pencucian selimut dan bed cover dengan mesin berkapasitas besar. Hasil bersih, wangi, dan lembut.',
                    'price': 30000.00,
                    'unit': 'per item',
                    'duration': '4-5 hari',
                    'image_url': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800'
                },
                {
                    'name': 'Cuci Gordyn',
                    'description': 'Layanan cuci gordyn dengan penanganan khusus sesuai jenis kain. Termasuk pemasangan kembali jika diperlukan.',
                    'price': 40000.00,
                    'unit': 'per set',
                    'duration': '7-10 hari',
                    'image_url': 'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800'
                },
                {
                    'name': 'Cuci Sprei',
                    'description': 'Pencucian sprei, sarung bantal, dan bed sheet dengan perhatian khusus pada kebersihan dan kelembutan kain.',
                    'price': 25000.00,
                    'unit': 'per set',
                    'duration': '3-4 hari',
                    'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800'
                },
                {
                    'name': 'Cuci Helm',
                    'description': 'Pembersihan helm secara menyeluruh, termasuk bagian dalam dan luar. Menghilangkan bau dan noda membandel.',
                    'price': 15000.00,
                    'unit': 'per item',
                    'duration': '2-3 hari',
                    'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'
                },
                {
                    'name': 'Cuci Tas',
                    'description': 'Perawatan tas kulit, kain, atau sintetis dengan metode yang sesuai. Membersihkan tanpa merusak material.',
                    'price': 30000.00,
                    'unit': 'per item',
                    'duration': '4-6 hari',
                    'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800'
                },
                {
                    'name': 'Cuci Jaket',
                    'description': 'Pencucian jaket dengan berbagai jenis bahan. Menggunakan deterjen khusus untuk menjaga kualitas jaket.',
                    'price': 35000.00,
                    'unit': 'per potong',
                    'duration': '3-5 hari',
                    'image_url': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=800'
                },
                {
                    'name': 'Cuci Jeans',
                    'description': 'Layanan khusus untuk pakaian jeans dengan treatment anti-pudar warna. Menjaga warna jeans tetap cerah.',
                    'price': 20000.00,
                    'unit': 'per potong',
                    'duration': '2-3 hari',
                    'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800'
                },
                {
                    'name': 'Cuci Kaos',
                    'description': 'Pencucian kaos dengan perhatian pada warna dan bentuk. Menggunakan deterjen yang aman untuk kain katun.',
                    'price': 10000.00,
                    'unit': 'per kg',
                    'duration': '1-2 hari',
                    'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800'
                },
                {
                    'name': 'Cuci Handuk',
                    'description': 'Pencucian handuk dengan desinfeksi menyeluruh. Menghilangkan bakteri dan jamur yang menempel.',
                    'price': 15000.00,
                    'unit': 'per kg',
                    'duration': '2-3 hari',
                    'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800'
                },
                {
                    'name': 'Cuci Sarung',
                    'description': 'Perawatan sarung dengan metode tradisional dan modern. Menjaga kesucian dan kebersihan sarung.',
                    'price': 18000.00,
                    'unit': 'per potong',
                    'duration': '3-4 hari',
                    'image_url': 'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800'
                },
                {
                    'name': 'Cuci Topi',
                    'description': 'Pembersihan topi berbagai jenis dengan perhatian pada bentuk dan warna. Menghilangkan debu dan noda.',
                    'price': 12000.00,
                    'unit': 'per item',
                    'duration': '1-2 hari',
                    'image_url': 'https://images.unsplash.com/photo-1575428652377-a2d80e2277fc?w=800'
                },
                {
                    'name': 'Cuci Masker',
                    'description': 'Sterilisasi dan pencucian masker kain. Menggunakan bahan desinfektan aman untuk kesehatan.',
                    'price': 8000.00,
                    'unit': 'per item',
                    'duration': '1 hari',
                    'image_url': 'https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=800'
                },
                {
                    'name': 'Cuci Korden',
                    'description': 'Pencucian korden dengan treatment anti-kusut. Menjaga tekstur dan warna korden tetap baik.',
                    'price': 45000.00,
                    'unit': 'per meter',
                    'duration': '5-7 hari',
                    'image_url': 'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800'
                },
                {
                    'name': 'Cuci Bantal',
                    'description': 'Pencucian bantal dengan pengeringan khusus. Menghilangkan tungau dan debu yang menempel.',
                    'price': 22000.00,
                    'unit': 'per item',
                    'duration': '3-4 hari',
                    'image_url': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800'
                },
                {
                    'name': 'Cuci Guling',
                    'description': 'Perawatan guling dengan pencucian mendalam. Mengembalikan kenyamanan dan kebersihan guling.',
                    'price': 25000.00,
                    'unit': 'per item',
                    'duration': '4-5 hari',
                    'image_url': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800'
                },
                {
                    'name': 'Cuci Matras',
                    'description': 'Pembersihan matras secara profesional. Menghilangkan noda, debu, dan alergen yang menempel.',
                    'price': 100000.00,
                    'unit': 'per item',
                    'duration': '7-10 hari',
                    'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800'
                }
            ]
            
            for service_data in services_data:
                service = LaundryService(**service_data)
                database.session.add(service)
            
            database.session.commit()
    
    return app
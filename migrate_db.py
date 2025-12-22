
import os
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from app import create_app
from app.extensions import database

def migrate_to_postgresql():
    """
    Migrasi data dari SQLite ke PostgreSQL
    """

    # Setup Flask app context
    app = create_app()

    # Database URLs
    sqlite_db = 'miya_laundry_database.db'
    postgres_url: str | None = os.environ.get('DATABASE_URL')

    if not postgres_url:
        print("Error: DATABASE_URL environment variable tidak ditemukan!")
        print("   Silakan set DATABASE_URL terlebih dahulu:")
        print("   export DATABASE_URL='postgresql://username:password@host:port/database_name'")
        return

    print("Memulai migrasi database...")
    print(f"Dari: {sqlite_db}")
    print(f"Ke: {postgres_url}")

    try:
        # Koneksi ke SQLite
        sqlite_conn = sqlite3.connect(sqlite_db)
        sqlite_cursor = sqlite_conn.cursor()

        # Koneksi ke PostgreSQL
        pg_conn = psycopg2.connect(postgres_url)
        pg_cursor = pg_conn.cursor()

        with app.app_context():
            # Buat semua tabel di PostgreSQL
            print("Membuat tabel di PostgreSQL...")
            database.create_all()

            # Migrasi tabel roles
            print("Migrasi tabel roles...")
            sqlite_cursor.execute("SELECT id, name, description FROM roles")
            roles = sqlite_cursor.fetchall()

            if roles:
                execute_values(pg_cursor,
                    "INSERT INTO roles (id, name, description) VALUES %s ON CONFLICT (id) DO NOTHING",
                    roles)
                print(f"   {len(roles)} roles berhasil dimigrasi")

            # Migrasi tabel users
            print("Migrasi tabel users...")
            sqlite_cursor.execute("""
                SELECT id, username, email, password, full_name, phone, address,
                       created_at, updated_at, role_id
                FROM users
            """)
            users = sqlite_cursor.fetchall()

            if users:
                execute_values(pg_cursor, """
                    INSERT INTO users (id, username, email, password, full_name, phone, address,
                                     created_at, updated_at, role_id)
                    VALUES %s ON CONFLICT (id) DO NOTHING
                """, users)
                print(f"   {len(users)} users berhasil dimigrasi")

            # Migrasi tabel laundry_services
            print("Migrasi tabel laundry_services...")
            sqlite_cursor.execute("""
                SELECT id, name, description, price, unit, duration, image_url,
                       is_active, created_at, updated_at
                FROM laundry_services
            """)
            services = sqlite_cursor.fetchall()

            if services:
                execute_values(pg_cursor, """
                    INSERT INTO laundry_services (id, name, description, price, unit, duration,
                                               image_url, is_active, created_at, updated_at)
                    VALUES %s ON CONFLICT (id) DO NOTHING
                """, services)
                print(f"   {len(services)} services berhasil dimigrasi")

            # Migrasi tabel service_orders
            print("Migrasi tabel service_orders...")
            sqlite_cursor.execute("""
                SELECT id, order_number, quantity, total_price, status, notes,
                       pickup_address, delivery_address, order_date, completed_date,
                       user_id, service_id
                FROM service_orders
            """)
            orders = sqlite_cursor.fetchall()

            if orders:
                execute_values(pg_cursor, """
                    INSERT INTO service_orders (id, order_number, quantity, total_price, status, notes,
                                              pickup_address, delivery_address, order_date, completed_date,
                                              user_id, service_id)
                    VALUES %s ON CONFLICT (id) DO NOTHING
                """, orders)
                print(f"   {len(orders)} orders berhasil dimigrasi")

            # Commit semua perubahan
            pg_conn.commit()

        # Tutup koneksi
        sqlite_conn.close()
        pg_conn.close()

        print("Migrasi database berhasil!")
        print("\nCatatan:")
        print("   - Pastikan untuk backup database SQLite sebelum production")
        print("   - Test aplikasi dengan database PostgreSQL")
        print("   - Update environment variables di platform deployment")

    except Exception as e:
        print(f"Error selama migrasi: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    success = migrate_to_postgresql()
    if success:
        print("\nMigrasi selesai! Database siap untuk deployment.")
    else:
        print("\nMigrasi gagal. Periksa error di atas.")
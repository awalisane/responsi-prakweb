
#Script deployment untuk Railway
#Gunakan script ini untuk mempersiapkan aplikasi sebelum deploy ke Railway#


import os
import subprocess
import sys

def prepare_deployment():
    """Persiapkan aplikasi untuk deployment"""

    print("Mempersiapkan deployment ke Railway...")

    # Check if .env exists
    if not os.path.exists('.env'):
        print("File .env tidak ditemukan!")
        print("Silakan copy dari .env.example:")
        print("cp .env.example .env")
        return False

    # Check DATABASE_URL in environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("DATABASE_URL tidak ditemukan di environment variables")
        print("Pastikan set DATABASE_URL di Railway dashboard")
        print("Format: postgresql://username:password@host:port/database_name")

    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Dependencies installed")
    except subprocess.CalledProcessError:
        print("ailed to install dependencies")
        return False

    # Test database connection
    print("Testing database connection...")
    try:
        subprocess.check_call([sys.executable, 'test_db.py'])
        print("Database connection OK")
    except subprocess.CalledProcessError:
        print("Database connection failed")
        print("Pastikan DATABASE_URL sudah benar")
        return False

    # Run database migration if needed
    if database_url and 'postgresql' in database_url:
        print("Running database migration...")
        try:
            subprocess.check_call([sys.executable, 'migrate_db.py'])
            print("Database migration completed")
        except subprocess.CalledProcessError:
            print("Database migration failed (mungkin sudah ada data)")

    print("Deployment preparation completed!")
    print("\n Next steps:")
    print("   1. Push code ke GitHub")
    print("   2. Connect repository ke Railway")
    print("   3. Set environment variables di Railway dashboard:")
    print("      - DATABASE_URL")
    print("      - SECRET_KEY")
    print("      - FLASK_ENV=production")
    print("   4. Deploy!")

    return True

if __name__ == "__main__":
    success = prepare_deployment()
    if not success:
        sys.exit(1)
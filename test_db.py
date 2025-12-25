
"""
testing koneksi database
Gunakan script ini untuk memverifikasi koneksi database sebelum deployment
"""

import os
from app import create_app
from app.extensions import database
from app.models.models.user import User
from app.models.models.role import Role
from app.models.models.service import LaundryService
from app.models.models.order import ServiceOrder

def test_database_connection():
    """Test koneksi dan basic queries ke database"""

    print("Testing database connection...")

    try:
        app = create_app()

        with app.app_context():
            print("Flask app context created successfully")

            # Test database connection
            with database.engine.connect() as conn:
                conn.execute(database.text("SELECT 1"))
            print("Database connection successful")

            # Test table counts
            users_count = User.query.count()
            roles_count = Role.query.count()
            services_count = LaundryService.query.count()
            orders_count = ServiceOrder.query.count()

            print("Database statistics:")
            print(f"Users: {users_count}")
            print(f"Roles: {roles_count}")
            print(f"Services: {services_count}")
            print(f"Orders: {orders_count}")

            # Test relationships
            if users_count > 0:
                sample_user = User.query.first()
                print(f"Sample user: {sample_user.username} ({sample_user.role.name})")

            if services_count > 0:
                sample_service = LaundryService.query.first()
                print(f"Sample service: {sample_service.name} - Rp {sample_service.price}")

            if orders_count > 0:
                sample_order = ServiceOrder.query.first()
                print(f"Sample order: {sample_order.order_number} - {sample_order.status}")

            print("All database tests passed!")
            return True

    except Exception as e:
        print(f"Database test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n Database siap untuk deployment!")
    else:
        print("\n Perbaiki masalah database sebelum deployment.")
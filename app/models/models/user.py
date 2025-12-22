from app.extensions import database
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, database.Model):
    """
    Model untuk menyimpan data pengguna sistem.
    Mengimplementasikan UserMixin dari Flask-Login untuk session management.
    """
    __tablename__ = 'users'
    
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False, index=True)
    email = database.Column(database.String(120), unique=True, nullable=False, index=True)
    password = database.Column(database.String(255), nullable=False)
    full_name = database.Column(database.String(100), nullable=False)
    phone = database.Column(database.String(20))
    address = database.Column(database.Text)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    updated_at = database.Column(database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key ke tabel roles
    role_id = database.Column(database.Integer, database.ForeignKey('roles.id'), nullable=False)
    
    # Relasi one-to-many dengan ServiceOrder
    orders = database.relationship('ServiceOrder', backref='customer', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_karyawan(self):
        """Helper method untuk mengecek apakah user adalah karyawan"""
        return self.role.name == 'Karyawan'
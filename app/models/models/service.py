from app.extensions import database
from datetime import datetime

class LaundryService(database.Model):
    """
    Model untuk menyimpan data layanan laundry yang ditawarkan.
    Berisi informasi detail tentang setiap jenis layanan.
    """
    __tablename__ = 'laundry_services'
    
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=False)
    price = database.Column(database.Numeric(10, 2), nullable=False)
    unit = database.Column(database.String(20), nullable=False)  # per kg, per item, per meter, dll
    duration = database.Column(database.String(50))  # estimasi waktu pengerjaan
    image_url = database.Column(database.String(500))
    is_active = database.Column(database.Boolean, default=True)
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    updated_at = database.Column(database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relasi one-to-many dengan ServiceOrder
    orders = database.relationship('ServiceOrder', backref='service', lazy='dynamic')
    
    def __repr__(self):
        return f'<LaundryService {self.name}>'
    
    def get_formatted_price(self):
        """Helper method untuk format harga dalam rupiah"""
        return f"Rp {self.price:,.0f}".replace(',', '.')
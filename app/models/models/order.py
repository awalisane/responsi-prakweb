from app.extensions import database
from datetime import datetime

class ServiceOrder(database.Model):
    """
    Model untuk menyimpan data pesanan layanan laundry.
    Mencatat transaksi antara customer dan service.
    """
    __tablename__ = 'service_orders'
    
    id = database.Column(database.Integer, primary_key=True)
    order_number = database.Column(database.String(50), unique=True, nullable=False)
    quantity = database.Column(database.Numeric(10, 2), nullable=False)
    total_price = database.Column(database.Numeric(12, 2), nullable=False)
    status = database.Column(database.String(20), default='Pending')  # Pending, Processing, Completed, Cancelled
    notes = database.Column(database.Text)
    pickup_address = database.Column(database.Text)
    delivery_address = database.Column(database.Text)
    order_date = database.Column(database.DateTime, default=datetime.utcnow)
    completed_date = database.Column(database.DateTime)
    
    # Foreign keys
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
    service_id = database.Column(database.Integer, database.ForeignKey('laundry_services.id'), nullable=False)
    
    def __repr__(self):
        return f'<ServiceOrder {self.order_number}>'
    
    def get_formatted_total(self):
        """Helper method untuk format total harga dalam rupiah"""
        return f"Rp {self.total_price:,.0f}".replace(',', '.')
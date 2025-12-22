from app.extensions import database
from datetime import datetime

class Role(database.Model):
    """
    Model untuk menyimpan role/peran pengguna dalam sistem.
    Mengimplementasikan Role-Based Access Control (RBAC).
    """
    __tablename__ = 'roles'
    
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True, nullable=False)
    description = database.Column(database.String(200))
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    
    # Relasi one-to-many dengan User
    users = database.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return f'<Role {self.name}>'
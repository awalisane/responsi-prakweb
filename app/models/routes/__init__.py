from .auth import auth_blueprint
from .main import main_blueprint
from .admin import admin_blueprint

__all__ = ['auth_blueprint', 'main_blueprint', 'admin_blueprint']
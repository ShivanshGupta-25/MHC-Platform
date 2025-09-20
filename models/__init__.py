from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = []
from .admin import Admin
__all__.append('Admin')
from .user import User
__all__.append('User')

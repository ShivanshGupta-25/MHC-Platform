from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# To define your db schema remove pass and structurize like this:
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
    # other fields...

class User(db.Model):
    __tablename__ = 'user'
    
    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.set_password(password)
        
    def set_password(self, plain_password):
        self.password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)
    
    def __repr__(self):
        return f'<User {self.email}>'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
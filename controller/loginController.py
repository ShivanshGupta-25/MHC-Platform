from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User

class LoginController:
    def __init__(self):
        self.view_base = 'login'

    def index(self):
        return render_template(f'{self.view_base}.html')
    
    
    def create(self):
        pass
    
    def store(self=None):
        email = request.form['email']
        password = request.form['password']
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['user_email'] = user.email
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password', 'error')
                return redirect(url_for('login'))
        else:
            flash('Please enter your email and password', 'error')
        return redirect(url_for('login'))
    def show(self, id):
        pass
    
    def edit(self, id):
        pass
    
    def update(self, id):
        pass
    
    def destroy(self, id):
        pass
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User
from models import db
class SignupController:
    def __init__(self):
        self.view_base = 'signup'

    def index(self):
        return render_template(f'{self.view_base}.html')
    
    
    def create(self):
        full_name = request.form['full_name']
        email = request.form['email']
        if request.form['password'] != request.form['confirm_password']:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        password = request.form['password']
        new_user = User(full_name=full_name, email=email, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
        
    def store(self=None):
        pass
    
    def show(self, id):
        pass
    
    def edit(self, id):
        pass
    
    def update(self, id):
        pass
    
    def destroy(self, id):
        pass
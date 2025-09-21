from flask import Blueprint, render_template

class DashboardController:
    def __init__(self):
        self.view_base = 'dashboard'

    def index(self):
        return render_template(f'{self.view_base}.html')
    
    
    def create(self):
        pass
    
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
  
import os
from flask_admin import Admin
from .models import (db, User, Models, Configurations, Fleet, Prices, Projects, Assignations, Budgets, Roles, Countries,
                    Nationalities, States, Employees)
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'united'
    admin = Admin(app, name='Jetstream DataBase', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Models, db.session))
    admin.add_view(ModelView(Configurations, db.session))
    admin.add_view(ModelView(Fleet, db.session))
    admin.add_view(ModelView(Prices, db.session))
    admin.add_view(ModelView(Projects, db.session))
    admin.add_view(ModelView(Assignations, db.session))
    admin.add_view(ModelView(Budgets, db.session))
    admin.add_view(ModelView(Roles, db.session))
    admin.add_view(ModelView(Countries, db.session))
    admin.add_view(ModelView(Nationalities, db.session))
    admin.add_view(ModelView(States, db.session))
    admin.add_view(ModelView(Employees, db.session))
    admin.add_view(ModelView(User, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
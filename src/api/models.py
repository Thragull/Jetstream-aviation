from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

#Database Design:
#Database structure for Fleet:

class Models(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f'Aircraft model {self.model_name}'

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model_name
        }

class Configurations(db.Model):
    __tablename__ = 'configurations'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
    model = db.relationship(Models)
    business = db.Column(db.Integer, nullable=False, default=0)
    economy = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Configuration for {self.model}: Y{self.economy}, C{self.business}'

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model_id,
            "business": self.business,
            "economy": self.economy
        }

class Fleet(db.Model):
    __tablename__ = 'fleet'
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(10), nullable=False, unique=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
    model = db.relationship(Models)
    configuration_id = db.Column(db.Integer, db.ForeignKey('configurations.id'), nullable=False)
    configuration = db.relationship(Configurations)
    asigned = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Aircraft: {self.registration}'

    def serialize(self):
        return {
            "id": self.id,
            "registration": self.registration,
            "model": self.model_id,
            "configuration": self.configuration_id,
            "assigned": self.assigned
        }

class Prices(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
    model = db.relationship(Models)
    configuration_id = db.Column(db.Integer, db.ForeignKey('configurations.id'), nullable=False)
    configuration = db.relationship(Configurations)
    crew = db.Column(db.Boolean, nullable=False,  default=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Price for aircraft: {self.model}'

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model_id,
            "configuration": self.configuration_id,
            "crew": self.crew,
            "price": self.price
        }
    
#Database structure for Projects:
    
class Projects(db.Model):
    __tablename__ = 'projects'
    id =  db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(50), unique=True, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "Project {}".format(self.project)
    
    def serialize(self):
        return {
            "id": self.id,
            "project": self.project,
            "start": self.start_date,
            "end": self.end_date
        }

class Assignations(db.Model):
    __tablename__ = 'assignations'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship(Projects)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=False)
    aircraft = db.relationship(Fleet)

    def __repr__(self):
        return 'Aircraft {} is assigned to project {}'.format(self.aircraft.registration, self.project.project)

    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "aircraft_id": self.aircraft_id
        }


class Budgets(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(50), nullable=False)
    client_surname = db.Column(db.String(50), nullable=False)
    client_business = db.Column(db.String(50), nullable=False)
    client_email = db.Column(db.String(150), nullable=False)
    client_phone = db.Column(db.BigInteger, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "We can negotiate with {}".format(self.client_business)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.client_name,
            "surname": self.client_surname,
            "business": self.client_business,
            "email": self.client_email,
            "phone": self.client_phone,
            "start": self.start_date,
            "end": self.end_date,
            "price": self.total_price
        }
    
#Database structure for Employees registration
    
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.role}"

    def serialize(self):
        return {
            "id": self.id,
            "role": self.role
        }

class Countries(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.country}"
    
    def serialize(self):
        return {
            "id": self.id,
            "country": self.country
        }

class Nationalities(db.Model):
    __tablename__ = 'nationalities'
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.nationality}"
    
    def serialize(self):
        return {
            "id": self.id,
            "nationality": self.nationality
        }

class States(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    country = db.relationship(Countries)
    state = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "{} from {}".format(self.state, self.country.country)
    
    def serialize(self):
        return{
            "id": self.id,
            "country": self.country_id,
            "state": self.state
        }

class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    crew_id = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship(Roles)
    department = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    nationality_id = db.Column(db.Integer, db.ForeignKey('nationalities.id'))
    nationality = db.relationship(Nationalities)
    address = db.Column(db.String(250))
    address2 = db.Column(db.String(250))
    address3 = db.Column(db.String(250))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship(Countries)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    state = db.relationship(States)
    city = db.Column(db.String(50))
    zipcode = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return "{} {} with code ({})".format(self.name, self.surname, self.crew_id)
    
    def serialize(self):
        return {
            "id": self.id,
            "crew_id": self.crew_id,
            
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
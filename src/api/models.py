from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Database Design:
#Fleet section:

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
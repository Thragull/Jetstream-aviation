"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import (db, Models, Configurations, Fleet, Prices, Projects, Assignations, Budgets, Roles, Countries,
                    Nationalities, States, Employees, Airports, Inflight, Duties, Flights, Hotels, Rosters, Salary_Prices,
                    Bank_Details, Payslips, Documents, Visibility, Departments)
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt



# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, support_credentials=True)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response

@app.route('/api/models', methods=['GET'])
@cross_origin(supports_credentials=True)
def getModels():
    models = Models.query.all()
    serialized_models = [model_name.serialize() for model_name in models]
    return jsonify(serialized_models), 200

@app.route('/api/configurations', methods=['GET'])
def getConfigurations():
    model = request.args.get("model")
    print(model)
    print(type(model))
    if model is None: 
        return jsonify({'msg': 'You must specify a model id'}), 400
    configurations = Configurations.query.filter_by(model_id=model).all()
    serialized_configurations = [configuration.serialize() for configuration in configurations]
    return jsonify(serialized_configurations), 200    


@app.route('/api/countries', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCountries():
    countries = Countries.query.all()
    serialized_countries = [country.serialize() for country in countries]
    return jsonify(serialized_countries), 200


@app.route('/api/nationalities', methods=['GET'])
@cross_origin(supports_credentials=True)
def getNationalities():
    nationalities = Nationalities.query.all()
    serialized_countries = [nationality.serialize() for nationality in nationalities]
    return jsonify(serialized_countries), 200


@app.route('/api/states', methods=['GET'])
def getStates():

    country_id = request.args.get('country_id')
    states = States.query.filter_by(country_id=country_id).all()
    serialized_states = [state.serialize() for state in states]
    return jsonify(serialized_states), 200



@app.route('/api/prices', methods=['GET'])
def getPrices():
    model_id = request.args.get('model_id')
    if model_id is None:
        return jsonify({'msg': 'You must specify a model ID'}), 400
    configuration_id = request.args.get('configuration_id')
    if configuration_id is None:
        return jsonify({'msg': 'You must specify a configuration ID'}), 400
    crew = request.args.get('crew')
    if crew is None:
        return jsonify({'msg': 'You must specify if there is or there is not crew'}), 400
    prices = Prices.query.filter_by(model_id=model_id, configuration_id=configuration_id, crew=crew).all()
    if prices == []:
        return jsonify({'msg': 'There is no price for the selected options.'}), 404
    serialized_prices =list(map(lambda price: price.serialize(), prices))
    return jsonify(serialized_prices), 200

@app.route('/api/roles', methods=['GET'])
@cross_origin(supports_credentials=True)
def getRoles():
    roles = Roles.query.all()
    serialized_roles = [role.serialize() for role in roles]
    return jsonify(serialized_roles), 200

@app.route('/api/departments', methods=['GET'])
@cross_origin(supports_credentials=True)
def getDepartments():
    departments = Departments.query.all()
    serialized_departments = [department.serialize() for department in departments]
    return jsonify(serialized_departments), 200

@app.route('/api/employees', methods=['GET'])
@cross_origin(supports_credentials=True)
def getEmployees():
    employees = Employees.query.with_entities(Employees.id, Employees.crew_id).all()
    serialized_employees = [{'id': employee.id, 'crew_id': employee.crew_id} for employee in employees]
    return jsonify(serialized_employees), 200
  
@app.route('/api/airports', methods=['GET'])
def get_airports():
    airports = Airports.query.all()
    serialized_airports = list(map(lambda airport: airport.serialize(), airports))
    return jsonify(serialized_airports)

@app.route('/api/hotels', methods=['GET'])
def get_hotels():
    base_id = request.args.get('base_id')
    if base_id is None:
        return jsonify({'msg': 'You must specify a base ID'}), 400
    hotels = Hotels.query.filter_by(base_id=base_id).all()
    if hotels == []:
        return jsonify({'msg': 'There are no Hotels for the specific Aiport Base'}), 404
    serialized_hotels = list(map(lambda hotel: hotel.serialize(), hotels))
    return jsonify(serialized_hotels), 200

@app.route('/api/signupEmployee', methods=['POST'])
@cross_origin(supports_credentials=True)
def signupUser():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': "You can not send empty info"}), 400
    if 'email' not in body: 
        return jsonify({'msg': "The email field is mandatory"}), 400
    if 'password' not in body: 
        return jsonify({'msg': "You must specify a password"}), 400
    if 'surname' not in body:
        return jsonify({'msg': "The surname field is mandatory"}), 400
    if 'name' not in body:
        return jsonify({'msg': "The name field is mandatory"}), 400
    if 'crew_id' not in body: 
        return jsonify({'msg': "The id field is mandatory"}), 400
    if 'role_id' not in body: 
        return jsonify({'msg': "The role field is mandatory"}), 400
    if 'department_id' not in body: 
        return jsonify({'msg': "The department field is mandatory"}), 400

    new_employee = Employees()
    new_employee.email = body['email']
    new_employee.password = body['password']
    new_employee.surname = body['surname']
    new_employee.name = body['name']
    new_employee.crew_id = body['crew_id']
    new_employee.gender = body['gender']
    new_employee.department_id = body['department_id']
    new_employee.role_id = body['role_id']
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'msg': "Employee successfully added to database"}), 200
 
@app.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    body = request.get_json(silent=True)
    if body is None: 
        return jsonify({'msg': "You must send info of login and password"}), 400
    if 'crew_id' not in body: 
        return jsonify({'msg': "You must specify your Id"}), 400
    if 'password' not in body: 
        return jsonify({'msg': 'You must write your password'}), 400

    # Necesitamos hacer un query para ver si el usuario existe, y luego comprobar que la contraseña coincida
    user = Employees.query.filter_by(crew_id=body["crew_id"]).first()
    if user is None:
        return jsonify({'msg': "The user does not exist"}), 400
    if user.password != body['password']: 
        return jsonify({'msg': 'wrong password'}), 400
    
    access_token = create_access_token(identity=user.crew_id)
    return jsonify({'msg': 'Login successful', 'token': access_token}), 200



@app.route("/protected", methods=["GET"])
@jwt_required() #Esto sirve para proteger el enlace
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity() #Este método me devuelve la identidad con el que fue creado
    return jsonify(logged_in_as=current_user), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)

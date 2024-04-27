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
    id = request.args.get('id')
    if id is None:
        models = Models.query.all()
        serialized_models = [model_name.serialize() for model_name in models]
        return jsonify(serialized_models), 200
    models = Models.query.filter_by(id=id).all()
    serialized_models = [model_name.serialize() for model_name in models]
    return jsonify(serialized_models), 200

@app.route('/api/configurations', methods=['GET'])
def getConfigurations():
    model = request.args.get("model")
    id = request.args.get('id')
    if model is None: 
        return jsonify({'msg': 'You must specify a model id'}), 400
    if id is None:
        configurations = Configurations.query.filter_by(model_id=model).all()
        serialized_configurations = [configuration.serialize() for configuration in configurations]
        return jsonify(serialized_configurations), 200
    configurations = Configurations.query.filter_by(model_id=model, id=id).all()
    serialized_configurations = [configuration.serialize() for configuration in configurations]
    return jsonify(serialized_configurations), 200

@app.route('/api/fleet', methods=['GET'])
def getFleet():
    model_id = request.args.get("model_id")
    configuration_id = request.args.get("configuration_id")
    if model_id is None and configuration_id is None:
        fleet = Fleet.query.all()
        if fleet == []:
            return jsonify({'msg': 'There are no aircrafts in Database'}), 404
        serialized_fleet = list(map(lambda plane: plane.serialize(), fleet))
        return jsonify(serialized_fleet), 200
    if model_id is None:
        fleet = Fleet.query.filter_by(configuration_id=configuration_id).all()
        if fleet == []:
            return jsonify({'msg': 'There are no aircrafts in Database with this configuration'}), 404
        serialized_fleet = list(map(lambda plane: plane.serialize(), fleet))
        return jsonify(serialized_fleet), 200
    if configuration_id is None:
        fleet = Fleet.query.filter_by(model_id=model_id).all()
        if fleet == []:
            return jsonify({'msg': 'There are no aircrafts in Database with this model'}), 404
        serialized_fleet = list(map(lambda plane: plane.serialize(), fleet))
        return jsonify(serialized_fleet), 200
    fleet = Fleet.query.filter_by(model_id=model_id, configuration_id=configuration_id).all()
    if fleet == []:
        return jsonify({'msg': 'There are no aircrafts in Database with this model and configuration'}), 404
    serialized_fleet = list(map(lambda plane: plane.serialize(), fleet))
    return jsonify(serialized_fleet), 200


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

@app.route('/api/projects', methods=['GET'])
@jwt_required()
def getProjects():
    projects = Projects.query.all()
    serialized_projects = list(map(lambda project: project.serialize(), projects))
    return jsonify(serialized_projects), 200

@app.route('/api/projects', methods=['POST'])
@jwt_required()
def createProject():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('project' not in body or
        'start' not in body or
        'end' not in body):
        return jsonify({'msg': 'One or more of the following is missing: Project name, Start date, End date'}), 400
    
    project = Projects()
    project.project = body['project']
    project.start_date = body['start']
    project.end_date = body['end']

    db.session.add(project)
    db.session.commit()

    return jsonify({'msg': 'New project created'}), 200

@app.route('/api/projects', methods=['PUT'])
@jwt_required()
def modifyProject():
    project_id = request.args.get('id')
    if project_id is None:
        return jsonify({'msg': 'You must specify a project ID'}),400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('project' not in body and
        'start' not in body and
        'end' not in body):
        return jsonify({'msg': 'You must specify at least one of the following fields: Project name, Start date, End date'}), 400
    project = Projects.query.get(project_id)
    if 'project' in body:
        project.project = body['project']
    if 'start' in body:
        project.start_date = body['start']
    if 'end' in body:
        project.end_date = body['end']

    db.session.commit()

    return jsonify({'msg': 'Project with name {} has been succesfully modified'.format(project.project)}), 200

@app.route('/api/projects', methods=['DELETE'])
@jwt_required()
def deleteProject():
    project_id = request.args.get('id')
    if project_id is None:
        return jsonify({'msg': 'You must specify a project ID'}), 400
    assignations = Assignations.query.filter_by(project_id=project_id).all()
    if len(assignations)>0:
        return jsonify({'msg': 'Project can\'t be deleted if it has aircrafts assigned'}), 400
    project = Projects.query.filter_by(id=project_id).first()
    if project is None:
        return jsonify({'msg': 'Project not found'}), 404
    
    db.session.delete(project)
    db.session.commit()
    return jsonify({'msg': 'Project {} has been succesfully deleted'.format(project.project)}), 200

@app.route('/api/assignations', methods=['GET'])
@jwt_required()
def getAssignations():
    assignations = Assignations.query.all()
    serialized_assignations = list(map(lambda assignation: assignation.serialize(), assignations))
    return jsonify(serialized_assignations), 200

@app.route('/api/assignations', methods=['POST'])
@jwt_required()
def createAssignations():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('project_id' not in body or
        'aircraft_id' not in body):
        return jsonify({'msg': 'One or more of the following is missing: Project ID, Aircraft ID'}), 400
    
    assignation = Assignations()
    assignation.project_id = body['project_id']
    assignation.aircraft_id = body['aircraft_id']

    aircraft = Fleet.query.filter_by(id=assignation.aircraft_id).first()
    if aircraft.assigned:
        return jsonify({'msg', 'The aircraft {} is already assigned to another project'.format(aircraft.registration)}), 400
    aircraft.assigned = True

    db.session.add(assignation)
    db.session.commit()

    return jsonify({'msg': 'New assignation created'}), 200

@app.route('/api/assignations', methods=['PUT'])
@jwt_required()
def modifyAssignations():
    assignation_id = request.args.get('id')
    if assignation_id is None:
        return jsonify({'msg': 'You must specify an assignation ID'}),400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('project_id' not in body and
        'aircraft_id' not in body):
        return jsonify({'msg': 'You must specify at least one of the following fields: Project ID, Aircraft ID'}), 400
    assignation = Assignations.query.get(assignation_id)
    if 'project_id' in body:
        assignation.project_id = body['project_id']
    if 'aircraft_id' in body:
        old_aircraft = Fleet.query.filter_by(id=assignation.aircraft_id).first()
        new_aircraft = Fleet.query.filter_by(id=body['aircraft_id']).first()
        if new_aircraft.assigned:
            return jsonify({'msg': 'The aircraft {} is already assigned to another project'.format(new_aircraft.registration)}), 400
        assignation.aircraft_id = body['aircraft_id']
        old_aircraft.assigned=False
        new_aircraft.assigned=True
        

    db.session.commit()

    return jsonify({'msg': 'Assignation succesfully modified'}), 200

@app.route('/api/assignations', methods=['DELETE'])
@jwt_required()
def deleteAssignation():
    assignation_id = request.args.get('id')
    if assignation_id is None:
        return jsonify({'msg': 'You must specify an assignation ID'}), 400
    assignation = Assignations.query.filter_by(id=assignation_id).first()
    if assignation is None:
        return jsonify({'msg': 'Assignation not found'}), 404
    aircraft= Fleet.query.filter_by(id=assignation.aircraft_id).first()
    aircraft.assigned=False

    db.session.delete(assignation)
    db.session.commit()
    return jsonify({'msg': 'Assignation with ID {} has been succesfully deleted'.format(assignation.id)}), 200

@app.route('/api/roles', methods=['GET'])
@jwt_required()
@cross_origin(supports_credentials=True)
def getRoles():
    id = request.args.get('id')
    if id is None:
        roles = Roles.query.all()
        serialized_roles = [role.serialize() for role in roles]
        return jsonify(serialized_roles), 200
    roles = Roles.query.filter_by(id=id).all()
    serialized_roles = [role.serialize() for role in roles]
    return jsonify(serialized_roles), 200

@app.route('/api/countries', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCountries():
    id = request.args.get('id')
    if id is None:
        countries = Countries.query.all()
        serialized_countries = [country.serialize() for country in countries]
        return jsonify(serialized_countries), 200
    countries = Countries.query.filter_by(id=id).all()
    serialized_countries = [country.serialize() for country in countries]
    return jsonify(serialized_countries), 200


@app.route('/api/nationalities', methods=['GET'])
@cross_origin(supports_credentials=True)
def getNationalities():
    id = request.args.get('id')
    if id is None:
        nationalities = Nationalities.query.all()
        serialized_countries = [nationality.serialize() for nationality in nationalities]
        return jsonify(serialized_countries), 200
    nationalities = Nationalities.query.filter_by(id=id).all()
    serialized_countries = [nationality.serialize() for nationality in nationalities]
    return jsonify(serialized_countries), 200


@app.route('/api/states', methods=['GET'])
def getStates():
    id = request.args.get('id')
    country_id = request.args.get('country_id')
    if id is None and country_id is None:
        states = States.query.all()
        serialized_states = [state.serialize() for state in states]
        return jsonify(serialized_states), 200
    if id is None:
        states = States.query.filter_by(country_id=country_id).all()
        serialized_states = [state.serialize() for state in states]
        return jsonify(serialized_states), 200
    states = States.query.filter_by(id=id).all()
    serialized_states = [state.serialize() for state in states]
    return jsonify(serialized_states), 200

@app.route('/api/departments', methods=['GET'])
@jwt_required()
@cross_origin(supports_credentials=True)
def getDepartments():
    id = request.args.get('id')
    if id is None:
        departments = Departments.query.all()
        serialized_departments = [department.serialize() for department in departments]
        return jsonify(serialized_departments), 200
    departments = Departments.query.filter_by(id=id).all()
    serialized_departments = [department.serialize() for department in departments]
    return jsonify(serialized_departments), 200

@app.route('/api/crew_id', methods=['GET'])
@jwt_required()
@cross_origin(supports_credentials=True)
def getCrewId():
    employees = Employees.query.with_entities(Employees.id, Employees.crew_id).all()
    serialized_employees = [{'id': employee.id, 'crew_id': employee.crew_id} for employee in employees]
    return jsonify(serialized_employees), 200
  
@app.route('/api/employee', methods=['GET'])
@jwt_required()
def getEmployeeByCrewID():
    crew_id = get_jwt_identity()
    if crew_id is None:
        return jsonify({'msn': 'You must specify a employee ID'}), 400
    employee = Employees.query.filter_by(crew_id=crew_id).first()
    if employee is None:
        return jsonify({'msg': 'The employee does not exists'}), 404
    if not employee.is_active:
        return jsonify({'msg': 'The employee does not exists'}), 404
    
    return jsonify(employee.serialize()), 200

@app.route('/api/signupEmployee', methods=['POST'])
@jwt_required()
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

    employee = Employees.query.filter_by(crew_id=body['crew_id']).first()
    if employee is None:
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
        return jsonify({'msg': "Employee successfully added to database"}), 201
    if employee.is_active:
        return jsonify({'msg': 'Employee {} already exist'.format(employee.crew_id)}), 400
    if not employee.is_active:
        employee.is_active = True
        
        db.session.commit()
        return jsonify({'msg': 'Employee succesfully added to database'}), 201

@app.route('/api/employee', methods=['PUT'])
@jwt_required()
def modifyEmployee():
    employee_id = request.args.get('id')
    if employee_id is None:
        return jsonify({'msg': 'You must specify an Employee ID'}), 400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': "You can not send empty info"}), 400
    if ("crew_id" not in body and
        "name" not in body and
        "surname" not in body and
        "email" not in body and
        "phone" not in body and
        "role" not in body and
        "department_id" not in body and
        "gender" not in body and
        "nationality_id" not in body and
        "address" not in body and
        "address2" not in body and
        "address3" not in body and
        "country_id" not in body and
        "state_id" not in body and
        "city" not in body and
        "zipcode" not in body and
        "birthday" not in body and
        "entry_date" not in body):
        return jsonify({'msg': 'None of the fields introduced can be modified'}), 400

    employee = Employees.query.filter_by(id=employee_id).first()
    if employee is None:
        return jsonify({'msg': 'Employee does not exist'}), 404
    if not employee.is_active:
        return jsonify({'msg': 'Employee does not exist'}), 404
    for key, value in body.items():
        if hasattr(employee, key):
            setattr(employee, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400

    db.session.commit()
    return jsonify({'msg': "Employee {} successfully modified".format(employee.crew_id)}), 200

@app.route('/api/employee', methods=['DELETE'])
@jwt_required()
def deleteEmployee():
    employee_id = request.args.get('id')
    if employee_id is None:
        return jsonify({'msg': 'You must specify an Employee ID'}), 400
    employee = Employees.query.filter_by(id=employee_id).first()
    if employee is None:
        return jsonify({'msg': 'Employee does not exist'}), 404
    if not employee.is_active:
        return jsonify({'msg': 'Employee does not exist'}), 404
    employee.is_active = False

    db.session.commit()
    return jsonify({'msg': 'Employee {} has been deleted'.format(employee.crew_id)}), 200

@app.route('/api/inflight', methods=['GET'])
@jwt_required()
def getInflight():
    employee_id = request.args.get('employee_id')
    if employee_id is None:
        return jsonify({'msg': 'You must specify the Employee ID'}), 400
    employee = Employees.query.filter_by(id=employee_id).first()
    department = Departments.query.filter_by(department='Inflight').first()
    if employee is None:
        return jsonify({'msg': 'The employee does not exist'}), 404
    if not employee.is_active:
        return jsonify({'msg': 'The employee does not exist'}), 404
    if employee.department_id != department.id:  # Acceder al atributo id del departamento
        return jsonify({'msg': 'This employee is not from Inflight Department'}), 400
    inflight_data = Inflight.query.filter_by(employee_id=employee_id).first()
    if inflight_data is None:
        return jsonify({'msg': 'There is no inflight data Yet'}), 404
    return jsonify(inflight_data.serialize()), 200

@app.route('/api/inflight', methods=['POST'])
@jwt_required()
def postInflight():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('employee_id' not in body or
        'license' not in body or
        'passport' not in body or
        'pass_expiration' not in body or
        'certificate_id' not in body or
        'cert_expiration' not in body or
        'home_base_id' not in body):
        return jsonify({'msg': 'There are mandatory fields missing in body'}), 400
    inflight_data = Inflight()
    for key, value in body.items():
        if hasattr(inflight_data, key):
            setattr(inflight_data, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    #Añadir Roster en base a los ya creados
    actual_employee = Employees.query.filter_by(id=body['employee_id']).first()
    employees_with_same_role = Employees.query.filter_by(role_id=actual_employee.role_id).all()
    count={
        1: 0,
        2: 0,
        3: 0
    }
    for employee in employees_with_same_role:
        employee_roster = Inflight.query.filter_by(employee_id=employee.id).first()
        if employee_roster:
            count[employee_roster.roster_assigned]+=1
    min_roster = min(count, key=count.get)
    print(min_roster)
    inflight_data.roster_assigned = min_roster
    db.session.add(inflight_data)
    db.session.commit()
    return jsonify({'msg': 'Inflight data created succesfully'}), 201

@app.route('/api/inflight', methods=['PUT'])
@jwt_required()
def editInflight():
    id = request.args.get('id')
    if id is None: 
        return jsonify({'msg': 'You must specify an ID'}), 400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('license' not in body and
        'passport' not in body and
        'pass_expiration' not in body and
        'certificate_id' not in body and
        'cert_expiration' not in body and
        'certificate_id2' not in body and
        'cert_expiration2' not in body and
        'certificate_id3' not in body and
        'cert_expiration3' not in body and
        'certificate_id4' not in body and
        'cert_expiration4' not in body and
        'home_base_id' not in body and
        'roster_assigned' not in body and
        "monthly_BH" not in body and
        "monthly_DH" not in body and
        "yearly_BH" not in body and
        "yearly_DH" not in body and
        "total_BH" not in body):
        return jsonify({'msg': 'None of the fields included in body can be modified'}), 400
    inflight_data = Inflight.query.filter_by(id=id).first()
    if inflight_data is None:
        return jsonify({'msg': 'The ID is incorrect.'}), 400
    for key, value in body.items():
        if hasattr(inflight_data, key):
            setattr(inflight_data, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    
    db.session.commit()
    return jsonify({'msg': 'Data updated succesfully'}), 200

@app.route('/api/inflight', methods=['DELETE'])
@jwt_required()
def delete_inflight():
    inflight_id = request.args.get('id')
    if inflight_id is None:
        return jsonify({'msg': 'You must specify an ID'}), 400
    inflight_data = Inflight.query.filter_by(id=inflight_id).first()
    if inflight_data is None:
        return jsonify({'msg': 'There is no data in Database'}), 404
    
    db.session.delete(inflight_data)
    db.session.commit()
    return jsonify({'msg': 'Inflight data has been deleted'}), 200

@app.route('/api/airports', methods=['GET'])
def get_airports():
    id = request.args.get('id')
    if id is None:
        airports = Airports.query.all()
        serialized_airports = list(map(lambda airport: airport.serialize(), airports))
        return jsonify(serialized_airports), 200
    airports = Airports.query.filter_by(id=id).all()
    serialized_airports = list(map(lambda airport: airport.serialize(), airports))
    return jsonify(serialized_airports), 200

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
    if not user.is_active:
        return jsonify({'msg': 'User {} is not active'.format(user.crew_id)}), 400
    
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

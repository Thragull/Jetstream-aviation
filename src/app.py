"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, math, jwt
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_swagger import swagger
from sqlalchemy import or_, and_
from api.utils import APIException, generate_sitemap
from api.models import (db, Models, Configurations, Fleet, Prices, Projects, Assignations, Budgets, Roles, Flags, Countries,
                    Nationalities, IntCodes, States, Languages, Employees, Airports, Inflight, Duties, Flights, Hotels, Rosters, Salary_Prices,
                    Bank_Details, Payslips, Documents, Visibility, Departments)
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from flask_jwt_extended import unset_jwt_cookies
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, timezone, time
from api.dbfiller import insert_data, insert_data2, insert_data3, insert_mandatory, compare_flags


def calculate_check_in(hora):
    check_in = hora.replace(hour=hora.hour - 1)
    return check_in

def calculate_check_out(hora):
    check_out_minutos = hora.hour * 60 + hora.minute + 30
    check_out = time(hour=math.floor(check_out_minutos / 60) % 24, minute=check_out_minutos % 60)
    return check_out

def transform_to_seconds(hour):
    return hour.hour * 3600 + hour.minute * 60 + hour.second

def add_hours(hour1, hour2):
    total_seconds = transform_to_seconds(hour1) + transform_to_seconds(hour2)
    total_minutes, remaining_seconds = divmod(total_seconds, 60)
    total_hours, remaining_minutes = divmod(total_minutes, 60)
    return time(hour=total_hours % 24, minute=remaining_minutes, second=remaining_seconds)

def calculate_time_interval(hour1, hour2):
    total_seconds = transform_to_seconds(hour2) - transform_to_seconds(hour1)
    return round(total_seconds/3600, 2)

def roster_calculations(roster_id):
    roster_to_calculate = Rosters.query.filter_by(id=roster_id).first()
    flights = []
    for i in range(1, 7):
        if getattr(roster_to_calculate, f"flight{i}_id") is not None:
            flights.append(Flights.query.filter_by(id=getattr(roster_to_calculate, f"flight{i}_id")).first())
    check_in_UTC = calculate_check_in(getattr(flights[0], "departure_UTC"))
    check_in_LT = calculate_check_in(getattr(flights[0], "departure_LT"))
    check_out_UTC = calculate_check_out(getattr(flights[len(flights)-1], "arrival_UTC"))
    check_out_LT = calculate_check_out(getattr(flights[len(flights)-1], "arrival_LT"))
    duty_hours = calculate_time_interval(check_in_UTC, check_out_UTC)
    block_hours = 0
    for flight in flights:
        block_hours += calculate_time_interval(getattr(flight, "departure_UTC"), getattr(flight, "arrival_UTC"))
    setattr(roster_to_calculate, "check_in_UTC", check_in_UTC)
    setattr(roster_to_calculate, "check_in_LT", check_in_LT)
    setattr(roster_to_calculate, "check_out_UTC", check_out_UTC)
    setattr(roster_to_calculate, "check_out_LT", check_out_LT)
    setattr(roster_to_calculate, "block_hours", block_hours)
    setattr(roster_to_calculate, "duty_hours", duty_hours)

def delete_roster_entry(employee_id, flight):
    existing_roster = Rosters.query.filter_by(employee_id=employee_id, date=flight.date).first()
    if existing_roster:
        employee_flights = []
        for i in range(1, 7):
            if getattr(existing_roster, f"flight{i}_id") is not None:
                employee_flights.append(Flights.query.filter_by(id=getattr(existing_roster, f"flight{i}_id")).first())
        if len(employee_flights) == 1:
            db.session.delete(existing_roster)
        else:
            setattr(existing_roster, f"flight{len(employee_flights)}_id", None)
            employee_flights.remove(flight)
            i=1
            for employee_flight in employee_flights:
                setattr(existing_roster, f"flight{i}_id", employee_flight.id)
                i+=1
            roster_calculations(getattr(existing_roster, "id"))
        db.session.commit()

def add_new_roster_entry(employee_id, flight):
    existing_roster = Rosters.query.filter_by(employee_id=employee_id, date=flight.date).first()
    if existing_roster:
        ground_duty = ['OFFH', 'HOL', 'GTR']
        if existing_roster.duty.duty in ground_duty:
            return jsonify({'msg': 'Employee is not available to fly on this date'}), 
        duty_id = Duties.query.filter_by(duty="FLT").first().id
        if existing_roster.duty_id != duty_id:
            existing_roster.duty_id = duty_id
        employee_flights = []
        for i in range(1, 7):
            if getattr(existing_roster, f"flight{i}_id") is None:
                employee_flights.append(flight)
                break
            else:
                employee_flights.append(Flights.query.filter_by(id=getattr(existing_roster, f"flight{i}_id")).first())
        else:
            return jsonify({'msg': 'Maximum number of flights per day reached for employee'}), 400
        if len(employee_flights) > 1:
            sorted_flights = sorted(employee_flights, key=lambda x: x.departure_UTC)
            i=1
            for sorted_flight in sorted_flights:
                setattr(existing_roster, f"flight{i}_id", sorted_flight.id)
                i+=1
        roster_calculations(getattr(existing_roster, "id"))
    else:
        duty_id = Duties.query.filter_by(duty="FLT").first().id
        roster_entry = Rosters(
                    date=flight.date,
                    employee_id=employee_id,
                    base_id=flight.departure_id,
                    duty_id=duty_id,
                    flight1_id=flight.id
                )
        db.session.add(roster_entry)
        db.session.commit()
        roster_calculations(getattr(roster_entry, "id"))



# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, support_credentials=True)

app.config["JWT_SECRET_KEY"] = "J3t$r34m-$up3r-P0w3r"  # Change this!

jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
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
def get_models():
    id = request.args.get('id')
    if id is None:
        models = Models.query.all()
        serialized_models = [model_name.serialize() for model_name in models]
        return jsonify(serialized_models), 200
    models = Models.query.filter_by(id=id).all()
    serialized_models = [model_name.serialize() for model_name in models]
    return jsonify(serialized_models), 200

@app.route('/api/configurations', methods=['GET'])
def get_configurations():
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
def get_fleet():
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
def get_prices():
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
def get_projects():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
    projects = Projects.query.all()
    serialized_projects = list(map(lambda project: project.serialize(), projects))
    return jsonify(serialized_projects), 200

@app.route('/api/projects', methods=['POST'])
@jwt_required()
def createProject():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
    assignations = Assignations.query.all()
    serialized_assignations = list(map(lambda assignation: assignation.serialize(), assignations))
    return jsonify(serialized_assignations), 200

@app.route('/api/assignations', methods=['POST'])
@jwt_required()
def createAssignations():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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

@app.route('/api/budgets', methods=['GET'])
@jwt_required()
def get_budgets():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
    id = request.args.get('id')
    client_name = request.args.get('client_name')
    client_surname = request.args.get('client_surname')
    client_business = request.args.get('client_business')
    email = request.args.get('email')
    phone = request.args.get('phone')
    pending = request.args.get('pending')
    accepted = request.args.get('accepted')

    conditions = []

    if id:
        conditions.append(Budgets.id == id)
    if client_name:
        conditions.append(Budgets.client_name == client_name)
    if client_surname:
        conditions.append(Budgets.client_surname == client_surname)
    if client_business:
        conditions.append(Budgets.client_business == client_business)
    if email:
        conditions.append(Budgets.email == email)
    if phone:
        conditions.append(Budgets.phone == phone)
    if pending:
        conditions.append(Budgets.pending == pending)
    if accepted:
        conditions.append(Budgets.accepted == accepted)
    
    if conditions:
        budgets = Budgets.query.filter(and_(*conditions)).all()
    else:
        budgets = Budgets.query.all()
    
    serialized_budgets = list(map(lambda budget: budget.serialize(), budgets))
    return jsonify(serialized_budgets)

@app.route('/api/budgets', methods=['POST'])
def post_budgets():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('client_name' not in body or
        'client_surname' not in body or
        'client_business' not in body or
        'client_email' not in body or
        'client_phone' not in body or
        'start_date' not in body or
        'end_date' not in body or
        'total_price' not in body):
        return jsonify({'msg': 'One or more mandatory fields are missing'}), 400
    budget = Budgets()

    for key, value in body.items():
        if hasattr(budget, key):
            setattr(budget, key, value)
        else:
            return jsonify({'msg': 'Invalid field {}'.format(key)}), 400
    setattr(budget, 'pending', True)
    db.session.add(budget)
    db.session.commit()
    return jsonify({'msg': 'New budget added. Pending of review'}), 201

@app.route('/api/budgets', methods=['PUT'])
@jwt_required()
def put_budget():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify the budget ID'}), 400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('start_date' not in body and
        'end_date' not in body and
        'total_price' not in body and
        'pending' not in body and
        'accepted' not in body):
        return jsonify({'msg': 'None of the fields included can be modified'}), 400
    budget = Budgets.query.filter_by(id=id).first()
    for key, value in body.items():
        if hasattr(budget, key):
            setattr(budget, key, value)
        else:
            return jsonify({'msg': 'Invalid field {}'.format(key)}), 400
    db.session.commit()
    return jsonify({'msg': 'Budget with ID {} succesfully updated'.format(id)}), 200

@app.route('/api/budgets', methods=['DELETE'])
@jwt_required()
def delete_budgets():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify a budget ID'}), 400
    budget = Budgets.query.filter_by(id=id).first()
    if budget is None:
        return jsonify({'msg': 'The budget does not exist'}), 404
    db.session.delete(budget)
    db.session.commit()
    return jsonify({'msg': 'Budget succesfully deleted'}), 200

@app.route('/api/roles', methods=['GET'])
@jwt_required()
@cross_origin(supports_credentials=True)
def getRoles():
    id = request.args.get('id')
    if id is None:
        roles = Roles.query.all()
        serialized_roles = list(map(lambda role: role.serialize(), roles))
        return jsonify(serialized_roles), 200
    role = Roles.query.filter_by(id=id).first()
    if role is None:
        return jsonify({'msg': 'Role not found'}), 404
    return jsonify(role.serialize()), 200

@app.route('/api/countries', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCountries():
    id = request.args.get('id')
    if id is None:
        countries = Countries.query.all()
        serialize_countries = list(map(lambda country: country.serialize(), countries))
        return jsonify(serialize_countries), 200
    country = Countries.query.filter_by(id=id).first()
    if country is None:
        return jsonify({'msg': 'Country not found'}), 404
    return jsonify(country.serialize()), 200

@app.route('/api/int_codes', methods=['GET'])
def get_int_code():
    id = request.args.get('id')
    if id is None:
        int_codes = IntCodes.query.all()
        serialize_int_codes = list(map(lambda int_code: int_code.serialize(), int_codes))
        return jsonify(serialize_int_codes), 200
    int_code = IntCodes.query.filter_by(id=id).first()
    if int_code is None:
        return jsonify({'msg': 'International Code not found'}), 404
    return jsonify(int_code.serialize()), 200


@app.route('/api/nationalities', methods=['GET'])
def get_nationalities():
    id = request.args.get('id')
    if id is None:
        nationalities = Nationalities.query.all()
        serialized_nationalities = list(map(lambda nationality: nationality.serialize(), nationalities))
        return jsonify(serialized_nationalities), 200
    nationality = Nationalities.query.filter_by(id=id).first()
    if nationality is None:
        return jsonify({'msg': 'Nationality not found'}), 404
    return jsonify(nationality.serialize()), 200

@app.route('/api/languages', methods=['GET'])
def get_languages():
    id = request.args.get('id')
    if id is None:
        languages = Languages.query.all()
        serialized_languages = list(map(lambda language: language.serialize(), languages))
        return jsonify(serialized_languages), 200
    language = Languages.query.filter_by(id=id).first()
    if language is None:
        return jsonify({'msg': 'Language not found'}), 404
    return jsonify(language.serialize()), 200

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
    credentials=get_jwt()
    crew_id = get_jwt_identity()
    if crew_id is None:
        return jsonify({'msn': 'You must specify a employee ID'}), 400
    employee = Employees.query.filter_by(crew_id=crew_id).first()
    if employee is None:
        return jsonify({'msg': 'The employee does not exists'}), 404
    if not employee.is_active:
        return jsonify({'msg': 'The employee does not exists'}), 404
    return jsonify(employee.serialize()), 200
    

@app.route('/api/filterEmployees', methods=['GET'])
@jwt_required()
def filter_employees():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if role_id is None: 
        return jsonify({'msg': 'Unauthorised access'}), 401
    role_id = request.args.get('role_id')
    department_id = request.args.get('department_id')
    id = request.args.get('id')
    if id is not None: 
        employees = Employees.query.filter_by(id=id).all()
        serialized_employees = list(map(lambda employee: employee.serialize(), employees))
        return jsonify(serialized_employees)
    if role_id is not None: 
        employees = Employees.query.filter_by(role_id=role_id).all()
        serialized_employees = list(map(lambda employee: employee.serialize(), employees))
        return jsonify(serialized_employees), 200
    if department_id is not None: 
        employees = Employees.query.filter_by(department_id=department_id).all()
        serialized_employees = list(map(lambda employee: employee.serialize(), employees))
        return jsonify(serialized_employees), 200
    return jsonify({'msg': 'You must specify a role or a department ID'}), 400
    
@app.route('/api/signupEmployee', methods=['POST'])
@jwt_required()
@cross_origin(supports_credentials=True)
def signup_user():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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
@cross_origin(supports_credentials=True)
@jwt_required()
def put_employee():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': "You can not send empty info"}), 400
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        if ('department' in body or 'role' in body):
            return jsonify({'msg': 'You are not authorised to perform certain changes'}), 401
    else:
        employee_id = request.args.get('id')
    if employee_id is None:
        return jsonify({'msg': 'You must specify an Employee ID'}), 400
    if( "crew_id" not in body and
        "name" not in body and
        "surname" not in body and
        "email" not in body and
        "phone" not in body and
        "role_id" not in body and
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
        if hasattr(employee, key) and key!="id":
            setattr(employee, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    db.session.commit()
    return jsonify({'msg': "Employee {} successfully modified".format(employee.crew_id)}), 200

@app.route('/api/employee', methods=['DELETE'])
@jwt_required()
def deleteEmployee():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorised access'}), 401
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
def get_inflight():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        print(employee_id)
    else:
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
        return jsonify({'msg': 'There is no inflight data yet'}), 404
    return jsonify(inflight_data.serialize()), 200

@app.route('/api/inflight', methods=['POST'])
@jwt_required()
def postInflight():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'msg': 'Body must contain something'}), 400
        if ('license' not in body or
            'passport' not in body or
            'pass_expiration' not in body or
            'certificate_id' not in body or
            'cert_expiration' not in body or
            'home_base_id' not in body):
            return jsonify({'msg': 'There are mandatory fields missing in body'}), 400
        inflight_data = Inflight.query.filter_by(employee_id=employee_id).first()
        if inflight_data is not None:
            return jsonify({'msg': 'The data already exists'}), 400
        inflight_data = Inflight()
        inflight_data.employee_id=employee_id
    else:
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
        inflight_data = Inflight.query.filter_by(employee_id=employee_id).first()
        if inflight_data is not None:
            return jsonify({'msg': 'The data already exists'}), 400
        inflight_data = Inflight()
    for key, value in body.items():
        if hasattr(inflight_data, key):
            setattr(inflight_data, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
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
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
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
        inflight_data = Inflight.query.filter_by(employee_id=employee_id).first()
    else:
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
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        inflight_data = Inflight.query.filter_by(employee_id=employee_id).first()
        if inflight_data is None:
            return jsonify({'msg': 'There is no data in Database'}), 404
    else:
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
    country_id = request.args.get('country_id')
    if country_id is not None: 
            airports = Airports.query.filter_by(country_id=country_id).all()
            serialized_airports = list(map(lambda airport: airport.serialize(), airports))
            return jsonify(serialized_airports), 200
    if id is None:
        airports = Airports.query.all()
        serialized_airports = list(map(lambda airport: airport.serialize(), airports))
        return jsonify(serialized_airports), 200
    airports = Airports.query.filter_by(id=id).all()
    serialized_airports = list(map(lambda airport: airport.serialize(), airports))
    return jsonify(serialized_airports), 200

@app.route('/api/duties', methods=['GET'])
@jwt_required()
def get_duties():
    id = request.args.get('id')
    if id is None: 
        duties = Duties.query.all()
        serialized_duties = list(map(lambda duty: duty.serialize(), duties))
        return jsonify(serialized_duties), 200
    duties = Duties.query.filter_by(id=id).all()
    serialized_duties = list(map(lambda duty: duty.serialize(), duties))
    return jsonify (serialized_duties), 200

@app.route('/api/flights', methods=['GET'])
@jwt_required()
def get_flights():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        employee = credentials.get('employee_id')

        id= request.args.get('id')
        date = request.args.get('date')
        duty_id = Duties.query.filter_by(duty='FLT').first().id

        if date:
            rosters = Rosters.query.filter_by(employee_id=employee, duty_id=duty_id, date=date).all()
        else:
            rosters = Rosters.query.filter_by(employee_id=employee, duty_id=duty_id).all()

        flights = []
        if id is not None:
            for roster in rosters:
                for i in range(1, 7):
                    if getattr(roster, f"flight{i}_id") == int(id):
                        print(roster)
                        flight=Flights.query.filter_by(id=id).first()
                        if flight is not None:
                            flights.append(flight)
        else:
            for roster in rosters:
                for i in range(1, 7):
                    id = getattr(roster, f"flight{i}_id")
                    flight = Flights.query.filter_by(id=id).first()
                    if flight is not None:
                        flights.append(flight)


    else:
        id = request.args.get('id')
        flight_number = request.args.get('flight_number')
        date = request.args.get('date')
        arrival = request.args.get('arrival_id')
        departure = request.args.get('departure_id')
        
        conditions = []

        if id:
            conditions.append(Flights.id == id)
        if flight_number:
            conditions.append(Flights.flight_number == flight_number)
        if date:
            conditions.append(Flights.date == date)
        if arrival:
            conditions.append(Flights.arrival_id == arrival)
        if departure:
            conditions.append(Flights.departure_id == departure)
    
        if conditions:
            flights = Flights.query.filter(and_(*conditions)).all()
        else:
            flights = Flights.query.all()

    serialized_flights = [flight.serialize() for flight in flights]
    return jsonify(serialized_flights), 200

@app.route('/api/flights', methods=['POST'])
@jwt_required()
def post_flights():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        return jsonify({'msg': 'Unauthorise access'}), 401
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('flight_number' not in body or
        'date' not in body or
        'departure_id' not in body or
        'arrival_id' not in body or
        'departure_UTC' not in body or
        'departure_LT' not in body or
        'arrival_UTC' not in body or
        'arrival_LT' not in body or
        'aircraft_id' not in body or
        'cpt_id' not in body or
        'fo_id' not in body or
        'sccm_id' not in body or
        'cc2_id' not in body or
        'cc3_id' not in body or
        'cc4_id' not in body):
        return jsonify({'msg': 'At least one of the mandatory fields is missing'}), 400
    
    # Convertir las cadenas de tiempo a objetos time
    for time_field in ['departure_UTC', 'departure_LT', 'arrival_UTC', 'arrival_LT']:
        if time_field in body:
            body[time_field] = datetime.strptime(body[time_field], '%H:%M:%S').time()

    # Crear el vuelo y agregarlo a la base de datos
    flight = Flights()
    for key, value in body.items():
        if hasattr(flight, key):
            setattr(flight, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    
    # Verificar si ya hay vuelos para este día
    existing_flights = Flights.query.filter_by(date=flight.date).all()

    #Guardamos el vuelo en la base de datos
    #Lo hacemos despues de verificar si ya hay vuelos para evitar conflicto
    db.session.add(flight)

    if existing_flights == []:
        # Si no hay vuelos previos, establecer el check-in y el check-out como los del vuelo actual
        check_in_UTC_time = calculate_check_in(flight.departure_UTC)
        check_in_LT_time = calculate_check_in(flight.departure_LT)
        check_out_UTC_time = calculate_check_out(flight.arrival_UTC)
        check_out_LT_time = calculate_check_out(flight.arrival_LT)
        total_block_hours = calculate_time_interval(flight.departure_UTC, flight.arrival_UTC)
    else:
        existing_flights.append(flight)
        earliest_flight=existing_flights[0]
        for existing_flight in existing_flights:
            if existing_flight.departure_UTC < earliest_flight.departure_UTC:
                earliest_flight=existing_flight
        latest_flight=existing_flights[0]
        for existing_flight in existing_flights:
            if existing_flight.arrival_UTC > latest_flight.arrival_UTC:
                latest_flight=existing_flight

        check_in_UTC_time = calculate_check_in(earliest_flight.departure_UTC)
        check_in_LT_time = calculate_check_in(earliest_flight.departure_LT)
        check_out_UTC_time = calculate_check_out(latest_flight.arrival_UTC)
        check_out_LT_time = calculate_check_out(latest_flight.arrival_LT)

        # Calcular las block hours
        total_block_hours = 0
        for existing_flight in existing_flights:
            total_block_hours += calculate_time_interval(existing_flight.departure_UTC, existing_flight.arrival_UTC)

    # Agregar los datos calculados al vuelo
    flight.check_in_UTC = check_in_UTC_time
    flight.check_in_LT = check_in_LT_time
    flight.check_out_UTC = check_out_UTC_time
    flight.check_out_LT = check_out_LT_time
    flight.block_hours = total_block_hours
    
    # Calcular Duty Hours
    duty_hours = calculate_time_interval(check_in_UTC_time, check_out_UTC_time)
    
    # Obtener el ID del duty correspondiente ("FLT")
    duty_id = Duties.query.filter_by(duty="FLT").first().id
    
    # Verificar si el empleado tiene un duty asignado previamente como "OFFH", "HOL" o "GTR"
    employee_duty_ids = ['OFFH', 'HOL', 'GTR']
    for employee_field in ['cpt_id', 'fo_id', 'sccm_id', 'cc2_id', 'cc3_id', 'cc4_id']:
        employee_id = body.get(employee_field)
        if employee_id:
            employee_duties = Rosters.query.filter_by(date=flight.date, employee_id=employee_id).all()
            for employee_duty in employee_duties:
                if employee_duty.duty.duty in employee_duty_ids:
                    return jsonify({'msg': 'Employee is not available to fly on this date'}), 400
    
    # Crear registros de roster para cada empleado asociado al vuelo
    roster_entries = []
    for employee_field in ['cpt_id', 'fo_id', 'sccm_id', 'cc2_id', 'cc3_id', 'cc4_id']:
        employee_id = body.get(employee_field)
        if employee_id:
            # Verificar si ya hay un roster creado para el empleado y el día dado
            existing_roster = Rosters.query.filter_by(date=flight.date, employee_id=employee_id).first()
            if existing_roster:
                # Actualizar el roster existente si ya había uno creado
                employee_flights = []
                for i in range(1, 7):
                    if getattr(existing_roster, f"flight{i}_id") is None:
                        employee_flights.append(Flights.query.filter_by(id=flight.id).first())
                        break
                    else:
                        employee_flights.append(Flights.query.filter_by(id=getattr(existing_roster, f"flight{i}_id")).first())
                else:
                    return jsonify({'msg': 'Maximum number of flights per day reached for employee'}), 400
                if len(employee_flights) > 1:
                    sorted_flights = sorted(employee_flights, key=lambda x: x.departure_UTC)
                    i=1
                    for sorted_flight in sorted_flights:
                        setattr(existing_roster, f"flight{i}_id", sorted_flight.id)
                        i+=1
                existing_roster.check_in_UTC = check_in_UTC_time
                existing_roster.check_in_LT = check_in_LT_time
                existing_roster.check_out_UTC = check_out_UTC_time
                existing_roster.check_out_LT = check_out_LT_time
                existing_roster.block_hours = total_block_hours
                existing_roster.duty_hours = duty_hours
            else:
                # Crear un nuevo registro de roster si no hay uno existente
                roster_entry = Rosters(
                    date=flight.date,
                    employee_id=employee_id,
                    base_id=flight.departure_id,
                    duty_id=duty_id,
                    flight1_id=flight.id,
                    check_in_UTC=check_in_UTC_time,
                    check_in_LT=check_in_LT_time,
                    check_out_UTC=check_out_UTC_time,
                    check_out_LT=check_out_LT_time,
                    block_hours=total_block_hours,
                    duty_hours=duty_hours
                )
                roster_entries.append(roster_entry)
    
    # Agregar los registros de roster a la base de datos
    db.session.add_all(roster_entries)
    db.session.commit()
    
    return jsonify({'msg': 'Flight and Roster entries added successfully'}), 201



@app.route('/api/flights', methods=['PUT'])
@jwt_required()
def update_flights():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        return jsonify({'msg': 'Unauthorise access'}), 401
    flight_id = request.args.get('id')
    if flight_id is None:
        return jsonify({'msg': 'Yoy must specify a Flight ID'}), 400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('flight_number' not in body and
        'departure_id' not in body and
        'arrival_id' not in body and
        'departure_UTC' not in body and
        'departure_LT' not in body and
        'arrival_UTC' not in body and
        'arrival_LT' not in body and
        'aircraft_id' not in body and
        'cpt_id' not in body and
        'fo_id' not in body and
        'sccm_id' not in body and
        'cc2_id' not in body and
        'cc3_id' not in body and
        'cc4_id' not in body and
        'cc5_id' not in body and
        'cc6_id' not in body and
        'cc7_id' not in body and
        'cc8_id' not in body):
        return jsonify({'msg': 'You must specify at least one field to be updated'}), 400
    flight = Flights.query.filter_by(id=flight_id).first()
    if flight is None:
        return jsonify({'msg': 'Flight does not exist'}), 404
    for time_field in ['departure_UTC', 'departure_LT', 'arrival_UTC', 'arrival_LT']:
        if time_field in body:
            body[time_field] = datetime.strptime(body[time_field], '%H:%M:%S').time()
    non_crew_fields =['flight_number', 'departure_id', 'arrival_id', 'departure_UTC', 'departure_LT', 'arrival_UTC', 'arrival_LT', 'aircraft_id']
    for field in non_crew_fields:
        if field in body and body[field] != getattr(flight, field):
            setattr(flight, field, body[field])
    ranks = ['cpt_id', 'fo_id', 'sccm_id', 'cc2_id', 'cc3_id', 'cc4_id', 'cc5_id', 'cc6_id', 'cc7_id', 'cc8_id']
    for rank in ranks:
        if rank in body and body[rank] != getattr(flight, rank):
            delete_roster_entry(getattr(flight, rank), flight)
            add_new_roster_entry(body[rank], flight)
            setattr(flight, rank, body[rank])
        else:
            roster = Rosters.query.filter_by(employee_id=getattr(flight, rank), date=flight.date).first()
            if roster:
                roster_calculations(getattr(roster, "id"))
    for key in body:
        if key not in non_crew_fields and key not in ranks:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400

    db.session.commit()
    return jsonify({'msg': 'Flight {} succesfully updated'.format(flight.flight_number)})

@app.route('/api/flights', methods=['DELETE'])
@jwt_required()
def delete_flight():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        return jsonify({'msg': 'Unauthorise access'}), 401
    flight_id = request.args.get('id')
    if flight_id is None:
        return jsonify({'msg': 'You must specify a Flight ID'}), 400
    flight = Flights.query.filter_by(id=flight_id).first()
    if flight is None:
        return jsonify({'msg': 'The flight does not exist in DB'}), 404
    ranks = ['cpt_id', 'fo_id', 'sccm_id', 'cc2_id', 'cc3_id', 'cc4_id', 'cc5_id', 'cc6_id', 'cc7_id', 'cc8_id']
    for rank in ranks:
        employee_id = getattr(flight, rank)
        if employee_id is not None:
            delete_roster_entry(employee_id, flight)
    db.session.delete(flight)
    db.session.commit()
    return jsonify({'msg': 'The flight {} has been succesfully deleted'.format(flight.flight_number)}), 200

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

@app.route('/api/roster', methods=['GET'])
@jwt_required()
def get_roster():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        employee = credentials.get('employee_id')
        id = id = request.args.get('id')
        date = request.args.get('date')

        conditions = []

        if id:
            conditions.append(Rosters.id == id)
        if employee:
            conditions.append(Rosters.employee_id == employee)
        if date:
            conditions.append(Rosters.date == date)
    else:
        id = request.args.get('id')
        employee = request.args.get('employee_id')
        base = request.args.get('base_id')
        duty = request.args.get('duty_id')
        date = request.args.get('date')
        
        conditions = []

        if id:
            conditions.append(Rosters.id == id)
        if employee:
            conditions.append(Rosters.employee_id == employee)
        if base:
            conditions.append(Rosters.base_id == base)
        if duty:
            conditions.append(Rosters.duty_id == duty)
        if date:
            conditions.append(Rosters.date == date)
        
    if conditions:
        rosters = Rosters.query.filter(and_(*conditions)).all()
    else:
        rosters = Rosters.query.all()

    serialized_rosters = list(map(lambda roster: roster.serialize(), rosters))
    return jsonify(serialized_rosters), 200

@app.route('/api/roster', methods=['POST'])
@jwt_required()
def post_roster():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        return jsonify({'msg': 'Unauthorise access'}), 401
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': "Body must contain something"}), 400
    if ("date"not in body or
        "employee_id" not in body or
        "base_id" not in body or
        "duty_id" not in body):
        return jsonify({'msg': 'One or more mandatory fields are missing in body'}), 400
    roster = Rosters.query.filter_by(employee_id=body['employee_id'], date=body['date']).first()
    if roster is None:
        roster = Rosters()
        for time_field in ["check_in_UTC", "check_in_LT", "check_out_UTC", "check_out_LT"]:
            if time_field in body:
                body[time_field] = datetime.strptime(body[time_field], '%H:%M:%S').time()
        for key, value in body.items():
            if hasattr(roster, key):
                setattr(roster, key, value)
            else:
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
        setattr(roster, "block_hours", 0)
        if "check_in_UTC" in body and "check_out_UTC" in body:
            setattr(roster, "duty_hours", calculate_time_interval(body["check_in_UTC"], body["check_out_UTC"]))
        db.session.add(roster)
        db.session.commit()
        return jsonify({'msg': 'Duty {} created for employee {}'.format(roster.duty, roster.employee)}), 201
    else:
        return jsonify({'msg': 'The employee already has a duty on that date. You can\'t create a new one'}), 400

@app.route('/api/roster', methods=['PUT'])
@jwt_required()
def put_roster():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        return jsonify({'msg': 'Unauthorise access'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify the roster ID'}), 400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ("base_id" not in body and
        "duty_id" not in body and
        "hotel_id" not in body and
        "check_in_UTC" not in body and
        "check_in_LT" not in body and
        "check_out_UTC" not in body and
        "check_out_LT"):
        return jsonify({'msg': 'You must specify at least one field to be updated'}), 400
    if ("date" in body or "employee_id" in body):
        return jsonify({'msg': 'To edit the employee or the date you must delete this register and create a new one'}), 400
    roster = Rosters.query.filter_by(id=id).first()
    if roster is None:
        return jsonify({'msg': 'Roster does not exist'}), 404
    for time_field in ["check_in_UTC", "check_in_LT", "check_out_UTC", "check_out_LT"]:
        if time_field in body:
            body[time_field] = datetime.strptime(body[time_field], '%H:%M:%S').time()
    for key, value in body.items():
        if hasattr(roster, key):
            setattr(roster, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    if "check_in_UTC" in body or "check_out_UTC" in body:
        setattr(roster, "duty_hours", calculate_time_interval(getattr(roster, "check_in_UTC"), getattr(roster, "check_out_UTC")))
    db.session.commit()
    return jsonify({'msg': 'Duty {} updated for employee {}'.format(roster.duty, roster.employee)}), 200

@app.route('/api/roster', methods=['DELETE'])
@jwt_required()
def delete_roster():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Crew Control').first().id != role_id:
        return jsonify({'msg': 'Unauthorise access'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify the roster ID'}), 400
    roster = Rosters.query.filter_by(id=id).first()
    if roster is None:
        return jsonify({'msg': 'Roster does not exist'}), 404
    if getattr(roster, "flight1_id") is not None:
        return jsonify({'msg': 'You must delete all flights for this employee first'}), 400
    db.session.delete(roster)
    db.session.commit()
    return jsonify({'msg': 'Roster with ID {} succesfully deleted'.format(id)}), 200

@app.route('/api/salary_prices', methods=['GET'])
@jwt_required()
def get_salary_prices():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'Unauthorise access'}), 401
    role_id = request.args.get('role_id')
    if role_id is None:
        return jsonify({'msg': 'You must specify a Role ID'}), 400
    salary_prices = Salary_Prices.query.filter_by(role_id=role_id).first()
    if salary_prices is None:
        return jsonify({'msg': 'There is no salary table for this role'}), 404
    return jsonify(salary_prices.serialize()), 200
                                    
@app.route('/api/bank_details', methods=['GET'])
@jwt_required()
def get_bank_details():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        bank_details = Bank_Details.query.filter_by(employee_id=employee_id).first()
        if bank_details is None:
            return jsonify({'msg': 'There is no bank details for this employee'}), 404
    else:
        id = request.args.get('id')
        employee_id = credentials.get('employee_id')
        if id is None:
            bank_details = Bank_Details.query.filter_by(employee_id=employee_id).first()
        else:
            bank_details = Bank_Details.query.filter_by(id=id).first()
        if bank_details is None:
            return jsonify({'msg': 'There is no bank details with this ID'}), 404
    return jsonify(bank_details.serialize()), 200

@app.route('/api/bank_details', methods=['POST'])
@jwt_required()
def post_bank_details():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'msg': 'Body must contain something'}), 400
        if 'IBAN' not in body:
            return jsonify({'msg': 'One or more of the mandatory fields are missing in body'}), 400
        bank_details = Bank_Details.query.filter_by(employee_id=employee_id).first()
        if bank_details is not None:
            return jsonify({'msg': 'This employee already have bank details registered in DB.'}), 400
        bank_details = Bank_Details()
        for key, value in body.items():
            if hasattr(bank_details, key):
                setattr(bank_details, key, value)
            else:
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    else:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'msg': 'Body must contain something'}), 400
        if ('employee_id' not in body or
            'IBAN' not in body):
            return jsonify({'msg': 'One or more of the mandatory fields are missing in body'}), 400
        bank_details = Bank_Details.query.filter_by(employee_id=body['employee_id']).first()
        if bank_details is not None:
            return jsonify({'msg': 'This employee already have bank details registered in DB.'}), 400
        bank_details = Bank_Details()
        for key, value in body.items():
            if hasattr(bank_details, key):
                setattr(bank_details, key, value)
            else:
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
        
    db.session.add(bank_details)
    db.session.commit()
    return jsonify({'msg': 'Bank details added for employee {}'.format(bank_details.employee)})

 
@app.route('/api/bank_details', methods=['PUT'])
@jwt_required()
def put_bank_details():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'msg': 'Body must contain something'}), 400
        if ('IBAN' not in body and 'tax_number' not in body):
            return jsonify({'msg': 'You must specify at least on of the fields to be updated'}), 400
        bank_details = Bank_Details.query.filter_by(employee_id=employee_id).first()
        if bank_details is None:
            return jsonify({'msg': 'There are no bank details with this ID'}), 404
        for key, value in body.items():
            if hasattr(bank_details, key):
                setattr(bank_details, key, value)
            else:
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    else:
        id = request.args.get('id')
        if id is None:
            return jsonify({'msg': 'You must specify a bank details ID'}), 400
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'msg': 'Body must contain something'}), 400
        if ('IBAN' not in body and 'tax_number' not in body):
            return jsonify({'msg': 'You must specify at least on of the fields to be updated'}), 400
        bank_details = Bank_Details.query.filter_by(id=id).first()
        if bank_details is None:
            return jsonify({'msg': 'There are no bank details with this ID'}), 404
        for key, value in body.items():
            if hasattr(bank_details, key):
                setattr(bank_details, key, value)
            else:
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    db.session.commit()
    return jsonify({'msg': 'Bank details succesfully updated for employee {}'.format(bank_details.employee)}), 200

@app.route('/api/bank_details', methods=['DELETE'])
@jwt_required()
def delete_bank_details():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get('employee_id')
        bank_details = Bank_Details.query.filter_by(employee_id=employee_id).first()
        if bank_details is None:
            return jsonify({'msg': 'There are no details for this employee'}), 404
    else:
        id = request.args.get('id')
        if id is None:
            return jsonify({'msg': 'You must specify an ID'}), 400
        bank_details = Bank_Details.query.filter_by(id=id).first()
        if bank_details is None:
            return jsonify({'msg': 'There are no details with this ID'}), 404
    db.session.delete(bank_details)
    db.session.commit()
    return jsonify({'msg': 'Bank details succesfully deleted'}), 200

@app.route('/api/payslips', methods=['GET'])
@jwt_required()
def get_payslips():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        employee_id = credentials.get("employee_id")
        if employee_id is None:
            return jsonify({'msg': 'You must specify an Employee ID'}), 400
        payslips = Payslips.query.filter_by(employee_id=employee_id).all()
        serialized_payslips = list(map(lambda payslip: payslip.serialize(), payslips))
        return jsonify(serialized_payslips), 200
    else:
        employee_id = request.args.get('employee_id')
        if employee_id is None:
            payslips = Payslips.query.all()
        else:
            payslips = Payslips.query.filter_by(employee_id=employee_id).all()
        serialized_payslips = list(map(lambda payslip: payslip.serialize(), payslips))
        return jsonify(serialized_payslips), 200

@app.route('/api/payslips', methods=['POST'])
@jwt_required()
def post_payslips():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'You have no permission to do this task'}), 401
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('employee_id' not in body or
        'month' not in body or
        'year' not in body or
        'href' not in body):
        return jsonify({'msg': 'One or more mandatory fields are missing'}), 400
    payslip = Payslips.query.filter_by(employee_id=body['employee_id'], month=body['month'], year=body['year']).first()
    if payslip is not None:
        return jsonify({'msg': 'There is alread a payslip for this employee on the selected dates'}), 405
    payslip = Payslips()
    for key, value in body.items():
        if hasattr(payslip, key):
            setattr(payslip, key, value)
        else:
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
    db.session.add(payslip)
    db.session.commit()
    return jsonify({'msg': 'Payslip created succesfully for employee {}'.format(payslip.employee)}), 201

@app.route('/api/payslips', methods=['PUT'])
@jwt_required()
def put_payslips():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'You have no permission to do this task'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify a Payslip ID'}), 400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if 'href' not in body:
        return jsonify({'msg': 'You must specify the new route to the file'}), 400
    payslip = Payslips.query.filter_by(id=id).first()
    if payslip is None:
        return jsonify({'msg': 'There is no payslip with this ID'}), 404
    setattr(payslip, 'href', body['href'])
    db.session.commit()
    return jsonify({'msg': 'Payslip updated succesfully'}), 200

@app.route('/api/payslips', methods=['DELETE'])
@jwt_required()
def delete_payslips():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'You have no permission to do this task'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify a Payslip ID'}), 400
    payslip = Payslips.query.filter_by(id=id).first()
    if payslip is None:
        return jsonify({'msg': 'There is no payslip with this ID'}), 404
    db.session.delete(payslip)
    db.session.commit()
    return jsonify({'msg': 'Payslip deleted succesfully'}), 200

@app.route('/api/documents', methods=['GET'])
@jwt_required()
def get_documents():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    id = request.args.get('id')
    if role_id is None:
        return jsonify({'msg': 'You have no authorisation'}), 401
    if id is None:
        visibility = Visibility.query.filter_by(role_id=role_id).all()
        documents = []
        for item in visibility:
            documents.append(Documents.query.filter_by(id=item.document_id).first())
        serialize_documents = list(map(lambda document: document.serialize(), documents))
        return jsonify(serialize_documents), 200
    visibility = Visibility.query.filter_by(document_id=id, role_id=role_id).first()
    if visibility is None:
        return jsonify({'msg': 'You have no authorisation to access this document'}), 401
    document = Documents.query.filter_by(id=id).first()
    return jsonify(document.serialize()), 200

@app.route('/api/documents', methods=['POST'])
@jwt_required()
def post_documents():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'You have no permission to do this task'}), 401
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('document_name' not in body or 'path' not in body):
        return jsonify({'msg': 'One or more mandatory fields are missing'}), 400
    document = Documents()
    if 'visibility' not in body:
        for key, value in body.items():
            if hasattr(document, key):
                setattr(document, key, value)
            else:
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400
        db.session.add(document)
        visibility = Visibility()
        role_id = Roles.query.filter_by(role='Manager').first().id
        visibility.role_id=role_id
        visibility.document_id=document.id
        db.session.add(visibility)
        db.session.commit()
        return jsonify({'msg': 'New document added succesfully'}), 201
    else:
        for key, value in body.items():
            if hasattr(document, key):
                setattr(document, key, value)
            elif key != 'visibility':
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400        
        db.session.add(document)
        visibility = []
        for item in body['visibility']:
            role_id = Roles.query.filter_by(role=item).first().id
            if role_id is None:
                return jsonify({'msg': 'Specific role in visibility {} not valid'.format(item)}), 400
            new_document_visibility = Visibility()
            new_document_visibility.role_id=role_id
            new_document_visibility.document_id= document.id
            visibility.append(new_document_visibility)
        db.session.add_all(visibility)
        db.session.commit()
        return jsonify({'msg': 'New document added succesfully'}), 201

@app.route('/api/documents', methods=['PUT'])
@jwt_required()
def put_documents():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'You have no permission to do this task'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify a Document ID'}), 400
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body must contain something'}), 400
    if ('document_name' not in body and 'path' not in body and 'visibility' not in body):
        return jsonify({'msg': 'You must specify at least one of the fields to be updated'}), 400
    if 'visibility' not in body:
        document = Documents.query.filter_by(id=id).first()
        for key, value in body.items():
            if hasattr(document, key):
                setattr(document, key, value)
            else:
                return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400    
        db.session.commit()
        return jsonify({'msg': 'Document {} succesfully updated'.format(document.document_name)}), 200
    document = Documents.query.filter_by(id=id).first()
    for key, value in body.items():
        if hasattr(document, key):
            setattr(document, key, value)
        elif key != 'visibility':
            return jsonify({'msg': 'Invalid field: {}'.format(key)}), 400   
    visibility = Visibility.query.filter_by(document_id=id).all()
    for item in visibility:
        if item.role.role not in body['visibility']:
            db.session.delete(item)
            visibility.remove(item)
    for item in body['visibility']:
        role_id = Roles.query.filter_by(role=item).first().id
        if role_id is None:
            return jsonify({'msg': 'Specific role in visibility {} not valid'.format(item)}), 400
        visibility = Visibility.query.filter_by(document_id=id, role_id=role_id).first()
        if visibility is None:
            visibility = Visibility()
            visibility.document_id=id
            visibility.role_id=role_id
            db.session.add(visibility)
    db.session.commit()
    return jsonify({'msg': 'Document {} succesfully updated'.format(document.document_name)}), 200

@app.route('/api/documents', methods=['DELETE'])
@jwt_required()
def delete_documents():
    credentials=get_jwt()
    role_id=credentials.get('role_id')
    if Roles.query.filter_by(role='Manager').first().id != role_id:
        return jsonify({'msg': 'You have no permission to do this task'}), 401
    id = request.args.get('id')
    if id is None:
        return jsonify({'msg': 'You must specify a Document ID'}), 400
    document = Documents.query.filter_by(id=id).first()
    if document is None:
        return jsonify({'msg': 'Document does not exist in DB'}), 404
    visibility = Visibility.query.filter_by(document_id=id).all()
    if visibility != []:
        for item in visibility:
            db.session.delete(item)
    db.session.delete(document)
    db.session.commit()
    return jsonify({'msg': 'Document succesfully deleted'}), 200

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
    
    other_employee_info = {
        "employee_id": user.id,
        "role_id": user.role_id
    }

    access_token = create_access_token(identity=user.crew_id, additional_claims=other_employee_info)
    return jsonify({'msg': 'Login successful', 'token': access_token}), 200

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    # Eliminar el token almacenado en el cliente
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

@app.route("/protected", methods=["GET"])
@jwt_required() #Esto sirve para proteger el enlace
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity() #Este método me devuelve la identidad con el que fue creado
    additional_claims = get_jwt()
    return jsonify(logged_in_as=current_user, additional_claims=additional_claims), 200

@app.route('/api/dbfiller_mandatory', methods=['GET'])
def dbfiller_mandatory():
    insert_mandatory()
    return jsonify({'msg': 'Mandatory fields completed'}), 201

@app.route('/api/dbfiller', methods=['GET'])
def dbfiller():
    insert_data()
    return jsonify({'msg': "Funciona"}), 201

@app.route('/api/dbfiller2', methods=['GET'])
def dbfiller2():
    insert_data2()
    return jsonify({'msg': "Funciona2"}), 201

@app.route('/api/dbfiller3', methods=['GET'])
def dbfiller3():
    insert_data3()
    return jsonify({'msg': "Funciona3"}), 201

@app.route('/api/prueba', methods=['GET'])
def prueba():
    compare_flags()
    return jsonify({'msg': 'correctly executed'}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)

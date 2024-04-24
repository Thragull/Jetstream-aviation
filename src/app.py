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



# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, support_credentials=True)

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
    if country_id is None: 
        return jsonify({'msg': 'You must specify a country id'}), 400
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

@app.route('/api/projects', methods=['GET'])
def getProjects():
    projects = Projects.query.all()
    serialized_projects = list(map(lambda project: project.serialize(), projects))
    return jsonify(serialized_projects), 200

@app.route('/api/projects', methods=['POST'])
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
def modifyProject():
    project_id = request.args.get('id')
    if project_id is None:
        return jsonify({'msg': 'You must specify a project ID'})
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
    return jsonify({'msg': 'Project {} has been succesfully deleted'.format(project.project)})

@app.route('/api/roles', methods=['GET'])
@cross_origin(supports_credentials=True)
def getRoles():
    roles = Roles.query.all()
    serialized_roles = [role.serialize() for role in roles]
    return jsonify(serialized_roles), 200

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






# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)

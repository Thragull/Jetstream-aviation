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
    assigned = db.Column(db.Boolean, default=False)

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
    aircraft = db.relationship(Fleet, foreign_keys=[aircraft_id])

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
    total_price = db.Column(db.BigInteger, nullable=False)
    pending = db.Column(db.Boolean, nullable=False, default=True)
    accepted = db.Column(db.Boolean)

    def __repr__(self):
        return "We can negotiate with {}".format(self.client_business)
    
    def serialize(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "client_surname": self.client_surname,
            "client_business": self.client_business,
            "client_email": self.client_email,
            "client_phone": self.client_phone,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "total_price": self.total_price,
            "pending": self.pending,
            "accepted": self.accepted
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

class Flags(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    flag = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.name}"
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'flag':self.flag
        }

class Countries(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), unique=True, nullable=False)
    flag_id = db.Column(db.Integer, db.ForeignKey('flags.id'), nullable=False)
    flag = db.relationship(Flags)

    def __repr__(self):
        return f"{self.country}"
    
    def serialize(self):
        return {
            'id': self.id,
            'country': self.country,
            'flag': self.flag.flag
        }

class Nationalities(db.Model):
    __tablename__ = 'nationalities'
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(50), unique=True, nullable=False)
    flag_id = db.Column(db.Integer, db.ForeignKey('flags.id'), nullable=False)
    flag = db.relationship(Flags)

    def __repr__(self):
        return f"{self.nationality}"
    
    def serialize(self):
        return {
            'id': self.id,
            'nationality': self.nationality,
            'flag': self.flag.flag
        }

class Languages(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), unique=True, nullable=False)
    flag_id = db.Column(db.Integer, db.ForeignKey('flags.id'), nullable=False)
    flag = db.relationship(Flags)

    def __repr__(self):
        return f'{self.language}'
    
    def serialize(self):
        return {
            'id': self.id,
            'language': self.language,
            'flag': self.flag.flag
        }

class IntCodes(db.Model):
    __tablename__ = 'int_code'
    id = db.Column(db.Integer, primary_key=True)
    int_code = db.Column(db.String(5), unique=True, nullable=False)
    flag_id = db.Column(db.Integer, db.ForeignKey('flags.id'), nullable=False)
    flag = db.relationship(Flags)

    def __repr__(self):
        return f'{self.int_code}'
    
    def serialize(self):
        return {
            'id': self.id,
            'int_code': self.int_code,
            'flag': self.flag.flag
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

class Departments(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.department}"

    def serialize(self):
        return {
            "id": self.id,
            "department": self.department
        }

class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    crew_id = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.BigInteger)
    password = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship(Roles)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    department = db.relationship(Departments)
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
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return "{} {} with code ({})".format(self.name, self.surname, self.crew_id)
    
    def serialize(self):
        return {
            "id": self.id,
            "crew_id": self.crew_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone": self.phone,
            "role_id": self.role_id,
            "department_id": self.department_id,
            "gender": self.gender,
            "nationality_id": self.nationality_id,
            "address": self.address,
            "address2": self.address2,
            "address3": self.address3,
            "country_id": self.country_id,
            "state_id": self.state_id,
            "city": self.city,
            "zipcode": self.zipcode,
            "birthday": self.birthday,
            "entry_date": self.entry_date,
            "is_active": self.is_active
        }

class Airports(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.Integer, primary_key=True)
    IATA_code = db.Column(db.String(3), unique=True, nullable=False)
    ICAO_code = db.Column(db.String(6), unique=True, nullable=False)
    airport_name = db.Column(db.String(100), unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    country = db.relationship(Countries)
    category = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return "{}: {}".format(self.IATA_code, self.airport_name)
    
    def serialize(self):
        return {
            "id": self.id,
            "IATA": self.IATA_code,
            "ICAO": self.ICAO_code,
            "airport": self.airport_name,
            "country": self.country_id,
            "category": self.category
        }


class Inflight(db.Model):
    __tablename__ = 'inflight'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'),unique=True, nullable=False)
    employee = db.relationship(Employees)
    license = db.Column(db.String(10), unique=True, nullable=False)
    passport = db.Column(db.String(10), unique=True, nullable=False)
    pass_expiration = db.Column(db.DateTime, nullable=False)
    certificate_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
    certificate = db.relationship(Models, foreign_keys=certificate_id)
    cert_expiration = db.Column(db.DateTime, nullable=False)
    certificate_id2 = db.Column(db.Integer, db.ForeignKey('models.id'))
    certificate2 = db.relationship(Models, foreign_keys=certificate_id2)
    cert_expiration2 = db.Column(db.DateTime)
    certificate_id3 = db.Column(db.Integer, db.ForeignKey('models.id'))
    certificate3 = db.relationship(Models, foreign_keys=certificate_id3)
    cert_expiration3 = db.Column(db.DateTime)
    certificate_id4 = db.Column(db.Integer, db.ForeignKey('models.id'))
    certificate4 = db.relationship(Models, foreign_keys=certificate_id4)
    cert_expiration4 = db.Column(db.DateTime)
    home_base_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    home_base = db.relationship(Airports)
    roster_assigned = db.Column(db.Integer, nullable=False)
    monthly_BH = db.Column(db.Integer, nullable=False, default=0)
    monthly_DH = db.Column(db.Integer, nullable=False, default=0)
    yearly_BH = db.Column(db.Integer, nullable=False, default=0)
    yearly_DH = db.Column(db.Integer, nullable=False, default=0)
    total_BH = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Employee {}".format(self.employee.crew_id)
    
    def serialize(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "license": self.license,
            "passport": self.passport,
            "pass_expiration": self.pass_expiration,
            "certificate_id": self.certificate_id,
            "cert_expiration": self.cert_expiration,
            "certificate_id2": self.certificate_id2,
            "cert_expiration2": self.cert_expiration2,
            "certificate_id3": self.certificate_id3,
            "cert_expiration3": self.cert_expiration3,
            "certificate_id4": self.certificate_id4,
            "cert_expiration4": self.cert_expiration4,
            "home_base": self.home_base_id,
            "roster_assigned": self.roster_assigned,
            "monthly_BH": self.monthly_BH,
            "monthly_DH": self.monthly_DH,
            "yearly_BH": self.yearly_BH,
            "yearly_DH": self.yearly_DH,
            "total_BH": self.total_BH
        }
        
class Duties(db.Model):
    __tablename__ = 'duties'
    id = db.Column(db.Integer, primary_key=True)
    duty = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return "{}".format(self.duty)
    
    def serialize(self):
        return {
            "id": self.id,
            "duty": self.duty
        }

class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    departure_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    departure = db.relationship(Airports, foreign_keys=departure_id)
    arrival_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    arrival = db.relationship(Airports, foreign_keys=arrival_id)
    departure_UTC = db.Column(db.Time, nullable=False)
    departure_LT = db.Column(db.Time, nullable=False)
    arrival_UTC = db.Column(db.Time, nullable=False)
    arrival_LT = db.Column(db.Time, nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=False)
    aircraft = db.relationship(Fleet)
    cpt_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    cpt = db.relationship(Employees, foreign_keys=cpt_id)
    fo_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    fo = db.relationship(Employees, foreign_keys=fo_id)
    sccm_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    sccm = db.relationship(Employees, foreign_keys=sccm_id)
    cc2_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    cc2 = db.relationship(Employees, foreign_keys=cc2_id)
    cc3_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    cc3 = db.relationship(Employees, foreign_keys=cc3_id)
    cc4_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    cc4 = db.relationship(Employees, foreign_keys=cc4_id)
    cc5_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    cc5 = db.relationship(Employees, foreign_keys=cc5_id)
    cc6_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    cc6 = db.relationship(Employees, foreign_keys=cc6_id)
    cc7_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    cc7 = db.relationship(Employees, foreign_keys=cc7_id)
    cc8_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    cc8 = db.relationship(Employees, foreign_keys=cc8_id)

    def __repr__(self):
        return "{} on the {}".format(self.flight_number, self.date)
    
    def serialize(self):
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "date": str(self.date),
            "departure": self.departure_id,
            "arrival": self.arrival_id,
            "departure_UTC": str(self.departure_UTC),
            "departure_LT": str(self.departure_LT),
            "arrival_UTC": str(self.arrival_UTC),
            "arrival_LT": str(self.arrival_LT),
            "aircraft": self.aircraft_id,
            "cpt": self.cpt_id,
            "fo": self.fo_id,
            "sccm": self.sccm_id,
            "cc2": self.cc2_id,
            "cc3": self.cc3_id,
            "cc4": self.cc4_id,
            "cc5": self.cc5_id,
            "cc6": self.cc6_id,
            "cc7": self.cc7_id,
            "cc8": self.cc8_id,
        }
    
class Hotels(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    base_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    base = db.relationship(Airports)

    def __repr__(self):
        return '{} - {}'.format(self.base.IATA_code, self.name)
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "base": self.base_id
        }

class Rosters(db.Model):
    __tablename__ = 'rosters'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship(Employees)
    base_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    base = db.relationship(Airports)
    duty_id = db.Column(db.Integer, db.ForeignKey('duties.id'), nullable=False)
    duty = db.relationship(Duties)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    hotel = db.relationship(Hotels)
    check_in_UTC = db.Column(db.Time)
    check_in_LT = db.Column(db.Time)
    flight1_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight1 = db.relationship(Flights, foreign_keys=flight1_id)
    flight2_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight2 = db.relationship(Flights, foreign_keys=flight2_id) 
    flight3_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight3 = db.relationship(Flights, foreign_keys=flight3_id) 
    flight4_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight4 = db.relationship(Flights, foreign_keys=flight4_id) 
    flight5_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight5 = db.relationship(Flights, foreign_keys=flight5_id) 
    flight6_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight6 = db.relationship(Flights, foreign_keys=flight6_id)
    check_out_UTC = db.Column(db.Time)
    check_out_LT = db.Column(db.Time)
    block_hours = db.Column(db.Float)
    duty_hours = db.Column(db.Float)

    def __repr__(self):
        return "Duty: {} for the {}".format(self.duty.duty, str(self.date))
    
    def serialize(self):
        return{
            "id": self.id,
            "date": str(self.date),
            "employee_id": self.employee_id,
            "base": self.base_id,
            "duty": self.duty_id,
            "hotel": self.hotel_id,
            "check_in_UTC": str(self.check_in_UTC),
            "check_in_LT": str(self.check_in_LT),
            "flight1": self.flight1_id,
            "flight2": self.flight2_id,
            "flight3": self.flight3_id,
            "flight4": self.flight4_id,
            "flight5": self.flight5_id,
            "flight6": self.flight6_id,
            "check_out_UTC": str(self.check_out_UTC),
            "check_out_LT": str(self.check_out_LT),
            "block_hours": self.block_hours,
            "duty_hours": self.duty_hours
        }

class Salary_Prices(db.Model):
    __tablename__ = 'salary_prices'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship(Roles)
    basic = db.Column(db.Integer, nullable=False)
    main_service = db.Column(db.Float, nullable=False)
    instruction = db.Column(db.Float, nullable=False)
    sec_bonus = db.Column(db.Float, nullable=False)
    per_diem = db.Column(db.Float, nullable=False)
    cleaning_serv = db.Column(db.Float, nullable=False)
    birthday_bonus = db.Column(db.Float, nullable=False)
    additional_bonus = db.Column(db.Float, nullable=False)
    special_project_bonus = db.Column(db.Float, nullable=False)
    bought_days = db.Column(db.Float, nullable=False)
    standby_days = db.Column(db.Float, nullable=False)
    theory_bonus = db.Column(db.Float, nullable=False)
    sick_leave = db.Column(db.Float, nullable=False)
    office_day = db.Column(db.Float, nullable=False)
    office_day_holidays = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'Salary table for {self.role}'
    
    def serialize(self):
        return {
            "id": self.id,
            "role_id": self.role_id,
            "basic": self.basic,
            "main_service": self.main_service,
            "instruction": self.instruction,
            "sec_bonus": self.sec_bonus,
            "per_diem": self.per_diem,
            "cleaning_serv": self.cleaning_serv,
            "birthday_bonus": self.birthday_bonus,
            "additional_bonus": self.additional_bonus,
            "special_project_bonus": self.special_project_bonus,
            "bought_days": self.bought_days,
            "standby_days": self.standby_days,
            "theory_bonus": self.theory_bonus,
            "sick_leave": self.sick_leave,
            "office_day": self.office_day,
            "office_day_holidays": self.office_day_holidays
        }
    
class Bank_Details(db.Model):
    __tablename__ = 'bank_details'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), unique=True, nullable=False)
    employee = db.relationship(Employees)
    IBAN = db.Column(db.String(35), nullable=False)
    tax_number = db.Column(db.String(25))

    def __repr__(self):
        return '{}: {}'.format(self.employee.crew_id, self.IBAN)

    def serialize(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "IBAN": self.IBAN,
            "tax_number": self.tax_number
        }

class Payslips(db.Model):
    __tablename__ = 'payslips'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship(Employees)
    month = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    href = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return 'Payslip {} for month {}'.format(self.id, self.month)
    
    def serialize(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "month": self.month,
            "year": self.year,
            "href": self.href
        }

class Documents(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String(50), nullable=False)
    path = db.Column (db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.document_name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "document_name": self.document_name,
            "path": self.path
        }
    
class Visibility(db.Model):
    __tablename__ = 'visibility'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'),nullable=False)
    role = db.relationship(Roles)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    document = db.relationship(Documents)
    
    def __repr__(self):
        return f'{self.role} sees {self.document.document_name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "role": self.role_id,
            "document_id": self.document_id
        }
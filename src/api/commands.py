
import click
from api.models import db, User, Models, Configurations, Fleet, Prices

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
models=["A320", "A321", "A330","A350", "B737", "B777", "B787"]
configurations = [
                    {"model": "A320", "economy": 180},
                    {"model": "A320", "business": 12, "economy": 150},
                    {"model": "A321", "economy": 220},
                    {"model": "A321", "business": 20, "economy": 200},
                    {"model": "A330", "economy": 250},
                    {"model": "A330", "business": 30, "economy": 220},
                    {"model": "A350", "economy": 300},
                    {"model": "A350", "business": 40, "economy": 260},
                    {"model": "B737", "economy": 189},
                    {"model": "B737", "business": 12, "economy": 159},
                    {"model": "B777", "economy": 220},
                    {"model": "B777", "business": 20, "economy": 200},
                    {"model": "B787", "economy": 240},
                    {"model": "B787", "business": 30, "economy": 210}
                 ]
fleet = [
            {"registration": "EC-ABC", "model": "A320", "business": 12, "economy": 150},
            {"registration": "LY-DEF", "model": "A320", "economy": 180},
            {"registration": "FR-GHI", "model": "A321", "business": 20, "economy": 200},
            {"registration": "US-JKL", "model": "A321", "economy": 220},
            {"registration": "DE-MNO", "model": "A330", "business": 30, "economy": 220},
            {"registration": "EC-PQR", "model": "A330", "economy": 250},
            {"registration": "LY-STU", "model": "A350", "business": 40, "economy": 260},
            {"registration": "US-VWX", "model": "A350", "economy": 300},
            {"registration": "FR-YZA", "model": "B737", "business": 12, "economy": 159},
            {"registration": "DE-BCD", "model": "B737", "economy": 189},
            {"registration": "EC-EFG", "model": "B777", "business": 20, "economy": 200},
            {"registration": "LY-HIJ", "model": "B777", "economy": 220},
            {"registration": "US-KLM", "model": "B787", "business": 30, "economy": 210},
            {"registration": "FR-NOP", "model": "B787", "economy": 240},
            {"registration": "US-ZAB", "model": "B777", "economy": 220},
            {"registration": "FR-CDE", "model": "B787", "business": 30, "economy": 210},
            {"registration": "DE-FGH", "model": "B787", "economy": 240},
            {"registration": "EC-IJK", "model": "A320", "business": 12, "economy": 150},
            {"registration": "LY-MNO", "model": "A320", "economy": 180},
            {"registration": "FR-PQR", "model": "A321", "business": 20, "economy": 200},
            {"registration": "US-STU", "model": "A321", "economy": 220},
            {"registration": "DE-VWX", "model": "A330", "business": 30, "economy": 220},
            {"registration": "EC-YZA", "model": "A330", "economy": 250},
            {"registration": "LY-BCD", "model": "A350", "business": 40, "economy": 260},
            {"registration": "US-EFG", "model": "A350", "economy": 300},
            {"registration": "FR-HIJ", "model": "B737", "business": 12, "economy": 159},
            {"registration": "DE-KLM", "model": "B737", "economy": 189},
            {"registration": "EC-NOP", "model": "B777", "business": 20, "economy": 200},
            {"registration": "LY-QRS", "model": "B777", "economy": 220},
            {"registration": "US-TUV", "model": "B787", "business": 30, "economy": 210},
            {"registration": "FR-WXY", "model": "B787", "economy": 240},
            {"registration": "US-IJK", "model": "B777", "economy": 220},
            {"registration": "FR-MNO", "model": "B787", "business": 30, "economy": 210},
            {"registration": "DE-PQR", "model": "B787", "economy": 240}
        ]

prices = [
            {"model": "A320", "business": 0, "economy": 180, "crew": False, "price": 60000},  
            {"model": "A320", "business": 0, "economy": 180, "crew": True, "price": 80000},   
            {"model": "A320", "business": 12, "economy": 150, "crew": False, "price": 65000}, 
            {"model": "A320", "business": 12, "economy": 150, "crew": True, "price": 85000},  
            {"model": "A321", "business": 0, "economy": 220, "crew": False, "price": 70000},  
            {"model": "A321", "business": 0, "economy": 220, "crew": True, "price": 90000},   
            {"model": "A321", "business": 20, "economy": 200, "crew": False, "price": 75000}, 
            {"model": "A321", "business": 20, "economy": 200, "crew": True, "price": 95000},  
            {"model": "A330", "business": 0, "economy": 250, "crew": False, "price": 80000},  
            {"model": "A330", "business": 0, "economy": 250, "crew": True, "price": 100000},   
            {"model": "A330", "business": 30, "economy": 220, "crew": False, "price": 85000}, 
            {"model": "A330", "business": 30, "economy": 220, "crew": True, "price": 105000},  
            {"model": "A350", "business": 0, "economy": 300, "crew": False, "price": 90000},  
            {"model": "A350", "business": 0, "economy": 300, "crew": True, "price": 110000},   
            {"model": "A350", "business": 40, "economy": 260, "crew": False, "price": 95000}, 
            {"model": "A350", "business": 40, "economy": 260, "crew": True, "price": 115000},  
            {"model": "B737", "business": 0, "economy": 189, "crew": False, "price": 6200},  
            {"model": "B737", "business": 0, "economy": 189, "crew": True, "price": 8200},   
            {"model": "B737", "business": 12, "economy": 159, "crew": False, "price": 6700}, 
            {"model": "B737", "business": 12, "economy": 159, "crew": True, "price": 8700},  
            {"model": "B777", "business": 0, "economy": 220, "crew": False, "price": 75000},  
            {"model": "B777", "business": 0, "economy": 220, "crew": True, "price": 95000},   
            {"model": "B777", "business": 20, "economy": 200, "crew": False, "price": 80000}, 
            {"model": "B777", "business": 20, "economy": 200, "crew": True, "price": 100000},  
            {"model": "B787", "business": 0, "economy": 240, "crew": False, "price": 85000},  
            {"model": "B787", "business": 0, "economy": 240, "crew": True, "price": 105000},   
            {"model": "B787", "business": 30, "economy": 210, "crew": False, "price": 90000}, 
            {"model": "B787", "business": 30, "economy": 210, "crew": True, "price": 110000},  
         ]


countries = [
                "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
                "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
                "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon",
                "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba",
                "Cyprus", "Czech Republic", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor",
                "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
                "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
                "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", 
                "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
                "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
                "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
                "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan",
                "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
                "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
                "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", 
                "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania",
                "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
                "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]


def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users") # name of our command
    @click.argument("count") # argument of out command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass

    @app.cli.command("insert-fleet")
    def insert_fleet():
        print("Creating models")
        for model in models:
            model_table = Models()
            model_table.model_name = model
            db.session.add(model_table)
            db.session.commit()
            print(f"Model {model} created")
        
        print("Creating configurations")

        for configuration in configurations:
            config_table = Configurations()
            model = Models.query.filter_by(model_name=configuration["model"]).first()
            config_table.model_id = model.id
            if "business" in configuration:
                config_table.business = configuration["business"]
            config_table.economy = configuration["economy"]
            db.session.add(config_table)
            db.session.commit()
            print("Configuration created for model {}".format(configuration['model']))
        
        print("Creating Fleet")

        for plane in fleet:
            aeroplane = Fleet()
            model = Models.query.filter_by(model_name=plane["model"]).first()
            aeroplane.model_id = model.id
            configuration = Configurations.query.filter_by(
                                                            model_id=model.id,
                                                            business=plane.get("business", 0),
                                                            economy=plane.get("economy")
                                                          ).first()
            aeroplane.configuration_id = configuration.id
            aeroplane.registration=plane["registration"]
            db.session.add(aeroplane)
            db.session.commit()
            print("Airplane {} added to the fleet".format(plane["model"]))
    
    @app.cli.command("insert-plane-prices")
    def insert_plane_prices():
        print("Creating prices")
        for price in prices:
            price_table=Prices()
            model = Models.query.filter_by(model_name=price["model"]).first()
            price_table.model_id = model.id
            configuration = Configurations.query.filter_by(
                                                            model_id=model.id,
                                                            business=price.get("business", 0),
                                                            economy=price.get("economy")
                                                          ).first()
            price_table.configuration_id=configuration.id
            price_table.crew = price["crew"]
            price_table.price = price["price"]
            db.session.add(price_table)
            db.session.commit()
            print("Airplane {} costs {}€ per day".format(price["model"], price["price"]))
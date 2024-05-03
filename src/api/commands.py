
import click, random
from api.models import (db, Models, Configurations, Fleet, Prices, Projects, Assignations, Budgets, Roles, Countries,
                    Nationalities, States, Employees, Airports, Inflight, Duties, Flights, Hotels, Rosters, Salary_Prices,
                    Bank_Details, Payslips, Documents, Visibility, Departments)
from datetime import datetime, timedelta

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

roles = ["Manager", "Crew Control", "Captain", "First Officer", "Senior", "Cabin Crew"]

departments = ["Management", "Crew Planning", "Inflight"]

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

nationalities = [
                    "Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Antiguans", "Argentinean", "Armenian", "Australian", "Austrian", "Azerbaijani",
                    "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Barbudans", "Batswana", "Belarusian", "Belgian", "Belizean", "Beninese", "Bhutanese", "Bolivian",
                    "Bosnian", "Brazilian", "British", "Bruneian", "Bulgarian", "Burkinabe", "Burmese", "Burundian", "Cambodian", "Cameroonian", "Canadian", "Cape Verdean",
                    "Central African", "Chadian", "Chilean", "Chinese", "Colombian", "Comoran", "Congolese", "Costa Rican", "Croatian", "Cuban", "Cypriot", "Czech",
                    "Danish", "Djibouti", "Dominican", "Dutch", "East Timorese", "Ecuadorean", "Egyptian", "Emirian", "Equatorial Guinean", "Eritrean", "Estonian",
                    "Ethiopian", "Fijian", "Filipino", "Finnish", "French", "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Greek", "Grenadian", "Guatemalan", 
                    "Guinea-Bissauan", "Guinean", "Guyanese", "Haitian", "Herzegovinian", "Honduran", "Hungarian", "I-Kiribati", "Icelander", "Indian", "Indonesian", 
                    "Iranian", "Iraqi", "Irish", "Israeli", "Italian", "Ivorian", "Jamaican", "Japanese", "Jordanian", "Kazakhstani", "Kenyan", "Kittian and Nevisian",
                    "Kuwaiti", "Kyrgyz", "Laotian", "Latvian", "Lebanese", "Liberian", "Libyan", "Liechtensteiner", "Lithuanian", "Luxembourger", "Macedonian", "Malagasy",
                    "Malawian", "Malaysian", "Maldivan", "Malian", "Maltese", "Marshallese", "Mauritanian", "Mauritian", "Mexican", "Micronesian", "Moldovan", "Monacan", 
                    "Mongolian", "Moroccan", "Mosotho", "Motswana", "Mozambican", "Namibian", "Nauruan", "Nepalese", "New Zealander", "Nicaraguan", "Nigerian", "Nigerien", 
                    "North Korean", "Northern Irish", "Norwegian", "Omani", "Pakistani", "Palauan", "Panamanian", "Papua New Guinean", "Paraguayan", "Peruvian", "Polish",
                    "Portuguese", "Qatari", "Romanian", "Russian", "Rwandan", "Saint Lucian", "Salvadoran", "Samoan", "San Marinese", "Sao Tomean", "Saudi", "Scottish",
                    "Senegalese", "Serbian", "Seychellois", "Sierra Leonean", "Singaporean", "Slovakian", "Slovenian", "Solomon Islander", "Somali", "South African",
                    "South Korean", "Spanish", "Sri Lankan", "Sudanese", "Surinamer", "Swazi", "Swedish", "Swiss", "Syrian", "Taiwanese", "Tajik", "Tanzanian", "Thai",
                    "Togolese", "Tongan", "Trinidadian or Tobagonian", "Tunisian", "Turkish", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbekistani", "Venezuelan",
                    "Vietnamese", "Welsh", "Yemenite", "Zambian", "Zimbabwean"
]

states = [
    {"country": "United States", "state": "Alabama"},
    {"country": "United States", "state": "Alaska"},
    {"country": "United States", "state": "Arizona"},
    {"country": "United States", "state": "Arkansas"},
    {"country": "United States", "state": "California"},
    {"country": "United States", "state": "Colorado"},
    {"country": "United States", "state": "Connecticut"},
    {"country": "United States", "state": "Delaware"},
    {"country": "United States", "state": "Florida"},
    {"country": "United States", "state": "Georgia"},
    {"country": "United States", "state": "Hawaii"},
    {"country": "United States", "state": "Idaho"},
    {"country": "United States", "state": "Illinois"},
    {"country": "United States", "state": "Indiana"},
    {"country": "United States", "state": "Iowa"},
    {"country": "United States", "state": "Kansas"},
    {"country": "United States", "state": "Kentucky"},
    {"country": "United States", "state": "Louisiana"},
    {"country": "United States", "state": "Maine"},
    {"country": "United States", "state": "Maryland"},
    {"country": "United States", "state": "Massachusetts"},
    {"country": "United States", "state": "Michigan"},
    {"country": "United States", "state": "Minnesota"},
    {"country": "United States", "state": "Mississippi"},
    {"country": "United States", "state": "Missouri"},
    {"country": "United States", "state": "Montana"},
    {"country": "United States", "state": "Nebraska"},
    {"country": "United States", "state": "Nevada"},
    {"country": "United States", "state": "New Hampshire"},
    {"country": "United States", "state": "New Jersey"},
    {"country": "United States", "state": "New Mexico"},
    {"country": "United States", "state": "New York"},
    {"country": "United States", "state": "North Carolina"},
    {"country": "United States", "state": "North Dakota"},
    {"country": "United States", "state": "Ohio"},
    {"country": "United States", "state": "Oklahoma"},
    {"country": "United States", "state": "Oregon"},
    {"country": "United States", "state": "Pennsylvania"},
    {"country": "United States", "state": "Rhode Island"},
    {"country": "United States", "state": "South Carolina"},
    {"country": "United States", "state": "South Dakota"},
    {"country": "United States", "state": "Tennessee"},
    {"country": "United States", "state": "Texas"},
    {"country": "United States", "state": "Utah"},
    {"country": "United States", "state": "Vermont"},
    {"country": "United States", "state": "Virginia"},
    {"country": "United States", "state": "Washington"},
    {"country": "United States", "state": "West Virginia"},
    {"country": "United States", "state": "Wisconsin"},
    {"country": "United States", "state": "Wyoming"},
    {"country": "Spain", "state": "Andalucía"},
    {"country": "Spain", "state": "Aragón"},
    {"country": "Spain", "state": "Principado de Asturias"},
    {"country": "Spain", "state": "Islas Baleares"},
    {"country": "Spain", "state": "País Vasco"},
    {"country": "Spain", "state": "Islas Canarias"},
    {"country": "Spain", "state": "Cantabria"},
    {"country": "Spain", "state": "Castilla y León"},
    {"country": "Spain", "state": "Castilla-La Mancha"},
    {"country": "Spain", "state": "Cataluña"},
    {"country": "Spain", "state": "Extremadura"},
    {"country": "Spain", "state": "Galicia"},
    {"country": "Spain", "state": "La Rioja"},
    {"country": "Spain", "state": "Comunidad de Madrid"},
    {"country": "Spain", "state": "Región de Murcia"},
    {"country": "Spain", "state": "Comunidad Foral de Navarra"},
    {"country": "Spain", "state": "Comunitat Valenciana"},
    {"country": "Spain", "state": "Ceuta"},
    {"country": "Spain", "state": "Melilla"},
    {"country": "Germany", "state": "Baden-Württemberg"},
    {"country": "Germany", "state": "Bayern"},
    {"country": "Germany", "state": "Berlin"},
    {"country": "Germany", "state": "Brandenburg"},
    {"country": "Germany", "state": "Bremen"},
    {"country": "Germany", "state": "Hamburg"},
    {"country": "Germany", "state": "Hessen"},
    {"country": "Germany", "state": "Mecklenburg-Vorpommern"},
    {"country": "Germany", "state": "Niedersachsen"},
    {"country": "Germany", "state": "Nordrhein-Westfalen"},
    {"country": "Germany", "state": "Rheinland-Pfalz"},
    {"country": "Germany", "state": "Saarland"},
    {"country": "Germany", "state": "Sachsen"},
    {"country": "Germany", "state": "Sachsen-Anhalt"},
    {"country": "Germany", "state": "Schleswig-Holstein"},
    {"country": "Germany", "state": "Thüringen"},
    {"country": "France", "state": "Auvergne-Rhône-Alpes"},
    {"country": "France", "state": "Bourgogne-Franche-Comté"},
    {"country": "France", "state": "Bretagne"},
    {"country": "France", "state": "Centre-Val de Loire"},
    {"country": "France", "state": "Corse"},
    {"country": "France", "state": "Grand Est"},
    {"country": "France", "state": "Hauts-de-France"},
    {"country": "France", "state": "Île-de-France"},
    {"country": "France", "state": "Normandie"},
    {"country": "France", "state": "Nouvelle-Aquitaine"},
    {"country": "France", "state": "Occitanie"},
    {"country": "France", "state": "Pays de la Loire"},
    {"country": "France", "state": "Provence-Alpes-Côte d'Azur"},
    {"country": "Portugal", "state": "Norte"},
    {"country": "Portugal", "state": "Centro"},
    {"country": "Portugal", "state": "Lisboa e Vale do Tejo"},
    {"country": "Portugal", "state": "Alentejo"},
    {"country": "Portugal", "state": "Algarve"},
    {"country": "Portugal", "state": "Região Autónoma dos Açores"},
    {"country": "Portugal", "state": "Região Autónoma da Madeira"},
    {"country": "Italy", "state": "Abruzzo"},
    {"country": "Italy", "state": "Basilicata"},
    {"country": "Italy", "state": "Calabria"},
    {"country": "Italy", "state": "Campania"},
    {"country": "Italy", "state": "Emilia-Romagna"},
    {"country": "Italy", "state": "Friuli-Venezia Giulia"},
    {"country": "Italy", "state": "Lazio"},
    {"country": "Italy", "state": "Liguria"},
    {"country": "Italy", "state": "Lombardia"},
    {"country": "Italy", "state": "Marche"},
    {"country": "Italy", "state": "Molise"},
    {"country": "Italy", "state": "Piemonte"},
    {"country": "Italy", "state": "Puglia"},
    {"country": "Italy", "state": "Sardegna"},
    {"country": "Italy", "state": "Sicilia"},
    {"country": "Italy", "state": "Toscana"},
    {"country": "Italy", "state": "Trentino-Alto Adige"},
    {"country": "Italy", "state": "Umbria"},
    {"country": "Italy", "state": "Valle d'Aosta"},
    {"country": "Italy", "state": "Veneto"},
    {"country": "United Kingdom", "state": "England"},
    {"country": "United Kingdom", "state": "Scotland"},
    {"country": "United Kingdom", "state": "Wales"},
    {"country": "United Kingdom", "state": "Northern Ireland"},
    {"country": "Brazil", "state": "Acre"},
    {"country": "Brazil", "state": "Alagoas"},
    {"country": "Brazil", "state": "Amapá"},
    {"country": "Brazil", "state": "Amazonas"},
    {"country": "Brazil", "state": "Bahia"},
    {"country": "Brazil", "state": "Ceará"},
    {"country": "Brazil", "state": "Espírito Santo"},
    {"country": "Brazil", "state": "Goiás"},
    {"country": "Brazil", "state": "Maranhão"},
    {"country": "Brazil", "state": "Mato Grosso"},
    {"country": "Brazil", "state": "Mato Grosso do Sul"},
    {"country": "Brazil", "state": "Minas Gerais"},
    {"country": "Brazil", "state": "Pará"},
    {"country": "Brazil", "state": "Paraíba"},
    {"country": "Brazil", "state": "Paraná"},
    {"country": "Brazil", "state": "Pernambuco"},
    {"country": "Brazil", "state": "Piauí"},
    {"country": "Brazil", "state": "Rio de Janeiro"},
    {"country": "Brazil", "state": "Rio Grande do Norte"},
    {"country": "Brazil", "state": "Rio Grande do Sul"},
    {"country": "Brazil", "state": "Rondônia"},
    {"country": "Brazil", "state": "Roraima"},
    {"country": "Brazil", "state": "Santa Catarina"},
    {"country": "Brazil", "state": "São Paulo"},
    {"country": "Brazil", "state": "Sergipe"},
    {"country": "Brazil", "state": "Tocantins"},
    {"country": "Brazil", "state": "Distrito Federal"},
    {"country": "India", "state": "Andhra Pradesh"},
    {"country": "India", "state": "Arunachal Pradesh"},
    {"country": "India", "state": "Assam"},
    {"country": "India", "state": "Bihar"},
    {"country": "India", "state": "Chhattisgarh"},
    {"country": "India", "state": "Goa"},
    {"country": "India", "state": "Gujarat"},
    {"country": "India", "state": "Haryana"},
    {"country": "India", "state": "Himachal Pradesh"},
    {"country": "India", "state": "Jharkhand"},
    {"country": "India", "state": "Karnataka"},
    {"country": "India", "state": "Kerala"},
    {"country": "India", "state": "Madhya Pradesh"},
    {"country": "India", "state": "Maharashtra"},
    {"country": "India", "state": "Manipur"},
    {"country": "India", "state": "Meghalaya"},
    {"country": "India", "state": "Mizoram"},
    {"country": "India", "state": "Nagaland"},
    {"country": "India", "state": "Odisha"},
    {"country": "India", "state": "Punjab"},
    {"country": "India", "state": "Rajasthan"},
    {"country": "India", "state": "Sikkim"},
    {"country": "India", "state": "Tamil Nadu"},
    {"country": "India", "state": "Telangana"},
    {"country": "India", "state": "Tripura"},
    {"country": "India", "state": "Uttar Pradesh"},
    {"country": "India", "state": "Uttarakhand"},
    {"country": "India", "state": "West Bengal"},
    {"country": "India", "state": "Andaman and Nicobar Islands"},
    {"country": "India", "state": "Chandigarh"},
    {"country": "India", "state": "Dadra and Nagar Haveli"},
    {"country": "India", "state": "Daman and Diu"},
    {"country": "India", "state": "Lakshadweep"},
    {"country": "India", "state": "Delhi"},
    {"country": "India", "state": "Puducherry"},
    {"country": "Canada", "state": "Alberta"},
    {"country": "Canada", "state": "British Columbia"},
    {"country": "Canada", "state": "Manitoba"},
    {"country": "Canada", "state": "New Brunswick"},
    {"country": "Canada", "state": "Newfoundland and Labrador"},
    {"country": "Canada", "state": "Nova Scotia"},
    {"country": "Canada", "state": "Ontario"},
    {"country": "Canada", "state": "Prince Edward Island"},
    {"country": "Canada", "state": "Quebec"},
    {"country": "Canada", "state": "Saskatchewan"},
    {"country": "Canada", "state": "Northwest Territories"},
    {"country": "Canada", "state": "Nunavut"},
    {"country": "Canada", "state": "Yukon"},
    {"country": "Mexico", "state": "Aguascalientes"},
    {"country": "Mexico", "state": "Baja California"},
    {"country": "Mexico", "state": "Baja California Sur"},
    {"country": "Mexico", "state": "Campeche"},
    {"country": "Mexico", "state": "Chiapas"},
    {"country": "Mexico", "state": "Chihuahua"},
    {"country": "Mexico", "state": "Coahuila"},
    {"country": "Mexico", "state": "Colima"},
    {"country": "Mexico", "state": "Durango"},
    {"country": "Mexico", "state": "Guanajuato"},
    {"country": "Mexico", "state": "Guerrero"},
    {"country": "Mexico", "state": "Hidalgo"},
    {"country": "Mexico", "state": "Jalisco"},
    {"country": "Mexico", "state": "México"},
    {"country": "Mexico", "state": "Michoacán"},
    {"country": "Mexico", "state": "Morelos"},
    {"country": "Mexico", "state": "Nayarit"},
    {"country": "Mexico", "state": "Nuevo León"},
    {"country": "Mexico", "state": "Oaxaca"},
    {"country": "Mexico", "state": "Puebla"},
    {"country": "Mexico", "state": "Querétaro"},
    {"country": "Mexico", "state": "Quintana Roo"},
    {"country": "Mexico", "state": "San Luis Potosí"},
    {"country": "Mexico", "state": "Sinaloa"},
    {"country": "Mexico", "state": "Sonora"},
    {"country": "Mexico", "state": "Tabasco"},
    {"country": "Mexico", "state": "Tamaulipas"},
    {"country": "Mexico", "state": "Tlaxcala"},
    {"country": "Mexico", "state": "Veracruz"},
    {"country": "Mexico", "state": "Yucatán"},
    {"country": "Mexico", "state": "Zacatecas"},
    {"country": "Mexico", "state": "Ciudad de México"},
    {"country": "Colombia", "state": "Amazonas"},
    {"country": "Colombia", "state": "Antioquia"},
    {"country": "Colombia", "state": "Arauca"},
    {"country": "Colombia", "state": "Atlántico"},
    {"country": "Colombia", "state": "Bolívar"},
    {"country": "Colombia", "state": "Boyacá"},
    {"country": "Colombia", "state": "Caldas"},
    {"country": "Colombia", "state": "Caquetá"},
    {"country": "Colombia", "state": "Casanare"},
    {"country": "Colombia", "state": "Cauca"},
    {"country": "Colombia", "state": "Cesar"},
    {"country": "Colombia", "state": "Chocó"},
    {"country": "Colombia", "state": "Córdoba"},
    {"country": "Colombia", "state": "Cundinamarca"},
    {"country": "Colombia", "state": "Guainía"},
    {"country": "Colombia", "state": "Guaviare"},
    {"country": "Colombia", "state": "Huila"},
    {"country": "Colombia", "state": "La Guajira"},
    {"country": "Colombia", "state": "Magdalena"},
    {"country": "Colombia", "state": "Meta"},
    {"country": "Colombia", "state": "Nariño"},
    {"country": "Colombia", "state": "Norte de Santander"},
    {"country": "Colombia", "state": "Putumayo"},
    {"country": "Colombia", "state": "Quindío"},
    {"country": "Colombia", "state": "Risaralda"},
    {"country": "Colombia", "state": "San Andrés y Providencia"},
    {"country": "Colombia", "state": "Santander"},
    {"country": "Colombia", "state": "Sucre"},
    {"country": "Colombia", "state": "Tolima"},
    {"country": "Colombia", "state": "Valle del Cauca"},
    {"country": "Colombia", "state": "Vaupés"},
    {"country": "Colombia", "state": "Vichada"},
    {"country": "China", "state": "Anhui"},
    {"country": "China", "state": "Beijing"},
    {"country": "China", "state": "Chongqing"},
    {"country": "China", "state": "Fujian"},
    {"country": "China", "state": "Gansu"},
    {"country": "China", "state": "Guangdong"},
    {"country": "China", "state": "Guangxi"},
    {"country": "China", "state": "Guizhou"},
    {"country": "China", "state": "Hainan"},
    {"country": "China", "state": "Hebei"},
    {"country": "China", "state": "Heilongjiang"},
    {"country": "China", "state": "Henan"},
    {"country": "China", "state": "Hubei"},
    {"country": "China", "state": "Hunan"},
    {"country": "China", "state": "Inner Mongolia"},
    {"country": "China", "state": "Jiangsu"},
    {"country": "China", "state": "Jiangxi"},
    {"country": "China", "state": "Jilin"},
    {"country": "China", "state": "Liaoning"},
    {"country": "China", "state": "Ningxia"},
    {"country": "China", "state": "Qinghai"},
    {"country": "China", "state": "Shaanxi"},
    {"country": "China", "state": "Shandong"},
    {"country": "China", "state": "Shanghai"},
    {"country": "China", "state": "Shanxi"},
    {"country": "China", "state": "Sichuan"},
    {"country": "China", "state": "Tianjin"},
    {"country": "China", "state": "Tibet"},
    {"country": "China", "state": "Xinjiang"},
    {"country": "China", "state": "Yunnan"},
    {"country": "China", "state": "Zhejiang"},
    {"country": "China", "state": "Hong Kong"},
    {"country": "China", "state": "Macao"},
    {"country": "Russia", "state": "Republic of Adygea"},
    {"country": "Russia", "state": "Altai Krai"},
    {"country": "Russia", "state": "Altai Republic"},
    {"country": "Russia", "state": "Amur Oblast"},
    {"country": "Russia", "state": "Arkhangelsk Oblast"},
    {"country": "Russia", "state": "Astrakhan Oblast"},
    {"country": "Russia", "state": "Republic of Bashkortostan"},
    {"country": "Russia", "state": "Belgorod Oblast"},
    {"country": "Russia", "state": "Bryansk Oblast"},
    {"country": "Russia", "state": "Republic of Buryatia"},
    {"country": "Russia", "state": "Chechen Republic"},
    {"country": "Russia", "state": "Chelyabinsk Oblast"},
    {"country": "Russia", "state": "Chukotka Autonomous Okrug"},
    {"country": "Russia", "state": "Chuvash Republic"},
    {"country": "Russia", "state": "Republic of Crimea"},
    {"country": "Russia", "state": "Republic of Dagestan"},
    {"country": "Russia", "state": "Jewish Autonomous Oblast"},
    {"country": "Russia", "state": "Ivanovo Oblast"},
    {"country": "Russia", "state": "Republic of Ingushetia"},
    {"country": "Russia", "state": "Irkutsk Oblast"},
    {"country": "Russia", "state": "Kabardino-Balkar Republic"},
    {"country": "Russia", "state": "Kaliningrad Oblast"},
    {"country": "Russia", "state": "Kaluga Oblast"},
    {"country": "Russia", "state": "Kamchatka Krai"},
    {"country": "Russia", "state": "Karachay-Cherkess Republic"},
    {"country": "Russia", "state": "Republic of Karelia"},
    {"country": "Russia", "state": "Kemerovo Oblast"},
    {"country": "Russia", "state": "Khabarovsk Krai"},
    {"country": "Russia", "state": "Republic of Khakassia"},
    {"country": "Russia", "state": "Khanty-Mansi Autonomous Okrug"},
    {"country": "Russia", "state": "Kirov Oblast"},
    {"country": "Russia", "state": "Komi Republic"},
    {"country": "Russia", "state": "Kostroma Oblast"},
    {"country": "Russia", "state": "Krasnodar Krai"},
    {"country": "Russia", "state": "Krasnoyarsk Krai"},
    {"country": "Russia", "state": "Kurgan Oblast"},
    {"country": "Russia", "state": "Kursk Oblast"},
    {"country": "Russia", "state": "Leningrad Oblast"},
    {"country": "Russia", "state": "Lipetsk Oblast"},
    {"country": "Russia", "state": "Magadan Oblast"},
    {"country": "Russia", "state": "Mari El Republic"},
    {"country": "Russia", "state": "Republic of Mordovia"},
    {"country": "Russia", "state": "Moscow"},
    {"country": "Russia", "state": "Moscow Oblast"},
    {"country": "Russia", "state": "Murmansk Oblast"},
    {"country": "Russia", "state": "Nenets Autonomous Okrug"},
    {"country": "Russia", "state": "Nizhny Novgorod Oblast"},
    {"country": "Russia", "state": "North Ossetia-Alania"},
    {"country": "Russia", "state": "Novgorod Oblast"},
    {"country": "Russia", "state": "Novosibirsk Oblast"},
    {"country": "Russia", "state": "Omsk Oblast"},
    {"country": "Russia", "state": "Orenburg Oblast"},
    {"country": "Russia", "state": "Oryol Oblast"},
    {"country": "Russia", "state": "Penza Oblast"},
    {"country": "Russia", "state": "Perm Krai"},
    {"country": "Russia", "state": "Primorsky Krai"},
    {"country": "Russia", "state": "Pskov Oblast"},
    {"country": "Russia", "state": "Rostov Oblast"},
    {"country": "Russia", "state": "Ryazan Oblast"},
    {"country": "Russia", "state": "Saint Petersburg"},
    {"country": "Russia", "state": "Sakha (Yakutia) Republic"},
    {"country": "Russia", "state": "Sakhalin Oblast"},
    {"country": "Russia", "state": "Samara Oblast"},
    {"country": "Russia", "state": "Saratov Oblast"},
    {"country": "Russia", "state": "Republic of Tatarstan"},
    {"country": "Russia", "state": "Tomsk Oblast"},
    {"country": "Russia", "state": "Tula Oblast"},
    {"country": "Russia", "state": "Tuva Republic"},
    {"country": "Russia", "state": "Tver Oblast"},
    {"country": "Russia", "state": "Tyumen Oblast"},
    {"country": "Russia", "state": "Udmurt Republic"},
    {"country": "Russia", "state": "Ulyanovsk Oblast"},
    {"country": "Russia", "state": "Vladimir Oblast"},
    {"country": "Russia", "state": "Volgograd Oblast"},
    {"country": "Russia", "state": "Vologda Oblast"},
    {"country": "Russia", "state": "Voronezh Oblast"},
    {"country": "Russia", "state": "Yamalo-Nenets Autonomous Okrug"},
    {"country": "Russia", "state": "Yaroslavl Oblast"},
    {"country": "Russia", "state": "Zabaykalsky Krai"},
    {"country": "Poland", "state": "Greater Poland"},
    {"country": "Poland", "state": "Kuyavian-Pomeranian"},
    {"country": "Poland", "state": "Lesser Poland"},
    {"country": "Poland", "state": "Łódź"},
    {"country": "Poland", "state": "Lower Silesian"},
    {"country": "Poland", "state": "Lublin"},
    {"country": "Poland", "state": "Lubusz"},
    {"country": "Poland", "state": "Masovian"},
    {"country": "Poland", "state": "Opole"},
    {"country": "Poland", "state": "Podkarpackie"},
    {"country": "Poland", "state": "Podlaskie"},
    {"country": "Poland", "state": "Pomeranian"},
    {"country": "Poland", "state": "Silesian"},
    {"country": "Poland", "state": "Świętokrzyskie"},
    {"country": "Poland", "state": "Warmian-Masurian"},
    {"country": "Poland", "state": "West Pomeranian"},
    {"country": "Argentina", "state": "Buenos Aires"},
    {"country": "Argentina", "state": "Catamarca"},
    {"country": "Argentina", "state": "Chaco"},
    {"country": "Argentina", "state": "Chubut"},
    {"country": "Argentina", "state": "Córdoba"},
    {"country": "Argentina", "state": "Corrientes"},
    {"country": "Argentina", "state": "Entre Ríos"},
    {"country": "Argentina", "state": "Formosa"},
    {"country": "Argentina", "state": "Jujuy"},
    {"country": "Argentina", "state": "La Pampa"},
    {"country": "Argentina", "state": "La Rioja"},
    {"country": "Argentina", "state": "Mendoza"},
    {"country": "Argentina", "state": "Misiones"},
    {"country": "Argentina", "state": "Neuquén"},
    {"country": "Argentina", "state": "Río Negro"},
    {"country": "Argentina", "state": "Salta"},
    {"country": "Argentina", "state": "San Juan"},
    {"country": "Argentina", "state": "San Luis"},
    {"country": "Argentina", "state": "Santa Cruz"},
    {"country": "Argentina", "state": "Santa Fe"},
    {"country": "Argentina", "state": "Santiago del Estero"},
    {"country": "Argentina", "state": "Tierra del Fuego, Antártida e Islas del Atlántico Sur"},
    {"country": "Argentina", "state": "Tucumán"}
]

airports = [
    {'IATA_code': 'AGP', 'ICAO_code': 'LEMG', 'airport_name': 'Málaga Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'ALC', 'ICAO_code': 'LEAL', 'airport_name': 'Alicante-Elche Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'BCN', 'ICAO_code': 'LEBL', 'airport_name': 'Barcelona-El Prat Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'BIO', 'ICAO_code': 'LEBB', 'airport_name': 'Bilbao Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'FUE', 'ICAO_code': 'GCFV', 'airport_name': 'Fuerteventura Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'GRO', 'ICAO_code': 'LEGE', 'airport_name': 'Girona-Costa Brava Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'GRX', 'ICAO_code': 'LEGR', 'airport_name': 'Federico García Lorca Granada-Jaén Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'IBZ', 'ICAO_code': 'LEIB', 'airport_name': 'Ibiza Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'LEI', 'ICAO_code': 'LEAM', 'airport_name': 'Almería Airport', 'country': 'Spain', 'category': 'B'},
    {'IATA_code': 'LPA', 'ICAO_code': 'GCLP', 'airport_name': 'Gran Canaria Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'MAD', 'ICAO_code': 'LEMD', 'airport_name': 'Adolfo Suárez Madrid-Barajas Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'MLN', 'ICAO_code': 'GEML', 'airport_name': 'Melilla Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'PMI', 'ICAO_code': 'LEPA', 'airport_name': 'Palma de Mallorca Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'SCQ', 'ICAO_code': 'LEST', 'airport_name': 'Santiago de Compostela Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'SPC', 'ICAO_code': 'GCLA', 'airport_name': 'La Palma Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'SVQ', 'ICAO_code': 'LEZL', 'airport_name': 'Seville Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'TFN', 'ICAO_code': 'GCXO', 'airport_name': 'Tenerife North Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'TFS', 'ICAO_code': 'GCTS', 'airport_name': 'Tenerife South Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'VLC', 'ICAO_code': 'LEVC', 'airport_name': 'Valencia Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'VLL', 'ICAO_code': 'LEVD', 'airport_name': 'Valladolid Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'XRY', 'ICAO_code': 'LEJR', 'airport_name': 'Jerez Airport', 'country': 'Spain', 'category': 'C'},
    {'IATA_code': 'ZAZ', 'ICAO_code': 'LEZG', 'airport_name': 'Zaragoza Airport', 'country': 'Spain', 'category': 'A'},
    {'IATA_code': 'LIS', 'ICAO_code': 'LPPT', 'airport_name': 'Lisbon Airport', 'country': 'Portugal', 'category': 'A'},
    {'IATA_code': 'OPO', 'ICAO_code': 'LPPR', 'airport_name': 'Porto Airport', 'country': 'Portugal', 'category': 'A'},
    {'IATA_code': 'FAO', 'ICAO_code': 'LPFR', 'airport_name': 'Faro Airport', 'country': 'Portugal', 'category': 'A'},
    {'IATA_code': 'FNC', 'ICAO_code': 'LPMA', 'airport_name': 'Madeira Airport', 'country': 'Portugal', 'category': 'A'},
    {'IATA_code': 'PDL', 'ICAO_code': 'LPPD', 'airport_name': 'João Paulo II Airport', 'country': 'Portugal', 'category': 'A'},
    {'IATA_code': 'CDG', 'ICAO_code': 'LFPG', 'airport_name': 'Charles de Gaulle Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'ORY', 'ICAO_code': 'LFPO', 'airport_name': 'Orly Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'NCE', 'ICAO_code': 'LFMN', 'airport_name': 'Nice Côte d\'Azur Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'MRS', 'ICAO_code': 'LFML', 'airport_name': 'Marseille Provence Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'LYS', 'ICAO_code': 'LFLL', 'airport_name': 'Lyon-Saint Exupéry Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'BOD', 'ICAO_code': 'LFBD', 'airport_name': 'Bordeaux-Mérignac Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'TLS', 'ICAO_code': 'LFBO', 'airport_name': 'Toulouse-Blagnac Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'NTE', 'ICAO_code': 'LFRS', 'airport_name': 'Nantes Atlantique Airport', 'country': 'France', 'category': 'A'},
    {'IATA_code': 'LIL', 'ICAO_code': 'LFQQ', 'airport_name': 'Lille Airport', 'country': 'France', 'category': 'B'},
    {'IATA_code': 'MPL', 'ICAO_code': 'LFMT', 'airport_name': 'Montpellier Méditerranée Airport', 'country': 'France', 'category': 'B'},
    {'IATA_code': 'BIQ', 'ICAO_code': 'LFBZ', 'airport_name': 'Biarritz Airport', 'country': 'France', 'category': 'B'},
    {'IATA_code': 'PGF', 'ICAO_code': 'LFMP', 'airport_name': 'Perpignan-Rivesaltes Airport', 'country': 'France', 'category': 'B'},
    {'IATA_code': 'BES', 'ICAO_code': 'LFRB', 'airport_name': 'Brest Bretagne Airport', 'country': 'France', 'category': 'B'},
    {'IATA_code': 'CFE', 'ICAO_code': 'LFLC', 'airport_name': 'Clermont-Ferrand Auvergne Airport', 'country': 'France', 'category': 'B'},
    {'IATA_code': 'LDE', 'ICAO_code': 'LFBT', 'airport_name': 'Tarbes-Lourdes-Pyrénées Airport', 'country': 'France', 'category': 'B'},
    {'IATA_code': 'EGC', 'ICAO_code': 'LFBE', 'airport_name': 'Bergerac Dordogne Périgord Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'CFR', 'ICAO_code': 'LFRK', 'airport_name': 'Caen Carpiquet Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'LRH', 'ICAO_code': 'LFBH', 'airport_name': 'La Rochelle-Île de Ré Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'CMF', 'ICAO_code': 'LFLB', 'airport_name': 'Chambéry Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'DOL', 'ICAO_code': 'LFRG', 'airport_name': 'Deauville - Normandie Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'ETZ', 'ICAO_code': 'LFJL', 'airport_name': 'Metz-Nancy-Lorraine Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'PIS', 'ICAO_code': 'LFBI', 'airport_name': 'Poitiers-Biard Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'UIP', 'ICAO_code': 'LFHU', 'airport_name': 'Quimper-Cornouaille Airport', 'country': 'France', 'category': 'C'},
    {'IATA_code': 'AHO', 'ICAO_code': 'LIEA', 'airport_name': 'Alghero-Fertilia Airport', 'country': 'Italy', 'category': 'B'},
    {'IATA_code': 'BDS', 'ICAO_code': 'LIBR', 'airport_name': 'Brindisi Airport', 'country': 'Italy', 'category': 'C'},
    {'IATA_code': 'BGY', 'ICAO_code': 'LIME', 'airport_name': 'Milan Bergamo Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'BLQ', 'ICAO_code': 'LIPE', 'airport_name': 'Bologna Guglielmo Marconi Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'BRI', 'ICAO_code': 'LIBD', 'airport_name': 'Bari Karol Wojtyła Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'CAG', 'ICAO_code': 'LIEE', 'airport_name': 'Cagliari Elmas Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'CTA', 'ICAO_code': 'LICC', 'airport_name': 'Catania Fontanarossa Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'FCO', 'ICAO_code': 'LIRF', 'airport_name': 'Leonardo da Vinci-Fiumicino Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'FLR', 'ICAO_code': 'LIRQ', 'airport_name': 'Florence Airport', 'country': 'Italy', 'category': 'C'},
    {'IATA_code': 'GOA', 'ICAO_code': 'LIMJ', 'airport_name': 'Genoa Cristoforo Colombo Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'LIN', 'ICAO_code': 'LIML', 'airport_name': 'Milan Linate Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'MXP', 'ICAO_code': 'LIMC', 'airport_name': 'Milan Malpensa Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'NAP', 'ICAO_code': 'LIRN', 'airport_name': 'Naples International Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'OLB', 'ICAO_code': 'LIEO', 'airport_name': 'Olbia Costa Smeralda Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'PMO', 'ICAO_code': 'LICJ', 'airport_name': 'Palermo Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'PMF', 'ICAO_code': 'LIMP', 'airport_name': 'Parma Airport', 'country': 'Italy', 'category': 'B'},
    {'IATA_code': 'PSA', 'ICAO_code': 'LIRP', 'airport_name': 'Pisa International Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'PUY', 'ICAO_code': 'LDPL', 'airport_name': 'Pula Airport', 'country': 'Italy', 'category': 'B'},
    {'IATA_code': 'TRN', 'ICAO_code': 'LIMF', 'airport_name': 'Turin Airport', 'country': 'Italy', 'category': 'B'},
    {'IATA_code': 'TRS', 'ICAO_code': 'LIPQ', 'airport_name': 'Trieste-Friuli Venezia Giulia Airport', 'country': 'Italy', 'category': 'B'},
    {'IATA_code': 'TSF', 'ICAO_code': 'LIPH', 'airport_name': 'Treviso Airport', 'country': 'Italy', 'category': 'B'},
    {'IATA_code': 'VCE', 'ICAO_code': 'LIPZ', 'airport_name': 'Venice Marco Polo Airport', 'country': 'Italy', 'category': 'A'},
    {'IATA_code': 'VRN', 'ICAO_code': 'LIPX', 'airport_name': 'Verona Villafranca Airport', 'country': 'Italy', 'category': 'B'},
    {'IATA_code': 'ZIA', 'ICAO_code': 'LIBC', 'airport_name': 'Palermo Boccadifalco Airport', 'country': 'Italy', 'category': 'C'},
    {'IATA_code': 'BER', 'ICAO_code': 'EDDB', 'airport_name': 'Berlin Brandenburg Airport', 'country': 'Germany', 'category': 'A'},
    {'IATA_code': 'CGN', 'ICAO_code': 'EDDK', 'airport_name': 'Cologne Bonn Airport', 'country': 'Germany', 'category': 'A'},
    {'IATA_code': 'DUS', 'ICAO_code': 'EDDL', 'airport_name': 'Düsseldorf Airport', 'country': 'Germany', 'category': 'A'},
    {'IATA_code': 'FRA', 'ICAO_code': 'EDDF', 'airport_name': 'Frankfurt Airport', 'country': 'Germany', 'category': 'A'},
    {'IATA_code': 'HAM', 'ICAO_code': 'EDDH', 'airport_name': 'Hamburg Airport', 'country': 'Germany', 'category': 'A'},
    {'IATA_code': 'LEJ', 'ICAO_code': 'EDDP', 'airport_name': 'Leipzig/Halle Airport', 'country': 'Germany', 'category': 'B'},
    {'IATA_code': 'MUC', 'ICAO_code': 'EDDM', 'airport_name': 'Munich Airport', 'country': 'Germany', 'category': 'A'},
    {'IATA_code': 'STR', 'ICAO_code': 'EDDS', 'airport_name': 'Stuttgart Airport', 'country': 'Germany', 'category': 'A'},
    {'IATA_code': 'TXL', 'ICAO_code': 'EDDT', 'airport_name': 'Berlin Tegel Airport', 'country': 'Germany', 'category': 'B'},
    {'IATA_code': 'HHN', 'ICAO_code': 'EDFH', 'airport_name': 'Frankfurt-Hahn Airport', 'country': 'Germany', 'category': 'B'},
    {'IATA_code': 'BHX', 'ICAO_code': 'EGBB', 'airport_name': 'Birmingham Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'BRS', 'ICAO_code': 'EGGD', 'airport_name': 'Bristol Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'EDI', 'ICAO_code': 'EGPH', 'airport_name': 'Edinburgh Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'GLA', 'ICAO_code': 'EGPF', 'airport_name': 'Glasgow Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'LGW', 'ICAO_code': 'EGKK', 'airport_name': 'London Gatwick Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'LHR', 'ICAO_code': 'EGLL', 'airport_name': 'London Heathrow Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'MAN', 'ICAO_code': 'EGCC', 'airport_name': 'Manchester Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'NCL', 'ICAO_code': 'EGNT', 'airport_name': 'Newcastle Airport', 'country': 'United Kingdom', 'category': 'A'},
    {'IATA_code': 'ATL', 'ICAO_code': 'KATL', 'airport_name': 'Hartsfield-Jackson Atlanta International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'BOS', 'ICAO_code': 'KBOS', 'airport_name': 'Logan International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'DEN', 'ICAO_code': 'KDEN', 'airport_name': 'Denver International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'DFW', 'ICAO_code': 'KDFW', 'airport_name': 'Dallas/Fort Worth International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'JFK', 'ICAO_code': 'KJFK', 'airport_name': 'John F. Kennedy International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'LAS', 'ICAO_code': 'KLAS', 'airport_name': 'McCarran International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'LAX', 'ICAO_code': 'KLAX', 'airport_name': 'Los Angeles International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'MCO', 'ICAO_code': 'KMCO', 'airport_name': 'Orlando International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'MIA', 'ICAO_code': 'KMIA', 'airport_name': 'Miami International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'ORD', 'ICAO_code': 'KORD', 'airport_name': 'O\'Hare International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'PHL', 'ICAO_code': 'KPHL', 'airport_name': 'Philadelphia International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'PHX', 'ICAO_code': 'KPHX', 'airport_name': 'Phoenix Sky Harbor International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'SEA', 'ICAO_code': 'KSEA', 'airport_name': 'Seattle-Tacoma International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'SFO', 'ICAO_code': 'KSFO', 'airport_name': 'San Francisco International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'SLC', 'ICAO_code': 'KSLC', 'airport_name': 'Salt Lake City International Airport', 'country': 'United States', 'category': 'A'},
    {'IATA_code': 'TPA', 'ICAO_code': 'KTPA', 'airport_name': 'Tampa International Airport', 'country': 'United States', 'category': 'A'}
]

hotels = [
    {'name': 'Hotel Málaga', 'base': 'AGP'},
    {'name': 'Beach Resort Alicante', 'base': 'ALC'},
    {'name': 'Barcelona Business Hotel', 'base': 'BCN'},
    {'name': 'Bilbao Boutique Hotel', 'base': 'BIO'},
    {'name': 'Fuerteventura Beach House', 'base': 'FUE'},
    {'name': 'Girona Golf Resort', 'base': 'GRO'},
    {'name': 'Granada Hilltop Hotel', 'base': 'GRX'},
    {'name': 'Ibiza Luxury Resort', 'base': 'IBZ'},
    {'name': 'Almería Airport Hotel', 'base': 'LEI'},
    {'name': 'Gran Canaria Spa Resort', 'base': 'LPA'},
    {'name': 'Madrid Airport Business Hotel', 'base': 'MAD'},
    {'name': 'Melilla City Hotel', 'base': 'MLN'},
    {'name': 'Palma de Mallorca Beach Resort', 'base': 'PMI'},
    {'name': 'Santiago de Compostela Historic Hotel', 'base': 'SCQ'},
    {'name': 'La Palma Eco Resort', 'base': 'SPC'},
    {'name': 'Seville City Center Hotel', 'base': 'SVQ'},
    {'name': 'Tenerife North Mountain Lodge', 'base': 'TFN'},
    {'name': 'Tenerife South Beachfront Hotel', 'base': 'TFS'},
    {'name': 'Valencia Urban Hotel', 'base': 'VLC'},
    {'name': 'Valladolid Countryside Retreat', 'base': 'VLL'},
    {'name': 'Jerez Airport Inn', 'base': 'XRY'},
    {'name': 'Zaragoza Business Hotel', 'base': 'ZAZ'},
    {'name': 'Lisbon Airport Residence', 'base': 'LIS'},
    {'name': 'Porto Riverside Hotel', 'base': 'OPO'},
    {'name': 'Faro Coastal Resort', 'base': 'FAO'},
    {'name': 'Madeira Island Retreat', 'base': 'FNC'},
    {'name': 'João Paulo II Airport Hotel', 'base': 'PDL'},
    {'name': 'Paris Charles de Gaulle Airport Hotel', 'base': 'CDG'},
    {'name': 'Orly Airport Transit Hotel', 'base': 'ORY'},
    {'name': 'Nice Airport Seafront Hotel', 'base': 'NCE'},
    {'name': 'Marseille Airport Boutique Hotel', 'base': 'MRS'},
    {'name': 'Lyon Airport Business Hotel', 'base': 'LYS'},
    {'name': 'Bordeaux Airport Vineyard Retreat', 'base': 'BOD'},
    {'name': 'Toulouse Airport Mountain Chalet', 'base': 'TLS'},
    {'name': 'Nantes Airport Countryside Lodge', 'base': 'NTE'},
    {'name': 'Lille Airport Urban Hotel', 'base': 'LIL'},
    {'name': 'Montpellier Airport Beach Resort', 'base': 'MPL'},
    {'name': 'Biarritz Airport Surfing Hostel', 'base': 'BIQ'},
    {'name': 'Perpignan Airport Vineyard B&B', 'base': 'PGF'},
    {'name': 'Brest Airport Cliffside Inn', 'base': 'BES'},
    {'name': 'Clermont-Ferrand Airport Chalet', 'base': 'CFE'},
    {'name': 'Tarbes-Lourdes Airport Pilgrim Hostel', 'base': 'LDE'},
    {'name': 'Bergerac Airport Countryside Retreat', 'base': 'EGC'},
    {'name': 'Caen Airport Historic Hotel', 'base': 'CFR'},
    {'name': 'La Rochelle Airport Seaside Resort', 'base': 'LRH'},
    {'name': 'Chambéry Airport Ski Lodge', 'base': 'CMF'},
    {'name': 'Deauville Airport Country Inn', 'base': 'DOL'},
    {'name': 'Metz-Nancy-Lorraine Airport Business Hotel', 'base': 'ETZ'},
    {'name': 'Poitiers Airport Tranquil Retreat', 'base': 'PIS'},
    {'name': 'Quimper Airport Coastal Hideaway', 'base': 'UIP'},
    {'name': 'Alghero-Fertilia Airport Boutique Hotel', 'base': 'AHO'},
    {'name': 'Brindisi Airport Relaxation Retreat', 'base': 'BDS'},
    {'name': 'Milan Bergamo Airport Business Hotel', 'base': 'BGY'},
    {'name': 'Bologna Airport City Center Hotel', 'base': 'BLQ'},
    {'name': 'Bari Airport Seaside Resort', 'base': 'BRI'},
    {'name': 'Cagliari Airport Oasis', 'base': 'CAG'},
    {'name': 'Catania Airport Mountain Retreat', 'base': 'CTA'},
    {'name': 'Rome Fiumicino Airport Luxury Resort', 'base': 'FCO'},
    {'name': 'Florence Airport Art Hotel', 'base': 'FLR'},
    {'name': 'Genoa Airport Business Hotel', 'base': 'GOA'},
    {'name': 'Milan Linate Airport City Hotel', 'base': 'LIN'},
    {'name': 'Milan Malpensa Airport Luxury Retreat', 'base': 'MXP'},
    {'name': 'Naples Airport Beachfront Resort', 'base': 'NAP'},
    {'name': 'Olbia Airport Boutique Lodge', 'base': 'OLB'},
    {'name': 'Palermo Airport Tranquil Getaway', 'base': 'PMO'},
    {'name': 'Parma Airport Countryside Retreat', 'base': 'PMF'},
    {'name': 'Pisa Airport Vineyard Inn', 'base': 'PSA'},
    {'name': 'Pula Airport Coastal Hideaway', 'base': 'PUY'},
    {'name': 'Turin Airport Ski Chalet', 'base': 'TRN'},
    {'name': 'Trieste Airport Hillside Retreat', 'base': 'TRS'},
    {'name': 'Treviso Airport Canal-side Hotel', 'base': 'TSF'},
    {'name': 'Venice Marco Polo Airport Luxury Resort', 'base': 'VCE'},
    {'name': 'Verona Airport Countryside Retreat', 'base': 'VRN'},
    {'name': 'Palermo Boccadifalco Airport Boutique Hotel', 'base': 'ZIA'},
    {'name': 'Berlin Brandenburg Airport City Hotel', 'base': 'BER'},
    {'name': 'Cologne Bonn Airport Business Hotel', 'base': 'CGN'},
    {'name': 'Düsseldorf Airport Urban Retreat', 'base': 'DUS'},
    {'name': 'Frankfurt Airport Luxury Resort', 'base': 'FRA'},
    {'name': 'Hamburg Airport Riverside Hotel', 'base': 'HAM'},
    {'name': 'Leipzig/Halle Airport Golf Resort', 'base': 'LEJ'},
    {'name': 'Munich Airport Alpine Lodge', 'base': 'MUC'},
    {'name': 'Stuttgart Airport Wellness Retreat', 'base': 'STR'},
    {'name': 'Berlin Tegel Airport City Center Hotel', 'base': 'TXL'},
    {'name': 'Frankfurt-Hahn Airport Countryside Retreat', 'base': 'HHN'},
    {'name': 'Birmingham Airport Business Hotel', 'base': 'BHX'},
    {'name': 'Bristol Airport Countryside Retreat', 'base': 'BRS'},
    {'name': 'Edinburgh Airport Urban Hotel', 'base': 'EDI'},
    {'name': 'Glasgow Airport Hillside Lodge', 'base': 'GLA'},
    {'name': 'London Gatwick Airport Seaside Resort', 'base': 'LGW'},
    {'name': 'London Heathrow Airport Luxury Hotel', 'base': 'LHR'},
    {'name': 'Manchester Airport City Center Hotel', 'base': 'MAN'},
    {'name': 'Newcastle Airport Riverside Retreat', 'base': 'NCL'},
    {'name': 'Hartsfield-Jackson Atlanta International Airport City Hotel', 'base': 'ATL'},
    {'name': 'Logan International Airport Business Hotel', 'base': 'BOS'},
    {'name': 'Denver International Airport Mountain Retreat', 'base': 'DEN'},
    {'name': 'Dallas/Fort Worth International Airport Luxury Resort', 'base': 'DFW'},
    {'name': 'John F. Kennedy International Airport Seaside Hotel', 'base': 'JFK'},
    {'name': 'McCarran International Airport Urban Retreat', 'base': 'LAS'},
    {'name': 'Los Angeles International Airport Boutique Hotel', 'base': 'LAX'},
    {'name': 'Orlando International Airport Family Resort', 'base': 'MCO'},
    {'name': 'Miami International Airport Beachfront Hotel', 'base': 'MIA'},
    {'name': 'O\'Hare International Airport Transit Hotel', 'base': 'ORD'},
    {'name': 'Philadelphia International Airport Urban Retreat', 'base': 'PHL'},
    {'name': 'Phoenix Sky Harbor International Airport Resort', 'base': 'PHX'},
    {'name': 'Seattle-Tacoma International Airport Hilltop Retreat', 'base': 'SEA'},
    {'name': 'San Francisco International Airport Luxury Resort', 'base': 'SFO'},
    {'name': 'Salt Lake City International Airport Mountain Lodge', 'base': 'SLC'},
    {'name': 'Tampa International Airport Beach Resort', 'base': 'TPA'},
    {'name': 'Hotel Costa del Sol', 'base': 'AGP'},
    {'name': 'Alicante Beach Club', 'base': 'ALC'},
    {'name': 'Barcelona Bayview Hotel', 'base': 'BCN'},
    {'name': 'Bilbao Riverside Hotel', 'base': 'BIO'},
    {'name': 'Fuerteventura Oasis Hotel', 'base': 'FUE'},
    {'name': 'Girona Hillside Retreat', 'base': 'GRO'},
    {'name': 'Granada Palace Hotel', 'base': 'GRX'},
    {'name': 'Ibiza Marina Resort', 'base': 'IBZ'},
    {'name': 'Almería Coastal Retreat', 'base': 'LEI'},
    {'name': 'Gran Canaria Beach Hotel', 'base': 'LPA'},
    {'name': 'Madrid Central Hotel', 'base': 'MAD'},
    {'name': 'Melilla Seaview Resort', 'base': 'MLN'},
    {'name': 'Palma de Mallorca Garden Hotel', 'base': 'PMI'},
    {'name': 'Santiago de Compostela City Hotel', 'base': 'SCQ'},
    {'name': 'La Palma Mountain Retreat', 'base': 'SPC'},
    {'name': 'Seville Riverside Inn', 'base': 'SVQ'},
    {'name': 'Tenerife Hilltop Hideaway', 'base': 'TFN'},
    {'name': 'Tenerife Sunset Resort', 'base': 'TFS'},
    {'name': 'Valencia Beach Hotel', 'base': 'VLC'},
    {'name': 'Valladolid City View Hotel', 'base': 'VLL'},
    {'name': 'Jerez Vineyard Retreat', 'base': 'XRY'},
    {'name': 'Zaragoza Riverside Lodge', 'base': 'ZAZ'},
    {'name': 'Lisbon Oceanfront Hotel', 'base': 'LIS'},
    {'name': 'Porto Cityscape Hotel', 'base': 'OPO'},
    {'name': 'Faro Coastal Paradise', 'base': 'FAO'},
    {'name': 'Madeira Island Oasis', 'base': 'FNC'},
    {'name': 'Ponta Delgada Bay Hotel', 'base': 'PDL'},
    {'name': 'Paris Eiffel Tower View Hotel', 'base': 'CDG'},
    {'name': 'Orly Airport Gateway Hotel', 'base': 'ORY'},
    {'name': 'Nice Riviera Retreat', 'base': 'NCE'},
    {'name': 'Marseille Seaside Escape', 'base': 'MRS'},
    {'name': 'Lyon Riverside Hotel', 'base': 'LYS'},
    {'name': 'Bordeaux Vineyard Villa', 'base': 'BOD'},
    {'name': 'Toulouse Mountain View Lodge', 'base': 'TLS'},
    {'name': 'Nantes Countryside Manor', 'base': 'NTE'},
    {'name': 'Lille Urban Oasis', 'base': 'LIL'},
    {'name': 'Montpellier Beachside Villa', 'base': 'MPL'},
    {'name': 'Biarritz Surfing Resort', 'base': 'BIQ'},
    {'name': 'Perpignan Vineyard Hideaway', 'base': 'PGF'},
    {'name': 'Brest Cliffside Escape', 'base': 'BES'},
    {'name': 'Clermont-Ferrand Mountain Lodge', 'base': 'CFE'},
    {'name': 'Lourdes Pilgrim Retreat', 'base': 'LDE'},
    {'name': 'Bergerac Riverside Lodge', 'base': 'EGC'},
    {'name': 'Caen Castle Hotel', 'base': 'CFR'},
    {'name': 'La Rochelle Coastal Mansion', 'base': 'LRH'},
    {'name': 'Chambéry Mountain Chalet', 'base': 'CMF'},
    {'name': 'Deauville Countryside Villa', 'base': 'DOL'},
    {'name': 'Metz-Nancy-Lorraine Countryside Inn', 'base': 'ETZ'},
    {'name': 'Poitiers Tranquil Villa', 'base': 'PIS'},
    {'name': 'Quimper Coastal Mansion', 'base': 'UIP'},
    {'name': 'Alghero-Fertilia Hillside Lodge', 'base': 'AHO'},
    {'name': 'Brindisi Seaside Retreat', 'base': 'BDS'},
    {'name': 'Milan Bergamo Riverside Hotel', 'base': 'BGY'},
    {'name': 'Bologna Cityscape Hotel', 'base': 'BLQ'},
    {'name': 'Bari Seaview Resort', 'base': 'BRI'},
    {'name': 'Cagliari Oasis Hotel', 'base': 'CAG'},
    {'name': 'Catania Mountain Lodge', 'base': 'CTA'},
    {'name': 'Rome Fiumicino Coastal Resort', 'base': 'FCO'},
    {'name': 'Florence Artistic Retreat', 'base': 'FLR'},
    {'name': 'Genoa Seaside Boutique Hotel', 'base': 'GOA'},
    {'name': 'Milan Linate Cityscape Hotel', 'base': 'LIN'},
    {'name': 'Milan Malpensa Mountain Resort', 'base': 'MXP'},
    {'name': 'Naples Beachfront Retreat', 'base': 'NAP'},
    {'name': 'Olbia Boutique Resort', 'base': 'OLB'},
    {'name': 'Palermo Tranquil Haven', 'base': 'PMO'},
    {'name': 'Parma Countryside Retreat', 'base': 'PMF'},
    {'name': 'Pisa Vineyard Villa', 'base': 'PSA'},
    {'name': 'Pula Coastal Getaway', 'base': 'PUY'},
    {'name': 'Turin Ski Lodge', 'base': 'TRN'},
    {'name': 'Trieste Hillside Resort', 'base': 'TRS'},
    {'name': 'Treviso Canal-side Retreat', 'base': 'TSF'},
    {'name': 'Venice Luxury Retreat', 'base': 'VCE'},
    {'name': 'Verona Vineyard Inn', 'base': 'VRN'},
    {'name': 'Palermo Airport Boutique Hotel', 'base': 'ZIA'},
    {'name': 'Berlin Riverside Hotel', 'base': 'BER'},
    {'name': 'Cologne Bonn Lakeside Resort', 'base': 'CGN'},
    {'name': 'Düsseldorf Urban Oasis', 'base': 'DUS'},
    {'name': 'Frankfurt Lakeside Resort', 'base': 'FRA'},
    {'name': 'Hamburg Seaside Retreat', 'base': 'HAM'},
    {'name': 'Leipzig/Halle Golf Resort', 'base': 'LEJ'},
    {'name': 'Munich Alpine Lodge', 'base': 'MUC'},
    {'name': 'Stuttgart Countryside Manor', 'base': 'STR'},
    {'name': 'Berlin Tegel City Hotel', 'base': 'TXL'},
    {'name': 'Frankfurt-Hahn Riverside Lodge', 'base': 'HHN'},
    {'name': 'Birmingham Lakeside Resort', 'base': 'BHX'},
    {'name': 'Bristol Hilltop Retreat', 'base': 'BRS'},
    {'name': 'Edinburgh Riverside Hotel', 'base': 'EDI'},
    {'name': 'Glasgow Lakeside Retreat', 'base': 'GLA'},
    {'name': 'London Gatwick Luxury Hotel', 'base': 'LGW'},
    {'name': 'London Heathrow Seaview Resort', 'base': 'LHR'},
    {'name': 'Manchester Central Hotel', 'base': 'MAN'},
    {'name': 'Newcastle Riverside Retreat', 'base': 'NCL'},
    {'name': 'Atlanta Airport Riverside Resort', 'base': 'ATL'},
    {'name': 'Boston Bay Hotel', 'base': 'BOS'},
    {'name': 'Denver Mountain Chalet', 'base': 'DEN'},
    {'name': 'Dallas/Fort Worth Lakeside Resort', 'base': 'DFW'},
    {'name': 'JFK Seaside Retreat', 'base': 'JFK'},
    {'name': 'Las Vegas Luxury Resort', 'base': 'LAS'},
    {'name': 'Los Angeles Seaview Hotel', 'base': 'LAX'},
    {'name': 'Orlando Beach Resort', 'base': 'MCO'},
    {'name': 'Miami Beachfront Resort', 'base': 'MIA'},
    {'name': 'O\'Hare Transit Hotel', 'base': 'ORD'},
    {'name': 'Philadelphia Riverside Retreat', 'base': 'PHL'},
    {'name': 'Phoenix Resort', 'base': 'PHX'},
    {'name': 'Seattle-Tacoma Mountain Lodge', 'base': 'SEA'},
    {'name': 'San Francisco Coastal Resort', 'base': 'SFO'},
    {'name': 'Salt Lake City Mountain Retreat', 'base': 'SLC'},
    {'name': 'Tampa Seaside Resort', 'base': 'TPA'}
]

prices_salaries = [
    {
        'role': 'Manager',
        'basic': 5000,
        'main_service': 50.0,
        'instruction': 100.0,
        'sec_bonus': 300.0,
        'per_diem': 25.0,
        'cleaning_serv': 50.0,
        'birthday_bonus': 200.0,
        'additional_bonus': 150.0,
        'special_project_bonus': 500.0,
        'bought_days': 150.0,
        'standby_days': 100.0,
        'theory_bonus': 200.0,
        'sick_leave': 300.0,
        'office_day': 300.0,
        'office_day_holidays': 400.0
    },
    {
        'role': 'Crew Control',
        'basic': 2500,
        'main_service': 30.0,
        'instruction': 50.0,
        'sec_bonus': 150.0,
        'per_diem': 20.0,
        'cleaning_serv': 30.0,
        'birthday_bonus': 100.0,
        'additional_bonus': 75.0,
        'special_project_bonus': 250.0,
        'bought_days': 100.0,
        'standby_days': 75.0,
        'theory_bonus': 150.0,
        'sick_leave': 200.0,
        'office_day': 200.0,
        'office_day_holidays': 300.0
    },
    {
        'role': 'Captain',
        'basic': 7000,
        'main_service': 70.0,
        'instruction': 150.0,
        'sec_bonus': 400.0,
        'per_diem': 35.0,
        'cleaning_serv': 70.0,
        'birthday_bonus': 300.0,
        'additional_bonus': 200.0,
        'special_project_bonus': 700.0,
        'bought_days': 200.0,
        'standby_days': 150.0,
        'theory_bonus': 300.0,
        'sick_leave': 400.0,
        'office_day': 400.0,
        'office_day_holidays': 500.0
    },
    {
        'role': 'First Officer',
        'basic': 6000,
        'main_service': 60.0,
        'instruction': 120.0,
        'sec_bonus': 350.0,
        'per_diem': 30.0,
        'cleaning_serv': 60.0,
        'birthday_bonus': 250.0,
        'additional_bonus': 175.0,
        'special_project_bonus': 600.0,
        'bought_days': 175.0,
        'standby_days': 125.0,
        'theory_bonus': 250.0,
        'sick_leave': 350.0,
        'office_day': 350.0,
        'office_day_holidays': 450.0
    },
    {
        'role': 'Senior',
        'basic': 4500,
        'main_service': 45.0,
        'instruction': 90.0,
        'sec_bonus': 250.0,
        'per_diem': 22.5,
        'cleaning_serv': 45.0,
        'birthday_bonus': 175.0,
        'additional_bonus': 125.0,
        'special_project_bonus': 450.0,
        'bought_days': 125.0,
        'standby_days': 90.0,
        'theory_bonus': 175.0,
        'sick_leave': 250.0,
        'office_day': 250.0,
        'office_day_holidays': 350.0
    },
    {
        'role': 'Cabin Crew',
        'basic': 2000,
        'main_service': 20.0,
        'instruction': 40.0,
        'sec_bonus': 100.0,
        'per_diem': 15.0,
        'cleaning_serv': 20.0,
        'birthday_bonus': 75.0,
        'additional_bonus': 50.0,
        'special_project_bonus': 200.0,
        'bought_days': 50.0,
        'standby_days': 40.0,
        'theory_bonus': 75.0,
        'sick_leave': 100.0,
        'office_day': 100.0,
        'office_day_holidays': 200.0
    }
]

employees = [
    {
        'crew_id': 'MGR',
        'name': 'Manuel',
        'surname': 'García Rodríguez',
        'email': 'mgarcia@jetstream.com',
        'password': 'man123',
        'department': 'Management',
        'role': 'Manager',
        'gender': 'Male',
    },
    {
        'crew_id': 'CLM',
        'name': 'Carmen',
        'surname': 'López Martínez',
        'email': 'clopez@jetstream.com',
        'password': 'car123',
        'department': 'Crew Planning',
        'role': 'Crew Control',
        'gender': 'Female',
    },
    {
        'crew_id': 'CRS',
        'name': 'Carlos',
        'surname': 'Ruiz Sánchez',
        'email': 'cruiz@jetstream.com',
        'password': 'carlos123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'JSM',
        'name': 'John',
        'surname': 'Smith',
        'email': 'jsmith@jetstream.com',
        'password': 'john123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'PLH',
        'name': 'Paul',
        'surname': 'Harrison',
        'email': 'pharrison@jetstream.com',
        'password': 'paul123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'EKC',
        'name': 'Eva',
        'surname': 'Kowalski',
        'email': 'ekowalski@jetstream.com',
        'password': 'eva123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Female',
    },
    {
        'crew_id': 'TGB',
        'name': 'Thomas',
        'surname': 'Berg',
        'email': 'tberg@jetstream.com',
        'password': 'thomas123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'ALF',
        'name': 'Alexandra',
        'surname': 'Fischer',
        'email': 'afischer@jetstream.com',
        'password': 'alex123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Female',
    },
    {
        'crew_id': 'VLM',
        'name': 'Victor',
        'surname': 'Larsen',
        'email': 'vlarsen@jetstream.com',
        'password': 'victor123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'SGA',
        'name': 'Sophie',
        'surname': 'Garcia',
        'email': 'sgarcia@jetstream.com',
        'password': 'sophie123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Female',
    },
    {
        'crew_id': 'NPK',
        'name': 'Nikolas',
        'surname': 'Papadopoulos',
        'email': 'npapadopoulos@jetstream.com',
        'password': 'nikolas123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'MMR',
        'name': 'Marie',
        'surname': 'Martin',
        'email': 'mmartin@jetstream.com',
        'password': 'marie123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Female',
    },
    {
        'crew_id': 'LTT',
        'name': 'Lucas',
        'surname': 'Tavares',
        'email': 'ltavares@jetstream.com',
        'password': 'lucas123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'GGI',
        'name': 'Giulia',
        'surname': 'Gallo',
        'email': 'ggallo@jetstream.com',
        'password': 'giulia123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Female',
    },
    {
        'crew_id': 'DSH',
        'name': 'David',
        'surname': 'Smith',
        'email': 'dsmith@jetstream.com',
        'password': 'david123',
        'department': 'Inflight',
        'role': 'Captain',
        'gender': 'Male',
    },
    {
        'crew_id': 'FOM',
        'name': 'Fátima',
        'surname': 'Martínez López',
        'email': 'fmartinez@jetstream.com',
        'password': 'fati123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Female',
    },
    {
        'crew_id': 'FOJ',
        'name': 'Frederik',
        'surname': 'Olsen',
        'email': 'folsen@jetstream.com',
        'password': 'frederik123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'FMO',
        'name': 'François',
        'surname': 'Moreau',
        'email': 'fmoreau@jetstream.com',
        'password': 'francois123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'FOW',
        'name': 'Fiona',
        'surname': 'Wong',
        'email': 'fwong@jetstream.com',
        'password': 'fiona123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Female',
    },
    {
        'crew_id': 'FOP',
        'name': 'Fernanda',
        'surname': 'Oliveira',
        'email': 'foliveira@jetstream.com',
        'password': 'fernanda123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Female',
    },
    {
        'crew_id': 'FOL',
        'name': 'Filip',
        'surname': 'Larsson',
        'email': 'flarsson@jetstream.com',
        'password': 'filip123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'FOH',
        'name': 'Fatima',
        'surname': 'Haas',
        'email': 'fhaas@jetstream.com',
        'password': 'fatima123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Female',
    },
    {
        'crew_id': 'FOB',
        'name': 'Fabien',
        'surname': 'Boucher',
        'email': 'fboucher@jetstream.com',
        'password': 'fabien123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'FOR',
        'name': 'Francesca',
        'surname': 'Rossi',
        'email': 'frossi@jetstream.com',
        'password': 'francesca123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Female',
    },
    {
        'crew_id': 'FOS',
        'name': 'Felix',
        'surname': 'Schmidt',
        'email': 'fschmidt@jetstream.com',
        'password': 'felix123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'FOC',
        'name': 'Francesco',
        'surname': 'Coppola',
        'email': 'fcoppola@jetstream.com',
        'password': 'francesco123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'FOG',
        'name': 'Frida',
        'surname': 'Gustafsson',
        'email': 'fgustafsson@jetstream.com',
        'password': 'frida123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Female',
    },
    {
        'crew_id': 'FOF',
        'name': 'Finn',
        'surname': 'OConnor',
        'email': 'foconnor@jetstream.com',
        'password': 'finn123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'FOD',
        'name': 'Freja',
        'surname': 'Dahl',
        'email': 'fdahl@jetstream.com',
        'password': 'freja123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Female',
    },
    {
        'crew_id': 'FOE',
        'name': 'Federico',
        'surname': 'Esposito',
        'email': 'fesposito@jetstream.com',
        'password': 'federico123',
        'department': 'Inflight',
        'role': 'First Officer',
        'gender': 'Male',
    },
    {
        'crew_id': 'SHR',
        'name': 'Santiago',
        'surname': 'Hernández Pérez',
        'email': 'shernandez@jetstream.com',
        'password': 'santi123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Male',
    },
    {
        'crew_id': 'SEN',
        'name': 'Sofia',
        'surname': 'Engel',
        'email': 'sengel@jetstream.com',
        'password': 'sofia123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SEH',
        'name': 'Sebastian',
        'surname': 'Hansen',
        'email': 'shansen@jetstream.com',
        'password': 'sebastian123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Male',
    },
    {
        'crew_id': 'SEB',
        'name': 'Sara',
        'surname': 'Eriksson',
        'email': 'seriksson@jetstream.com',
        'password': 'sara123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SEK',
        'name': 'Sven',
        'surname': 'Keller',
        'email': 'skeller@jetstream.com',
        'password': 'sven123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Male',
    },
    {
        'crew_id': 'SEF',
        'name': 'Sara',
        'surname': 'Fischer',
        'email': 'sfischer@jetstream.com',
        'password': 'sara123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SEM',
        'name': 'Sophie',
        'surname': 'Müller',
        'email': 'smuller@jetstream.com',
        'password': 'sophie123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SEG',
        'name': 'Sebastian',
        'surname': 'Garcia',
        'email': 'sgarcia@jetstream.com',
        'password': 'sebastian123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Male',
    },
    {
        'crew_id': 'SEO',
        'name': 'Sara',
        'surname': 'Olsson',
        'email': 'solsson@jetstream.com',
        'password': 'sara123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SEJ',
        'name': 'Svenja',
        'surname': 'Jensen',
        'email': 'sjensen@jetstream.com',
        'password': 'svenja123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SED',
        'name': 'Simon',
        'surname': 'Dahl',
        'email': 'sdahl@jetstream.com',
        'password': 'simon123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Male',
    },
    {
        'crew_id': 'SEV',
        'name': 'Sofia',
        'surname': 'Vogel',
        'email': 'svogel@jetstream.com',
        'password': 'sofia123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SEC',
        'name': 'Sébastien',
        'surname': 'Chapuis',
        'email': 'schapuis@jetstream.com',
        'password': 'sebastien123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Male',
    },
    {
        'crew_id': 'SEL',
        'name': 'Sara',
        'surname': 'Eklund',
        'email': 'seklund@jetstream.com',
        'password': 'sara123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Female',
    },
    {
        'crew_id': 'SEZ',
        'name': 'Sebastian',
        'surname': 'Zimmermann',
        'email': 'szimmermann@jetstream.com',
        'password': 'sebastian123',
        'department': 'Inflight',
        'role': 'Senior',
        'gender': 'Male',
    },
    {
        'crew_id': 'CGR',
        'name': 'Celia',
        'surname': 'Gómez Ramírez',
        'email': 'cgomez@jetstream.com',
        'password': 'celia123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCA',
        'name': 'Chiara',
        'surname': 'Abate',
        'email': 'cabate@jetstream.com',
        'password': 'chiara123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCB',
        'name': 'Carlos',
        'surname': 'Borges',
        'email': 'cborges@jetstream.com',
        'password': 'carlos123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCC',
        'name': 'Clara',
        'surname': 'Cruz',
        'email': 'ccruz@jetstream.com',
        'password': 'clara123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCD',
        'name': 'Cristian',
        'surname': 'Delgado',
        'email': 'cdelgado@jetstream.com',
        'password': 'cristian123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCE',
        'name': 'Charlotte',
        'surname': 'Eriksson',
        'email': 'ceriksson@jetstream.com',
        'password': 'charlotte123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCF',
        'name': 'Christophe',
        'surname': 'Fournier',
        'email': 'cfournier@jetstream.com',
        'password': 'christophe123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCG',
        'name': 'Catarina',
        'surname': 'Gomes',
        'email': 'cgomes@jetstream.com',
        'password': 'catarina123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCH',
        'name': 'Caleb',
        'surname': 'Harris',
        'email': 'charris@jetstream.com',
        'password': 'caleb123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCI',
        'name': 'Céline',
        'surname': 'Ibrahim',
        'email': 'cibrahim@jetstream.com',
        'password': 'celine123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCJ',
        'name': 'Connor',
        'surname': 'Jones',
        'email': 'cjones@jetstream.com',
        'password': 'connor123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCK',
        'name': 'Carmen',
        'surname': 'Kowalski',
        'email': 'ckowalski@jetstream.com',
        'password': 'carmen123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCL',
        'name': 'Claire',
        'surname': 'Leroy',
        'email': 'cleroy@jetstream.com',
        'password': 'claire123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCM',
        'name': 'Christian',
        'surname': 'Müller',
        'email': 'cmuller@jetstream.com',
        'password': 'christian123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCN',
        'name': 'Carolina',
        'surname': 'Nunes',
        'email': 'cnunes@jetstream.com',
        'password': 'carolina123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCO',
        'name': 'Carla',
        'surname': 'Olivier',
        'email': 'colivier@jetstream.com',
        'password': 'carla123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCP',
        'name': 'Christopher',
        'surname': 'Petersen',
        'email': 'cpetersen@jetstream.com',
        'password': 'christopher123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCQ',
        'name': 'Camilla',
        'surname': 'Quintana',
        'email': 'cquintana@jetstream.com',
        'password': 'camilla123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCR',
        'name': 'Carlos',
        'surname': 'Ramos',
        'email': 'cramos@jetstream.com',
        'password': 'carlos123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCS',
        'name': 'Clara',
        'surname': 'Silva',
        'email': 'csilva@jetstream.com',
        'password': 'clara123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCT',
        'name': 'Cristiano',
        'surname': 'Tavares',
        'email': 'ctavares@jetstream.com',
        'password': 'cristiano123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCU',
        'name': 'Céline',
        'surname': 'Unger',
        'email': 'cunger@jetstream.com',
        'password': 'celine123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCV',
        'name': 'Carl',
        'surname': 'Vogel',
        'email': 'cvogel@jetstream.com',
        'password': 'carl123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCW',
        'name': 'Caroline',
        'surname': 'Wagner',
        'email': 'cwagner@jetstream.com',
        'password': 'caroline123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCX',
        'name': 'Cristina',
        'surname': 'Xu',
        'email': 'cxu@jetstream.com',
        'password': 'cristina123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'CCY',
        'name': 'Curtis',
        'surname': 'Yan',
        'email': 'cyan@jetstream.com',
        'password': 'curtis123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'CCZ',
        'name': 'Chiara',
        'surname': 'Zhang',
        'email': 'czhang@jetstream.com',
        'password': 'chiara123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'MAR',
        'name': 'Maria',
        'surname': 'Anders',
        'email': 'manders@jetstream.com',
        'password': 'maria123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'ADL',
        'name': 'Adam',
        'surname': 'Levy',
        'email': 'alevy@jetstream.com',
        'password': 'adam123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'ELO',
        'name': 'Emma',
        'surname': 'Olsson',
        'email': 'eolsson@jetstream.com',
        'password': 'emma123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'JAM',
        'name': 'Jens',
        'surname': 'Aagaard',
        'email': 'jaagaard@jetstream.com',
        'password': 'jens123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'LEE',
        'name': 'Linda',
        'surname': 'Edwards',
        'email': 'leedwards@jetstream.com',
        'password': 'linda123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'MAT',
        'name': 'Marius',
        'surname': 'Antonsen',
        'email': 'mantonsen@jetstream.com',
        'password': 'marius123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'ANA',
        'name': 'Ana',
        'surname': 'Hernández',
        'email': 'ahernandez@jetstream.com',
        'password': 'ana123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'MOS',
        'name': 'Miguel',
        'surname': 'Oliveira',
        'email': 'moliveira@jetstream.com',
        'password': 'miguel123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'JUL',
        'name': 'Julia',
        'surname': 'Larsson',
        'email': 'jlarsson@jetstream.com',
        'password': 'julia123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'LUI',
        'name': 'Lucas',
        'surname': 'Ivanov',
        'email': 'livanov@jetstream.com',
        'password': 'lucas123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'YAN',
        'name': 'Yanis',
        'surname': 'Andrei',
        'email': 'yandrei@jetstream.com',
        'password': 'yanis123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'EVA',
        'name': 'Eva',
        'surname': 'Makarova',
        'email': 'emakarova@jetstream.com',
        'password': 'eva123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'OLI',
        'name': 'Olivia',
        'surname': 'Isaksson',
        'email': 'oisaksson@jetstream.com',
        'password': 'olivia123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'FIN',
        'name': 'Finn',
        'surname': 'Nielsen',
        'email': 'finn@jetstream.com',
        'password': 'finn123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'MAI',
        'name': 'Maïlys',
        'surname': 'Adams',
        'email': 'madams@jetstream.com',
        'password': 'mailys123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'SAN',
        'name': 'Sandra',
        'surname': 'Nielsen',
        'email': 'snielsen@jetstream.com',
        'password': 'sandra123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    },
    {
        'crew_id': 'LAR',
        'name': 'Lars',
        'surname': 'Andersen',
        'email': 'landersen@jetstream.com',
        'password': 'lars123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Male',
    },
    {
        'crew_id': 'PAT',
        'name': 'Patricia',
        'surname': 'Tavares',
        'email': 'ptavares@jetstream.com',
        'password': 'patricia123',
        'department': 'Inflight',
        'role': 'Cabin Crew',
        'gender': 'Female',
    }
]

duties=['OFFH', 'OFFD', 'HOL', 'SBYM', 'SBYA', 'SBYN', 'RES', 'POS', 'GTR', 'FLT']



def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass
    
    def insert_models():
        print("Creating models")
        for model in models:
            model_token = Models()
            model_token.model_name = model
            db.session.add(model_token)
            db.session.commit()
            print(f"Model {model} created")

    def insert_configurations():
        print("Creating configurations")
        for configuration in configurations:
            config_token = Configurations()
            model = Models.query.filter_by(model_name=configuration["model"]).first()
            config_token.model_id = model.id
            if "business" in configuration:
                config_token.business = configuration["business"]
            config_token.economy = configuration["economy"]
            db.session.add(config_token)
            db.session.commit()
            print("Configuration created for model {}".format(configuration['model']))

    def insert_fleet():
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
    
    def insert_plane_prices():
        print("Creating prices")
        for price in prices:
            price_token=Prices()
            model = Models.query.filter_by(model_name=price["model"]).first()
            price_token.model_id = model.id
            configuration = Configurations.query.filter_by(
                                                            model_id=model.id,
                                                            business=price.get("business", 0),
                                                            economy=price.get("economy")
                                                          ).first()
            price_token.configuration_id=configuration.id
            price_token.crew = price["crew"]
            price_token.price = price["price"]
            db.session.add(price_token)
            db.session.commit()
            print("Airplane {} costs {}€ per day".format(price["model"], price["price"]))

    def insert_roles():
        print("Creating enterprise roles")
        for role in roles:
            role_token=Roles()
            role_token.role = role
            db.session.add(role_token)
            db.session.commit()
            print("Role {} added to the enterprise".format(role))
    
    def insert_departments():
        print("Creating enterprise departments")
        for department in departments:
            department_token=Departments()
            department_token.department = department
            db.session.add(department_token)
            db.session.commit()
            print("Role {} added to the enterprise".format(department))

    def insert_countries():
        print("Creating list of Countries")
        for country in countries:
            country_token=Countries()
            country_token.country = country
            db.session.add(country_token)
            db.session.commit()
            print("Country {} added to DataBase".format(country))

    def insert_nationalities():
        print("Creating list of Nationalities")
        for nationality in nationalities:
            nationality_token=Nationalities()
            nationality_token.nationality = nationality
            db.session.add(nationality_token)
            db.session.commit()
            print("Nationality {} added to DataBase".format(nationality))
    
    def insert_worldwide_states():
        print("Creating list of States around the World")
        for state in states:
            state_token=States()
            country = Countries.query.filter_by(country=state["country"]).first()
            state_token.country_id = country.id
            state_token.state= state["state"]
            db.session.add(state_token)
            db.session.commit()
            print("{} from {} added to DataBase".format(state["state"], state["country"]))

    def insert_airports():
        print("Creating lists of Airports")
        for airport in airports:
            airport_token=Airports()
            country = Countries.query.filter_by(country=airport["country"]).first()
            airport_token.country_id = country.id
            airport_token.IATA_code = airport['IATA_code']
            airport_token.ICAO_code = airport['ICAO_code']
            airport_token.airport_name = airport['airport_name']
            airport_token.category = airport['category']
            db.session.add(airport_token)
            db.session.commit()
            print("{}: {}".format(airport['IATA_code'], airport['airport_name']))

    def insert_hotels():
        print("Creating lists of Hotels in bases")
        for hotel in hotels:
            hotel_token=Hotels()
            base = Airports.query.filter_by(IATA_code=hotel["base"]).first()
            hotel_token.base_id = base.id
            hotel_token.name = hotel["name"]
            db.session.add(hotel_token)
            db.session.commit()
            print("{} in {} base".format(hotel["name"], base.IATA_code))

    def insert_salary_prices():
        print("Creating lists of salaries by roles")
        for price in prices_salaries:
            price_token=Salary_Prices()
            role = Roles.query.filter_by(role=price["role"]).first()
            price_token.role_id = role.id
            price_token.basic = price["basic"]
            price_token.main_service = price["main_service"]
            price_token.instruction = price["instruction"]
            price_token.sec_bonus = price["sec_bonus"]
            price_token.per_diem = price["per_diem"]
            price_token.cleaning_serv = price["cleaning_serv"]
            price_token.birthday_bonus = price["birthday_bonus"]
            price_token.additional_bonus = price["additional_bonus"]
            price_token.special_project_bonus = price["special_project_bonus"]
            price_token.bought_days = price["bought_days"]
            price_token.standby_days = price["standby_days"]
            price_token.theory_bonus = price["theory_bonus"]
            price_token.sick_leave = price["sick_leave"]
            price_token.office_day = price["office_day"]
            price_token.office_day_holidays = price["office_day_holidays"]
            db.session.add(price_token)
            db.session.commit()
            print("Salary table for {}".format(role.role))
    
    def insert_employees():
        print("Creating list of Employees")
        for employee in employees:
            employee_token= Employees()
            role = Roles.query.filter_by(role=employee["role"]).first()
            employee_token.role_id = role.id
            department = Departments.query.filter_by(department=employee["department"]).first()
            employee_token.department_id = department.id
            employee_token.crew_id = employee['crew_id']
            employee_token.name = employee['name']
            employee_token.surname = employee['surname']
            employee_token.email = employee['email']
            employee_token.phone = random.randint(100000000, 999999999)
            employee_token.password = employee['password']
            employee_token.gender = employee['gender']
            db.session.add(employee_token)
            db.session.commit()
            print("Employee {} with crew id {} created".format(employee['name'], employee['crew_id']))

    

    def createRandomPassport():
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789012345678901234567890', k=random.randint(6,9)))
    
    def createRandomLicense():
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789012345678901234567890', k=random.randint(5,8)))

    def insert_inflight_details():
        print("creating Licenses and passports for Cabin crew and pilots")
        passports=[]
        licenses=[]
        for employee in employees:
            if employee['department'] == 'Inflight':
                details_token = Inflight()
                crew_member = Employees.query.filter_by(crew_id=employee['crew_id']).first()
                details_token.employee_id = crew_member.id
                passport=createRandomPassport()
                while passport in passports:
                    passport=createRandomPassport()
                passports.append(passport)
                license=createRandomLicense()
                while license in licenses:
                    license = createRandomLicense()
                licenses.append(license)
                details_token.passport = passport
                details_token.license = license
                details_token.pass_expiration = datetime.now()+ timedelta(days=random.randint(180, 1825))
                model = Models.query.filter_by(model_name='A320').first()
                details_token.certificate_id = model.id
                details_token.cert_expiration = datetime.now()+ timedelta(days=random.randint(60, 365))
                models_assigned = ['A320']
                number_of_licenses=1
                random_cert = random.randint(0,len(models)-1)
                certificates = []
                while models[random_cert] not in models_assigned and number_of_licenses < 4:
                    model = Models.query.filter_by(model_name=models[random_cert]).first()
                    models_assigned.append(models[random_cert])
                    certificates.append(model.id)
                    random_cert = random.randint(0,len(models)-1)
                    number_of_licenses+=1
                if number_of_licenses > 1:
                    details_token.certificate_id2 = certificates[0]
                    details_token.cert_expiration2 = datetime.now()+ timedelta(days=random.randint(60, 365))
                if number_of_licenses > 2:
                    details_token.certificate_id3 = certificates[1]
                    details_token.cert_expiration3 = datetime.now()+ timedelta(days=random.randint(60, 365))
                if number_of_licenses > 3:
                    details_token.certificate_id4 = certificates[2]
                    details_token.cert_expiration4 = datetime.now()+ timedelta(days=random.randint(60, 365))
                base = Airports.query.filter_by(IATA_code=airports[random.randint(0,107)]['IATA_code']).first()
                details_token.home_base_id = base.id
                details_token.roster_assigned = random.randint(1,3)
                details_token.monthly_BH = random.randint(0,100)
                details_token.monthly_DH = details_token.monthly_BH + details_token.monthly_BH*0.25
                details_token.yearly_BH = random.randint(details_token.monthly_BH,900)
                details_token.yearly_DH = details_token.yearly_BH + details_token.yearly_BH*0.25
                details_token.total_BH = random.randint(details_token.yearly_BH, 15000)
                db.session.add(details_token)
                db.session.commit()
                print("Added inflight details for employee {}".format(employee['crew_id']))

    def insert_duties():
        print("Creating duties")
        for duty in duties:
            duty_token = Duties()
            duty_token.duty = duty
            db.session.add(duty_token)
            db.session.commit()
            print(f"Duty {duty} created")

    def generate_iban():
        country_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
        bban = ''.join(random.choices('1234567890', k=18))
        iban = f'{country_code}{bban}'
        return iban
    
    def insert_bank_details():
        for employee in employees:
            bank_token = Bank_Details()
            person = Employees.query.filter_by(crew_id=employee['crew_id']).first()
            bank_token.employee_id = person.id
            bank_token.IBAN = generate_iban()
            db.session.add(bank_token)
            db.session.commit()
            print("IBAN created for {}".format(employee['crew_id']))



    
    @app.cli.command("insert-data")
    def insert_data():
        insert_models()
        insert_configurations()
        insert_fleet()
        insert_plane_prices()
        insert_roles()
        insert_departments()
        insert_countries()
        insert_nationalities()
        insert_worldwide_states()
        insert_airports()
        insert_hotels()
        insert_employees()
        insert_inflight_details()
        insert_duties()
        insert_salary_prices()
        insert_bank_details()
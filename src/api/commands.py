
import click
from api.models import db, User, Models, Configurations, Fleet, Prices, Roles, Countries, Nationalities, States, Employees

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

roles = ["Manager", "Crew Control", "Captain", "First Oficer", "Senior", "Cabin Crew"]

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
    
    def insert_models():
        print("Creating models")
        for model in models:
            model_table = Models()
            model_table.model_name = model
            db.session.add(model_table)
            db.session.commit()
            print(f"Model {model} created")

    def insert_configurations():
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

    def insert_roles():
        print("Creating enterprise roles")
        for role in roles:
            role_table=Roles()
            role_table.role = role
            db.session.add(role_table)
            db.session.commit()
            print("Role {} added to the enterprise".format(role))

    def insert_countries():
        print("Creating list of Countries")
        for country in countries:
            country_table=Countries()
            country_table.country = country
            db.session.add(country_table)
            db.session.commit()
            print("Country {} added to DataBase".format(country))

    def insert_nationalities():
        print("Creating list of Nationalities")
        for nationality in nationalities:
            nationality_table=Nationalities()
            nationality_table.nationality = nationality
            db.session.add(nationality_table)
            db.session.commit()
            print("Nationality {} added to DataBase".format(nationality))
    
    def insert_worldwide_states():
        print("Creating list of States around the World")
        for state in states:
            state_table=States()
            country = Countries.query.filter_by(country=state["country"]).first()
            state_table.country_id = country.id
            state_table.state= state["state"]
            db.session.add(state_table)
            db.session.commit()
            print("{} from {} added to DataBase".format(state["state"], state["country"]))
    
    @app.cli.command("insert-data")
    def insert_data():
        insert_models()
        insert_configurations()
        insert_fleet()
        insert_plane_prices()
        insert_roles()
        insert_countries()
        insert_nationalities()
        insert_worldwide_states()
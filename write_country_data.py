import requests

from models import Country

# Create a SQLAlchemy instance
from app import app
from extensions import db # Import your Flask app and SQLAlchemy

# Initialize the SQLAlchemy app (you can also import your app configuration if needed)


url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
data = response.json()

# Print data
with app.app_context():
    db.session.query(Country).delete()
    for d in data:
        common_name = d.get('name', {}).get('common', 'none')
        if common_name != "Antarctica ":
            if common_name == "United States":
                capitals = "Washington DC"
            else:
                capitals = ", ".join(d.get('capital', 'none')) or 'none'
            official_name = d.get('name', {}).get('official', 'none')
            cca3 = d.get('cca3', 'none')
            population = str(d.get('population', 'none'))
            region = d.get('region', 'none')
            subregion = d.get('subregion', 'none')
            continents = ", ".join(d.get('continents', ['none']))
            languages = ", ".join(d.get('languages', ['none']))
            currencies = ", ".join(d.get('currencies', ['none']))
            new_country = Country(name=common_name,
                                  official_name=official_name,
                                  cca3=cca3,
                                  capitals=capitals,
                                  population=population,
                                  continents=continents,
                                  region=region,
                                  subregion=subregion,
                                  languages=languages,
                                  currencies=currencies)
            db.session.add(new_country)  # Add to the session

    try:
        db.session.commit()  # Commit the session
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()  # Rollback in case of error

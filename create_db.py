from app import app # Import your Flask app and SQLAlchemy
from extensions import db
from models import * # Import your models
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Diagnostic: Inspect and print the metadata (table definitions)
print("SQLAlchemy Metadata:")
print(db.metadata.tables)
# Create the database tables
with app.app_context():

    try:
        db.drop_all()
        db.create_all()
        print("Database tables created.")
    except Exception as e:
        print(f"An error occurred: {e}")


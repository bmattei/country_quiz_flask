from app import app # Import your Flask app and SQLAlchemy
from extensions import db
from models import * # Import your models
import logging

def create_db():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# Create the database tables
    with app.app_context():
        db_uri = db.engine.url
        print("Database URI:", db_uri)
        try:
          db.drop_all()
          db.create_all()
          print("Database tables created.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_db()
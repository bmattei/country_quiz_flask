# config.py

import os

class Config:
    # Set your application's secret key and other configurations here
    SECRET_KEY = os.environ.get('COUNTRY_SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI =  'sqlite:///country.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

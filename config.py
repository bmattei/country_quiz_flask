
import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class DevelopmentConfig(Config):
    # Set your application's secret key and other configurations here
    SQLALCHEMY_DATABASE_URI = 'sqlite:///country.db'

class TestConfig(Config):
    # Set your application's secret key and other configurations here
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    # Production-specific configurations
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_country.db'
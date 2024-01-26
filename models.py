from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

from datetime import datetime

# Add this import
from extensions import db



class Country(db.Model):
    __tablename__ = 'countries'  # Explicitly setting the table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    official_name = db.Column(db.String(128), nullable=True)

    cca3 = db.Column(db.String(3), unique=True, nullable=False)
    capitals = db.Column(db.String(256), nullable=True)
    population = db.Column(db.Integer)
    continents = db.Column(db.String(128), nullable=True)
    region = db.Column(db.String(128), nullable=True)
    subregion = db.Column(db.String(128), nullable=True)
    languages = db.Column(db.String(128), nullable=True)
    currencies = db.Column(db.String(128), nullable=True)



class Question(db.Model):

    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(128), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    games = db.relationship('Game', secondary = 'games_questions', back_populates='questions')


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(256), nullable=False)
    score = db.Column(db.Integer, default=0)
    incorrect = db.Column(db.Integer, default=0)
    correct = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', secondary='games_questions', back_populates = "games")



class GamesQuestions(db.Model):
    __tablename__ = 'games_questions'
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)





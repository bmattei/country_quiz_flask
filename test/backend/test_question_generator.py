import unittest
import os


os.environ["FLASK_ENV"] = 'testing'
from app import app, db
from write_static_data import initialize_db
from models import Country, Question, Game
from backend.question_generator import QuestionGenerator
from constants import CAPITAL_QUESTION, CONTINENT_QUESTION, POPULATION_QUESTION
from sqlalchemy import select
from constants import *

class MyTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        # Executed once before all tests
        cls.app = app
        cls.app_context = app.app_context()
        cls.app_context.push()
        initialize_db()


    @classmethod
    def tearDownClass(cls):
        # Executed once after all tests
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    @classmethod
    def populate_static_data(cls):
        # Add countries and questions here
        # ...
        pass
    def setUp(self):
        # Executed before each test
        # Set up dynamic data or other test-specific setup
        pass

    def tearDown(self):
        # Executed after each test
        # Clean up dynamic data or other test-specific teardown
        pass

    def test_question_is_returned(self):
        with self.app.app_context():
            print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])
            database_url = str(db.engine.url)
            print("Database URL FROM ENGINE:", database_url)
            game_record = Game(user='john',
                            difficulty= 15,
                            correct=0,
                            incorrect=0,
                            score=0)
            db.session.add(game_record)
            db.session.commit()
            qg = QuestionGenerator(game_record)
            status, q,choices = qg.get_question()
            self.assertEqual(SUCCESS, status)
            self.assertIsNotNone(q)
            self.assertIsNotNone(choices)

    def test_question_is_unique(self):
        with self.app.app_context():
            count = db.session.query(Question).filter(Question.difficulty <= 5).count()
            game_record = Game(user='john',
                               difficulty=5,
                               correct=0,
                               incorrect=0,
                               score=0)
            db.session.add(game_record)
            db.session.commit()
            question_ids = []
            print(f"COUNT {count}")
            for i in range(count):
                print(f"i------ {i}")
                qg = QuestionGenerator(game_record)
                status, q,choices = qg.get_question()
                self.assertEqual(SUCCESS, status)
                self.assertIsNotNone(q)
                self.assertIsNotNone(choices)
                self.assertNotIn(q.id, question_ids)
                question_ids.append(q.id)

    def test_end_of_questions(self):
        with self.app.app_context():
            count = db.session.query(Question).filter(Question.difficulty <= 5).count()
            game_record = Game(user='john',
                               difficulty=5,
                               correct=0,
                               incorrect=0,
                               score=0)
            db.session.add(game_record)
            db.session.commit()
            question_ids = []
            qg = QuestionGenerator(game_record)

            for i in range(count):
                status, q,choices = qg.get_question()
                self.assertEqual(SUCCESS, status)
                self.assertIsNotNone(q)
                self.assertIsNotNone(choices)
                self.assertNotIn(q.id, question_ids)
                question_ids.append(q.id)

            status, q, choices = qg.get_question()
            self.assertEqual(NO_MORE_RECORDS, status)


    def test_capital_choices(self):
        game_record = Game(user='john',
                           difficulty=15,
                           correct=0,
                           incorrect=0,
                           score=0)
        db.session.add(game_record)
        db.session.commit()
        qg = QuestionGenerator(game_record)
        status, q, choices = qg.get_question(qtype=CAPITAL_QUESTION)
        self.assertEqual(status, SUCCESS)
        print(choices)
        for city in choices:
            results = db.session.execute(
                select(Country)
                .where(Country.capitals.like(f"%{city}%"))
            ).scalars().first()

            self.assertIsNotNone(city, "All Capital chocies should be in DB")
            self.assertEqual(choices.count(city), 1,
                             "City should not appear twice in choices")
    def test_continent_choices(self):
        game_record = Game(user='john',
                           difficulty=15,
                           correct=0,
                           incorrect=0,
                           score=0)
        db.session.add(game_record)

        db.session.commit()
        qg = QuestionGenerator(game_record)
        status, q, choices = qg.get_question(qtype=CONTINENT_QUESTION)
        self.assertEqual(SUCCESS, status)
        print(choices)
        continents = ['Europe', 'Antarctica', 'Asia', 'North America', 'Africa',
                      'South America']

        self.assertEqual(continents, choices)





    def test_country_data(self):
        with self.app.app_context():
            country_count = db.session.query(Country).count()
            print(f"Country count {country_count}")
            self.assertGreater(country_count, 0, "No countries found in DB")

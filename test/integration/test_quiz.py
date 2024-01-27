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

client = app.test_client()


class MyTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        # Executed once before all tests
        cls.app = app
        cls.app_context = app.app_context()
        cls.app_context.push()
        initialize_db()

    def test_home_page(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Country Quiz!', response.data)

if __name__ == '__main__':
    unittest.main()
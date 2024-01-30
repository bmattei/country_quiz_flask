from flask import session

from flask_testing import TestCase
from bs4 import BeautifulSoup



import os

os.environ["FLASK_ENV"] = 'testing'
from app import app, db
from write_static_data import initialize_db
from models import Country, Question, Game
from backend.question_generator import QuestionGenerator
from constants import CAPITAL_QUESTION, CONTINENT_QUESTION, POPULATION_QUESTION
from sqlalchemy import select
from constants import *


class MyTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    @classmethod
    def setUpClass(cls):
        # Executed once before all tests
        cls.app = app
        cls.app_context = app.app_context()
        cls.app_context.push()
        initialize_db()

    def test_homepage_elements(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.data, 'html.parser')

        # Test for header
        header = soup.find('h3')
        self.assertIsNotNone(header)
        self.assertEqual(header.text, 'Welcome to the Country Quiz!')

        # Test for name input
        name_input = soup.find('input', {'id': 'name', 'type': 'text'})
        self.assertIsNotNone(name_input)

        # Test for level select
        level_select = soup.find('select', {'id': 'level'})
        self.assertIsNotNone(level_select)
        options = level_select.find_all('option')
        self.assertEqual(len(options), 3)  # Expecting 3 options

        # Test for start button
        start_button = soup.find('button', text='Start Quiz')
        self.assertIsNotNone(start_button)

        # Test for end button
        end_button = soup.find('button', text='End Game')
        self.assertIsNotNone(end_button)

    def test_start_quiz(self):
        with self.client:
            response = self.client.post('/start_quiz', data={
               'name': 'Test User',
               'level': 'Beginner'
            }, follow_redirects=True)

        soup = BeautifulSoup(response.data, 'html.parser')
        h5_headers = soup.find_all('h5')

        self.assertEqual(len(h5_headers), 4)
        self.assertIn('Correct/Total:',h5_headers[0].text )
        self.assertIn('Current Score:',h5_headers[1].text )
        self.assertIn('Personal Best:',h5_headers[2].text )
        self.assertIn("All-time High:",h5_headers[3].text )
        h2_header = soup.find("h2")
        self.assertIsNotNone(h2_header)
        self.assertEqual("?", h2_header.text[-1] )
        choices = soup.find(id="choices")
        self.assertIsNotNone(choices)
        radio_buttons = soup.find_all('input', type='radio')
        self.assertTrue(len(radio_buttons) > 4, "Radio buttons not found")
        end_button = soup.find('button', text='End Game')
        self.assertIsNotNone(end_button)




if __name__ == '__main__':
    import unittest
    unittest.main()

import unittest
import os

os.environ["FLASK_ENV"] = 'testing'
from app import app, db  # Import the app after setting the environment variable
from write_static_data import initialize_db

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait




from time import sleep, time
import subprocess
import requests

INDEX_URL = "http://127.0.0.1:9999"


# Setting Flask environment to 'testing'

# Initialize the Flask test client

class SystemTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Executed once before all tests
        print("Current Working Directory:", os.getcwd())

        print(f"FLASK_ENV     {os.environ['FLASK_ENV']}")

        initialize_db()

        cls.server = subprocess.Popen(['python3', '../../app.py'])
        cls.wait_for_server_to_start()

    @classmethod
    def wait_for_server_to_start(cls):
        """Polls the server to check if it's up and running."""
        attempts = 0
        max_wait = 5
        while attempts < max_wait:
            print("WAITING FOR SERVER")
            try:
                response = requests.get(INDEX_URL)
                if response.status_code == 200:
                    print("Server started successfully.")
                    return
            except requests.ConnectionError:
                # Server not yet up
                pass
            sleep(1)  # Wait for a second before retrying
            attempts += 1
        raise Exception("Failed to start Flask server.")

    @classmethod
    def tearDownClass(cls):
        # Terminate the Flask server process started in setUpClass
        cls.server.terminate()
        cls.server.wait()  #

    def setUp(self):
        # Initialize the Chrome WebDriver for each test

        # Specify the path to chromedriver using the Service class
        s = Service('/usr/local/bin/chromedriver')
        self.driver = webdriver.Chrome(service=s)

    def tearDown(self):
        # Close the browser window after each test
        self.driver.quit()

    def get_element_text(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element.text
        except TimeoutException:
            self.fail(f"Element not found: {by}='{value}'")
        except NoSuchElementException:
            self.fail(f"Element not found: {by}='{value}'")
    def test_verify_title(self):
        # Navigate to the specified URL
        self.driver.get(INDEX_URL)
        self.assertIn('Country Quiz', self.driver.title)

    def test_elements_on_page(self):
        # Verify the heading is present
        self.driver.get(INDEX_URL)

        heading_text = self.get_element_text(By.TAG_NAME, "h1")
        self.assertEqual(heading_text, "Welcome to the Country Quiz!")

        # Verify the form fields and buttons
        name_field = self.get_element_text(By.ID, "name")
        self.assertIsNotNone(name_field)

        level_select = self.get_element_text(By.ID, "level")
        self.assertIsNotNone(level_select)

        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        self.assertEqual(submit_button.get_attribute("value"), "Start Quiz")

        # Verify the labels
        name_label = self.driver.find_element(By.XPATH, "//label[@for='name']")
        self.assertEqual(name_label.text, "Name:")

        level_label = self.driver.find_element(By.XPATH, "//label[@for='level']")
        self.assertEqual(level_label.text, "Choose a level:")


if __name__ == '__main__':
    unittest.main()

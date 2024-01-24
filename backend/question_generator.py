import random
from models import Country, Question
from sqlalchemy import func, select
from constants import *
from flask import current_app
from helpers import format_number

from extensions import db


class QuestionGenerator:

    def __init__(self, game_record):
        self.game_record = game_record

        return

    def get_capital_choices(self, q):
        countries = db.session.query(Country) \
            .filter(Country.name != q.country, Country.capitals != 'none') \
            .order_by(func.random())
        choices = []

        for i in range(7):
            capital = countries[i].capitals.split(',')[0]
            choices.append(capital)
        index = random.randint(0, len(choices))  # Generates a random index
        choices.insert(index, q.answer)
        return choices

    def get_continent_choices(self, q):

        countries = db.session.query(Country) \
            .filter(Country.name != q.country, Country.continents != 'Oceana') \
            .order_by(func.random())
        choices = []

        for i in range(7):
            continent = countries[i].continents.split(',')[0]
            choices.append(continent)
        index = random.randint(0, len(choices))  # Generates a random index
        choices.insert(index, q.answer)
        return choices

    def get_population_choices(self, q):
        choices = []
        population = int(q.answer)
        max_pop = population * 15
        min_pop = population // 10
        while len(choices) < 7:
            choice = random.randint(min_pop, max_pop)
            if choice > (population * 1.1) or choice < (population * 0.9):
                choices.append(format_number(choice))
        index = random.randint(0, len(choices))  # Generates a random index
        choices.insert(index, format_number(population))



        return choices

    def get_question(self):
        current_app.logger.debug("Enter get_question")
        # Assuming 'func.random()' is appropriate for your database
        try:
            question_record = db.session.execute(
                select(Question)
                .where(Question.difficulty <= self.game_record.difficulty)
                .order_by(func.random())
            ).scalars().first()

            current_app.logger.debug(f"get_question: question_record {question_record}")
            if not question_record:
                current_app.logger.debug(f"get_question: FAILED GETTING QUESTION RECORD")
                return None  # or handle the case where no question is found

            choices = []
            if question_record.type == POPULATION_QUESTION:
                choices = self.get_population_choices(question_record)
            elif question_record.type == CONTINENT_QUESTION:
                choices = self.get_continent_choices(question_record)
            elif question_record.type == CAPITAL_QUESTION:
                choices = self.get_capital_choices(question_record)
            current_app.logger.debug(
                f"Exit get_question: q: {question_record.question} ans: {question_record.answer} c: {choices}")
        except Exception as e:
            current_app.logger.debug(f"get_question exceptions {e}")
            return None

        return question_record, choices

import random
from models import Country, Question, GamesQuestions
from sqlalchemy import func, select, distinct, and_
from constants import *
from flask import current_app
from helpers import format_number

from extensions import db


class QuestionGenerator:

    def __init__(self, game):
        self.game = game

        self.continents = ['Europe', 'Antarctica', 'Asia', 'North America', 'Africa', 'South America']



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
        choices = self.continents
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

    def get_question(self, qtype=None):
        current_app.logger.debug("Enter get_question")
        # Assuming 'func.random()' is appropriate for your database
        try:
            # Start building the query
            query = select(Question).outerjoin(
                GamesQuestions,
                and_(
                    Question.id == GamesQuestions.question_id,
                    GamesQuestions.game_id == self.game.id
                )
            ).where(
                GamesQuestions.game_id == None , # Select questions not linked to this game
                Question.difficulty <= self.game.difficulty
            ).order_by(
                func.random()  # Order the results randomly
            )


            # Add a filter for question type if qtype is specified
            if qtype is not None:
                query = query.where(Question.type == qtype)

            question_record = db.session.execute(
                query.order_by(func.random())
            ).scalars().first()

            current_app.logger.debug(f"get_question: question_record {question_record}")
            if not question_record:
                current_app.logger.debug(f"get_question: ")
                return NO_MORE_RECORDS, None, None  # or handle the case where no question is found
            else:
                used_question = GamesQuestions(game_id=self.game.id, question_id=question_record.id)
                db.session.add(used_question)
                db.session.commit()

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
            return UNEXPECTED_ERROR, None, None

        return SUCCESS, question_record, choices

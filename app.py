
# from config import Config
from flask import Flask, current_app, render_template, request, session, redirect, url_for, flash

from extensions import db
from backend.question_generator import QuestionGenerator
from models import Game, Question
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from helpers import format_number
from flask import Flask, render_template, flash

from config import DevelopmentConfig, TestConfig, ProductionConfig
from constants import *
import os

app = Flask(__name__, instance_relative_config=True)

env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
elif env == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(DevelopmentConfig)


app.config.from_pyfile('config.py', silent=True)



db.init_app(app)


def game_over(game_record):
    flash("End off Game")

    if game_record is None:
        return render_template('end_of_game.html')
    else:
        if game_record.score > session["personal_best"]:
            flash(f"This is a new personal best! Previous best: {session['personal_best']}")
            personal_best = game_record.score
        else:
            personal_best = session['personal_best']

        if game_record.score > session["alltime_high"]:
            flash(f"This is the RECORD HIGH SCORE!!! Previous High:  {session['alltime_high']}")
            alltime_high = game_record.score
        else:
            alltime_high = session['alltime_high']


        return render_template('end_of_game.html',
                               correct=game_record.correct,
                               total=game_record.correct + game_record.incorrect,
                               personal_best=personal_best,
                               alltime_high=session["alltime_high"],
                               score=game_record.score
                               )
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    try:
        current_app.logger.debug("ENTRY start_quiz")
        name = request.form.get('name')
        level = request.form.get('level')
        difficulty = {
                      "Beginner": 5,
                      "Expert": 10,
                      "Genius": 15
                     }[level]

        new_game = Game(user=name,
                        difficulty=difficulty,
                        correct=0,
                        incorrect=0,
                        score=0)
        db.session.add(new_game)
        db.session.commit()
        session['game_id'] = new_game.id
        flash(f"Ok {name} let's get started!")

        current_app.logger.debug(f"start_quiz new_game: {new_game}")
        current_app.logger.debug(f"start_quiz session: {session}")
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        flash('An error occurred while starting the game. Please try again.', 'error')
        # Redirect to a safe page or render an error template
        return game_over(None)
        # You can pass the name and level as query parameters if needed

    session["alltime_high"] = db.session.query(func.max(Game.score)).scalar()
    session["personal_best"] = db.session.query(func.max(Game.score)).filter(Game.user == name).scalar()


    return redirect(url_for('show_question'))


@app.route('/question')
def show_question():
    current_app.logger.debug(f"ENTRY show_question session: {session}")

    # Retrieve and display the question
    game_record = db.session.get(Game, session['game_id'])

    current_app.logger.debug(f"show_question game_record: {game_record}")

    qg = QuestionGenerator(game_record)
    current_app.logger.debug(f"show_question question_info: {qg}")

    status, question_record, choices = qg.get_question()

    if status == NO_MORE_RECORDS:
        return redirect(url_for('end_of_game'))

    session['question_id'] = question_record.id
    try:

        db.session.commit()
        current_app.logger.debug(f"end show_question session: {session}")
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        flash('An error occurred while rendering a question.', 'error')
        # Redirect to a safe page or render an error template
        return redirect(url_for('end_of_game'))
    return render_template('question.html',
                           correct=game_record.correct,
                           total= game_record.correct + game_record.incorrect,
                           personal_best=session["personal_best"],
                           alltime_high=session["alltime_high"],
                           score=game_record.score,
                           question=question_record,
                           choices=choices,
                           )



@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    current_app.logger.debug(f"Entry submit_answer. Session: {session}")
    game_record = db.session.query(Game).get(session['game_id'])
    question_record = db.session.query(Question).get(session['question_id'])
    users_choice = request.form.get('choice')
    message = ""
    if question_record.type == POPULATION_QUESTION:
        correct_answer = format_number(int(question_record.answer))
    else:
        correct_answer = question_record.answer

    if users_choice == correct_answer:
        game_record.correct += 1
        game_record.score += question_record.difficulty
        flash(f"Correct!")
    else:
        game_record.incorrect += 1
        game_record.score -= 5
        if question_record.type == POPULATION_QUESTION:
            flash(f"The correct answer was {format_number(question_record.answer)}. ")
        else:
            flash(f"The correct answer was {question_record.answer}. ", 'danger')

    total = game_record.correct + game_record.incorrect

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        flash('An error occurred while updating the score.', 'error')
        # Redirect to a safe page or render an error template
        return game_over(game_record)



    if ((users_choice == correct_answer) or (total < MIN_QUESTIONS)):
        if total >= MIN_QUESTIONS:
            flash("You are in the bonus", 'danger')
        return redirect(url_for('show_question'))
    else:
        return game_over(game_record)


@app.route('/end_of_game',methods=['POST'])
def end_of_game():

    if session['game_id'] is None:
        return game_over(None)
    else:
        game_record = db.session.query(Game).get(session['game_id'])
        return game_over(game_record)


if __name__ == "__main__":
    print("List of routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
    app.run(port=9999)

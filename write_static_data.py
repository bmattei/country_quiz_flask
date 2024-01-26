from write_country_data import write_country_data
from write_questions import write_question_data
from create_db import create_db


def initialize_db():
    create_db()
    write_country_data()
    write_question_data()


if __name__ == "__main__":
    initialize_db()

from models import Question, Country
from sqlalchemy import select
# Create a SQLAlchemy instance
from app import app  # Import your Flask app and SQLAlchemy
from extensions import db
from constants import POPULATION_QUESTION, CONTINENT_QUESTION, CAPITAL_QUESTION


def write_question_data():

    with app.app_context():
        db.session.query(Question).delete()
        stmt = select(Country)
        # print(stmt)
        result = db.session.execute(stmt)
        for row in result.scalars():
            # Assuming 'Country' has attributes like 'name', 'official_name', etc.
            # You can access each attribute using dot notation

            # print(f"LANGUAGE {row.languages} CURRENCY: {row.currencies} \n")
            list = row.capitals.split(", ")
            # print(list)
            difficulty = 5
            if row.population < 20000000:
                difficulty = 15
            elif row.population < 100000000:
                difficulty = 10
            if len(list) == 1:
                new_question = Question(question=f"What is the capital of {row.name}?",
                                        answer=row.capitals,
                                        difficulty=difficulty,
                                        type=CAPITAL_QUESTION,
                                        country=row.name
                                        )

                db.session.add(new_question)
            else:
                new_question = Question(question=f"{row.name} has multiple capitals.  Pick one of them?",
                                        answer=list[0],
                                        difficulty=difficulty,
                                        type=CONTINENT_QUESTION,
                                        country=row.name

                                        )
                db.session.add(new_question)

            clist = row.continents.split(", ")
            if len(clist) == 1:
                if row.continents != "Oceania":
                    new_question = Question(question=f"What continent is {row.name} on?",
                                            answer=row.continents,
                                            difficulty=difficulty,
                                            type=CONTINENT_QUESTION,
                                            country=row.name
                                            )
                    db.session.add(new_question)


            new_question = Question(question=f"The population of {row.name} is approximately?",
                                    answer=row.population,
                                    difficulty= 15,
                                    type= POPULATION_QUESTION,
                                    country=row.name)
            db.session.add(new_question)
        try:
            db.session.commit()  # Commit the session
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()  # Rollback in case of error

if __name__ == "__main__":
    write_question_data()
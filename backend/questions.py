from typing import Dict, Any

from backend.country_data import CountryData
import random


class Questions:

    def __init__(self, level):
        self.cd = CountryData()
        self.quiz_countries = None
        self.continents = self.cd.get_continents()

        difficulty_to_pop = {'Expert': None,
                             'Advanced': 20000000,
                             'Beginner': 100000000
                             }
        population = difficulty_to_pop[level]
        self.quiz_countries = self.cd.get_countries(population=population)

    def get_question(self):
        q_types = [self.what_continent, self.whats_the_capital]
        q_function = random.choice(q_types)
        qa = q_function()
        return qa

    def whats_the_capital(self):
        num_answers = 7
        if self.quiz_countries:
            country_info = random.choice(self.quiz_countries)
            self.quiz_countries.remove(country_info)
            qa = {}
            name = country_info['Common_Name']
            qa["Question"] = f"What's the capital of {name}? "
            capitals = self.cd.get_random_capitals(num_answers)

            answer = country_info['Capital']
            # We get one extra capital incase we randomly get the answer in our list.
            # So we can remove it and still have the correct number of answers.  Else
            # we just remove the last capital.

            if answer in capitals:
                capitals.remove(answer)
            else:
                capitals.pop(-1)
            # Insert the element at the random index
            random_index = random.randint(0, len(capitals))
            capitals.insert(random_index, answer)

            qa['Choices'] = capitals
            qa['Country'] = name
            qa['Answer'] = answer
            return qa

    def what_continent(self):
        qa = None
        country_info: dict[Any, Any]={}
        if self.quiz_countries:
            try:
                country_info = random.choice(self.quiz_countries)
                self.quiz_countries.remove(country_info)

                qa = {}
                name = country_info['Common_Name']

                qa["Question"] = f"On what continent is {name} on? "
                choices = self.continents
                continent = country_info["Continent(s)"]
                qa["Answer"] = continent
                qa["Choices"] = choices
                qa["Country"] = name
            except Exception as e:
                print("exception ", e)
                print(country_info)

        return qa

import requests
import pandas as pd


class CountryData:
    # class variables
    _instance = None
    _data_loaded = False

    # add comment to trigger workflow
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CountryData, cls).__new__(cls)
        return cls._instance

    # Singleton
    def __init__(self):
        if not self._data_loaded:
            data = self._load_data()
            self.countries_df = data["df"]
            self.countries_json = data["json"]
            self._create_common_name_column()
            self._df_loaded = True

    @staticmethod
    def _load_data():
        url = "https://restcountries.com/v3.1/all"
        try:
            response = requests.get(url)
            response.raise_for_status()
            json = response.json()
            countries_df = pd.DataFrame(json)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            countries_df = pd.DataFrame()
        except requests.exceptions.RequestException as req_err:
            print(f"Error during requests to {url}: {req_err}")
            countries_df = pd.DataFrame()
        except Exception as err:
            print(f"An error occurred: {err}")
            countries_df = pd.DataFrame()
        return {"json": json, "df": countries_df}

    # In the country data there is the common names and official names (more names?)
    # In Panda columns can be complex structures in this case the column is a data dictionary
    # To make it easier to access the common_name we pull it out of names column dictionary
    # Into its own column that is just a string.  Note this is panda magic and it is looping
    # through ever row.
    def _create_common_name_column(self):
        self.countries_df['common_name'] = self.countries_df['name'].apply(lambda x: x['common'])

    @staticmethod
    def _get_capital(series):
        capital="Unknown"
        try:
            data = series.get('capital', 'Unknown')
            if pd.isna(data):
                capital = 'Unknown'
            elif isinstance(data, list):
            # If it's a list, filter out NaN values and join
                filtered_capitals = [str(c) for c in data if not pd.isna(c)]
                capital = ', '.join(filtered_capitals) if filtered_capitals else 'Unknown'
            else:
            # If it's a single value (not a list), convert to string directly
                capital = str(data)
        except Exception as e:
            print(f"data: {data}")
            print("An unexpected error occurred:", e)

        return capital
    @staticmethod
    def _df_to_dictionary(series):
        info_dict = {}
        try:
            info_dict["Common_Name"] = series.get('common_name', 'Unknown')
            info_dict["Official_Name"] = series['name'].get('official', 'Unknown') if 'name' in series else 'Unknown'

            # Check if 'continent' is a string or list, then handle accordingly
            continent = series.get('continents', 'Unknown')
            info_dict["Continent(s)"] = continent if isinstance(continent, str) else ', '.join(continent)
            info_dict["Capital"] = CountryData._get_capital(series)
            info_dict["Region"] = series.get("region", 'Unknown')

        except Exception as e:
            print("An unexpected error occurred:", e)

        return info_dict

    def _filter_countries(self, continent=None, population=None, population_direction='greater', common_name=None):
        filtered_df = self.countries_df
        if continent:
            filtered_df = filtered_df[filtered_df['continents'] == continent]

        if population is not None:
            if population_direction == 'greater':
                filtered_df = filtered_df[filtered_df['population'] > population]
            elif population_direction == 'less':
                filtered_df = filtered_df[filtered_df['population'] < population]

        if common_name:
            filtered_df = filtered_df[filtered_df['common_name'].str.contains(common_name, case=False, na=False)]

        return filtered_df

    def get_countries(self, population=None):
        filtered_df = self.countries_df
        if population:
            filtered_df = self._filter_countries(population=population)
        countries = []
        for index, row in filtered_df.iterrows():
            countries.append(self._df_to_dictionary(row))
        return countries

    def get_random_capitals(self, count):
        capitals_list = self.countries_df['capital'].dropna().sample(count).apply(
            lambda x: ', '.join(x) if isinstance(x, list) else x).to_list()
        return capitals_list

    def get_continents(self):
        unique_continents = set()

        for item in self.countries_df['continents']:
            if isinstance(item, list):
                # Add individual continents
                for continent in item:
                    unique_continents.add(continent)
                # Join the continents into a single string for countries spanning multiple continents
                continent_str = ', '.join(item)
                unique_continents.add(continent_str)
            else:
                unique_continents.add(item)
        return list(unique_continents)

    def get_regions(self):
        regions = self.countries_df['region'].unique().tolist()
        return regions

    def get_countries_in_continent(self, continent_name):
        filtered_df = self.countries_df[self.countries_df['continents'] == continent_name]
        country_names = filtered_df['common_name'].unique().tolist()
        return country_names

    def get_country(self, country):
        df = self.countries_df.loc[self.countries_df['common_name'] == country]
        dictionary = self._df_to_dictionary(df)
        return dictionary

    def get_random_country(self, population=None):
        filtered_df = self.countries_df
        if population:
            filtered_df = self._filter_countries(population=population)

        country = filtered_df.sample()

        dictionary = self._df_to_dictionary(country)
        return dictionary

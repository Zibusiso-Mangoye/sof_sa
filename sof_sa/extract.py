import pandas as pd
from sqlalchemy import create_engine
from utility_functions import get_credentials

sofraw_df18 = pd.read_csv("..\\data\\survey_results_public_2018.csv", low_memory=False)
sofraw_df19 = pd.read_csv("..\\data\\survey_results_public_2019.csv", low_memory=False)
sofraw_df20 = pd.read_csv("..\\data\\survey_results_public_2020.csv", low_memory=False)
sofraw_df21 = pd.read_csv("..\\data\\survey_results_public_2021.csv", low_memory=False)

# Loading the data to a staging database
credentials = get_credentials(".\conf\staging_db_credentials.json")
DATABASE_URL = f'mysql+mysqlconnector://{credentials["user"]}:{credentials["password"]}@{credentials["host"]}/{credentials["database"]}'
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

with engine.connect() as connection:
    sofraw_df18.to_sql("raw_stackoverflow2018", con=connection, if_exists='replace')
    

#load_data(sofraw_df18, "raw_stackoverflow2018", credentials)
#load_data(sofraw_df19, "raw_stackoverflow2019", credentials)
#load_data(sofraw_df20, "raw_stackoverflow2020", credentials)
#load_data(sofraw_df21, "raw_stackoverflow2021", credentials)

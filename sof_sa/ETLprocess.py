import logging
import pandas as pd
from utility_functions import get_credentials, load_data, scrape_data

# Getting the data from different sources
url = 'https://www.globalbrainforce.com/blog/software-developer-salary-around-the-world/'
web_data = scrape_data(url)[3]
sofraw_df20 = pd.read_csv("..\\data\\survey_results_public_2020.csv", low_memory=False)
sofraw_df21 = pd.read_csv("..\\data\\survey_results_public_2021.csv", low_memory=False)

# Loading the data to a staging database
credentials = get_credentials(".\conf\staging_db_credentials.json")
load_data(web_data, "pl_salary_staging", credentials)
load_data(sofraw_df20, "stackoverflow2020", credentials)
load_data(sofraw_df21, "stackoverflow2021", credentials)

# Transforming the data

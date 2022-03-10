import pandas as pd
from extract import scrape_data, load_raw_data_to_db

# The url that contains salary data 
url = 'https://www.globalbrainforce.com/blog/software-developer-salary-around-the-world/'

# Scrape the web for the table
web_data = scrape_data(url)

sofraw_df20 = pd.read_csv("..\\data\\survey_results_public_2020.csv", low_memory=False)
sofraw_df21 = pd.read_csv("..\\data\\survey_results_public_2021.csv", low_memory=False)

# Load the data to a staging database
load_raw_data_to_db(web_data, sofraw_df20, sofraw_df21)

# transform the data and load to production database

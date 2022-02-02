from logger import logger
import pandas as pd
from utility_functions import connect2db, db_config, scrape_data

# Setting up logging 
#File to log to
log_file = '.\\logs\\extraction.log'
log = logger(log_file)

log.info(">> EXTRACTION PROCESS STARTED")
log.info(">> LOADING DATABASE CREDENTIALS")

try:
    creds = db_config("..\\dev_dbconfig.yaml", 0)
    engine = connect2db(**creds)
except Exception as err:
    log.exception(err, exc_info=1) 
    raise Exception('>> FAILED TO LOAD IN DATABASE CREDENTIALS')

# The url that contains salary data 
url = 'https://www.globalbrainforce.com/blog/software-developer-salary-around-the-world/'

try:
    # Scraping the data from the url
    _data = scrape_data(url)[3]
except Exception as err:
    log.exception(err) 
    raise Exception(f'>> FAILED TO SCRAPE THE URL : {url}')

# Writing data to the database 
# Table name : pl_salary_staging
with engine.connect() as connection:
    _data.to_sql('pl_salary_staging', con=connection, if_exists='replace')

# Now working with csv files from stackoverflow survey
# loading in data 
sofraw_df20 = pd.read_csv("..\\data\\survey_results_public_2020.csv")
sofraw_df21 = pd.read_csv("..\\data\\survey_results_public_2021.csv")
jetraw_df21 = pd.read_csv("..\\data\\2021_sharing_data_outside.csv")

with engine.connect() as connection:
    sofraw_df20.to_sql('sofraw_20', con=connection, if_exists='replace')
    sofraw_df21.to_sql('sofraw_21', con=connection, if_exists='replace')
    jetraw_df21.to_sql('jetraw_21', con=connection, if_exists='replace')

log.info(">> EXTRACTION PROCESS COMPLETED SUCCESSFULLY")
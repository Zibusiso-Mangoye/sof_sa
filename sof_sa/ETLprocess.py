import logging
import pandas as pd
from utility_functions import get_credentials, open_db, scrape_data

# Loading data from local csv files
def extract_raw_data() -> None:
    
    logging.info(">> EXTRACTION PROCESS COMPLETED SUCCESSFULLY")
    
    # The url that contains salary data 
    url = 'https://www.globalbrainforce.com/blog/software-developer-salary-around-the-world/'
    
    # Data
    sofraw_df20 = pd.read_csv("..\\data\\survey_results_public_2020.csv", low_memory=False)
    sofraw_df21 = pd.read_csv("..\\data\\survey_results_public_2021.csv", low_memory=False)
    web_data = scrape_data(url)
    
    try:
        creds = get_credentials(".\conf\staging_db_credentials.json")
        engine = open_db(creds)
    except Exception as err:
        logging.exception(err, exc_info=1) 
        raise Exception('>> FAILED TO LOAD IN DATABASE CREDENTIALS')

    with engine.connect() as connection:
        sofraw_df20.to_sql('sofraw_20', con=connection, if_exists='replace')
        sofraw_df21.to_sql('sofraw_21', con=connection, if_exists='replace')
        web_data.to_sql('pl_salary_staging', con=connection, if_exists='replace')

    logging.info(">> EXTRACTION PROCESS COMPLETED SUCCESSFULLY")

extract_raw_data
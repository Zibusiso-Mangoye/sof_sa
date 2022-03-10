from sqlalchemy import false
from logger import logger
import pandas as pd
from utility_functions import connect2db, db_config, scrape_data

# Setting up logging 
#File to log to
log_file = '.\\logs\\extraction.log'
log = logger(log_file)

log.info(">> EXTRACTION PROCESS STARTED")

def scrape_data(url):
    """
    A function to scrape data from the web.
    Params :
        url - url for the web page to be scraped.
    Returns:
        Tables in the web page in a list of pandas dataframe objects
    """
    header = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/53>",
    "X-Requested-With" : "XMLHttpRequest"
    }
    try:
        r = requests.get(url, headers=header)
        # Only need the third table from the scraped data
        web_data = pd.read_html(r.text)[3]
        
        return web_data
    except Exception as err:
        log.exception(err) 
        raise Exception(f'>> FAILED TO SCRAPE THE URL : {url}')
    
# Loading data from local csv files
def load_raw_data_to_db(web_data, sofraw_df20, sofraw_df21):
    
    log.info(">> LOADING DATABASE CREDENTIALS")
    try:
        creds = db_config("..\\dev_dbconfig.yaml", 0)
        engine = connect2db(**creds)
    except Exception as err:
        log.exception(err, exc_info=1) 
        raise Exception('>> FAILED TO LOAD IN DATABASE CREDENTIALS')

    with engine.connect() as connection:
        sofraw_df20.to_sql('sofraw_20', con=connection, if_exists='replace')
        sofraw_df21.to_sql('sofraw_21', con=connection, if_exists='replace')
        web_data.to_sql('pl_salary_staging', con=connection, if_exists='replace')

    log.info(">> EXTRACTION PROCESS COMPLETED SUCCESSFULLY")

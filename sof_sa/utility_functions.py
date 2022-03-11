import json
import logging
import requests
import pandas as pd
from contextlib import contextmanager
from sqlalchemy import create_engine, engine

@contextmanager
def open_db(credentials : dict) -> engine.Connection:
    """Connects to the databse specified in the credentials

    Args:
        credentials (dict): Database credentials in the form user, password, host, database name

    Returns:
        engine: a sqlalchemy engine object
    """
    
    try:
        engine = create_engine(f'mysql://{credentials["user"]}:{credentials["password"]}@{credentials["host"]}/{credentials["database"]}')
        return engine.connect()
    except Exception as error:
        logging.error(error)    
        

def get_credentials(filepath : str) -> dict:
    """Loads database credentials from file.
    Args: 
        filepath - path to the json file

    Returns :
        A dictionary containing database credentials
    """
    
    with open(filepath, "r") as file:
        data = json.loads(file.read())
   
    return data

def scrape_data(url):
    """A function to scrape data from the web.
    Args:
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
        web_data = pd.read_html(r.text)
        return web_data
    
    except Exception as err:
        logging.exception(err) 
        raise Exception(f'>> FAILED TO SCRAPE DATA FROM URL : {url}')
    
    
def load_data(data_to_load : pd.DataFrame, name_of_table : str, credentials : dict) -> None:
    """Loads data to a database. The database in use is specified in the credentials argument.
    
    Args: 
        - data_to_load(pd.DataFrame): The data to be loaded into the database.
        - name_of_table(str): The name of the table to be used when load the data to the database.
        - credentials(dict): A dictionary containing the credentials in the order user, password, host, database name
        
    Returns:
        None 
    """
    
    with open_db(credentials) as connection:
        data_to_load.to_sql(name_of_table, con=connection, if_exists='replace')
        
    logging.info(f"LOADED TABLE WITH NAME: {name_of_table}")
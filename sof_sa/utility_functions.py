import json
import logging
import requests
from sqlalchemy import create_engine
import pandas as pd
from contextlib import contextmanager


@contextmanager
def open_db(credentials : dict):
    """Connects to the databse specified in the credentials

    Args:
        credentials (dict): Database credentials {"user":"user","password": "password","host": "host","database": "database name"}

    Yields:
        Iterator[mysql.connector.cursor]: a cursor object
    """
    
    try:
        engine = create_engine(f'mysql://{credentials["user"]}:{credentials["password"]}@{credentials["host"]}/{credentials["database"]}')
        return engine
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
        # Only need the third table from the scraped data
        web_data = pd.read_html(r.text)
        return web_data
    
    except Exception as err:
        logging.exception(err) 
        raise Exception(f'>> FAILED TO SCRAPE THE URL : {url}')
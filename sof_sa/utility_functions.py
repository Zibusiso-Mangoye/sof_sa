import yaml
import requests
import pandas as pd
from sqlalchemy import create_engine

def connect2db(**db_credentials):
    """
    Handles database connections using sqlalchemy's create_engine function
    Params :
        db_credentials - a dictionary that contains user, password, host, port and database name 
    Returns :
        an sqlalchemy engine object
    """

    engine = create_engine(f"mysql+pymysql://{db_credentials['DBUSER']}:{db_credentials['DBPASSWORD']}@{db_credentials['DBHOST']}:{db_credentials['DBPORT']}/{db_credentials['DBNAME']}")
    return engine

def db_config(filepath : str, which_db : int) -> dict:
    """
    Loads database credentials information from a yaml file.
    Params : 
        filepath - path to the yaml file
        stagingortarget - integer value that chooses the database to use. 
                        - valid choices are 1 for target db or 0 for staging db
    Returns : 
        A nested dictionary containing name of db and credentials
    """
    valid = {0, 1}
    if which_db not in valid:
        raise ValueError("results: status must be one of %r." % valid)
    
    db = 'SOF_DB'
    if which_db == 0:
        db = 'STAGING_DB'

    with open(filepath, "r") as f:
        try:
            parameters = yaml.safe_load(f)['DATABASE'][which_db][db]
            
        except yaml.YAMLError as exc:
            print(exc) # log this
    return parameters
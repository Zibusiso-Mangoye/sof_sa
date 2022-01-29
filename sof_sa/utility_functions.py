import yaml
from sqlalchemy import create_engine

def connect2db(**db_credentials):
    """
    Handles database connections using sqlalchemy's create_engine function
    Params :
        db_credentials - a dictionary that contains user, password, host, port and database name 
    Returns :
        an sqlalchemy engine object
    """

    engine = create_engine(f"""mysql+pymysql://{db_credentials['DBUSER']}:{db_credentials['DBPASSWORD']}
                            @{db_credentials['DBHOST']}:{db_credentials['DBPORT']}/{db_credentials['DBNAME']}"""
                            )
    return engine

def db_config(filepath, STAGINGORTARGET):

    with open(filepath, "r") as stream:
        try:
            parameters = yaml.safe_load(stream)['DATABASE'][STAGINGORTARGET]
        except yaml.YAMLError as exc:
            print(exc) # log this
    return parameters
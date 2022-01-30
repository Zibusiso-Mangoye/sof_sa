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

def db_config(filepath : str, STAGINGORTARGET : int) -> dict:
    """
    Loads database credentials information from a yaml file.
    Params : 
        filepath - path to the yaml file
        STAGINGORTARGET - integer value that chooses the database to use. 
                        - valid choices are 1 for target db or 0 for staging db
    Returns : 
        A nested dictionary containing name of db and credentials
    """
    # Checking validity of argument STAGINGORTARGET
    valid = {0, 1}
    if STAGINGORTARGET not in valid:
        raise ValueError("results: status must be one of %r." % valid)

    with open(filepath, "r") as f:
        try:
            parameters = yaml.safe_load(f)['DATABASE'][STAGINGORTARGET]
        except yaml.YAMLError as exc:
            print(exc) # log this
    return parameters
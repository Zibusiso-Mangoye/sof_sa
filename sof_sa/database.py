import json
import logging
import pandas as pd
from sqlalchemy import create_engine 

class Database:
    def get_credentials(filepath : str) -> dict:
        """Loads database credentials from file.
        Args: 
            filepath - path to the json file

        Returns:
            A dictionary containing database credentials
        """
        with open(filepath, "r") as file:
            data = json.loads(file.read())
    
        return data

    def load_data_into_db(filepath: str, name_of_table: str, credentials: dict) -> None:
        """Loads data to a database. The database in use is specified in the credentials argument.
        
        Args: 
            - data_to_load(pd.DataFrame): The data to be loaded into the database.
            - name_of_table(str): The name of the table to be used when load the data to the database.
            - credentials(dict): A dictionary containing the credentials in the order user, password, host, database name
            
        Returns:
            None 
        """
        
        try:
            data_to_load = pd.read_csv(filepath, low_memory=False)
            
            DATABASE_URL = f'postgresql+psycopg2://{credentials["user"]}:{credentials["password"]}@{credentials["host"]}:{credentials["port"]}/{credentials["database"]}'
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            with engine.connect() as connection:
                data_to_load.to_sql(name_of_table, con=connection, if_exists='replace')
                logging.info(f"LOADED TABLE WITH NAME: {name_of_table}")
        except Exception as e:
            logging.error(e)

    def get_data_from_db(path_to_sql_file: str, credentials: dict) -> pd.DataFrame:
        """Executes an sql query 

        Args:
            path_to_sql_file (str): path to the sql file that contains the sql statement to execute.
            credentials (dict): credentials to the database where the query will be executed 

        Returns:
            pd.DataFrame: a pandas dataframe representing the results of the query
        """
        try:
            DATABASE_URL = f'postgresql+psycopg2://{credentials["user"]}:{credentials["password"]}@{credentials["host"]}:{credentials["port"]}/{credentials["database"]}'
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)

            with open(path_to_sql_file, 'r') as file, engine.connect() as connection:
                df = pd.read_sql_query(file.read(), connection)
                return df
        except Exception as e:
            logging.error(e)
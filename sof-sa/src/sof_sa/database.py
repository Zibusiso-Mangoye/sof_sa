import json
import logging
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine 

class Database:
    def get_credentials(self, filepath: str) -> dict:
        """Loads database credentials from file.
        Args: 
            filepath - path to the json file

        Returns:
            A dictionary containing database credentials
        """
        with open(filepath, "r") as file:
            data = json.loads(file.read())
    
        return data

    def load_data_into_db(self, name_of_table: str, credentials: dict, df: pd.DataFrame = None, filepath: str = '') -> None:
        """Loads data into database specified in the credentials

        Args:
            name_of_table (str): name of table
            credentials (dict): credentials to be used
            df (pd.DataFrame, optional): dataframe to load into database. Defaults to None.
            filepath (str, optional): path to csv file to load into database. Defaults to ''.

        Raises:
            ValueError: if not dataframe is provided and file path is ''
            ValueError: if both dataframe and filepath are provided
        """
        
        if df is None and filepath == '':
            raise ValueError("Provide either a dataframe or a filepath to a csv file")
        elif not df is None and Path(filepath).suffix == '.csv':
            raise ValueError("A dataframe and a filepath to a csv file was provided please provide one or the other not both")
        
        if not df is None:
            data_to_load = df
        else:
            data_to_load = pd.read_csv(filepath, low_memory=False)
            
        try:    
            DATABASE_URL = f'postgresql+psycopg2://{credentials["user"]}:{credentials["password"]}@{credentials["host"]}:{credentials["port"]}/{credentials["database"]}'
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            with engine.connect() as connection:
                data_to_load.to_sql(name_of_table, con=connection, if_exists='replace')
                logging.info(f"LOADED TABLE WITH NAME: {name_of_table}")
        except Exception as e:
            logging.error(e)

    def get_data_from_db(self, path_to_sql_file: str, credentials: dict) -> pd.DataFrame:
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
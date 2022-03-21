import json
import logging
import numpy as np
import pandas as pd
from sqlalchemy import create_engine 

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

def load_data(data_to_load : pd.DataFrame, name_of_table : str, credentials : dict) -> None:
    """Loads data to a database. The database in use is specified in the credentials argument.
    
    Args: 
        - data_to_load(pd.DataFrame): The data to be loaded into the database.
        - name_of_table(str): The name of the table to be used when load the data to the database.
        - credentials(dict): A dictionary containing the credentials in the order user, password, host, database name
        
    Returns:
        None 
    """
    
    try:
        DATABASE_URL = f'postgresql+psycopg2://{credentials["user"]}:{credentials["password"]}@{credentials["host"]}:{credentials["port"]}/{credentials["database"]}'
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as connection:
            data_to_load.to_sql(name_of_table, con=connection, if_exists='replace')
            logging.info(f"LOADED TABLE WITH NAME: {name_of_table}")
    except Exception as error:
        logging.error(error)
    

def replace_with_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces missing values in the column Age with the mean of the column
    
    Args: 
        - df(pd.DataFrame): The dataframe to be modified.
        
    Returns:
        - a dataframe with the modified column
    """
    mean_age = round(df['Age'].mean())
    df['Age'].replace(np.nan, mean_age, inplace=True)
    return df

def clean_gender_column(df: pd.DataFrame) -> list:
    """Removes ; and chooses the first option in a column that contains rows that have multiple values
    
    Args: 
        - df(pd.DataFrame): The dataframe to be modified.
        
    Returns:
        - a list of new gender values.
    """
    new_list = []
    df['Gender'] = df.Gender.astype(str)
    for gender in df['Gender']:
        if gender == None:
            new_items = 'None'
            new_list.append(new_items)
        elif ';' in gender:
            new_items = gender.split(";")[0]
            new_list.append(new_items)
        else:
            new_list.append(gender)
    return new_list

def clean_ethnicity_column(df: pd.DataFrame) -> list:
    """Removes ; and chooses the first option in a column that contains rows that have multiple values
    
    Args: 
        - df(pd.DataFrame): The dataframe to be modified.
        
    Returns:
        - a list of new ethinicity values.
    """
    new_list = []
    df['Ethnicity'] = df.Ethnicity.astype(str)

    for ethnicity in df['Ethnicity']:
        if type(ethnicity) == float:
            new_items = 'none'
            new_list.append(new_items)
        elif ';' in ethnicity:
            new_items = ethnicity.split(";")[0]
            new_list.append(new_items)
        else:
            new_list.append(ethnicity)
    return new_list

def remove_outlier(df_in: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Removes outliers in df_in where column=col_name
    
    Args: 
        - df_in(pd.DataFrame): The dataframe to be modified.
        - col_name(str): Name of the column to be modified within the dataframe.
    
    Returns:
        - a dataframe with the modified column 
    """
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out
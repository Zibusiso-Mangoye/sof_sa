import numpy as np
import pandas as pd

def age_to_range(number: int) -> str:
    """Checks if a certain value falls within a certain range then retruns the appropriate string

    Args:
        number (int): number to be checked

    Returns:
        str: a string based on the number passed
    """

    if number < 18:
        return 'Under 18 years old'
    elif number >= 18 and number <= 24:
        return '18 - 24 years old'
    elif number >= 25 and number <= 30:
        return '25 - 30 years old'
    elif number >= 31 and number <= 36:
        return '31 - 36 years old'
    elif number >= 37 and number <= 42:
        return '37 - 42 years old'
    elif number >= 43 and number <= 48:
        return '43 - 48 years old'
    elif number >= 49 and number <= 54:
        return '49 - 54 years old'
    elif number >= 55 and number <= 60:
        return '55 - 60 years old'
    elif number > 60:
        return 'Over 60 years old'
    
def clean_age_column(age) -> str:
    """Cleans the age column of a dataframe

    Args:
        age (Any): An int, str or float representing age

    Returns:
        str: a string based on the age passed
    """
    if isinstance(age, str):
        n = age.replace(" ", "")
        if 'or' in n:
            return age_to_range(int(n[0:2]))
                
        if 'Under' in n:
            return age_to_range(int(n[5:7]))
            
        if '-' in n:
            return age_to_range((int(n[0:2]) + int(n[3:5]))//2)
                
        if 'Prefer' in n:
            return 'Prefer not to say'
        
        if n is None:
            return 'Prefer not to say'
            
    if isinstance(age, float) or isinstance(age, int):
        return age_to_range(round(age))

def replace_na_with_mean_in_age_column(df: pd.DataFrame, column_name: str) -> None:
    
    """Replaces na values in column of a dataframe with mean

    Args:
        df (pd.DataFrame): dataframe to be modified
        column_name (str): column in dataframe
    
    Raises:
        ValueError: if the column passed does not exist in dataframe
    """
    
    if not column_name in df.columns:
        raise ValueError(f"No column named {column_name} in dataframe.")
    
    age_list = df[column_name].to_list()
    new_age = []

    for age in age_list:
        if isinstance(age, str):
            n = age.replace(" ", "")
            if 'or' in n:
                new_age.append(int(n[0:2]))
                
            if 'Under' in n:
                new_age.append(int(n[5:7]))
            
            if '-' in n:
                new_age.append((int(n[0:2]) + int(n[3:5]))//2)
                
            if 'Prefer' in n or 'None' in n:
                new_age.append(np.nan)
        
        if isinstance(age, float):
            if np.isnan(age):
                new_age.append(age)
            else:
                new_age.append(round(age))
                
    sum_of_numbers = 0
    length_of_number = 0
    for x in new_age:
        if isinstance(x, int):
            sum_of_numbers += x
            length_of_number += 1 
    mean = round(sum_of_numbers/length_of_number)

    df[column_name].fillna(mean, inplace=True)
    
def add_transgender_option(df: pd.DataFrame) -> list:
    e = []
    for gender, choice in zip(df['gender'].to_list(), df['transgender'].to_list()):
        
        if isinstance(choice, str) and isinstance(gender, str): 
            if 'Yes' in choice:
                e.append(gender +  ';Transgender')
                
            if 'No' in choice:
                e.append(gender)
            
            if 'Prefer not to say' in choice or 'Or, in your own words:' in choice:
                e.append(None)
                
        if isinstance(choice, type(None)) or isinstance(gender, type(None)):
            e.append(gender)
        
    return e
    
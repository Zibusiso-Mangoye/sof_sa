"""
This is a boilerplate pipeline 'data_engineering'
"""
import pandas as pd
from collections import Counter

def count_unique_items_in_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Counts unique elements in dataframe column. Column must have semicolon separated values or nan values in column

    Args:
        df (pd.DataFrame): dataframe to be modified
        column_name (str): column name in dataframe

    Returns:
        pd.DataFrame: new dataframe contain value and count of value in df
    
    Raises:
        ValueError: if the column passed does not exist in dataframe
    """
    
    column_name = column['column_name']
    if column_name not in df.columns:
        raise ValueError(f"No column named {column_name} in dataframe.")

    column_as_list = df[column_name].tolist()

    new_list = []
    for list_item in column_as_list: 

        # for nan values
        if isinstance(list_item, type(None)):
            new_list.append(list_item)

        if isinstance(list_item, str): 
            new_list.extend(list_item.split(";"))

    # find the number of occurances of a item in a list
    occ = Counter(new_list)
    language = []
    count = []
    for x in occ:
        key = x
        value = occ[key]
        language.append(key)
        count.append(value)

    df_temp = pd.DataFrame(list(zip(language, count)), columns = [column_name, 'count'])
    df_temp.set_index(column_name, inplace=True)
    df_temp.sort_values(by='count', ascending=False, inplace=True)
    return df_temp

def merge_dfs_on_index(dataset_18: pd.DataFrame, dataset_19: pd.DataFrame,
                       dataset_20: pd.DataFrame, dataset_21: pd.DataFrame, column_names: list) -> pd.DataFrame:
    """Merges dataframes on index.

    Args:
        dataset_18 (pd.DataFrame): 2018 dataset
        dataset_19 (pd.DataFrame): 2019 dataset
        dataset_20 (pd.DataFrame): 2020 dataset
        dataset_21 (pd.DataFrame): 2021 dataset
        column_names (list): column names to use in the resulting dataframe.

    Returns:
        pd.DataFrame: a dataframe with column names 
    """
    
    df18_19 = pd.merge(dataset_18, dataset_19, left_index=True, right_index=True)
    df20_21 = pd.merge(dataset_20, dataset_21, left_index=True, right_index=True)
    dfs_merged = pd.merge(df18_19, df20_21, left_index=True, right_index=True)
    dfs_merged.columns = column_names
    
    return dfs_merged

def rename_values_in_col_on_index(df: pd.DataFrame, column_params: dict = None) -> pd.DataFrame:
    """Renames values of the index.

    Args:
        df (pd.DataFrame): dataframe to be modified
        column_params (dict, optional): parameters the contain data to be used to rename. Defaults to None.

    Raises:
        ValueError: when no data is passed

    Returns:
        pd.DataFrame: dataframe with renamed values
    """
    
    rename_data = column_params['rename']
    
    if 'data' not in rename_data:
        raise ValueError("Rename should be a dict with key\n \t>  'rename' - the actual data to be used in renaming")
             
    df.rename(index=rename_data, inplace=True)
    
    return df
    

def add_missing_values_in_index(df: pd.DataFrame, column_params: dict = None) -> pd.DataFrame:
    """Adds values to the end of the dataframe and sets their values to 0.

    Args:
        df (pd.DataFrame): dataframe to be modified
        column_params (dict, optional): parameters the contain data to be used to add.. Defaults to None.

    Raises:
        ValueError: when no data is paased

    Returns:
        pd.DataFrame: dataframe with addition values set to 0
    """
    edit_values = column_params['edit']
    
    if edit_values is not None:
        raise ValueError("Data to use in editing dataframe is empty.\n Must be a list")
    
    for i in edit_values:
        if i not in df.index.values:
            df.loc[i] = 0
    
    return df
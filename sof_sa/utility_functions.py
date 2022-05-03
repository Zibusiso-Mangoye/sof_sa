import pandas as pd
from collections import Counter

def count_unique_items_in_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Counts unique elements in dataframe column. Column must have semicolon separated values or nan values in column

    Args:
        df (pd.DataFrame): dataframe to be modified
        column_name (str): column name in dataframe

    Returns:
        pd.DataFrame: new dataframe contain value and count of value in df
    
    Raises:
        ValueError: if the column passed does not exist in dataframe
    """
    if not column_name in df.columns:
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

def create_df(dataframe_list: list, column_name: str, rename: bool = False) -> pd.DataFrame:
    """Merges dataframes on column_name

    Args:
        dataframe_list (list): a list of dataframes to merge
        column_name (str): column name to merge dataframes on 

    Returns:
        pd.DataFrame: merged dataframe
        
    Raises:
        ValueError: if the list of dataframes passed is not equal to four
    """
    if len(dataframe_list) != 4:
        raise ValueError("List of dataframes must be equal to four(4)")
     
    dfs = []
    for df in dataframe_list:
        if rename:
            df1 = count_unique_items_in_column(df, column_name).rename(index={'Google Cloud Platform/App Engine': 'Google Cloud Platform', 'Azure': 'Microsoft Azure'})
        else:
            df1 = count_unique_items_in_column(df, column_name)
        dfs.append(df1)
        
    df18_19 = pd.merge(dfs[0], dfs[1], on=column_name)
    df20_21 = pd.merge(dfs[2], dfs[3], on=column_name)
    dfs_merged = pd.merge(df18_19, df20_21, on=column_name)
    dfs_merged.columns = ['2018', '2019', '2020', '2021']
    
    return dfs_merged


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

def _merge(dataframe_list: list) -> pd.DataFrame:
    """Merges dataframes on index

    Args:
        dataframe_list (list): a list of dataframes to merge

    Returns:
        pd.DataFrame: merged dataframe
        
    Raises:
        ValueError: if the list of dataframes passed is not equal to four
    """
    if len(dataframe_list) != 4:
        raise ValueError("List of dataframes must be equal to four(4)")
        
    df18_19 = pd.merge(dataframe_list[0], dataframe_list[1], left_index=True, right_index=True)
    df20_21 = pd.merge(dataframe_list[2], dataframe_list[3], left_index=True, right_index=True)
    dfs_merged = pd.merge(df18_19, df20_21, left_index=True, right_index=True)
    dfs_merged.columns = ['2018', '2019', '2020', '2021']
    
    return dfs_merged

def merge_dfs(df_list: list, column_name: str, rename: bool = False, rename_data: dict = {}, fill_missing: bool = False, missing_values: dict = {}):
    """Merge dataframes into one dataframe. 

    Args:
        df_list (list): list of dataframes to merge
        column_name (str): column name to merge dataframes on
        rename (bool, optional): option to rename any values or not. Defaults to False.
        rename_data (dict, optional): data for renaming. Defaults to {}.
        fill_missing (bool, optional): fill in missing data or not. Defaults to False.
        missing_values (dict, optional): missing data values. Defaults to {}.

    Raises:
        ValueError: if rename is set to true but no data provided
        ValueError: if fill_missing is set to true but no data provided

    Returns:
        pd.DataFrame : merged dataframe
    """
    if rename:
        if len(rename_data) == 0:
            raise ValueError('Rename specified as True but no data provided')
        
        df18 = count_unique_items_in_column(df_list[0], column_name).rename(index=rename_data)
    else: 
        df18 = count_unique_items_in_column(df_list[0], column_name)
        
    if fill_missing:
        if len(missing_values) == 0:
            raise ValueError('Fill missing specified as True but no data provided')
        
        if not rename:
            df18 = count_unique_items_in_column(df_list[0], column_name)
            
        for i in missing_values:
            if i not in df18.index.values:
                df18.loc[i] = 0
                
    if not rename and not fill_missing:
        df18 = count_unique_items_in_column(df_list[0], column_name) 
        
    df19 = count_unique_items_in_column(df_list[1], column_name)
    df20 = count_unique_items_in_column(df_list[2], column_name)
    df21 = count_unique_items_in_column(df_list[3], column_name)
    
    l = [df18, df19, df20, df21]

    dfs_merged = _merge(l)
    return dfs_merged
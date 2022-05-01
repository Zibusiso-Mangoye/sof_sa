import pandas as pd
from sof_sa.database import Database
from sof_sa.utility_functions import merge_dfs, replace_na_with_mean, clean_age_column, add_trans_option

def main() -> None:
    
    # extract load data from raw csv files into staging database
    db = Database()
    credentials = db.get_credentials("..\sof_sa\conf\staging_db_credentials.json")

    db.load_data("data\\survey_results_public_2018.csv", "raw_stackoverflow2018", credentials)
    db.load_data("data\\survey_results_public_2019.csv", "raw_stackoverflow2019", credentials)
    db.load_data("data\\survey_results_public_2020.csv", "raw_stackoverflow2020", credentials)
    db.load_data("data\\survey_results_public_2021.csv", "raw_stackoverflow2021", credentials)

    # load data from staging db
    df2018 = db.get_data_from_db("..\sof_sa\SQL\select_2018_data.sql", credentials)
    df2019 = db.get_data_from_db("..\sof_sa\SQL\select_2019_data.sql", credentials)
    df2020 = db.get_data_from_db("..\sof_sa\SQL\select_2020_data.sql", credentials)
    df2021 = db.get_data_from_db("..\sof_sa\SQL\select_2021_data.sql", credentials)

    # transform that data
    # Question 1 
    dataframes = [df2018, df2019, df2020, df2021]
    # Languages
    languages = merge_dfs(dataframes, 'language_worked_with')
    future_languages = merge_dfs(dataframes, 'language_desire_next_year')

    # databases
    databases = merge_dfs(dataframes, 'database_worked_with')
    future_databases = merge_dfs(dataframes, 'database_desire_next_year')

    # platforms
    platforms = merge_dfs(dataframes, 'platform_worked_with')
    future_platforms = merge_dfs(dataframes, 'platform_desire_next_year')

    # web_frameworks
    web_frameworks = merge_dfs(dataframes, 'web_framework_have_worked_with')
    future_web_frameworks = merge_dfs(dataframes, 'web_framework_want_to_work_with')
    
    # Question 2
    replace_na_with_mean(df2018, 'age')
    replace_na_with_mean(df2019, 'age')
    replace_na_with_mean(df2020, 'age')
    replace_na_with_mean(df2021, 'age')

    df2018['age'] = df2018['age'].apply(clean_age_column)
    df2019['age'] = df2019['age'].apply(clean_age_column)
    df2020['age'] = df2020['age'].apply(clean_age_column)
    df2021['age'] = df2021['age'].apply(clean_age_column)
    
    # In the 2018 dataset the choices were male and female but in other datasets its man and woman so changing the 2018 dataset index
    list_of_choices = []
    for item in df2018['gender'].to_list():
        if isinstance(item, type(None)):
            list_of_choices.append(item)
            
        if isinstance(item, str):
            if 'Male' in item:
                list_of_choices.append(item.replace('Male', 'Man'))
            elif 'Female' in item:
                list_of_choices.append(item.replace('Female', 'Woman'))
            else:
                list_of_choices.append(item)
    
    df2018['gender'] = list_of_choices
    
    df2019['gender'] = add_trans_option(df2019)
    df2020['gender'] = add_trans_option(df2020)
    df2021['gender'] = add_trans_option(df2021)

    gender = merge_dfs(dataframes, 'gender')
    # load that data to production db
    
if __name__ == 'main':
    main()
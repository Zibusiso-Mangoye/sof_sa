from platform import platform
from sof_sa.database import Database
from sof_sa.utility_functions import merge_dfs
from sof_sa.transform import replace_na_with_mean_in_age_column, clean_age_column, add_transgender_option


def main() -> None:
    
    # extract load data from raw csv files into staging database
    db = Database()
    staging_credentials = db.get_credentials("..\sof_sa\conf\staging_db_credentials.json")
    db.load_data_into_db("raw_stackoverflow2018", staging_credentials, "..\\data\\survey_results_public_2018.csv")
    db.load_data_into_db("raw_stackoverflow2019", staging_credentials, "..\\data\\survey_results_public_2019.csv")
    db.load_data_into_db("raw_stackoverflow2020", staging_credentials, "..\\data\\survey_results_public_2020.csv")
    db.load_data_into_db("raw_stackoverflow2021", staging_credentials, "..\\data\\survey_results_public_2021.csv")

    # load data from staging db
    df2018 = db.get_data_from_db("..\sof_sa\SQL\select_2018_data.sql", staging_credentials)
    df2019 = db.get_data_from_db("..\sof_sa\SQL\select_2019_data.sql", staging_credentials)
    df2020 = db.get_data_from_db("..\sof_sa\SQL\select_2020_data.sql", staging_credentials)
    df2021 = db.get_data_from_db("..\sof_sa\SQL\select_2021_data.sql", staging_credentials)

    # transform that data
    # Question 1 
    dataframes = [df2018, df2019, df2020, df2021]
    
    # Languages
    languages = merge_dfs(dataframes, 'language_worked_with')
    future_languages = merge_dfs(dataframes, 'language_desire_next_year')

    # databases
    databases = merge_dfs(dataframes, 'database_worked_with', rename=True, 
                          rename_data={'SQL Server': 'Microsoft SQL Server', 'IBM Db2': 'IBM DB2', 'Amazon DynamoDB': 'DynamoDB'},
                          fill_missing=True, missing_values=['Cassandra', 'Couchbase', 'Firebase'])
    
    future_databases = merge_dfs(dataframes, 'database_desire_next_year', rename=True, 
                          rename_data={'SQL Server': 'Microsoft SQL Server', 'IBM Db2': 'IBM DB2', 'Amazon DynamoDB': 'DynamoDB'},
                          fill_missing=True, missing_values=['Couchbase', 'Firebase'])

    # Platforms
    platforms = merge_dfs(dataframes, 'platform_worked_with', rename=True, 
                          rename_data={'Google Cloud Platform/App Engine': 'Google Cloud Platform', 'Azure': 'Microsoft Azure'})

    future_platforms = merge_dfs(dataframes, 'platform_desire_next_year', rename=True, 
                          rename_data={'Google Cloud Platform/App Engine': 'Google Cloud Platform', 'Azure': 'Microsoft Azure'})
    
    # web_frameworks
    web_frameworks = merge_dfs(dataframes, 'web_framework_have_worked_with', rename=True, 
                               rename_data={'React': 'React.js', 'Angular': 'Angular.js', 'Angular/Angular.js': 'Angular.js'}, 
                               fill_missing=True, missing_values=['ASP.NET', 'jQuery', 'Vue.js', 'Flask', 'Laravel',  'Express', 'Ruby on Rails', 'Drupal'])

    future_web_frameworks = merge_dfs(dataframes, 'web_framework_want_to_work_with', rename=True, 
                               rename_data={'React': 'React.js', 'Angular': 'Angular.js', 'Angular/Angular.js': 'Angular.js'}, 
                               fill_missing=True, missing_values=['ASP.NET', 'jQuery', 'Vue.js', 'Flask', 'Laravel',  'Express', 'Ruby on Rails', 'Drupal'])
    
    # Question 2
    replace_na_with_mean_in_age_column(df2018, 'age')
    replace_na_with_mean_in_age_column(df2019, 'age')
    replace_na_with_mean_in_age_column(df2020, 'age')
    replace_na_with_mean_in_age_column(df2021, 'age')

    df2018['age'] = df2018['age'].apply(clean_age_column)
    df2019['age'] = df2019['age'].apply(clean_age_column)
    df2020['age'] = df2020['age'].apply(clean_age_column)
    df2021['age'] = df2021['age'].apply(clean_age_column)
    
    age = merge_dfs(dataframes, 'age')
    
    df2019['gender'] = add_transgender_option(df2019)
    df2020['gender'] = add_transgender_option(df2020)
    df2021['gender'] = add_transgender_option(df2021)

    gender = merge_dfs(dataframes, 'gender', rename=True, rename_data={'Male': 'Man', 'Female': 'Woman'})
    
    # load that data to production db
    production_credentials = db.get_credentials("..\sof_sa\conf\prod_db_credentials.json")
    db.load_data_into_db("languages", production_credentials, languages)
    db.load_data_into_db("future_languages", production_credentials, future_languages)
    db.load_data_into_db("databases", production_credentials, databases)
    db.load_data_into_db("future_databases", production_credentials, future_databases)
    db.load_data_into_db("platforms", production_credentials, platforms)
    db.load_data_into_db("future_platforms", production_credentials, future_platforms)
    db.load_data_into_db("web_frameworks", production_credentials, web_frameworks)
    db.load_data_into_db("future_web_frameworks", production_credentials, future_web_frameworks)
    db.load_data_into_db("age", production_credentials, age)
    db.load_data_into_db("gender", production_credentials, gender)
    

if __name__ == 'main':
    main()
import os
import logging
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from utility_functions import get_credentials, open_db, remove_outlier, add_year, replace_with_mean, clean_gender_column, clean_ethnicity_column


with open('./SQL/select_2018_data.sql', 'r') as f18, open('./SQL/select_2019_data.sql', 'r') as f19, open('./SQL/select_2020_data.sql', 'r') as f20:
    select_query_18 = f18.read()
    select_query_19 = f19.read()
    select_query_20 = f20.read()
    
credentials = get_credentials(".\conf\staging_db_credentials.json")
   
with open_db(credentials) as conn:
    df18 = pd.read_sql(select_query_18, index_col='Respondent', con=conn)
    df19 = pd.read_sql(select_query_19, index_col='Respondent', con=conn)
    df20 = pd.read_sql(select_query_20, index_col='Respondent', con=conn)

if (df18.shape[0] != 0 and df19.shape[0] != 0 and  df20.shape[0] != 0):
    logging.info("READING DATA FROM DATABASE COMPLETED")

# Cleaning the data 
try:
    # Adding a column Year to each dataframe to easily categorize the data by year 
    df18 = add_year(df18, 2018)
    df19 = add_year(df19, 2019)
    df20 = add_year(df20, 2020)

    # In the 2018 dataframe the column Age is in range form.
    # Problem : Age in 2018 was recorded as a range however in 2019 and 2020 it was recorded as a sinlge 
    #           value hence data in the column Age do not match. 
    # Solution: Take the mean of each range in the 2018 column and set that to Age for that particular
    #           column (for example a Age entry with range 28-32 will be replaced by 30)
    
    alist = list(df18['Age'])
    new_age = []

    # Calculating the average of the range chosen and adding it as the age
    # The records with age as Under 18 years old and 65 years or older will be replace by 18 and 65 
    for age in alist:
        if age != None:
            if '-' in age:
                age1 = int(age.split(' ')[0])
                age2 = int(age.split(' ')[2])
                new_age.append((age1 + age2)/2)
            elif age == "Under 18 years old":
                age_u18 = int(age.split(' ')[1])
                new_age.append(age_u18)
            elif age == "65 years or older":
                age_u18 = int(age.split(' ')[0])
                new_age.append(age_u18)
        else:
            new_age.append(age)

    # replacing the column Age with the new ages
    df18['Age'] = new_age

    # replacing the missing age values with the mean of the column
    df18 = replace_with_mean(df18)
    df19 = replace_with_mean(df19)
    df20 = replace_with_mean(df20)

    # Making column Age the correct data type
    df18.Age = df18.Age.astype(int)

    # Exploring the Gender column
    # Removing ambiguity in the gender column
    df18['Gender'] = clean_gender_column(df18)
    df19['Gender'] = clean_gender_column(df19)
    df20['Gender'] = clean_gender_column(df20)

    # Normalizing the columns of df_2019 and df_2020 
    converted_gender_names = {"Gender": {"Man": "Male", "Woman": "Female"}}
    df19.replace(converted_gender_names, inplace=True) 
    df20.replace(converted_gender_names, inplace=True)

    # Merging the Gender and Trans columns in the 2019 and 2020 datasets since the option was offered under Gender in 2018
    # For the 2020 dataset
    conditions_df_2019 = [
        df19['Gender'].eq('Male') & df19['Trans'].eq('Yes'),
        df19['Gender'].eq('Male') & df19['Trans'].eq('No'),
        df19['Gender'].eq('Female') & df19['Trans'].eq('Yes'),
        df19['Gender'].eq('Female') & df19['Trans'].eq('No'),
        df19['Gender'].eq(np.nan) & df19['Trans'].eq('Yes'),
        df19['Gender'].eq(np.nan) & df19['Trans'].eq('No'),
    ]
    choices_df_2020 = ['Transgender','Male','Transgender','Female', 'Transgender', np.nan]
    df19['Gender'] = np.select(conditions_df_2019, choices_df_2020, default=0)

    # For the 2020 dataset
    conditions_df_2020 = [
        df20['Gender'].eq('Male') & df20['Trans'].eq('Yes'),
        df20['Gender'].eq('Male') & df20['Trans'].eq('No'),
        df20['Gender'].eq('Female') & df20['Trans'].eq('Yes'),
        df20['Gender'].eq('Female') & df20['Trans'].eq('No'),
        df20['Gender'].eq(np.nan) & df20['Trans'].eq('Yes'),
        df20['Gender'].eq(np.nan) & df20['Trans'].eq('No')
    ]
    choices_df_2020 = ['Transgender','Male','Transgender','Female', 'Transgender', np.nan]
    df20['Gender'] = np.select(conditions_df_2020, choices_df_2020, default=0)

    # Standardizing the JobSatisfaction column in the 2018 dataset
    l = {"JobSatisfaction" : {'Moderately satisfied':'Slightly satisfied', 'Moderately dissatisfied':'Slightly dissatisfied', 
                            'Extremely dissatisfied':'Very dissatisfied', 'Extremely satisfied':'Very satisfied'}}
    df18.replace(l, inplace=True)

    # Exploring the ethnicity column
    # Removing ambiguity in the gender column
    df18['Ethnicity'] = clean_ethnicity_column(df18)
    df19['Ethnicity'] = clean_ethnicity_column(df19)
    df20['Ethnicity'] = clean_ethnicity_column(df20)

    # The 2018 and 2019 datasets have similar values in the Ethnicity column except for addition of 'Multiracial' and
    # 'Biracial'. However the 2020 dataset has some inconsistences when compared with the other datasets therefore 
    # renaming values in the 2020 dataset.
    l_ethnicity = {"Ethnicity" : {'Indigenous (such as Native American, Pacific Islander, or Indigenous Australian)':'Native American, Pacific Islander, or Indigenous Australian',
     'Hispanic or Latino/a/x':'Hispanic or Latino/Latina'}}
    df20.replace(l_ethnicity, inplace=True) 

    # Merging the datasets
    df = pd.concat([df18, df19, df20])

    # The number of missing values in the salary column is to big and replacing the missing values with mean
    # will greatly affect the outcome of the analysis, therefore all missing values in the salary column
    # are dropped
    df = df[df['Salary'].notna()]

    # Now that all numeric columns do not contain nan's, fillna can be used to fill missing values in all 
    # other columns of type object 
    df.fillna('none', inplace=True)

    # Now outliers will be removed from columns containing numeric data namely Age and Salary 
    df = remove_outlier(df, 'Age')
    df = remove_outlier(df, 'Salary')

    # Since respondent ID is a randomized value it is only for maintaining uniqueness therefore resetting 
    # it will not affect the analysis resetting Respondent column from random values to ordered values 
    # going from 1,2...
    nlist = list(np.arange(df.shape[0]))
    df['Respondent'] = nlist
    df.set_index('Respondent', inplace=True)

    # Other columns do not need cleaning at this stage because their entries can be used for different purposes
    # so thats when the proper cleaning will be applied.
    logging.info("DATASET CONTAINS %s COLUMNS AND %s ROWS", df.shape[1], df.shape[0])
    logging.info("DATA CLEANING COMPLETE")
    logging.info(">> TRANSFORMATION PROCESS COMPLETED SUCCESSFULLY")

except Exception as e:
    logging.exception(e) 

# Loading data into production database
cols_interested_in = {
    "respondent_tbl" : ['Gender', 'Ethnicity', 'Age', 'Year'],
    "currtech_tbl" : ['DatabaseWorkedWith', 'LanguageWorkedWith', 'PlatformWorkedWith', 'FrameworkWorkedWith', 'Year'],
    "sat_tbl" : ['FormalEducation', 'Salary', 'JobSatisfaction', 'Year'],
    "dev_tbl" : ['DevType', 'Year']}

# creating tables
respondent_table = df[cols_interested_in['respondent_tbl']]
curtech_table = df[cols_interested_in['currtech_tbl']]
sat_table = df[cols_interested_in['sat_tbl']]
dev_table = df[cols_interested_in['dev_tbl']]

# loading the tables to the database
credentials_prod = get_credentials(".\conf\staging_db_credentials.json")

with open_db(credentials_prod) as connection:
    respondent_table.to_sql('respondents', con=connection, if_exists='replace')
    curtech_table.to_sql('current_tech', con=connection, if_exists='replace')
    sat_table.to_sql('satisfaction', con=connection, if_exists='replace')
    dev_table.to_sql('developer_types', con=connection, if_exists='replace') 

logging.info(">> LOADING DATABASE TO TARGET DATABASE COMPLETED SUCCESSFULLY")
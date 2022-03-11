import pandas as pd
from extract import extract_raw_data

'''
# The url that contains salary data 
url = 'https://www.globalbrainforce.com/blog/software-developer-salary-around-the-world/'

# Scrape the web for the table
web_data = scrape_data(url)



# Load the data to a staging database
load_raw_data_to_db(web_data, sofraw_df20, sofraw_df21)

# transform the data and load to production database'''

print(get_credentials("sof_sa\conf\staging_db_credentials.json"))

from utility_functions import count_unique_items_in_column, merge_dfs

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
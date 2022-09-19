# """
# This is a boilerplate pipeline 'data_engineering'
# generated using Kedro 0.18.2
# """
from .nodes import count_unique_items_in_column, rename_values_in_col_on_index, merge_dfs_on_index, add_missing_values_in_index
from kedro.pipeline import Pipeline, node, pipeline

platform = [
    node(
        name= 'count_unique_items_in_2018_dataset',
        func= count_unique_items_in_column,
        inputs=['2018_dataset', 'params:database_desire_next_year'],
        outputs=['2018_processed_counting']
    ),
    node(
        name= 'rename_items_in_2018_dataset',
        func= rename_values_in_col_on_index,
        inputs=['2018_processed_counting', 'params:database_desire_next_year'],
        outputs=['2018_processed_renaming']
    ),
    node(
        name= 'add_missing_values_in_index_in_2018_dataset',
        func= add_missing_values_in_index,
        inputs=['2018_processed_renaming', 'params:database_desire_next_year'],
        outputs=['2018_processed']
    ),
    node(
        name= 'count_unique_items_in_2019_dataset',
        func= count_unique_items_in_column,
        inputs=['2019_dataset', 'params:database_desire_next_year'],
        outputs=['2019_processed']
    ),
    node(
        name= 'count_unique_items_in_2020_dataset',
        func= count_unique_items_in_column,
        inputs=['2020_dataset', 'params:database_desire_next_year'],
        outputs=['2020_processed']
    ),
    node(
        name= 'count_unique_items_in_2021_dataset',
        func= count_unique_items_in_column,
        inputs=['2021_dataset', 'params:database_desire_next_year'],
        outputs=['2021_processed']
    ),
    node(
        name= 'merge',
        func= merge_dfs_on_index,
        inputs=['2018_processed', '2019_processed', '2020_processed', '2021_processed', 'params:years'],
        outputs=['platforms']
    )
]

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        platform
    )
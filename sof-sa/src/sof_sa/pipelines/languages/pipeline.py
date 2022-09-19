from kedro.pipeline import Pipeline, node, pipeline
from .nodes import count_unique_items_in_column, merge_dfs_on_index

def create_pipeline(**kwargs) -> Pipeline:
    
    column = 'params:languages'
    return pipeline([
        node(
            name= 'count_unique_items_in_2018_dataset',
            func= count_unique_items_in_column,
            inputs=['2018_dataset', column],
            outputs=['2018_processed']
            ),
        node(
            name= 'count_unique_items_in_2019_dataset',
            func= count_unique_items_in_column,
            inputs=['2019_dataset', column],
            outputs=['2019_processed']
            ),
        node(
            name= 'count_unique_items_in_2020_dataset',
            func= count_unique_items_in_column,
            inputs=['2020_dataset', column],
            outputs=['2020_processed']
            ),
        node(
            name= 'count_unique_items_in_2021_dataset',
            func= count_unique_items_in_column,
            inputs=['2021_dataset', column],
            outputs=['2021_processed']
            ),
        node(
            name= 'merge',
            func= merge_dfs_on_index,
            inputs=['2018_processed', '2019_processed', '2020_processed', '2021_processed', 'params:years'],
            outputs=['languages']
            )
    ])

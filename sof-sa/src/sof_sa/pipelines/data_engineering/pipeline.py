"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            lambda x: x,
            name = 'load_data_into_db',
            inputs=['public_2018_data', 'public_2019_data', 'public_2020_data', 'public_2021_data'],
            outputs=['2018_dataset', '2019_dataset', '2020_dataset', '2021_dataset']
    
        )
    ])

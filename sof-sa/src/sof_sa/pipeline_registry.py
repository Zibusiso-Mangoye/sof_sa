"""Project pipelines."""

import pandas as pd
from kedro.pipeline import Pipeline, node, pipeline

from .pipelines import languages, databases, cloud_platforms, web_frameworks

def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    languages_pipeline = languages.create_pipeline()
    databases_pipeline = databases.create_pipeline()
    cloud_platforms_pipeline = cloud_platforms.create_pipeline()
    web_frameworks_pipeline = web_frameworks.create_pipeline()
    
    return {
        "languages_pipeline": languages_pipeline,
        "databases_pipeline": databases_pipeline,
        "cloud_platforms_pipeline": cloud_platforms_pipeline,
        "web_frameworks_pipeline": web_frameworks_pipeline,
        "load_data": pipeline([
            node(
                name='load_2018_data',
                # Kedro takes care of loading and retrieving data from the database using its catalog system.
                # The input would be a csv catalog entry and output a postgres catalog entry.
                func=lambda x: x, 
                inputs='public_2018_data',
                outputs='raw_stackoverflow2018'
            ),
            node(
                name='load_2019_data',
                func=lambda x: x,
                inputs='public_2019_data',
                outputs='raw_stackoverflow2019'
            ),
            node(
                name='load_2020_data',
                func=lambda x: x,
                inputs='public_2020_data',
                outputs='raw_stackoverflow2020'
            ),
            node(
                name='load_2021_data',
                func=lambda x: x,
                inputs='public_2021_data',
                outputs='raw_stackoverflow2021',
                
            )
        ])
        }

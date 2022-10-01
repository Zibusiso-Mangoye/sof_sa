# Languages pipeline

## Overview

This pipeline:
- Uses a SELECT query to filter columns from a staging database based on year
    - A [MemoryDataSet](https://kedro.readthedocs.io/en/stable/kedro.io.MemoryDataSet.html) are returned for each year
- For each year
    - The languages column is filtered
    - Transformed 
- The transformed datasets are merged into a table `Languages`

## Flow
![img](kedro_pipeline_languages.png)*Flow of the full pipeline visualized*

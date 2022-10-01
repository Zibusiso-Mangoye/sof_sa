# Pipeline cloud_platforms

## Overview

This pipeline:
- Uses a SELECT query to filter columns from a staging database based on year
    - A [MemoryDataSet](https://kedro.readthedocs.io/en/stable/kedro.io.MemoryDataSet.html) are returned for each year
- For each year
    - The plpatforms column is filtered
    - Transformed 
- The transformed datasets are merged into a table `platforms`

## Flow
![img](kedro-pipeline-platforms.png)*Flow of the full pipeline visualized*

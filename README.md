# sof_sa
## Analyzing past and current trends in software engineering and development using Stack Overflow Developer Survey data

### Table of Contents
- Introduction
- What I learned
- Project Architecture
- Getting Started
    - Prerequisites
    - Installation
    - Running the project
    - Built with
- Results
- Author 

## Introduction 

For this project, I was interestested in using Stack Overflow's annual developer survey responses from 2018 to 2021 in order to better understand:

### *How much impact has the pandemic had on developer's choice of tech stack?*
This is question is broken down to four parts:
- Which programming languages have gained popularity from 2018 to 2021?
- Which database services have gained popularity from 2018 to 2021?
- Which cloud platforms have gained popularity from 2018 to 2021?
- Which web frameworks have gained popularity from 2018 to 2021?

## What I learned 

- How to extract, transform and load data using pandas and Numpy 
- Data Modelling 
- Writing SQL queries and how to execute SQL in python 
- Using Postgres with python

## Project Architecture 
![img](imgs/Batch_Processing_pipeline.jpg)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

-  Virtualenv for package management

        python -m pip install --user virtualenv
    More details about virtualenv [here](https://virtualenv.pypa.io/en/latest/user_guide.html#introduction)

- An active instance of PostgreSQL on your local machine or on the cloud 
    To install PostgreSQL on your local host follow the instructions provided in the official documentation [here](https://www.postgresql.org/docs/current/tutorial-install.html)
    For cloud based instances follow the instructions provided by the cloud provider.

- The data used in this project was downloaded from [StackOverflow](https://insights.stackoverflow.com/survey)

### Installation

        git clone <repo>
        cd <repo>
        virtualenv venv 
to create your new environment (called 'venv' here)

        source venv/bin/activate 
to activate the virtual environment

        pip install -r requirements.txt 
to install the requirements in the current environment.

### Running the project

        kedro run
 
- This runs the whole ETL process. The outcome is a production database instance on Postgres.
- Check the notebooks folder for a more detailed explanation of the etl process. 

### Built With

- Python - ETLprocess
- PostgreSQL - Data Storage
- virtualenv - Package management
- Power BI - Data Visualization

## Results

The main findings of the report can be found at the post available here(report under construction).

## Author 

- Zibusiso Mangoye
    [linkedIn](https://www.linkedin.com/in/zibusiso-n-mangoye-411227173)

## License
This project is offered under the GNU GENERAL PUBLIC LICENSE V3, 2007 for more read [LICENSE](LICENSE) 

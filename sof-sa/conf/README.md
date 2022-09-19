This folder should be used to store configuration files used by Kedro or by separate tools.

## Local configuration

The `local` folder should be used for configuration that is either user-specific (e.g. IDE configuration) or protected (e.g. security keys).

> *Note:* Please do not check in any local configuration to version control.

## Base configuration

The `base` folder is for shared configuration, such as non-sensitive and project-related configuration that may be shared across team members.

WARNING: Please do not put access credentials in the base configuration folder.

## Instructions

create a `credentials.yml` file in the local directory if it does not exist.
In the `credentials.yml` file put your database connection strings for staging and production.
An example credentials.yml file:
```
    dev_postgres:
        con: postgresql+psycopg2://username:password@host:port/database_name

    prod_postgres:
        con: postgresql+psycopg2://username:password@host:port/database_name
```
This example shows the required information in order to connect to a postgres database.

## Find out more
You can find out more about configuration from the [user guide documentation](https://kedro.readthedocs.io/en/stable/04_user_guide/03_configuration.html).

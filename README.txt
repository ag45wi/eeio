Web interface can be accessed via: https://inovasitiadahenti.com/eeio

Python version: 3.10.11
requirement file for dependecies: reqs.txt

Database for user login: MySQL
    Configuration file: db_config.py
    Create db & table:
        create database db_eeio;
        use db_eeio;
        CREATE TABLE user (
            userid varchar(100) NOT NULL UNIQUE PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE
        );

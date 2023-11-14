# SARBase

An attempt to create search and rescue database for logging SAR jobs and activities.

(c) 2019-2023 Vadim Likholetov


# How to prepare MySQL database

    mysql> CREATE DATABASE sarbaseapp;
    mysql> CREATE USER 'sarbaseuser'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON sarbaseapp.* TO 'sarbaseuser'@'localhost';
    mysql> SET @@GLOBAL.sql_mode := REPLACE(@@GLOBAL.sql_mode, 'NO_ZERO_DATE', '');
    mysql> FLUSH PRIVILEGES;
    mysql> EXIT;



#!/bin/bash

echo Initialising the database...

mysql -u root --password=password  sarbaseapp <  /docker-entrypoint-initdb.d/mysql_dump.sql


import os

dbuser = os.environ.get('MYSQL_USER', 'root')
dbpassword = os.environ.get('MYSQL_PASSWORD', 'bebrasus69')
dbhost = os.environ.get('MYSQL_HOST', 'localhost')
dbport = os.environ.get('MYSQL_PORT', '3306')
dbname = os.environ.get('MYSQL_DATABASE', 'se_backend')

dbtype = "mysql"
dbdriver = "pymysql"


# DATABASE USER COLUMNS CONFIG
email_length = 32
name_length = 16
password_length = 32
token_length = 32


# DATABASE PUBLICATION COLUMNS CONFIG
text_length = 3000
title_length = 100
description_length = 250
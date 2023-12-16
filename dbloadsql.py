import json
import os
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import connect

load_dotenv("creds.env")

# Get MySQL connection details from environment variables
db_user = os.environ.get("MYSQL_USER")
db_password = os.environ.get("MYSQL_PASSWORD")
db_host = os.environ.get("MYSQL_HOST")
db_name = os.environ.get("MYSQL_DATABASE")

# SSL configuration
ssl_ca = os.environ.get("MYSQL_SSL_CA")


print(db_user,db_password,db_host,db_name)

# Establish MySQL connection with SSL
mysql_config = {
    'user':db_user,
    'password':db_password,
    'host':db_host,
    'database':db_name,
    'ssl_ca':ssl_ca
}

#print(mysql_config)
# JSON file path
json_file_path = '/Users/asampathkuma/Downloads/Project4000/data4.json'

# MySQL connection
connection = mysql.connector.connect(**mysql_config)
cursor = connection.cursor()

# Read and parse JSON file
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Loop through each record in the JSON data
for record in data.get('MasterSheet', []):
    # Define the MySQL insert query
    insert_query = """
    INSERT INTO PasuramsArthamTable
    (Sno, Prabandham, PasuramNumber, Pasuram, PattuNumber, Word, Padham, Meaning, Alzwar, PadhamNumber)
    VALUES (%(Sno)s, %(Prabandham)s, %(PasuramNumber)s, %(Pasuram)s, %(PattuNumber)s, %(Word)s, %(Padham)s,  %(Meaning)s, %(Alzwar)s, %(PadhamNumber)s)
    """
    print(record)
    # Execute the insert query with the current record
    cursor.execute(insert_query, record)

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()

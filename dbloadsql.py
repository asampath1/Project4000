import json
import os
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import connect

load_dotenv("dbcreds.env")
load_dotenv("dbcreds.env")

# Get MySQL connection details from environment variables
db_host= os.getenv("DB_HOST")
db_user=os.getenv("DB_USERNAME")
db_passwd= os.getenv("DB_PASSWORD")
db_name= os.getenv("DB_NAME")
db_port=os.getenv("DB_PORT")
db_ssl_ca=os.getenv("DB_SSL_CA")

print("SSL CA Path:", db_ssl_ca)

db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    user=db_user,
    password=db_passwd,
    host=db_host,
    port=db_port,
    database=db_name,
    ssl_ca=db_ssl_ca
)


#print(mysql_config)
# JSON file path
json_file_path = '/Users/asampathkuma/Downloads/Project4000/data4.json'

# MySQL connection
connection = db_pool.get_connection()
cursor = connection.cursor(dictionary=True)

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
   # print(record)
    # Execute the insert query with the current record
    cursor.execute(insert_query, record)

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()

import json
import mysql.connector

# MySQL connection details
mysql_config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'password',
    'database': 'tamildb'
}

# JSON file path
json_file_path = '/Users/asampathkuma/Downloads/4K Pasuram/data4.json'

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
    #print(record)
    # Execute the insert query with the current record
    cursor.execute(insert_query, record)

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()

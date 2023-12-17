from flask import Flask, render_template, request
import mysql.connector
import mysql.connector.pooling
from mysql.connector.constants import ClientFlag
from mysql.connector import connect
import os
from dotenv import load_dotenv
load_dotenv("dbcreds.env")

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

print('MYSQL_CONFIG', mysql_config)

app = Flask(__name__)

def execute_query(query, params=None):
    cursor.execute(query, params)
    return cursor.fetchall()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Route for the first search query
@app.route('/search1', methods=['POST'])
def search1():
    if request.method == 'POST':
        search_term = request.form['search_term']

        # MySQL connection
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor(dictionary=True)

        # Execute the search query
        search_query = f"SELECT * FROM PasuramsArthamTable WHERE Word LIKE '%{search_term}%'"
        cursor.execute(search_query)
        results = cursor.fetchall()

        # Close the MySQL connection
        cursor.close()
        connection.close()

        # Process the data to group by Pasuram and list words with meanings
        processed_results = []
        pasurams_seen = set()

        for result in results:
            pasuram_key = str(result['PasuramNumber'])+ ' ' + result['Prabandham'] + ' ' + str(result['PattuNumber'])
            Padham_Number = str(result['PadhamNumber'])
            if pasuram_key not in pasurams_seen:
                pasurams_seen.add(pasuram_key)
                # Add pasuram once
                processed_results.append({
                    'Prabandham': pasuram_key,
                    'Pasuram': result['Pasuram'],
                    'Words': [{'Padham_Number':Padham_Number,'Word': result['Word'], 'Meaning': result['Meaning']}]
                })
            else:
                # Add word with meaning
                for pasuram in processed_results:
                    if pasuram['Pasuram'] == result['Pasuram']:
                        pasuram['Words'].append({'Word': result['Word'], 'Meaning': result['Meaning']})
                        break

        return render_template('index.html', results=processed_results, search_term=search_term)

    return render_template('index.html', results=None, search_term=None)

@app.route('/search2', methods=['POST'])
def search2():
    if request.method == 'POST':
        search_term = request.form['search_term']

        # MySQL connection
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor(dictionary=True)

        # Execute the search query '%{search_term}%'
        #search_query = f"SELECT * FROM tamildb.PasuramsArthamTable WHERE Pasuram LIKE '(%{search_term}%)' OR PasuramNumber = {search_term}"
        #cursor.execute(search_query)
        search_query = "SELECT * FROM tamildb.PasuramsArthamTable WHERE Pasuram LIKE %s OR PasuramNumber = %s"
        cursor.execute(search_query, ('%' + search_term + '%', search_term))

        results = cursor.fetchall()

        # Close the MySQL connection
        cursor.close()
        connection.close()

        # Process the data to group by Pasuram and list words with meanings
        processed_results = []
        pasurams_seen = set()

        for result in results:
            pasuram_key = str(result['PasuramNumber'])+ ' ' + result['Prabandham'] + ' ' + str(result['PattuNumber'])
            Padham_Number = str(result['PadhamNumber'])
            if pasuram_key not in pasurams_seen:
                pasurams_seen.add(pasuram_key)
                # Add pasuram once
                processed_results.append({
                    'Prabandham': pasuram_key,
                    'Pasuram': result['Pasuram'],
                    'Words': [{'Padham_Number':Padham_Number,'Word': result['Word'], 'Meaning': result['Meaning']}]
                })
            else:
                # Add word with meaning
                for pasuram in processed_results:
                    if pasuram['Pasuram'] == result['Pasuram']:
                        pasuram['Words'].append({'Word': result['Word'], 'Meaning': result['Meaning']})
                        break

        return render_template('index.html', results=processed_results, search_term=search_term)

    return render_template('index.html', results=None, search_term=None)

if __name__ == '__main__':
    app.run(debug=True)

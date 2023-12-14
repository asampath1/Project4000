from flask import Flask, render_template, request
import mysql.connector
from mysql.connector.constants import ClientFlag
app = Flask(__name__)

# MySQL connection details
'''
mysql_config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'password',
    'database': 'tamildb'
}
'''
mysql_config = {
    'host': 'aws.connect.psdb.cloud',
    'user': '3l0zksrxndu5y1x7nsx8',
    'password': 'pscale_pw_H8FontNjzCT9wTiGYwfFwxpDuxObaKyNPsQf088hNaN',
    'database': 'tamildb',
    'ssl_ca': '/etc/ssl/cert.pem'
}


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

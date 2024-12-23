from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_cors import CORS
from newtest import submit_prompt
import json
from flask import Flask, jsonify
import pyodbc
import re
import urllib
import ast

strResult = ''

app = Flask(__name__, static_url_path="", static_folder="static")
CORS(app) 

db_config = {
    'username': 'CloudSA18a9a8b4',  
    'password': '?j67XDjSiyQFH=D',               
    'server': 'startechhacx.database.windows.net',  
    'database': 'Sobergraphics'   
}

connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};' \
                    f'SERVER={db_config["server"]};' \
                    f'DATABASE={db_config["database"]};' \
                    f'UID={db_config["username"]};' \
                    f'PWD={db_config["password"]};' \
                    f'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    print(data)
    response = submit_prompt(data['prompt'])
    print("RESPONSE", response)
    data2 = str(response)
    print(response['output'])
    return redirect(url_for('.previewPage', data=response['output'], title=response['title'], image=response['image']))

@app.route('/tidy_json', methods=['POST'])
def tidy_json():
    json_data = request.args.get('data')

    if not json_data:
        return jsonify({"error": "No JSON data provided"}), 400

    cleaned_text = format_json_to_text(json_data)

    return jsonify({"tidied_text": cleaned_text})

def format_json_to_text(data):
    """
    Function to convert JSON data into a tidy text format.
    Adjust the formatting based on your specific requirements.
    """
    lines = []
    
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f" - {item}")
        else:
            lines.append(f"{key}: {value}")

    return "\n".join(lines)

@app.route('/test', methods=['GET'])
def test():
    try:
        conn = pyodbc.connect(connection_string)
        print('after connection')
        conn.close()
        return "Connection to Azure SQL Server successful!"
    except pyodbc.Error as err:
        return f"Error: {err}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['GET'])
def promptPage():
    return render_template('nextpage.html')

@app.route('/result', methods=['GET'])
def previewPage():
    return render_template('poster_trial2.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)


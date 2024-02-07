
from flask import Flask, jsonify, render_template,request
import json
import csv
from math import sqrt
import pandas as pd
import psycopg2
import numpy as np
import joblib
import requests

app = Flask(__name__)

# Configure PostgreSQL connection
DB_NAME = 'Project4'
DB_USER = 'postgres'
DB_PASSWORD = 'Subhan786!'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'

# Connect to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Function to execute a query and fetch data from the database
def fetch_data(query):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return data
    except Exception as e:
        return str(e)
 
# Route to get all data from a specific table
@app.route('/bureau', methods=['GET'])
def Bureau():
    query = "SELECT * FROM bureau LIMIT 99999;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
# Route to get all data from a specific table
@app.route('/bureau_balance', methods=['GET'])
def bureauBalance():
    query = "SELECT * FROM bureau_balance LIMIT 99999;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
# Route to get all data from a specific table
@app.route('/credit_card_balance', methods=['GET'])
def creditCardBalance():
    query = "SELECT * FROM credit_card_balance LIMIT 99999;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
@app.route('/installments_payments', methods=['GET'])
def InstallmentPayment():
    query = "SELECT * FROM installments_payments LIMIT 99999;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
@app.route('/pOS_CASH_balance', methods=['GET'])
def PosCashBalance():
    query = 'SELECT * From "pOS_CASH_balance" LIMIT 99999;'
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500

@app.route('/previous_application', methods=['GET'])
def previousApplication():
    query = "SELECT * From previous_application LIMIT 99999;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
@app.route('/application_train', methods=['GET'])
def applicationTrain():
    query = 'SELECT * From "Application_train" LIMIT 99999;'
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500

@app.route('/api.html')
def api():
    return render_template('api.html')

def create_table():
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS test_applicant (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            "AMT_INCOME_TOTAL" INTEGER,
            job_type VARCHAR(255),
            own_property VARCHAR(3),
            "FLAG_MOBIL" INTEGER,
            "FLAG_OWN_CAR" INTEGER,
            marital_status VARCHAR(255),
            living_arrangement VARCHAR(255),
            education VARCHAR(255),
            years_experience INTEGER
        );
    '''
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

# Call the create_table function to ensure the table is created when the application starts
create_table()

@app.route('/form.html')
def form():
    return render_template('form.html')

@app.route('/submitData', methods=['POST'])
def submit_data():
    try:
        
        data = request.json
        

        query = '''
            INSERT INTO test_applicant (first_name, last_name, "AMT_INCOME_TOTAL", job_type, own_property, 
                                        "FLAG_MOBIL", "FLAG_OWN_CAR", marital_status, living_arrangement, 
                                        education, years_experience)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
        '''

        values = (
            data['firstName'],
            data['lastName'],
            data['AMT_INCOME_TOTAL'],
            data['jobType'],
            data['ownProperty'],
            data['FLAG_MOBIL'],
            data['FLAG_OWN_CAR'],
            data['maritalStatus'],
            data['livingArrangement'],
            data['education'],
            data['yearsExperience'],
        )

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query, values)

        #  # Fetch the last inserted row with the id
        # cursor.execute("SELECT AMT_INCOME_TOTAL, FLAG_MOBIL, FLAG_OWN_CAR FROM test_applicant ORDER BY id DESC LIMIT 1;")
        last_row = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Data submitted successfully!', 'data': last_row})
    
    except Exception as e:
        return jsonify({'error': str(e)})
# New API endpoint to fetch the last row
@app.route('/getLastRow', methods=['GET'])
def get_last_row():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Fetch column names dynamically from information_schema
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'test_applicant';")
        columns = [row[0] for row in cursor.fetchall()]

        # Construct the final SELECT query with case-sensitive column names
        column_names_string = ', '.join(f'"{col}"' for col in columns)
        select_query = f"SELECT {column_names_string} FROM test_applicant ORDER BY id DESC LIMIT 1;"
        cursor.execute(select_query)
        last_row = cursor.fetchone()

        cursor.close()
        conn.close()

        # Combine column names and values in the response
        response_data = dict(zip(columns, last_row))

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)})
    
# Load the machine learning model
model = joblib.load('model1.joblib')

# API endpoint to get input data
INPUT_DATA_API_ENDPOINT = 'http://127.0.0.1:5000/getLastRow'

@app.route('/runModel', methods=['GET'])
def run_model():
    try:
        # Fetch input data from the API
        input_data_response = requests.get(INPUT_DATA_API_ENDPOINT)
        
        if input_data_response.status_code != 200:
            return jsonify({'error': f'Failed to fetch input data. Status code: {input_data_response.status_code}'})
        
        input_data = input_data_response.json()

        # Create a DataFrame with feature names
        features = pd.DataFrame({
            'AMT_INCOME_TOTAL': [input_data["AMT_INCOME_TOTAL"]],
            'FLAG_MOBIL': [input_data["FLAG_MOBIL"]],
            'FLAG_OWN_CAR': [input_data["FLAG_OWN_CAR"]]
        })

        # Assuming 'model' is a classifier (e.g., RandomForestClassifier)
        probability_result = model.predict_proba(features)[:, 1]  # Extract the probability for class 1

        # Round the probability result to two decimal places
        probability_result_rounded = round(probability_result.item(), 2)

        return jsonify({'probability_result': [[probability_result_rounded]]})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

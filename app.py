
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
DB_NAME = 'project4'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
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
@app.route('/pos_cash_balance', methods=['GET'])
def PosCashBalance():
    query = 'SELECT * From "pos_cash_balance" LIMIT 99999;'
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
    query = 'SELECT * From "application_train" LIMIT 99999;'
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
            "DAYS_ID_PUBLISH" INTEGER,
            "DAYS_BIRTH" INTEGER,
            "DAYS_REGISTRATION" INTEGER,
            "DAYS_LAST_PHONE_CHANGE" INTEGER,
            "AMT_ANNUITY_x" INTEGER,
            "SK_ID_CURR" INTEGER,
            "AMT_CREDIT"INTEGER,
            "DAYS_EMPLOYED" INTEGER,
            "AMT_GOODS_PRICE" INTEGER,
            "AMT_INCOME_TOTAL" INTEGER,
            "HOUR_APPR_PROCESS_START" INTEGER,
            "AMT_REQ_CREDIT_BUREAU_YEAR" INTEGER,
            "OWN_CAR_AGE" VARCHAR(3),
            "OBS_30_CNT_SOCIAL_CIRCLE" VARCHAR(255),
            "OBS_60_CNT_SOCIAL_CIRCLE" VARCHAR(255),
            "AMT_PAYMENT" INTEGER,
            "DAYS_ENTRY_PAYMENT" INTEGER,
            "AMT_INSTALMENT" INTEGER,
            "DAYS_INSTALMENT" INTEGER,
            "NUM_INSTALMENT_NUMBER" INTEGER,
            "CNT_INSTALMENT_FUTURE" INTEGER,
             "MONTHS_BALANCE_x" INTEGER,
            "CNT_FAM_MEMBERS" INTEGER,
            "CNT_INSTALMENT" INTEGER,
            "CNT_INSTALMENT_MATURE_CUM" INTEGER,
            "MONTHS_BALANCE_Credit_card_balance" INTEGER
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

@app.route('/pre_evaluation.html')
def form():
    return render_template('pre_evaluation.html')

@app.route('/submitData', methods=['POST'])
def submit_data():
    try:
        
        data = request.json
        

        query = '''
            INSERT INTO test_applicant (first_name, last_name, "DAYS_ID_PUBLISH", "DAYS_BIRTH", "DAYS_REGISTRATION", "DAYS_LAST_PHONE_CHANGE",
              "AMT_ANNUITY_x", "SK_ID_CURR", "DAYS_EMPLOYED", "AMT_GOODS_PRICE", "AMT_INCOME_TOTAL",
              "HOUR_APPR_PROCESS_START", "AMT_REQ_CREDIT_BUREAU_YEAR", "OWN_CAR_AGE",
              "OBS_30_CNT_SOCIAL_CIRCLE", "OBS_60_CNT_SOCIAL_CIRCLE", "AMT_PAYMENT",
              "DAYS_ENTRY_PAYMENT", "AMT_INSTALMENT", "DAYS_INSTALMENT", "NUM_INSTALMENT_NUMBER",
              "CNT_INSTALMENT_FUTURE", "MONTHS_BALANCE_x", "CNT_FAM_MEMBERS", "CNT_INSTALMENT",
              "CNT_INSTALMENT_MATURE_CUM", "MONTHS_BALANCE_Credit_card_balance")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
model = joblib.load('model_probability.joblib')

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
            "DAYS_ID_PUBLISH": [input_data['DAYS_ID_PUBLISH']],
            "DAYS_BIRTH": [input_data['DAYS_BIRTH']],
            "DAYS_REGISTRATION": [input_data['DAYS_REGISTRATION']],
            "DAYS_LAST_PHONE_CHANGE": [input_data['DAYS_LAST_PHONE_CHANGE']],
            "AMT_ANNUITY_x": [input_data['AMT_ANNUITY_x']],
            "SK_ID_CURR": [input_data['SK_ID_CURR']],
            "DAYS_EMPLOYED": [input_data['DAYS_EMPLOYED']],
            "AMT_GOODS_PRICE": [input_data['AMT_GOODS_PRICE']],
            "AMT_INCOME_TOTAL": [input_data['AMT_INCOME_TOTAL']],
            "HOUR_APPR_PROCESS_START": [input_data['HOUR_APPR_PROCESS_START']],
            "AMT_REQ_CREDIT_BUREAU_YEAR": [input_data['AMT_REQ_CREDIT_BUREAU_YEAR']],
            "OWN_CAR_AGE": [input_data['OWN_CAR_AGE']],
            "OBS_30_CNT_SOCIAL_CIRCLE": [input_data['OBS_30_CNT_SOCIAL_CIRCLE']],
            "OBS_60_CNT_SOCIAL_CIRCLE": [input_data['OBS_60_CNT_SOCIAL_CIRCLE']],
            "AMT_PAYMENT": [input_data['AMT_PAYMENT']],
            "DAYS_ENTRY_PAYMENT": [input_data['DAYS_ENTRY_PAYMENT']],
            "AMT_INSTALMENT": [input_data['AMT_INSTALMENT']],
            "DAYS_INSTALMENT": [input_data['DAYS_INSTALMENT']],
            "NUM_INSTALMENT_NUMBER": [input_data['NUM_INSTALMENT_NUMBER']],
            "CNT_INSTALMENT_FUTURE": [input_data['CNT_INSTALMENT_FUTURE']],
            "MONTHS_BALANCE_x": [input_data['MONTHS_BALANCE_x']],
            "CNT_FAM_MEMBERS": [input_data['CNT_FAM_MEMBERS']],
            "CNT_INSTALMENT": [input_data['CNT_INSTALMENT']],
            "CNT_INSTALMENT_MATURE_CUM": [input_data['CNT_INSTALMENT_MATURE_CUM']],
            "MONTHS_BALANCE_Credit_card_balance": [input_data['MONTHS_BALANCE_Credit_card_balance']]
        })

        # Assuming 'model' is a classifier (e.g., RandomForestClassifier)
        probability_result = model.predict_proba(features)[:, 1]

        # Round the probability result to two decimal places
        probability_result_rounded = round(probability_result.item(), 2)

        return jsonify({'probability_result': [[probability_result_rounded]]})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

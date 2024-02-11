
from flask import Flask, jsonify, render_template,request,redirect
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
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            age INT NOT NULL, 
            email VARCHAR(100) NOT NULL,
            phone_number VARCHAR(10) NOT NULL,
            SK_ID_CURR INT NOT NULL,
            AMT_INCOME_TOTAL FLOAT NOT NULL,
            AMT_REQ_CREDIT_BUREAU_YEAR FLOAT NOT NULL,
            OBS_30_CNT_SOCIAL_CIRCLE FLOAT NOT NULL,
            OBS_60_CNT_SOCIAL_CIRCLE FLOAT NOT NULL,
            AMT_ANNUITY_x FLOAT NOT NULL,
            CNT_INSTALMENT_MATURE_CUM FLOAT NOT NULL,
            AMT_PAYMENT FLOAT NOT NULL,
            DAYS_ENTRY_PAYMENT FLOAT NOT NULL,
            AMT_INSTALMENT FLOAT NOT NULL,
            DAYS_INSTALMENT FLOAT NOT NULL,
            NUM_INSTALMENT_NUMBER FLOAT NOT NULL,
            CNT_INSTALMENT_FUTURE FLOAT NOT NULL,
            CNT_INSTALMENT FLOAT NOT NULL,
            MONTHS_BALANCE_Credit_card FLOAT NOT NULL,
            MONTHS_BALANCE_x FLOAT NOT NULL,
            CNT_FAM_MEMBERS FLOAT NOT NULL,
            OWN_CAR_AGE FLOAT NOT NULL        
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
            INSERT INTO test_applicant (first_name, last_name, age, email, phone_number,CNT_FAM_MEMBERS,
            OWN_CAR_AGE, SK_ID_CURR, AMT_INCOME_TOTAL, AMT_REQ_CREDIT_BUREAU_YEAR, OBS_30_CNT_SOCIAL_CIRCLE, OBS_60_CNT_SOCIAL_CIRCLE,
            AMT_ANNUITY_x, CNT_INSTALMENT_MATURE_CUM, AMT_PAYMENT, DAYS_ENTRY_PAYMENT, AMT_INSTALMENT, DAYS_INSTALMENT,
            NUM_INSTALMENT_NUMBER, CNT_INSTALMENT_FUTURE, CNT_INSTALMENT, MONTHS_BALANCE_Credit_card, 
            MONTHS_BALANCE_x)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            RETURNING *;
        '''

        values = (
            data['firstName'],
            data['lastName'],
            data['age'],
            data['email'],
            data['phoneNumber'],
            data['CNT_FAM_MEMBERS'],
            data['OWN_CAR_AGE'],
            data['SK_ID_CURR'],
            data['AMT_INCOME_TOTAL'],
            data['AMT_REQ_CREDIT_BUREAU_YEAR'],
            data['OBS_30_CNT_SOCIAL_CIRCLE'],
            data['OBS_60_CNT_SOCIAL_CIRCLE'],
            data['AMT_ANNUITY_x'],
            data['CNT_INSTALMENT_MATURE_CUM'],
            data['AMT_PAYMENT'],
            data['DAYS_ENTRY_PAYMENT'],
            data['AMT_INSTALMENT'],
            data['DAYS_INSTALMENT'],
            data['NUM_INSTALMENT_NUMBER'],
            data['CNT_INSTALMENT_FUTURE'],
            data['CNT_INSTALMENT'],
            data['MONTHS_BALANCE_Credit_card'],
            data['MONTHS_BALANCE']            
        ) 

        conn = connect_to_db() 
        cursor = conn.cursor()
        cursor.execute(query, values)

       
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
        select_query = f"SELECT * FROM test_applicant ORDER BY (SELECT NULL) DESC LIMIT 1;"
        cursor.execute(select_query)
        last_row = cursor.fetchone()

        cursor.close()
        conn.close()

        # Check if last_row is not None before trying to iterate over it
        if last_row is not None:
            # Combine column names and values in the response
            response_data = dict(zip(columns, last_row))
            return jsonify(response_data)
        else:
            return jsonify({'error': 'No data found'})

    except Exception as e:
        return jsonify({'error': str(e)})
       
# Load the machine learning model
model = joblib.load('model_probability1.joblib')

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
            "AMT_ANNUITY_x": [input_data['AMT_ANNUITY_x']],
            "SK_ID_CURR": [input_data['SK_ID_CURR']],
            "AMT_CREDIT": [input_data['AMT_CREDIT']],
            "DAYS_EMPLOYED": [input_data['DAYS_EMPLOYED']],
            "AMT_GOODS_PRICE": [input_data['AMT_GOODS_PRICE']],
            "AMT_INCOME_TOTAL": [input_data['AMT_INCOME_TOTAL']],
            "AMT_REQ_CREDIT_BUREAU_YEAR": [input_data['AMT_REQ_CREDIT_BUREAU_YEAR']],
            "OBS_30_CNT_SOCIAL_CIRCLE": [input_data['OBS_30_CNT_SOCIAL_CIRCLE']],
            "OBS_60_CNT_SOCIAL_CIRCLE": [input_data['OBS_60_CNT_SOCIAL_CIRCLE']],
            "AMT_PAYMENT": [input_data['AMT_PAYMENT']],
            "DAYS_ENTRY_PAYMENT": [input_data['DAYS_ENTRY_PAYMENT']],
            "DAYS_INSTALMENT": [input_data['DAYS_INSTALMENT']],
            "AMT_INSTALMENT": [input_data['AMT_INSTALMENT']],
            "NUM_INSTALMENT_NUMBER": [input_data['NUM_INSTALMENT_NUMBER']],
            "CNT_INSTALMENT_MATURE_CUM": [input_data['CNT_INSTALMENT_MATURE_CUM']],
            "CNT_INSTALMENT_FUTURE": [input_data['CNT_INSTALMENT_FUTURE']],
            "CNT_INSTALMENT": [input_data['CNT_INSTALMENT']],
            "MONTHS_BALANCE_x": [input_data['MONTHS_BALANCE']],
            "CNT_FAM_MEMBERS": [input_data['CNT_FAM_MEMBERS']],
            "MONTHS_BALANCE_Credit_card": [input_data['MONTHS_BALANCE_Credit_card']]
        })

        # Assuming 'model' is a classifier (e.g., RandomForestClassifier)
        probability_result = model.predict_proba(features)[:, 1]

        # Round the probability result to two decimal places
        probability_result_rounded = round(probability_result.item(), 2)

        # Determine loan eligibility based on the probability
        loan_eligibility = 'approved' if probability_result_rounded <= 0.25 else 'not approved'

        # Redirect to a new route with the result
        return redirect(f'/result?probability={probability_result_rounded}&eligibility={loan_eligibility}')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/result', methods=['GET'])
def show_result():
    try:
        # Get probability and eligibility from query parameters
        probability = float(request.args.get('probability', 0.0))
        eligibility = request.args.get('eligibility', 'unknown')

        return render_template('result.html', probability=probability, eligibility=eligibility)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Run the application
if __name__ == '__main__':
    app.run(debug=True)

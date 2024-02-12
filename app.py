
from flask import Flask, jsonify, render_template,request
import json
import csv
from math import sqrt
import pandas as pd
import psycopg2
import numpy as np
import joblib
import requests
from datetime import datetime

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
            "SK_ID_CURR" SERIAL PRIMARY KEY,
            "firstName" VARCHAR(255),
            "lastName" VARCHAR(255),
            dob DATE,
            "DAYS_BIRTH" INTEGER,
            email VARCHAR(255),
            "phoneNumber" BIGINT,
            address VARCHAR(255),
            marital_status VARCHAR(255),
            "CNT_FAM_MEMBERS" INTEGER,
            "CNT_CHILDREN" INTEGER,
            "AMT_INCOME_TOTAL" NUMERIC,
            "AMT_GOODS_PRICE" NUMERIC,
            "OWN_CAR_AGE" INTEGER,
            "AMT_CREDIT" NUMERIC,
            "AMT_ANNUITY_x" NUMERIC,
            eod DATE,
            "DAYS_EMPLOYED" INTEGER,
            registeration DATE,
            "DAYS_REGISTRATION" INTEGER,
            identity DATE,
            "DAYS_ID_PUBLISH" INTEGER,
            phone DATE,
            "DAYS_LAST_PHONE_CHANGE" INTEGER,
            "AMT_REQ_CREDIT_BUREAU_QRT" INTEGER,
            "CNT_INSTALMENT" INTEGER,
            "CNT_INSTALMENT_FUTURE" INTEGER
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
        print("Received Data:", data)  # Add this line for logging

        query = '''
            INSERT INTO test_applicant (
                "firstName",
                "lastName",
                dob,
                "DAYS_BIRTH",
                email,
                "phoneNumber",
                address,
                marital_status,
                "CNT_FAM_MEMBERS",
                "CNT_CHILDREN",
                "AMT_INCOME_TOTAL",
                "AMT_GOODS_PRICE",
                "OWN_CAR_AGE",
                "AMT_CREDIT",
                "AMT_ANNUITY_x",
                eod,
                "DAYS_EMPLOYED",
                registeration,
                "DAYS_REGISTRATION",
                identity,
                "DAYS_ID_PUBLISH",
                phone,
                "DAYS_LAST_PHONE_CHANGE",
                "AMT_REQ_CREDIT_BUREAU_QRT",
                "CNT_INSTALMENT",
                "CNT_INSTALMENT_FUTURE"
            )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
        '''

        values = (
            data['firstName'],
            data['lastName'],
            data['dob'],
            data['DAYS_BIRTH'],
            data['email'],
            data['phoneNumber'],
            data['address'],
            data['marital_status'],
            data['CNT_FAM_MEMBERS'],
            data['CNT_CHILDREN'],
            data['AMT_INCOME_TOTAL'],
            data['AMT_GOODS_PRICE'],
            data['OWN_CAR_AGE'],
            data['AMT_CREDIT'],
            data['AMT_ANNUITY_x'],
            data['eod'],
            data['DAYS_EMPLOYED'],
            data['registeration'],
            data['DAYS_REGISTRATION'],
            data['identity'],
            data['DAYS_ID_PUBLISH'],
            data['phone'],
            data['DAYS_LAST_PHONE_CHANGE'],
            data['AMT_REQ_CREDIT_BUREAU_QRT'],
            data['CNT_INSTALMENT'],
            data['CNT_INSTALMENT_FUTURE']
        )

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query, values)

        # Check if fetchone() result is not None before iterating
        last_row = cursor.fetchone()
        if last_row is not None:
            print("Last Row:", last_row)  # Add this line for logging

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Data submitted successfully!', 'data': last_row})
    
    except Exception as e:
        print("Error:", str(e))  # Add this line for logging
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
        select_query = f'SELECT {column_names_string} FROM test_applicant ORDER BY "SK_ID_CURR" DESC LIMIT 1;'
        cursor.execute(select_query)
        last_row = cursor.fetchone()

        cursor.close()
        conn.close()

        # Combine column names and values in the response
        response_data = dict(zip(columns, last_row))

        return jsonify(response_data)

    except Exception as e:
        print("Error:", str(e))  # Add this line for logging
        return jsonify({'error': str(e)})
    
# # Load the machine learning models
classifier_model = joblib.load('model_probability_feature.joblib')
regressor_model = joblib.load('model_predict_feature.joblib')

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
            'SK_ID_CURR':[input_data["SK_ID_CURR"]],
            'DAYS_BIRTH': [input_data["DAYS_BIRTH"]],
            'DAYS_REGISTRATION': [input_data["DAYS_REGISTRATION"]],
            'DAYS_ID_PUBLISH': [input_data["DAYS_ID_PUBLISH"]],
            'DAYS_LAST_PHONE_CHANGE': [input_data["DAYS_LAST_PHONE_CHANGE"]],
            'AMT_ANNUITY_x': [input_data["AMT_ANNUITY_x"]],
            'AMT_CREDIT': [input_data["AMT_CREDIT"]],
            'DAYS_EMPLOYED': [input_data["DAYS_EMPLOYED"]],
            'AMT_INCOME_TOTAL': [input_data["AMT_INCOME_TOTAL"]],
            'AMT_GOODS_PRICE': [input_data["AMT_GOODS_PRICE"]],
            'OWN_CAR_AGE': [input_data["OWN_CAR_AGE"]],
            'CNT_FAM_MEMBERS': [input_data["CNT_FAM_MEMBERS"]],
            'CNT_INSTALMENT_FUTURE': [input_data["CNT_INSTALMENT_FUTURE"]],
            'CNT_INSTALMENT': [input_data["CNT_INSTALMENT"]],
            'CNT_CHILDREN': [input_data["CNT_CHILDREN"]],
            'AMT_REQ_CREDIT_BUREAU_QRT': [input_data["AMT_REQ_CREDIT_BUREAU_QRT"]]
            })

        # features for Regressor model
        features_predict = features
        # Drop feature names before making predictions
        features_probab = features

        # Assuming 'classifier_model' is a classifier (e.g., RandomForestClassifier)
        probability_result = classifier_model.predict_proba(features_probab)[:, 1]  # Extract the probability for class 1

        # Calculate the score as 100 - probability_result
        score = 100 - round(probability_result.item() * 100, 2)

        # Assuming 'regressor_model' is a regressor (e.g., RandomForestRegressor)
        # If the model is a regressor, make sure to use the feature names
        regression_result = regressor_model.predict(features_predict)

        # Round the probability result to two decimal places
        probability_result_rounded = round(probability_result.item(), 2)

        # Set predicted amount to $0 if score is less than 50
        predicted_amount = 0 if score < 50 else regression_result.item()

        if probability_result_rounded < 0.50:
            result_message = f"Congratulations! You are eligible for the loan.\nPredicted Amount: ${predicted_amount:,.2f}\nScore: {score}%"
        else:
            result_message = "Sorry, you are not eligible for the loan."

        return render_template('result.html', result_message=result_message)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Run the application
if __name__ == '__main__':
    app.run(debug=True)

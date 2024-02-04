from flask import Flask, jsonify, render_template,request
import json
import csv
from math import sqrt
import pandas as pd
import psycopg2


app = Flask(__name__)
# 
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
    return render_template('api.html')

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

# @app.route('/api.html')
# def api():
#     return render_template('api.html')

# -------------------------
if __name__ == '__main__':
    app.run(debug=True)

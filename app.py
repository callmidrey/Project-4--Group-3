from flask import Flask, jsonify, render_template,request
import json
import csv
from math import sqrt
import pandas as pd
import psycopg2


app = Flask(__name__)
# 
# Configure PostgreSQL connection
DB_NAME = 'Project3'
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
@app.route('/properties', methods=['GET'])
def properties():
    query = "SELECT * FROM property;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
# Route to get all data from a specific table
@app.route('/parks', methods=['GET'])
def parks():
    query = "SELECT * FROM parks;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
# Route to get all data from a specific table
@app.route('/schools', methods=['GET'])
def schools():
    query = "SELECT * FROM schools;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
@app.route('/restaurants', methods=['GET'])
def restaurants():
    query = "SELECT * FROM restaurants;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
@app.route('/gyms', methods=['GET'])
def gyms():
    query = "SELECT * From gyms;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500

@app.route('/grocery', methods=['GET'])
def groceries():
    query = "SELECT * From grocery;"
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500
@app.route('/publictransport', methods=['GET'])
def publictransport():
    query = 'SELECT * FROM "publicTransport"'
    data = fetch_data(query)
    if isinstance(data, list):
        return jsonify(data)
    else:
        return jsonify({'error': data}), 500

@app.route('/api.html')
def api():
    return render_template('api.html')

# -------------------------
if __name__ == '__main__':
    app.run(debug=True)

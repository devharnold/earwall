#!/usr/bin/env python3
from flask import Flask, jsonify
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

@app.route("/")
def startApp():
    return (f"Hello World!")

@app.route('/')
def home():
    #connecting to our db
    conn = get_db_connection()
    cur = conn.cursor()

    #execute a raw sql query
    cur.execute('SELECT version();')

    db_version = cur.fetchone()

    #close the connection
    cur.close()
    conn.close()

    return jsonify({'PostgreSQL version': db_version})

if __name__ == "__main__":
    app.run(debug=True)
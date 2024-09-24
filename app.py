#!/usr/bin/env python3
from flask import Flask, jsonify
import os
import psycopg2
from dotenv import load_dotenv
from models.engine.db_storage import get_db_connection

load_dotenv()

app = Flask(__name__)

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
    get_db_connection()
    app.run(debug=True)
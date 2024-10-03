#eth wallet database

from flask import Flask
from web3 import Web3
import psycopg2
import os
import dotenv
from dotenv import load_dotenv

app = Flask(__name__)


import os
import requests
from dotenv import load_dotenv
from dotenv import load_dotenv


load_dotenv()

def get_mpesa_token():
    """Generates an OAuth token from mpesa API"""
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")


    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Error fetching token: {response.text}")
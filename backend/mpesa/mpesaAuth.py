# Authorization request API provided by mpesa
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Meant to fetch the mpesa authentication token

url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
querystring = {"grant_type":"client_credentials"}
payload = ""
response = requests.request("GET", "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials", headers = {'Authorization': os.getenv("AUTH_BASIC") })
print(response.text.encode('utf-8'))


response
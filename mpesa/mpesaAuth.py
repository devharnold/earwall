# Authorization request API provided by mpesa

import requests

url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
querystring = {"grant_type":"client_credentials"}
payload = ""
response = requests.request("GET", "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials", headers = {'Authorization': 'Basic T2ZXQUVHM0J6aGFjQXdOanhmeDRKbXpZMk54dTVUdFhOQXZLaWxBT0pnYnFWYUdIOlJKRTRRc01BZVNUUnpmMjZSZFdVZms0blhJQkdBVmw3STFIaGk1TmxZSmNBdWc4bFFtUTZSdjlsRmJ4R2NxZ1E=' })
print(response.text.encode('utf-8'))

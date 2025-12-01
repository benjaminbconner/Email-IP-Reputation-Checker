import os
import requests
from dotenv import load_dotenv

load_dotenv()  # make sure this is called once at app startup

API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def check_ip(ip_address):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    if "data" in result:
        return result["data"]
    elif "errors" in result:
        return {"error": result["errors"][0]["detail"]}
    else:
        return {"error": "Unexpected response format"}

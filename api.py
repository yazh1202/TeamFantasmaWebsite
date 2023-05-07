import requests
import json
from dotenv import load_dotenv
import os
def api_call(keywords):
    load_dotenv()
    url = "https://jsearch.p.rapidapi.com/search"
    
    querystring = {"query":keywords,"page":"1","num_pages":"5"}

    headers = {
        "X-RapidAPI-Key": os.getenv('api_key'),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    
    return json_data
import requests
import json
from dotenv import load_dotenv
import os
def api_call(keywords):
    load_dotenv()
    url = "https://jsearch.p.rapidapi.com/search"
    
    querystring = {"query":keywords,"page":"1","num_pages":"20"}

    headers = {
        "X-RapidAPI-Key": os.getenv('api_key'),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    
    return json_data

# CHATGPT API CALLING
def gpt_api_call(content="Tell me a joke"):
    url = "https://chatgpt-api6.p.rapidapi.com/standard-gpt"

    payload = { "conversation": [
            {
                "role": "user",
                "content": content
            }
        ] }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv('api_key'),
        "X-RapidAPI-Host": "chatgpt-api6.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
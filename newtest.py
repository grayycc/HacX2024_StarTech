import os
import requests
import base64
import configparser
import dalle3

config = configparser.ConfigParser()
config.read('config.ini')

API_ENDPOINT = config['openai']['api_endpoint']
API_DEPLOYMENT_SOBER = config['openai']['api_deployment-sober']
API_VERSION = config['openai']['api_version']
API_KEY = config['openai']['api_key']
API_CONTENT = "application/json"
ENDPOINT = API_ENDPOINT + API_DEPLOYMENT_SOBER +  "/chat/completions?api-version=" + API_VERSION

data = None 

def submit_prompt(prompt_input: str):
  headers = {
    "Content-Type": API_CONTENT,
    "api-key": API_KEY,
  }

  payload = {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt_input
          }
        ]
      }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 150
  }

  titlePayload = {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": f"Generate a short title for the following prompt: {prompt_input} " 
          }
        ]
      }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 100
  }
  try:
      response = requests.post(ENDPOINT, headers=headers, json=payload)
      image_response = dalle3.generate_image(prompt_input)
      print("IMAGE_RESPONSE", image_response)
      
      response.raise_for_status()  
  except requests.RequestException as e:
      raise SystemExit(f"Failed to make the request. Error: {e}")


  global data
  data = response.json()['choices'][0]['message']['content']

  try:
     title_response = requests.post(ENDPOINT, headers=headers, json=titlePayload)
     print("TITLE", title_response.json())
     titleData = title_response.json()['choices'][0]['message']['content']
  except:
     titleData = "title"
    
  print("DATA", data)
  data = { "output": data, "image": image_response, "title": titleData }

  return data

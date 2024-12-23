import os
from openai import AzureOpenAI
import json
import configparser

def generate_image(prompt: str) -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')

    client = AzureOpenAI(
        api_version="2024-05-01-preview",
        azure_endpoint="https://hacxsources.openai.azure.com/",
        api_key=config['openai']['api_key'],
    )

    result = client.images.generate(
        model="Dalle3", 
        prompt= prompt + ' without text',
        n=1
    )

    image_url = json.loads(result.model_dump_json())['data'][0]['url']
    return image_url

if __name__ == "__main__":
    x = input('Enter your request? ') 
    image_url = generate_image(x)
    print(image_url)

    with open('poster_trial2.html', 'r') as file:
        html_content = file.read()

    html_content = html_content.replace('{{ image_url }}', image_url)

    with open('poster_trial2.html', 'w') as file:
        file.write(html_content)
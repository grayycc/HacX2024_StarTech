import requests
from PIL import Image
from io import BytesIO
from dalle3 import image_url

def convert_image(url, output_format='PNG', output_file='output_image'):
    try:
    
        response = requests.get(url)
        response.raise_for_status()  

        
        image = Image.open(BytesIO(response.content))
        
        
        output_file_path = f"{output_file}.{output_format.lower()}"
        image.save(output_file_path, format=output_format)

        print(f"Image successfully saved as {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

#image_url_2 = 'https://example.com/path/to/image.jpg' 
convert_image(image_url, output_format='PNG', output_file='converted_image')

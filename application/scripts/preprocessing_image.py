import requests
import base64
from typing import Dict
from rembg import remove
from imageKit_api import upload_file_imageKit

def read_image(image: str, credentials: Dict[str, str]) -> tuple[str, str]:
    image = upload_file_imageKit(image, credentials)
    image_url = image['url']
    
    api_url = "https://api.ocr.space/parse/image"
    
    payload = {
        "apikey": credentials['api_ocr_space'],
        "language": "eng",
        "url": image_url,
        "filetype": "URL",
    }

    response = requests.post(api_url, data=payload)
    result = response.json()

    # Check if OCR was successful
    if result.get("IsErroredOnProcessing"):
        return ("", "")

    # Extract the extracted text and image URL
    output_text = result.get("ParsedResults")[0].get("ParsedText").splitlines()
    
    return output_text, image_url

def remove_background(image_url: str, credentials: Dict[str, str]):
    response = requests.get(image_url)
    image_data = response.content

    # Process the image data to remove the background
    image_without_background = remove(image_data)
    image_without_background = base64.b64encode(image_without_background).decode('utf-8')

    upload_image = upload_file_imageKit(image_without_background, credentials)
    
    return upload_image['url']
    
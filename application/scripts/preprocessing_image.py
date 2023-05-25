import requests
import base64
import asyncio
from PIL import Image
from pyzbar import pyzbar
from io import BytesIO
import numpy as np
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
        return ("", image_url)

    # Extract the extracted text and image URL
    output_text = result.get("ParsedResults")[0].get("ParsedText").splitlines()
    
    return output_text, image_url

async def preprocess_vinyl_images(images, credentials):
    # Read first image
    text_from_image_1, image_url_1 = await asyncio.to_thread(read_image, images[0], credentials)
    text_from_images = [{"text_from_image": text_from_image_1, "url": image_url_1}]
    # Other images
    other_image_tasks = [asyncio.to_thread(upload_file_imageKit, other_image, credentials) for other_image in images[1:]]
    other_image_urls = await asyncio.gather(*other_image_tasks)

    text_from_images.extend({"text_from_image": "EMPTY", "url": other_image_url['url']} for other_image_url in other_image_urls)
    
    return text_from_images

def get_cd_barcode(image: bytes, credentials: dict):
    upload_image = upload_file_imageKit(image, credentials)
    image_url = upload_image['url']
    response = requests.get(image_url).content

    image = np.array(Image.open(BytesIO(response)).convert('RGB'))
    barcodes = pyzbar.decode(image)

    for barcode in barcodes:
        if data := barcode.data.decode("utf-8"):
             return data, image_url
    
    return "", image_url

async def preprocess_cd_images(images, credentials):
    # Read second image 
    text_from_image, image_url_2 = await asyncio.to_thread(get_cd_barcode, images[1], credentials)

    # First image
    image_url_1 = await asyncio.to_thread(upload_file_imageKit, images[0], credentials)

    text_from_images = [
        {"text_from_image": "EMPTY", "url": image_url_1['url']},
        {"text_from_image": text_from_image, "url": image_url_2},
    ]
    # Other images
    other_image_tasks = [asyncio.to_thread(upload_file_imageKit, other_image, credentials) for other_image in images[2:]]
    other_image_urls = await asyncio.gather(*other_image_tasks)

    text_from_images.extend({"text_from_image": "EMPTY", "url": other_image_url['url']} for other_image_url in other_image_urls)
    
    return text_from_images

def remove_background(image_url: str, credentials: Dict[str, str]):
    response = requests.get(image_url)
    image_data = response.content

    # Process the image data to remove the background
    image_without_background = remove(image_data)
    image_without_background = base64.b64encode(image_without_background).decode('utf-8')

    upload_image = upload_file_imageKit(image_without_background, credentials)
    
    return upload_image['url']
    
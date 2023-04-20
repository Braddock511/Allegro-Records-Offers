import re
import base64
import requests
import numpy as np
import multiprocessing
from PIL import Image
from pyzbar import pyzbar
from io import BytesIO
from time import sleep
from azure_api import clear_image
from imageKit_api import upload_file_imageKit
from chunks import search_data, preprocess_data

def search_data_parallel(text_from_image: list, discogs_token: str, type_record: str, image_data: bool) -> list[dict]:
    # Split the text_from_image list into chunks
    num_chunks = multiprocessing.cpu_count()
    chunk_size = len(text_from_image) // num_chunks
    if chunk_size == 0:
        chunk_size = 1
    chunks = [text_from_image[i:i+chunk_size] for i in range(0, len(text_from_image), chunk_size)]

    with multiprocessing.Pool() as pool:
        results = pool.starmap(search_data, [(chunk, discogs_token, type_record, image_data) for chunk in chunks])

    return [item for sublist in results for item in sublist]
        

def preprocess_data_parallel(text_from_image: str|list, credentials: dict, type_record: str, image_data: bool = True) -> dict:
    # Get the Discogs API token from the credentials list
    discogs_token = credentials["api_discogs_token"]

    # Clean up the input string
    if isinstance(text_from_image, str):
        text_from_image = text_from_image.replace("{", "").replace("}", "").split(",")

    # Search the Discogs API for vinyl records matching the input texts
    results = search_data_parallel(text_from_image, discogs_token, type_record, image_data)
    
    # Discogs limit -> 1 request per second
    sleep(1)

    # Split the results list into chunks
    num_chunks = multiprocessing.cpu_count()
    chunk_size = len(results) // num_chunks
    if chunk_size == 0:
        chunk_size = 1
    chunks = [results[i:i+chunk_size] for i in range(0, len(results), chunk_size)]
    with multiprocessing.Pool() as pool:
        discogs_information = pool.starmap(preprocess_data, [(chunk, discogs_token) for chunk in chunks])

    return [item for sublist in discogs_information for item in sublist]


def remove_background(image_url: str, credentials: dict) -> str:
    # Clear the image background
    encoded_image = base64.b64encode(clear_image(image_url, credentials)).decode()
    
    # Upload the cleared image to ImageKit
    upload_image = upload_file_imageKit(encoded_image, credentials)
    clear_image_url = upload_image['url']

    return clear_image_url

def get_cd_barcode(image: str, credentials: dict):
    upload_image = upload_file_imageKit(image, credentials)
    image_url = upload_image['url']
    response = requests.get(image_url).content

    image = np.array(Image.open(BytesIO(response)).convert('RGB'))
    barcodes = pyzbar.decode(image)

    for barcode in barcodes:
        data = barcode.data.decode("utf-8")
        if data:
            return data, image_url
    
    return "", image_url

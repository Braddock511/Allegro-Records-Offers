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
from discogs_api import get_vinyl, get_cd, get_price
from imageKit_api import upload_file_imageKit


def process_chunk(chunk: list, discogs_token: str, type_record: str, image_data: bool) -> list:
    discogs_data_output = []
    punctuation = "<"'"'"'@:^`!#$%&*();?'\'[]{}=+,>"
    remove_punctuation = re.compile(r"^[a-zA-Z {}]*$".format(re.escape(punctuation)))

    for text in chunk:
        if 5 < len(text) < 50:
            # Remove any text within parentheses if data is a image
            if not image_data:
                text = re.sub(r'\(', ' (', text)
                text = re.sub(r'\([^)]*\)', '', text)

            # Check if the text contains only ASCII characters
            if not re.search(r'[^\u0000-\u007F]', text):
                if not remove_punctuation.match(text):

                    # Remove any unwanted characters from the text if data is a image
                    if image_data:
                        text = text.replace('"', "").replace("'", "").replace("A", "").replace("B", "").replace(" ", "").replace("-", "").replace("~", "")

                    if type_record == "Vinyl":
                        discogs_data = get_vinyl(text, discogs_token)

                    elif type_record == "CD":
                        discogs_data = get_cd(text, discogs_token)

                    if 'results' in discogs_data.keys():
                        for disc_data in discogs_data['results']:
                            if image_data:
                                discogs_text = disc_data['catno'].replace('"', "").replace("'", "").replace("A", "").replace("B", "").replace(" ", "").replace("-", "").replace("~", "")
                                if text == discogs_text:
                                    discogs_data_output.append(disc_data)
                                    break

                            else:
                                discogs_data_output.append(disc_data)

    return discogs_data_output

def search_data_parallel(text_from_image: list, discogs_token: str, type_record: str, image_data: bool) -> list[dict]:

    # Split the text_from_image list into chunks
    num_chunks = multiprocessing.cpu_count()
    chunk_size = len(text_from_image) // num_chunks
    if chunk_size == 0:
        chunk_size = 1
    chunks = [text_from_image[i:i+chunk_size] for i in range(0, len(text_from_image), chunk_size)]

    # Process the chunks in parallel
    with multiprocessing.Pool() as pool:
        results = pool.starmap(process_chunk, [(chunk, discogs_token, type_record, image_data) for chunk in chunks])

    # Flatten the results and return
    return [item for sublist in results for item in sublist]
        

def preprocess_data(text_from_image: str|list, credentials: dict, type_record: str, image_data: bool = True) -> dict:
    # Get the Discogs API token from the credentials list
    discogs_token = credentials["api_discogs_token"]

    # Clean up the input string
    if isinstance(text_from_image, str):
        text_from_image = text_from_image.replace("{", "").replace("}", "").split(",")

    # Search the Discogs API for vinyl records matching the input texts
    results = search_data_parallel(text_from_image, discogs_token, type_record, image_data)
    
    # Discogs limit -> 1 request per second
    sleep(1)

    id = '-'
    label = '-'
    country = '-'
    year = '-'
    uri = '-'
    genre = '-'
    title = '-'
    price = '-'
    barcode = '-'

    # Reshape list to 1
    if isinstance(text_from_image, list):
        text_from_image_temp = []
        text_from_image_temp.append(text_from_image)
        text_from_image = text_from_image_temp

    discogs_information = []

    for _ in range(len(text_from_image)):
        information = {"id": id, "label": label, "country": country, "year": year, "uri": f"https://www.discogs.com{uri}", "genre": genre, "title": title, "price": price, "barcode": barcode}

        for result in results:
            if isinstance(result, dict):
                id = result['id']
                price = get_price(id, discogs_token)
                uri = result['uri']
                genre = result['genre'][0]
                title = result['title']
                title = title.replace("*", "").replace("•", "").replace("†", " ").replace("º", " ").replace("—", " ")
                country = result.get('country') if result.get('country') else '-'
                year = result.get('year') or result.get('released') if (result.get('year') or result.get('released')) else '-'
                barcode = result.get('barcode', [''])[0].replace(" ", "") if result.get('barcode') else '-'
                label = result.get('label', [''])[0] + " | " + result.get('catno', '') if result.get('label') else '-'

            information = {"id": id, "label": label, "country": country, "year": year, "uri": f"https://www.discogs.com{uri}", "genre": genre, "title": title, "price": price, "barcode": barcode}
            discogs_information.append(information)

    return discogs_information


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

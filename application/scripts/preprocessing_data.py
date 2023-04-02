import re
import base64
import requests
import numpy as np
from PIL import Image
from pyzbar import pyzbar
from io import BytesIO
from azure_api import clear_image
from discogs_api import get_vinyl, get_cd, get_price
from imageKit_api import upload_file_imageKit

def search_data(data: list, discogs_token: str, type_record: str, image_data: bool) -> list[dict]: 
    output_data = []
    punctuation = "<"'"'"'@:^`!#$%&*();?'\'[]{}=+,>"
    remove_punctuation = r"^[a-zA-Z {}]*$".format(re.escape(punctuation))

    for code in data:
        if 5 < len(code) < 50:
            # Remove any text within parentheses if data is a image
            if not image_data:
                code = re.sub(r'\(', ' (', code)
                code = re.sub(r'\([^)]*\)', '', code)
            # Check if the code contains only ASCII characters
            if not re.search(r'[^\u0000-\u007F]', code):
                if not re.match(remove_punctuation, code):
                    # Remove any unwanted characters from the code if data is a image
                    if image_data:
                        code = code.replace('"', "").replace("'", "").replace("A", "").replace("B", "").replace(" ", "").replace("-", "").replace("~", "")
                        
                    if type_record == "Vinyl":
                        discogs_data = get_vinyl(code, discogs_token)
                    elif type_record == "CD":
                        discogs_data = get_cd(code, discogs_token)

                    if 'results' in discogs_data.keys():
                        for disc_data in discogs_data['results']:
                            if image_data:
                                discogs_code = disc_data['catno'].replace('"', "").replace("'", "").replace("A", "").replace("B", "").replace(" ", "").replace("-", "").replace("~", "")
                                if code == discogs_code:
                                    output_data.append(disc_data)
                                    break
                            else:
                                output_data.append(disc_data)

    return output_data
        

def preprocess_data(data: str|list, credentials: dict, type_record: str, url: str = "", image_data: bool = True) -> dict:
    # Get the Discogs API token from the credentials list
    discogs_token = credentials["api_discogs_token"]

    # Clean up the input string
    if isinstance(data, str):
        data = data.replace("{", "").replace("}", "").split(",")

    # Search the Discogs API for vinyl records matching the input codes
    results = search_data(data, discogs_token, type_record, image_data)

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
    if isinstance(data, list):
        data_temp = []
        data_temp.append(data)
        data = data_temp

    output = {"url": url, "data": []}

    for _ in range(len(data)):
        information = {"id": id, "label": label, "country": country, "year": year, "uri": f"https://www.discogs.com{uri}", "genre": genre, "title": title, "price": price, "barcode": barcode}

        for result in results:
            if isinstance(result, dict):
                id = result['id']
                price = get_price(id, discogs_token)
                uri = result['uri']
                genre = result['genre'][0]
                barcode = result['barcode'][0].replace(" ", "") if 'barcode' in result.keys() else "-"
                title = result['title']
                title = title.replace("*", "").replace("•", "").replace("†", " ").replace("º", " ").replace("—", " ")

                try: 
                    country = result['country']
                except KeyError:
                    pass
                try:
                    year = result['year']
                except KeyError:
                    pass
                try:
                    label = result['label'][0] + " | " + result['catno']
                except KeyError:
                    pass


            information = {"id": id, "label": label, "country": country, "year": year, "uri": f"https://www.discogs.com{uri}", "genre": genre, "title": title, "price": price, "barcode": barcode}
            output['data'].append(information)

    return output


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

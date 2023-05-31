import requests
import urllib3
import json
import re
from collections import Counter
from time import sleep
from database import get_allegro_offers
from discogs_api import get_tracklist
from preprocessing_image import remove_background

urllib3.disable_warnings()

def allegro_verification(client_id: str, client_secret: str) -> str:
    payload = {'client_id': client_id}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    response = requests.post("https://allegro.pl/auth/oauth/device", auth=(client_id, client_secret), headers=headers, data=payload, verify=False)

    return response.json()

def get_allegro_token(client_id: str, client_secret: str, device_code: str) -> str:
    while True:
        sleep(1)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'urn:ietf:params:oauth:grant-type:device_code', 'device_code': device_code}
        response = requests.post("https://allegro.pl/auth/oauth/token", auth=(client_id, client_secret), headers=headers, data=data, verify=False)

        token = json.loads(response.text)

        if response.status_code == 200:
            return token['access_token']
        
def get_my_offers(credentials: dict, limit: int, offset: int, type_offer: str, type_record: str, genre: str) -> dict:
    allegro_token = credentials["api_allegro_token"]
    
    if type_record == "Vinyl":
        categories = {"all": 279, "ballad": 1410, "blues": 1411, "folk, world, & country": 5639, "country": 1145, "dance": 5638, "kids": 5626, "ethno": 5639, "jazz": 289, "carols": 5625, "metal": 260981, "alternative": 10830, "electronic": 261112, "film": 322237, "latin": 286, "classical": 286, "new": 284, "opera": 261156, "pop": 261039, "hip-hop": 261040, "rap": 261040, "reggae": 1413, "rock": 261043, "rock'n'roll": 5623, "single": 261041, "compilations": 1419, "soul": 1420, "synth-pop": 321961, "other": 293, "sets": 9531}
        
    elif type_record == "CD":
        categories = {"all": 175, "ballad": 1361, "blues": 261036, "folk, world, & country": 261100, "country": 1143, "dance": 261035, "disco": 89757, "kids": 261028, "ethno": 261100, "jazz": 260, "carols": 5607, "metal": 261128, "alternative": 261029, "electronic": 261111, "film": 322237, "latin": 9536, "classical": 9536, "religious": 89751, "new": 261042, "opera": 9537, "pop": 261039, "hip-hop": 261044, "rap": 261044, "reggae": 1413, "rock": 261110, "rock'n'roll": 5605, "single": 322236, "compilations": 261102, "soul": 181, "synth-pop": 321960, "other": 191, "sets": 9530}
    else:
        genre = ""
    
    if genre:
        genre = categories.get(genre)
        genre = f"&category.id={genre}"

    if type_offer == "all":
        type_offer = ""
    
    elif type_offer == "BUY_NOW":
        type_offer = "&sellingMode.format=BUY_NOW"
    
    elif type_offer == "AUCTION":
        type_offer = "&sellingMode.format=AUCTION"

    headers = {'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    url = f"https://api.allegro.pl/sale/offers?publication.status=ACTIVE&limit={limit}&offset={offset}{type_offer}{genre}"
    result = requests.get(url, headers=headers, verify=False)
    
    return result.json()

def get_offer_info(credentials: dict, offer_id: int) -> dict:
    allegro_token = credentials["api_allegro_token"]

    headers = {'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    
    result = requests.get(url, headers=headers, verify=False)
    
    return result.json()

def handle_allegro_errors(data: dict, result: dict, credentials: dict) -> dict:
    """
    Handles errors returned by the Allegro API during product offers processing.
    
    Args:
        data (dict): The data dictionary containing product information.
        result (dict): The dictionary containing the result returned by the Allegro API.
        credentials (dict): The dictionary containing API credentials.
        
    Returns:
        dict: The modified result dictionary after handling the errors.
    """
    errors = []
    url = 'https://api.allegro.pl/sale/product-offers'

    for _ in range(5):
        if 'errors' not in result:
            break
        
        error_messages = [error['message'] for error in result['errors']]
        user_messages = [error['userMessage'] for error in result['errors']]

        if 'Request Timeout' not in error_messages:
            for msg in error_messages:
                if "Existing Product related" in msg:
                    category = re.findall(r"product category .*", msg)[0]
                    new_genre = re.sub(r"\D", "", category)
                    data['productSet'][0]['product']['category']['id'] = new_genre
                    errors.append("Genre")

                elif "Wykonawca" in msg:
                    artist = re.findall(r"parameter value .*", msg)[0]
                    new_artist = re.sub(r'\((.*?)\)', r'\1', artist.replace("parameter value", "")).strip()
                    data['productSet'][0]['product']['parameters'][0]['values'] = [new_artist]
                    errors.append("Artist")

                elif "Tytuł" in msg:
                    title = re.findall(r"parameter value .*", msg)[0]
                    new_title = re.sub(r'\((.*?)\)', r'\1', title.replace("parameter value", "")).strip()       
                    data['productSet'][0]['product']['parameters'][1]['values'] = [new_title]
                    errors.append("Title")

                elif "Invalid GTIN" in msg:
                    new_barcode = msg.split(" - ")[1].split(" in ")[0]
                    if len(new_barcode) not in [8, 10, 12, 13, 14]:
                        new_barcode = f"0{new_barcode}"
                    data['productSet'][0]['product']['parameters'][3]['values'] = [new_barcode.strip()]
                    errors.append("EAN")
                    
                else:
                    errors.append("OTHER ERRORS THAT CAN'T BE CHANGE")

            if any("'Wytwórnia'" in msg or "Wytwórnia" in msg for msg in user_messages):
                parameters = data['productSet'][0]['product']['parameters']
                data['productSet'][0]['product']['parameters'] = [parameter for parameter in parameters if parameter['name'] != "Wytwórnia"]
                errors.append("Label")

            if any("'Rok wydania'" in msg or "Rok wydania" in msg for msg in user_messages):
                parameters = data['productSet'][0]['product']['parameters']
                data['productSet'][0]['product']['parameters'] = [parameter for parameter in parameters if parameter['name'] != "Rok wydania"]
                errors.append("Release")

        # Checking for repeated errors
        count_error = Counter(errors).values()
        if any(count > 1 for count in count_error):
            break

        result = requests.post(url, headers={'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=data, verify=False).json()

    return result

def create_offer(credentials: dict, discogs_data: dict, carton: str, condition: str, images: list, type_record: str, type_offer: str, duration: str, clear: bool) -> dict:
    if type_record in {"Vinyl", "Winyl"}:
        categories = {"all": 279, "latin": 286, "ballad": 1410, "blues": 1411, "country": 1145, "dance": 5638, "children's": 5626, "ethno": 5639, "jazz": 289, "carols": 5625, "metal": 260981, "alternative": 10830, "electronic": 261112, "film": 292, "classical": 286, "new": 284, "opera": 261156, "pop": 261039, "hip hop": 261040, "reggae": 1413, "rock": 261043, "rock'n'roll": 5623, "single": 261041, "compilations": 1419, "funk / soul": 1420, "soul": 1420, "synth-pop": 321961, "other": 293, "sets": 9531}
    elif type_record == "CD":
        categories = {"all": 175, "latin": 9536, "ballad": 1361, "blues": 261036, "country": 1143, "dance": 261035, "disco": 89757, "children's": 261028, "ethno": 261100, "jazz": 260, "carols": 5607, "metal": 261128, "alternative": 261029, "electronic": 261111, "film": 322237, "classical": 9536, "religious": 89751, "new": 261042, "opera": 9537, "pop": 261127, "hip hop": 261044, "reggae": 182, "rock": 261110, "rock'n'roll": 5605, "single": 322236, "compilations": 261102, "funk / soul": 181,"soul": 181, "synth-pop": 321960, "other": 191, "sets": 9530}

    conditions = {"Near Mint (NM or M-)": "-M", "Mint (M)": "M", "Excellent (EX)": "EX", "Very Good Plus (VG+)": "VG+", "Very Good (VG)": "VG", "Good (G)": "G", "Fair (F)": "F"}

    # Discogs data
    record_id = discogs_data['id']
    title = discogs_data['title']
    label = discogs_data['label'].replace("&", "")
    country = discogs_data['country'].replace("&", ", ")
    released = discogs_data['year']
    genre = discogs_data['genre']
    price = discogs_data['price']
    barcode = "".join(re.findall('\d+', discogs_data['barcode']))
    tracklist = get_tracklist(record_id, credentials["api_discogs_token"])

    # Allegro data
    allegro_offer = json.loads(get_allegro_offers()[0]['offer_data'])
    allegro_id = allegro_offer['id']
    offer_info = get_offer_info(credentials, allegro_id)
    
    payments = offer_info['payments']
    location = offer_info['location']
    delivery = allegro_offer['delivery']
    duration_offer = None
    republish = False
    selling = {
        "format": type_offer,
        "price": {
            "amount": price,
            "currency": "PLN"
        }
    }
    category = categories.get(genre.lower())
    condition = conditions.get(condition)
    author = title.split("-")[0]
    name = " ".join(title.split("-")[1:])
    full_name = f'{author.strip()}.{carton}' if len(f'{author} - {name}.{carton}') > 50 else f'{author} - {name}.{carton}'
    allegro_condition = ["Nowy", "11323_1"] if condition == "M" else ["Używany", "11323_2"]
    
    if type_offer == "AUCTION":
        duration_offer = duration
        republish = True
        selling = {
            "format": type_offer,
            "startingPrice": {
                "amount": price,
                "currency": "PLN"
            }
        }

    if clear:
        first_image = images[0]
        clear_first_image = remove_background(first_image, credentials)
        images = [clear_first_image, *list(images[1:])]


    if type_record == "Vinyl":
        data = {
            "name": full_name.strip(),

            "productSet": [{
                "product": {
                    "name": title.strip(),
                    "category": {
                        "id": category
                    },
                    "parameters": [
                        {
                            "name": "Wykonawca",
                            "values": [author.strip()]
                        },
                        {
                            "name": "Tytuł",
                            "values": [name.strip()]
                        },
                        {
                            "name": "Nośnik",
                            "values": ["Winyl"]
                        }
                    ],

                    "images": images,
                },
            }],

            "parameters": [{'id': '11323', 'name': 'Stan', 'values': [allegro_condition[0]], 'valuesIds': [allegro_condition[1]], 'rangeValue': None}],
            
            "sellingMode": selling,

            "publication": {
                "republish": republish,
                "duration": duration_offer
            },

            "images": images,

            'description': {'sections': [{'items': [{'type': 'IMAGE', 'url': images[0]}, {'type': 'TEXT', 'content': f'<p><b>STAN PŁYT/Y: {condition}</b></p><p><b>WYTWÓRNIA: {label}</b></p><p><b>KRAJ POCHODZENIA: {country}</b></p><p><b>ROK WYDANIA: {released}</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': tracklist}]}, {'items': [{'type': 'IMAGE', 'url': images[1]}, {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>PŁYTY SĄ SOLIDNIE ZABEZPIECZONE PODCZAS WYSYŁKI</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>.{carton} OZNACZA ETYKIETĘ KARTONU</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY (M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>DOSKONAŁY (EX)</b> - odtwarzana, z widoczną niewielką ilością delikatnych rysek lub inną bardzo drobną wadą nie wpływającą na jakość dźwięku.</li><li><b>BARDZO DOBRY Z PLUSEM (VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) </b> - nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - grana bardzo często, może posiadać widoczne głębsze rysy.</li><li><b>ZŁY</b> <b>(F)</b> - poważniejsze rysy.</li></ul>'}]}]},

            "stock": {"available": 1},

            "payments": payments,
            'location': location,
            'delivery': delivery
    }
    
    elif type_record == "CD":
        data = {
            "name": full_name.strip(),

            "productSet": [{
                "product": {
                    "name": title.strip(),
                    "category": {
                        "id": category
                    },
                    "parameters": [
                        {
                            "name": "Wykonawca",
                            "values": [author.strip()]
                        },
                        {
                            "name": "Tytuł",
                            "values": [name.strip()]
                        },
                        {
                            "name": "Nośnik",
                            "values": ["CD"]
                        },
                        {
                            'name': 'EAN (GTIN)',
                            'values': [barcode.strip()]
                        },
                    ],

                    "images": images,
                },
            }],

            "parameters": [{'id': '11323', 'name': 'Stan', 'values': [allegro_condition[0]], 'valuesIds': [allegro_condition[1]], 'rangeValue': None}],
            
            "sellingMode": selling,

            "publication": {
                "republish": republish,
                "duration": duration_offer
            },

            "images": images,

            'description': {'sections': [{'items': [{'type': 'IMAGE', 'url': images[0]}, {'type': 'TEXT', 'content': f'<p><b>STAN PŁYT/Y: {condition}</b></p><p><b>WYTWÓRNIA: {label}</b></p><p><b>KRAJ POCHODZENIA: {country}</b></p><p><b>ROK WYDANIA: {released}</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': tracklist}]}, {'items': [{'type': 'IMAGE', 'url': images[1]}, {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>PŁYTY SĄ SOLIDNIE ZABEZPIECZONE PODCZAS WYSYŁKI</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>.{carton} OZNACZA ETYKIETĘ KARTONU</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY (M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>DOSKONAŁY (EX)</b> - odtwarzana, z widoczną niewielką ilością delikatnych rysek lub inną bardzo drobną wadą nie wpływającą na jakość dźwięku.</li><li><b>BARDZO DOBRY Z PLUSEM (VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) </b> - nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - grana bardzo często, może posiadać widoczne głębsze rysy.</li><li><b>ZŁY</b> <b>(F)</b> - poważniejsze rysy.</li></ul>'}]}]},

            "stock": {"available": 1},

            "payments": payments,
            'location': location,
            'delivery': delivery
        }

    # If year release is empty add new
    if not "Rok wydania" in [parameter['name'] for parameter in data['productSet'][0]['product']['parameters']] and released != "-": 
        data['productSet'][0]['product']['parameters'].append({"name": "Rok wydania", "values": [released]})

    # If year label is empty add new
    if not "Wytwórnia" in [parameter['name'] for parameter in data['productSet'][0]['product']['parameters']] and label != "-": 
        data['productSet'][0]['product']['parameters'].append({"name": "Wytwórnia", "values": [label.split(" | ")[0]]})

    url = 'https://api.allegro.pl/sale/product-offers'
    result = requests.post(url, headers={'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=data, verify=False).json()

    if 'errors' in result:
        result = handle_allegro_errors(data, result, credentials)
            
    return result

def get_condition_and_carton(credentials: dict, offer_id: str) -> tuple[str, str]:
    allegro_token = credentials["api_allegro_token"]

    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    product = requests.get(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}).json()

    name = product['name']
    carton = f'.{name.split(".")[-1]}'
    if len(carton) > 4:
        carton = f'.{name.split(")")[-1]}'
    description = product['description']

    conditions = ['M', 'MINT', '-M', 'M-', 'MINT-', '-MINT', 'MINT-.', '  MINT-', 'MINT, FOLIA',
                'EX', 'EX+', 'EX++', 'EX-', 'EX.', 'EXCELLENT', 
                'VG', 'VG+', 'VG++','VG-', 'VERY GOOD', 'BARDZO DOBRY', 'BARDZO DOBRY.',
                'G', 'GOOD', 'GOOD+', 'DOBRY', 'MINT-.DO UMYCIA', "MINT. NOWA ZAFOLIOWANA",
                'BARDZO DOBRY.PŁYTA DO UMYCIA', 'BARDZO DOBRY.DROBNE RYSKI', 'BARDZO DOBRY.DO UMYCIA']

    # Find the condition of the product in the description
    condition = re.findall(r'STAN .{1,10}: .*', str(description))
    
    if condition == []:
        condition = re.findall(r'PŁYTA W STANIE .*', str(description))

    try:
        # Remove any html tags
        condition = re.sub(r"<.*", '', condition[0])
    except IndexError:
        return ("", "")

    # Get the actual condition
    condition = condition.split(": ")[-1]

    return ("", "") if condition.upper() not in conditions else (condition, carton)

def edit_description(credentials: dict, offer_id: str, images: list, new_information: dict) -> dict:
    condition_carton = get_condition_and_carton(credentials, offer_id)

    if not condition_carton:
        return {}

    condition, carton = condition_carton
    record_id = new_information['id']
    label = new_information['label'].replace("&", "")
    country = new_information['country'].replace("&", "")
    released = new_information['year'].replace("&", "")
    price = new_information.get('price', "")
    offer = get_offer_info(credentials, offer_id)

    if not "Rok wydania" in [parameter['name'] for parameter in offer['productSet'][0]['product']['parameters']] and released != "-":
        offer['productSet'][0]['product']['parameters'].append({"name": "Rok wydania", "values": [released]})

    if not "Wytwórnia" in [parameter['name'] for parameter in offer['productSet'][0]['product']['parameters']] and label != "-":
        offer['productSet'][0]['product']['parameters'].append({"name": "Wytwórnia", "values": [label.split(" | ")[0]]})

    offer['description'] = {
        'sections': [
                    {
                        'items': [
                            {'type': 'IMAGE', 'url': images[0]},
                            {'type': 'TEXT', 'content': f'<p><b>STAN PŁYT/Y: {condition}</b></p><p><b>WYTWÓRNIA: {label}</b></p><p><b>KRAJ POCHODZENIA: {country}</b></p><p><b>ROK WYDANIA: {released}</b></p>'}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'TEXT', 'content': get_tracklist(record_id, credentials["api_discogs_token"])}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'IMAGE', 'url': images[1]}, 
                            {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>PŁYTY SĄ SOLIDNIE ZABEZPIECZONE PODCZAS WYSYŁKI</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>{carton.replace("&", "")} OZNACZA ETYKIETĘ KARTONU</b></p>'}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY (M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>DOSKONAŁY (EX)</b> - odtwarzana, z widoczną niewielką ilością delikatnych rysek lub inną bardzo drobną wadą nie wpływającą na jakość dźwięku.</li><li><b>BARDZO DOBRY Z PLUSEM (VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) </b> - nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - grana bardzo często, może posiadać widoczne głębsze rysy.</li><li><b>ZŁY</b> <b>(F)</b> - poważniejsze rysy.</li></ul>'}
                        ]
                    }
                ]
            }
    offer['productSet'][0]['product']['images'] = images

    if price:
        offer['sellingMode'] = {"price": {"amount": price, "currency": "PLN"}}

    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    result = requests.patch(url, headers={'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=offer, verify=False)
    
    return result.json()

def edit_images(credentials: dict, offer_id: str, images: list) -> dict:
    allegro_token = credentials["api_allegro_token"]
    
    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    result = requests.patch(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json={'images': images}, verify=False)
    
    return result.json()

def get_payment_history(credentials: dict, limit: int, offset: int) -> dict:
    allegro_token = credentials["api_allegro_token"]
    
    url = f"https://api.allegro.pl/payments/payment-operations?limit={limit}&offset={offset}"
    result = requests.get(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, verify=False)
    
    return result.json()

def swap_cartons(credentials: dict, change_carton: str, change_to_carton: str) -> dict:
    """
    Swaps the carton name in Allegro offers with a new carton name.

    Args:
        credentials (dict): The dictionary containing API credentials.
        change_carton (str): The old carton name to be replaced.
        change_to_carton (str): The new carton name to replace with.

    Returns:
        dict: The JSON response returned by the Allegro API after updating the offers.
    """
    allegro_token = credentials["api_allegro_token"]
    
    offers = get_allegro_offers()
    filter_offers = []
    for offer in offers:
        offer = json.loads(offer['offer_data'])
        name = offer['name']
        carton = name.split(".")[-1]
        
        if carton == change_carton:
            filter_offers.append(offer)
         
    for filter_offer in filter_offers:
        # change carton in name
        offer = get_offer_info(credentials, filter_offer['id'])
        name = offer['name']
        without_carton = name[:len(name)-len(change_carton)] # name without old carton
        new_name = f"{without_carton}{change_to_carton}"
        offer['name'] = new_name
        
        # change carton in description if exist      
        description = offer['description']
        for i, section in enumerate(description['sections']):
            for j, item in enumerate(section['items']):
                if item.get("content") and change_carton in item['content']:
                    offer['description']['sections'][i]['items'][j]['content'] = item['content'].replace(change_carton, change_to_carton)
                            
        url = f"https://api.allegro.pl/sale/product-offers/{offer['id']}"
        result = requests.patch(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=offer, verify=False)
        
    return result.json()

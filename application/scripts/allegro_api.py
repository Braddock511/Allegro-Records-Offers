import requests
import urllib3
import json
import re
from typing import List
from collections import Counter
from time import sleep
from database import get_allegro_offers
from discogs_api import get_tracklist
from preprocessing_image import remove_background

urllib3.disable_warnings()

genres = {"latin": "muzyka klasyczna", "ballad": "ballada, poezja śpiewana", "blues": "blues, rhythm'n'blues", "country": "country", "dance": "dance", "disco": "disco polo, biesiadna, karaoke", "children's": "dla dzieci", "folk, world, & country": "ethno, folk, world music", "ethno": "ethno, folk, world music", "jazz": "jazz, swing", "carols": "kolędy", "metal": "metal", "alternative": "muzyka alternatywna", "electronic": "muzyka elektroniczna", "stage & screen": "muzyka filmowa", "classical": "muzyka klasyczna", "religious": "muzyka religijna, oazowa", "new": "nowe brzmienia", "opera": "opera, operetka", "pop": "pop", "hip hop": "rap, hip-hop", "reggae": "reggae, ska", "rock": "rock", "rock'n'roll": "rock'n'roll", "single": "single", "compilations": "składanki", "funk / soul": "soul, funk", "soul": "soul, funk", "synth-pop": "synth-pop", "other": "pozostałe", "sets": "zestawy, pakiety", "non-music": "pozostałe"}

def allegro_verification(client_id: str, client_secret: str) -> str:
    payload = {'client_id': client_id}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    response = requests.post("https://allegro.pl/auth/oauth/device", auth=(client_id, client_secret), headers=headers, data=payload, verify=False)

    return response.json()

def get_allegro_tokens(client_id: str, client_secret: str, device_code: str) -> str:
    while True:
        sleep(1)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'urn:ietf:params:oauth:grant-type:device_code', 'device_code': device_code}
        response = requests.post("https://allegro.pl/auth/oauth/token", auth=(client_id, client_secret), headers=headers, data=data, verify=False)

        token = json.loads(response.text)

        if response.status_code == 200:
            return token['access_token'], token['refresh_token']
    
def refresh_token(credentials: dict) -> str:
    while True:
        sleep(1)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'refresh_token', 'refresh_token': credentials['api_allgero_refresh_token']}
        response = requests.post("https://allegro.pl/auth/oauth/token", auth=(credentials['api_allegro_id'], credentials['api_allegro_secret']), headers=headers, data=data, verify=False)

        token = json.loads(response.text)
        
        if response.status_code == 200:
            return token['access_token'], token['refresh_token']
        elif response.status_code == 400:
            return None, None

def get_user_info(credentials: dict):
    headers = {'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    result = requests.get("https://api.allegro.pl/me", headers=headers, verify=False).json()
    return result

def get_my_offers(credentials: dict, limit: int, offset: int, type_offer: str, genre: str = "") -> dict:
    if genre:
        genre = genres.get(genre)
        genre = f"&gatunek={genre}"

    if type_offer == "all":
        type_offer = ""
    
    elif type_offer == "BUY_NOW":
        type_offer = "&sellingMode.format=BUY_NOW"
    
    elif type_offer == "AUCTION":
        type_offer = "&sellingMode.format=AUCTION"

    headers = {'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    url = f"https://api.allegro.pl/sale/offers?publication.status=ACTIVE&limit={limit}&offset={offset}{type_offer}{genre}"
    result = requests.get(url, headers=headers, verify=False).json()
    
    return result

def get_offer_info(credentials: dict, offer_id: int) -> dict:
    headers = {'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    result = requests.get(f"https://api.allegro.pl/sale/product-offers/{offer_id}", headers=headers, verify=False).json()
    return result

def get_description(images: List[str], condition: str, label_name: str, series: str, country: str, released: str, tracklist: str, carton: str):
    return {
            'sections': [
                        {
                            'items': [
                                {'type': 'IMAGE', 'url': images[0]},
                                {'type': 'TEXT', 'content': f"""
                                 <p><b>Stan płyt/y:</b> {condition}</p>
                                 <p><b>Wytwórnia:</b> {label_name.replace("&", "&amp;")}</p>
                                 <p><b>Numer katalogowy:</b> {series}</p>
                                 <p><b>Kraj pochodzenia:</b> {country.replace("&", "&amp;")}</p>
                                 <p><b>Rok wydania:</b> {released}</p>
                                 <p><b>Karton:</b> {carton}</p>
                                 """}
                            ]
                        },
                        {
                            'items': [
                                {'type': 'TEXT', 'content': """
                                 <p><b>Jak oceniamy płyty:</b></p>
                                 <ul>
                                 <li><b>Idealny (M) 🏆: </b>Płyta nowa, bez najmniejszych śladów użycia.</li>
                                 <li><b>Niemalże Idealny (M-) ✨: </b> Praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li>
                                 <li><b>Doskonały (EX) 🌟: </b> Odtwarzana, z widoczną niewielką ilością delikatnych rysek lub inną bardzo drobną wadą nie wpływającą na jakość dźwięku.</li>
                                 <li><b>Bardzo Dobry z Plusem (VG+) 👌: </b> Bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li>
                                 <li><b>Bardzo Dobry (VG) 👍: </b> Nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li>
                                 <li><b>Dobry (G) 😐: </b> Grana bardzo często, może posiadać widoczne głębsze rysy.</li>
                                 <li><b>Zły (F) ⚠️: </b> Poważniejsze rysy.</li>
                                 </ul>
                                 """}
                            ],
                        },
                        {
                            'items': [
                                {'type': 'IMAGE', 'url': images[-1]}, 
                                {'type': 'TEXT', 'content': f"""
                                 <p><b>Dlaczego warto kupić?</b></p>
                                 <p><b>✨ Gwarancja satysfakcji: </b>Ponad 10 lat doświadczenia na rynku, co zapewnia wysoką jakość obsługi.</p>
                                 <p><b>🔒 Bezpieczeństwo: </b>Starannie zabezpieczamy płyty na czas wysyłki, aby dotarły do Ciebie w nienaruszonym stanie.</p>
                                 <p><b>🚀 Szybka dostawa: </b>Przesyłka w 1-2 dni robocze - ciesz się swoją muzyką już wkrótce!</p>
                                 """}
                            ]
                        },
                        {
                            'items': [
                                {'type': 'TEXT', 'content': tracklist}
                            ]
                        },
                        {
                            'items': [
                                {'type': 'TEXT', 'content': """
                                <p><b>Dodatkowe informacje:</b> Jeżeli masz pytania dotyczące stanu płyty czy jakichkolwiek innych szczegółów, śmiało zapytaj! Jesteśmy tu, aby pomóc i udzielić wszystkich niezbędnych informacji. 💬</p>
                                 <p><b>Co oznacza karton w opisie:</b> Jest to oznaczenie kartonu, w którym znajduje się płyta, co ułatwia identyfikację i organizację.</p>
                                 <p><b>Podziel się swoją opinią po zakupie i dołącz do grona zadowolonych klientów! 🌟</b></p>"""}
                            ]
                        }
                    ]
            }

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

    for _ in range(3):
        if 'errors' not in result:
            break
        
        error_messages = [error['message'] for error in result['errors']]
        user_messages = [error['userMessage'] for error in result['errors']]

        if 'Request Timeout' not in error_messages:
            for msg in error_messages:
                if "Wykonawca" in msg:
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

    if 'errors' in result:
        code = result["errors"][0]["code"]

        if code == "UploadImageRequestTimeoutException":
            result["errors"][0]["userMessage"] = "Błąd wysyłania zdjęć. Spróbuj jeszcze raz"

    return result

def create_offer(credentials: dict, offer_data: dict, carton: str, type_record: str, type_offer: str, duration: str, clear: bool) -> dict:
    conditions = {"Near Mint (NM or M-)": "M-", "Mint (M)": "M", "Excellent (EX)": "EX", "Very Good Plus (VG+)": "VG+", "Very Good (VG)": "VG", "Good (G)": "G", "Fair (F)": "F"}

    # Discogs data
    record_id = offer_data['id']
    title = (offer_data['title']).strip()
    label = offer_data['label']
    country = offer_data['country']
    released = offer_data['year']
    genre = offer_data['genre']
    price = offer_data['price']
    price = price.replace(",", ".") if isinstance(price, str) else price
    images = offer_data['images']
    condition = offer_data['condition']
    barcode = ("".join(re.findall('\d+', offer_data['barcode']))).strip()
    tracklist = get_tracklist(record_id, credentials["api_discogs_token"])

    # Allegro data    
    payments = json.loads(credentials['payments'])
    location = json.loads(credentials['location'])
    delivery = json.loads(credentials['delivery'])
    duration_offer = None
    republish = False
    selling = {
        "format": type_offer,
        "price": {
            "amount": price,
            "currency": "PLN"
        }
    }
    genre = genres.get(genre.lower())
    condition = conditions.get(condition)
    author = (title.split("-")[0]).strip()
    try:
        name = (" ".join(title.split("-")[1:])).strip()
    except IndexError:
        name = ""
        
    # Combine author, name, and carton
    full_name = (f'{author} - {name}.{carton}' if len(f'{author} - {name}.{carton}') <= 75 and name != "" else f'{author}.{carton}').strip()

    # If the length is still greater than 50, truncate the author name
    if len(full_name) > 75:
        full_name = (f'{full_name.split(" ")[0]}.{carton}').strip()
        full_name.replace(",", "") # Remove unwanted comma
    
    allegro_condition = ["Nowy", "11323_1"] if condition == "M" else ["Używany", "11323_2"]
    label_name, series = label.split(" | ")
    
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
            "name": full_name,

            "productSet": [{
                "product": {
                    "name": title,
                    "category": {
                        "id": 1
                    },
                    "parameters": [
                        {
                            "name": "Wykonawca",
                            "values": [author]
                        },
                        {
                            "name": "Tytuł",
                            "values": [name]
                        },
                        {
                            "name": "Nośnik",
                            "values": ["Winyl"]
                        },
                        {
                            "name": "Gatunek",
                            "values": [genre]
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

            'description': get_description(images, condition, label_name, series, country, released, tracklist, carton),

            "stock": {"available": 1},

            "payments": payments,
            'location': location,
            'delivery': delivery
    }
    
    elif type_record == "CD":
        data = {
            "name": full_name,

            "productSet": [{
                "product": {
                    "name": title,
                    "category": {
                        "id": 1
                    },
                    "parameters": [
                        {
                            "name": "Wykonawca",
                            "values": [author]
                        },
                        {
                            "name": "Tytuł",
                            "values": [name]
                        },
                        {
                            "name": "Nośnik",
                            "values": ["CD"]
                        },
                        {
                            'name': 'EAN (GTIN)',
                            'values': [barcode]
                        },
                        {
                            "name": "Gatunek",
                            "values": [genre]
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

            'description': get_description(images, condition, label_name, series, country, released, tracklist, carton),

            "stock": {"available": 1},

            "payments": payments,
            'location': location,
            'delivery': delivery
        }

    parameters = data['productSet'][0]['product']['parameters']
    
    # If year release is empty add new
    if not "Rok wydania" in [parameter['name'] for parameter in parameters] and released != "-": 
        parameters.append({"name": "Rok wydania", "values": [released]})

    # If label is empty add new
    if not "Wytwórnia" in [parameter['name'] for parameter in parameters] and label != "-": 
        parameters.append({"name": "Wytwórnia", "values": [label_name]})

    # If series is empty add new
    if not "Seria" in [parameter['name'] for parameter in parameters] and series != "-": 
        parameters.append({"name": "Seria", "values": [series]})

    url = 'https://api.allegro.pl/sale/product-offers'
    result = requests.post(url, headers={'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=data, verify=False).json()

    if 'errors' in result:
        result = handle_allegro_errors(data, result, credentials)
            
    return result

def get_condition_and_carton(credentials: dict, offer_id: str) -> tuple[str, str]:
    allegro_token = credentials["api_allegro_token"]

    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    product = requests.get(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}).json()

    description = product['description']

    # Find the carton
    carton_pattern = re.compile(r'<b>Karton:</b>\s*(.*?)</p>')
    carton_match = carton_pattern.search(str(description))
    try:
        if carton_result := carton_match.group(1):
            carton = carton_result
    except AttributeError:
        name = product['name']
        carton = f'.{name.split(".")[-1]}'
        if len(carton) > 4:
            carton = f'.{name.split(")")[-1]}'

            if len(carton) > 5:
                carton = "-"

    carton = carton.rsplit(".", 1)[-1]

    if not carton:
        raise

    # Find the condition
    conditions = ['M', 'MINT', '-M', 'M-', 'MINT-', '-MINT', 'MINT-.', '  MINT-', 'MINT, FOLIA',
                'EX', 'EX+', 'EX++', 'EX-', 'EX.', 'EXCELLENT', 
                'VG', 'VG+', 'VG++','VG-', 'VERY GOOD', 'BARDZO DOBRY', 'BARDZO DOBRY.',
                'G', 'GOOD', 'GOOD+', 'DOBRY', "F", 'MINT-.DO UMYCIA', "MINT. NOWA ZAFOLIOWANA",
                'BARDZO DOBRY.PŁYTA DO UMYCIA', 'BARDZO DOBRY.DROBNE RYSKI', 'BARDZO DOBRY.DO UMYCIA']

    conditions.sort(key=len, reverse=True)
    
    escaped_conditions = [re.escape(condition) for condition in conditions]

    condition_pattern = re.compile(r'(?<!\w)(' + '|'.join(escaped_conditions) + r')(?!\w)')

    condition_match = condition_pattern.search(str(description))
    if condition_result := condition_match.group(0):
        condition = condition_result
    else:
        raise

    return (condition, carton)

def edit_offer(credentials: dict, offer_id: str, images: list, new_information: dict, listing_similar: bool, edit_price: bool, edit_description: bool, to_buy: bool) -> dict:
    record_id = new_information['id']
    label = new_information['label']
    country = new_information['country']
    released = new_information['year']
    price = new_information.get('price', "")
    cover_image = new_information["cover_image"]
    offer = get_offer_info(credentials, offer_id)
    parameters = offer['productSet'][0]['product']['parameters']
    
    type_record = [parameter['values'][0] for parameter in parameters if parameter['name'] == 'Nośnik'][0]
    
    label_name, series = label.split(" | ")
    
    if type_record != "płyta DVD":
        if not "Rok wydania" in [parameter['name'] for parameter in parameters] and released != "-":
            parameters.append({"name": "Rok wydania", "values": [released]})

        if not "Wytwórnia" in [parameter['name'] for parameter in parameters] and label_name != "-":
            parameters.append({"name": "Wytwórnia", "values": [label_name]})

        if not "Seria" in [parameter['name'] for parameter in parameters] and series != "-": 
            parameters.append({"name": "Seria", "values": [series]})

    if edit_description:
        condition_carton = get_condition_and_carton(credentials, offer_id)

        if not condition_carton:
            return {}

        if cover_image:
            images.insert(0, cover_image)

        condition, carton = condition_carton
        tracklist = get_tracklist(record_id, credentials["api_discogs_token"])
        description = get_description(images, condition, label_name, series, country, released, tracklist, carton)

        offer['description'] = description
        # DO usunięcia
        title_without_carton = offer["name"].rsplit(".", 1)[0] 
        title_without_carton = title_without_carton.replace("–", "-")
        
        if released:
            offer["name"] = f"{title_without_carton} ({released}, {type_record})"
        else:
            offer["name"] = f"{title_without_carton} ({type_record})"

    offer['productSet'][0]['product']['images'] = images
    price = price.replace(",", ".") if isinstance(price, str) else price

    if edit_price:
        offer['sellingMode']['price'] = {"amount": price, "currency": "PLN"}
    elif offer['sellingMode'].get('startingPrice', ""):
        offer['sellingMode']['price'] = {"amount": offer['sellingMode']['startingPrice']['amount'], "currency": "PLN"}
        
    if to_buy:
        offer['sellingMode']['format'] = "BUY_NOW"
        
        offer['publication']['duration'] = None
        offer['publication']['endedBy'] = None
        offer['publication']['endingAt'] = None
        offer['publication']['republish'] = False
    
    if listing_similar:
        offer['publication']['status'] = "ACTIVE"
                
        url = "https://api.allegro.pl/sale/product-offers"
        result = requests.post(url, headers={'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=offer, verify=False)
    else:
        url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
        result = requests.patch(url, headers={'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=offer, verify=False)

    if cover_image:
        offer = get_offer_info(credentials, offer_id)
        edited_offer_images = offer['images']
        sort_images = [edited_offer_images[-1], *edited_offer_images[:-1]]
        edit_images(credentials, offer_id, sort_images)

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

def swap_specific_carton(credentials: dict, change_carton: str, change_to_carton: str, offer_id: str) -> dict:
    allegro_token = credentials["api_allegro_token"]
    offer = get_offer_info(credentials, offer_id)

    # change carton in name
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
    
    offers = get_allegro_offers(credentials['user_key'])
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

def orders(credentials: dict):
    allegro_token = credentials["api_allegro_token"]
    url = f"https://api.allegro.pl/order/checkout-forms"
    result = requests.get(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, verify=False)

    return result.json()
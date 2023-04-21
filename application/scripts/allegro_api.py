import requests
import urllib3
import json
import re
from collections import Counter
from time import sleep
from discogs_api import get_tracklist
from preprocessing_data import remove_background

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
        categories_lp = {"all": 279, "ballad": 1410, "blues": 1411, "folk, world, & country": 5639, "country": 1145, "dance": 5638, "kids": 5626, "ethno": 5639, "jazz": 289, "carols": 5625, "metal": 260981, "alternative": 10830, "electronic": 261112, "film": 322237, "latin": 286, "classical": 286, "new": 284, "opera": 261156, "pop": 261039, "hip-hop": 261040, "rap": 261040, "reggae": 1413, "rock": 261043, "rock'n'roll": 5623, "single": 261041, "compilations": 1419, "soul": 1420, "synth-pop": 321961, "other": 293, "sets": 9531}
        genre = categories_lp.get(genre)
    
    elif type_record == "CD":
        categories_cd = {"all": 175, "ballad": 1361, "blues": 261036, "folk, world, & country": 261100, "country": 1143, "dance": 261035, "disco": 89757, "kids": 261028, "ethno": 261100, "jazz": 260, "carols": 5607, "metal": 261128, "alternative": 261029, "electronic": 261111, "film": 322237, "latin": 9536, "classical": 9536, "religious": 89751, "new": 261042, "opera": 9537, "pop": 261039, "hip-hop": 261044, "rap": 261044, "reggae": 1413, "rock": 261110, "rock'n'roll": 5605, "single": 322236, "compilations": 261102, "soul": 181, "synth-pop": 321960, "other": 191, "sets": 9530}
        genre = categories_cd.get(genre)

    if type_offer == "all":
        type_offer = ""
    
    elif type_offer == "BUY_NOW":
        type_offer = "&sellingMode.format=BUY_NOW"
    
    elif type_offer == "AUCTION":
        type_offer = "&sellingMode.format=AUCTION"

    headers = {'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    url = f"https://api.allegro.pl/sale/offers?publication.status=ACTIVE&limit={limit}&offset={offset}&category.id={genre}{type_offer}"

    result = requests.get(url, headers=headers, verify=False)
    
    return result.json()

def get_offer_info(credentials: dict, offer_id: int) -> dict:
    allegro_token = credentials["api_allegro_token"]

    headers = {'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    
    result = requests.get(url, headers=headers, verify=False)
    
    return result.json()

def create_offer(credentials: dict, data: dict, carton: str, condition: str, images: list, type_record: str, type_offer: str, duration: str, clear: bool) -> dict:
    if type_record == "Vinyl":
        categories = {"all": 279, "ballad": 1410, "blues": 1411, "country": 1145, "dance": 5638, "children's": 5626, "ethno": 5639, "jazz": 289, "carols": 5625, "metal": 260981, "alternative": 10830, "electronic": 261112, "film": 322237, "classical": 9536, "new": 284, "opera": 261156, "pop": 261039, "rap": 261040, "reggae": 1413, "rock": 261043, "rock'n'roll": 5623, "single": 261041, "compilations": 1419, "funk / soul": 1420, "soul": 1420, "synth-pop": 321961, "other": 293, "sets": 9531}
    elif type_record == "CD":
        categories = {"all": 175, "ballad": 1361, "blues": 261036, "country": 1143, "dance": 261035, "disco": 89757, "children's": 261028, "ethno": 261100, "jazz": 260, "carols": 5607, "metal": 261128, "alternative": 261029, "electronic": 261111, "film": 322237, "classical": 9536, "religious": 89751, "new": 261042, "opera": 9537, "pop": 261039, "rap": 261040, "reggae": 1413, "rock": 261110, "rock'n'roll": 5605, "single": 322236, "compilations": 261102, "funk / soul": 181,"soul": 181, "synth-pop": 321960, "other": 191, "sets": 9530}

    conditions = {"Near Mint (NM or M-)": "-M", "Mint (M)": "M", "Excellent (EX)": "EX", "Very Good Plus (VG+)": "VG+", "Very Good (VG)": "VG", "Good (G)": "G", "Fair (F)": "F"}

    # Discogs data
    id = data['id']
    title = data['title']
    label = data['label'].replace("&", "")
    country = data['country']
    released = data['year']
    genre = data['genre']
    price = data['price']
    barcode = data['barcode']
    tracklist = get_tracklist(id, credentials["api_discogs_token"])

    # Allegro data
    allegro_offer = get_my_offers(credentials, 1, 0, "all", "Vinyl", "all")['offers'][0]
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
        images = [clear_first_image, *[image for image in images[1:]]]


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

        'description': {'sections': [{'items': [{'type': 'IMAGE', 'url': images[0]}, {'type': 'TEXT', 'content': f'<p><b>STAN PŁYT/Y: {condition}</b></p><p><b>WYTWÓRNIA: {label}</b></p><p><b>KRAJ POCHODZENIA: {country}</b></p><p><b>ROK WYDANIA: {released}</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': tracklist}]}, {'items': [{'type': 'IMAGE', 'url': images[1]}, {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>.{carton} OZNACZA ETYKIETĘ KARTONU</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY (M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>DOSKONAŁY (EX)</b> - odtwarzana, z widoczną niewielką ilością delikatnych rysek lub inną bardzo drobną wadą nie wpływającą na jakość dźwięku.</li><li><b>BARDZO DOBRY Z PLUSEM (VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) </b> - nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - grana bardzo często, może posiadać widoczne głębsze rysy.</li><li><b>ZŁY</b> <b>(F)</b> - poważniejsze rysy.</li></ul>'}]}]},

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

            'description': {'sections': [{'items': [{'type': 'IMAGE', 'url': images[0]}, {'type': 'TEXT', 'content': f'<p><b>STAN PŁYT/Y: {condition}</b></p><p><b>WYTWÓRNIA: {label}</b></p><p><b>KRAJ POCHODZENIA: {country}</b></p><p><b>ROK WYDANIA: {released}</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': tracklist}]}, {'items': [{'type': 'IMAGE', 'url': images[1]}, {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>.{carton} OZNACZA ETYKIETĘ KARTONU</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY (M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>DOSKONAŁY (EX)</b> - odtwarzana, z widoczną niewielką ilością delikatnych rysek lub inną bardzo drobną wadą nie wpływającą na jakość dźwięku.</li><li><b>BARDZO DOBRY Z PLUSEM (VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) </b> - nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - grana bardzo często, może posiadać widoczne głębsze rysy.</li><li><b>ZŁY</b> <b>(F)</b> - poważniejsze rysy.</li></ul>'}]}]},

            "stock": {"available": 1},

            "payments": payments,
            'location': location,
            'delivery': delivery
        }

    if not "Rok wydania" in [parameter['name'] for parameter in data['productSet'][0]['product']['parameters']] and released != "-": 
        data['productSet'][0]['product']['parameters'].append({"name": "Rok wydania", "values": [released]})

    if not "Wytwórnia" in [parameter['name'] for parameter in data['productSet'][0]['product']['parameters']] and label != "-": 
        data['productSet'][0]['product']['parameters'].append({"name": "Wytwórnia", "values": [label.split(" | ")[0]]})

    i = 0
    errors = []

    while i<10:
        url = f'https://api.allegro.pl/sale/product-offers'
        result = requests.post(url, headers={'Authorization': f'Bearer {credentials["api_allegro_token"]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=data, verify=False)

        try:
            error = result.json()['errors'][0]

            if "Existing Product related" in error['message']:
                # Update category ID
                category = re.findall(r"product category: .*", error['userMessage'])
                new_genre = "".join(re.findall(r"\d", str(category)))

                data['productSet'][0]['product']['category']['id'] = new_genre

            elif "The provided parameter 'Wykonawca'" in error['message']:
                # Update artist
                category = re.findall(r"product parameter .*", error['userMessage'])[0]
                new_artist = category.replace("product parameter", "")
                new_artist = re.sub(r"[.`]", "", new_artist)
                
                data['productSet'][0]['product']['parameters'][0]['values'] = [new_artist.strip()]
                
            elif "The provided parameter 'Tytuł'" in error['message']:
                # Update title
                category = re.findall(r"product parameter .*", error['userMessage'])[0]
                new_title = category.replace("product parameter", "")
                new_title = re.sub(r"[.`]", "", new_title)

                data['productSet'][0]['product']['parameters'][1]['values'] = [new_title.strip()]
                
            elif "Invalid GTIN" in error['message']:
                # Update barcode
                new_barcode = error['message'].split(" - ")[1].split(" in ")[0]

                if len(new_barcode) not in [8, 10, 12, 13, 14]:
                    new_barcode = "0" + new_barcode

                data['productSet'][0]['product']['parameters'][3]['values'] = [new_barcode.strip()]         

            elif "'Wytwórnia'" in error['userMessage'] or "Wytwórnia" in error['userMessage']:
                parameters = data['productSet'][0]['product']['parameters']

                for i, parameter in enumerate(parameters):
                    if parameter['name'] == "Wytwórnia":
                        del parameters[i]

            elif "'Rok wydania'" in error['userMessage'] or "Rok wydania" in error['userMessage']:
                parameters = data['productSet'][0]['product']['parameters']
                for i, parameter in enumerate(parameters):
                    if parameter['name'] == "Rok wydania":
                        del parameters[i]


            if error['message'] != "Request Timeout":
                errors.append(error['message'])

            # Checking that the given error does not repeating
            count_error = Counter(errors).values()

            for count in count_error:
                if count > 1:
                    i = 10

            i+=1
            
        except:
            break
    
    return result.json()

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
        return False

    # Get the actual condition
    condition = condition.split(": ")[-1]

    if condition.upper() not in conditions:
        return False

    return condition, carton

def edit_description(credentials: dict, offer_id: str, images: list, information: dict) -> dict:
    condition_carton = get_condition_and_carton(credentials, offer_id)

    if not condition_carton:
        return False

    condition, carton = condition_carton
    id = information['id']
    label = information['label'].replace("&", "")
    country = information['country'].replace("&", "")
    released = information['year'].replace("&", "")
    price = information['price'] if 'price' in information.keys() else ""
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
                            {'type': 'TEXT', 'content': get_tracklist(id, credentials["api_discogs_token"])}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'IMAGE', 'url': images[1]}, 
                            {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>{carton.replace("&", "")} OZNACZA ETYKIETĘ KARTONU</b></p>'}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY</b> MINT<b>(M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY MINT- (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>BARDZO DOBRY Z PLUSEM</b> <b>(VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) -</b> nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - poważniejsze rysy.</li></ul>'}
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

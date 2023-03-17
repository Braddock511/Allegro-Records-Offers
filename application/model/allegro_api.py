import requests
import urllib3
import json
import re
from time import sleep
from discogs_api import get_tracklist
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
        
def get_my_offers(credentials: list, limit: int, offset: int, type_offer: str, type_record: str, genre: str) -> dict:
    allegro_token = credentials[-1]
    if type_record == "vinyl":
        categories_lp = {"all": 279, "ballad": 1410, "blues": 1411, "country": 1145, "dance": 5638, "kids": 5626, "ethno": 5639, "jazz": 289, "carols": 5625, "metal": 260981, "alternative": 10830, "electronic": 261112, "film": 322237, "classical": 9536, "new": 284, "opera": 261156, "pop": 261039, "rap": 261040, "reggae": 1413, "rock": 261043, "rock'n'roll": 5623, "single": 261041, "compilations": 1419, "soul": 1420, "synth-pop": 321961, "other": 293, "sets": 9531}
        genre = categories_lp.get(genre)
    elif type_record == "cd":
        categories_cd = {"all": 175, "ballad": 1361, "blues": 261036, "country": 1143, "dance": 261035, "disco": 89757, "kids": 261028, "ethno": 261100, "jazz": 260, "carols": 5607, "metal": 261128, "alternative": 261029, "electronic": 261111, "film": 322237, "classical": 9536, "religious": 89751, "new": 261042, "opera": 9537, "pop": 261039, "rap": 261040, "reggae": 1413, "rock": 261110, "rock'n'roll": 5605, "single": 322236, "compilations": 261102, "soul": 181, "synth-pop": 321960, "other": 191, "sets": 9530}
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

def get_offer_info(credentials: list, offer_id: int) -> dict:
    allegro_token = credentials[-1]
    headers = {'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}
    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    result = requests.get(url, headers=headers, verify=False)
    return result.json()

def create_offer_vinyl(credentials: list, data: list, cartoon: str, condition: str, images: list):
    categories_lp = {'Blues': '1411', 'Classical': '286', 'Electronic': '261112', 'Folk, World, & Country': '5639', 'Funk / Soul': '1420', 'Hip Hop': '261040', 'Jazz': '289', 'Pop': '261039', 'Reggae': '1413', 'Rock': '261043'}
    conditions = {"Near Mint (NM or M-)": "-M", "Mint (M)": "M", "Very Good Plus (VG+)": "VG+", "Very Good (VG)": "VG", "Good (G)": "G"}
    
    # Discogs data
    data = data[0]
    id = data['id']
    title = data['title']
    label = data['label']
    country = data['country']
    released = data['year']
    genre = data['genre']
    price = data['price']
    tracklist = get_tracklist(id, credentials[7])

    # Allegro data
    allegro_offer = get_my_offers(credentials, 1, 0, "vinyl", "all")['offers'][0]
    allegro_id = allegro_offer['id']
    offer_info = get_offer_info(credentials, allegro_id)

    payments = offer_info['payments']
    location = offer_info['location']
    delivery = allegro_offer['delivery']
    category = categories_lp.get(genre)
    condition = conditions.get(condition)
    author, name = title.split("-")
    name = f'{author} - {name}.{cartoon}'

    if len(name) > 50:
        name = f'{author}.{cartoon}' 

    data = {
        "name": name,

        "productSet": [{
            "product": {
                "name": f'{author} - {name}',
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

        "parameters": [{'id': '11323', 'name': 'Stan', 'values': ['Używany'], 'valuesIds': ['11323_2'], 'rangeValue': None}],
        
        "sellingMode": {
            "price": {
                "amount": price,
                "currency": "PLN"
            }
        },

        "images": images,

        'description': {'sections': [{'items': [{'type': 'IMAGE', 'url': images[0]}, {'type': 'TEXT', 'content': f'<p><b>STAN PŁYT/Y: {condition}</b></p><p><b>WYTWÓRNIA: {label}</b></p><p><b>KRAJ POCHODZENIA: {country}</b></p><p><b>ROK WYDANIA: {released}</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': tracklist}]}, {'items': [{'type': 'IMAGE', 'url': images[-1]}, {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>.{cartoon} OZNACZA OZNACZENIE KARTONU</b></p>'}]}, {'items': [{'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY</b> MINT<b>(M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY MINT- (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>BARDZO DOBRY Z PLUSEM</b> <b>(VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) -</b> nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - poważniejsze rysy.</li></ul>'}]}]},

        "stock": {"available": 1},

        "payments": payments,
        'location': location,
        'delivery': delivery
    }

    i = 0

    while i!=10:
        url = f'https://api.allegro.pl/sale/product-offers'
        result = requests.post(url, headers={'Authorization': f'Bearer {credentials[-1]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=data, verify=False)

        try:
            error = result.json()['errors'][0]['message']

            if "Existing Product related" in error:
                # Update category ID)
                error = result.json()
                error = error['errors'][0]['userMessage']

                category = re.findall(r"product category: .*", error)
                new_genre = "".join(re.findall(r"\d", str(category)))

                data['productSet'][0]['product']['category']['id'] = new_genre
            
            elif "The provided parameter 'Wykonawca'" in error:
                # Update artist
                error = result.json()
                error = error['errors'][0]['userMessage']
                
                category = re.findall(r"product parameter .*", error)[0]
                new_artist = category.replace("product parameter", "")
                new_artist = re.sub(r"[.`]", "", new_artist)
                
                if new_artist:
                    data['productSet'][0]['product']['parameters'][1]['values'] = [new_artist.strip()]
                else:
                    return result.json()
                                
            elif "The provided parameter 'Tytuł'" in error:
                # Update title
                error = result.json()
                error = error['errors'][0]['userMessage']
                
                category = re.findall(r"product parameter .*", error)[0]
                new_title = category.replace("product parameter", "")
                new_title = re.sub(r"[.`]", "", new_title)
                
                if new_title:
                    data['productSet'][0]['product']['parameters'][2]['values'] = [new_title.strip()]
                
                else:
                    return result.json()
            
            elif "Request Timeout" in error:
                pass
            
            i+=1
            
        except:
            break
    
    return result.json()

def get_condition_and_cartoon(credentials: list, offer_id: str):
    allegro_token = credentials[-1]
    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    product = requests.get(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}).json()

    name = product['name']
    cartoon = f'.{name.split(".")[-1]}'
    description = product['description']

    # predefined conditions of the product
    conditions = ['M', 'MINT', '-M', 'M-', 'MINT-', '-MINT', 'MINT-.', '  MINT-', 'MINT, FOLIA',
                'EX', 'EX+', 'EX++', 'EX-', 'EX.', 'EXCELLENT', 
                'VG', 'VG+', 'VG++','VG-', 'VERY GOOD', 'BARDZO DOBRY', 'BARDZO DOBRY.',
                'G', 'GOOD', 'GOOD+', 'DOBRY', 'MINT-.DO UMYCIA', "MINT. NOWA ZAFOLIOWANA",
                'BARDZO DOBRY.PŁYTA DO UMYCIA', 'BARDZO DOBRY.DROBNE RYSKI', 'BARDZO DOBRY.DO UMYCIA']

    # find the condition of the product in the description using regular expression
    condition = re.findall(r'STAN .{1,10}: .*', str(description))
    
    if condition == []:
        condition = re.findall(r'PŁYTA W STANIE .*', str(description))

    try:
        # clean the condition by removing any html tags
        condition = re.sub(r"<.*", '', condition[0])
    except IndexError:
        return False

    # split the condition to only get the actual condition
    condition = condition.split(": ")[-1]

    if condition.upper() not in conditions:
        return False

    return condition, cartoon

def edit_description(credentials: list, offer_id: str, images: str, information: dict):
    condition_cartoon = get_condition_and_cartoon(credentials, offer_id)

    if not condition_cartoon:
        return False

    condition, cartoon = condition_cartoon
    id = information['id']
    label = information['label']
    country = information['country']
    released = information['year']

    data = {
        'description': {
            'sections': [
                    {
                        'items': [
                            {'type': 'IMAGE', 'url': images[0]},
                            {'type': 'TEXT', 'content': f'<p><b>STAN PŁYT/Y: {condition}</b></p><p><b>WYTWÓRNIA: {label}</b></p><p><b>KRAJ POCHODZENIA: {country}</b></p><p><b>ROK WYDANIA: {released}</b></p>'}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'TEXT', 'content': get_tracklist(id, credentials[7])}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'IMAGE', 'url': images[-1]}, 
                            {'type': 'TEXT', 'content': f'<p><b>WSZYSTKIE PŁYTY OCENIANE SĄ WIZUALNIE - BEZ ICH ODTWARZANIA.</b></p><p><b>ZAPRASZAM NA INNE MOJE AUKCJE</b></p><p><b>{cartoon} OZNACZA ETYKIETĘ KARTONU</b></p>'}
                        ]
                    },
                    {
                        'items': [
                            {'type': 'TEXT', 'content': '<p><b>JAK OCENIAMY PŁYTY:</b></p><ul><li><b>IDEALNY</b> MINT<b>(M)</b> -&nbsp;płyta nowa lub nie odtwarzana, bez najmniejszych śladów użycia.</li><li><b>NIEMALŻE IDEALNY MINT- (M-)</b> - praktycznie idealna, jednak odtwarzana raz lub kilka razy.</li><li><b>BARDZO DOBRY Z PLUSEM</b> <b>(VG+)</b> - bardzo dobry stan, może mieć drobne ryski. Odtwarzana wiele razy, jednak z dużą dbałością.</li><li><b>BARDZO DOBRY (VG) -</b> nadal całkiem dobry stan, może mieć więcej drobnych rysek, lub może posiadać głębszą rysę. Odtwarzana wiele razy.</li><li><b>DOBRY</b> <b>(G)</b> - poważniejsze rysy.</li></ul>'}
                        ]
                    }
                ]
            }
        }

    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    result = requests.patch(url, headers={'Authorization': f'Bearer {credentials[-1]}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json=data, verify=False)
    return result.json()

def edit_images(credentials: list, offer_id: str, images: list):
    allegro_token = credentials[-1]
    url = f"https://api.allegro.pl/sale/product-offers/{offer_id}"
    result = requests.patch(url, headers={'Authorization': f'Bearer {allegro_token}', 'Accept': "application/vnd.allegro.public.v1+json", "Content-Type":'application/vnd.allegro.public.v1+json'}, json={'images': images}, verify=False)
    return result
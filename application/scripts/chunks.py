import re
from scripts.discogs_api import get_vinyl, get_cd, get_price

def search_data(chunk: list, discogs_token: str, type_record: str, image_data: bool) -> list:
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

def preprocess_data(chunk: list, discogs_token: str) -> list:
    id = '-'
    label = '-'
    country = '-'
    year = '-'
    uri = '-'
    genre = '-'
    title = '-'
    price = '-'
    barcode = '-'
    discogs_information = []
    information = {"id": id, "label": label, "country": country, "year": year, "uri": f"https://www.discogs.com{uri}", "genre": genre, "title": title, "price": price, "barcode": barcode}

    for result in chunk:
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




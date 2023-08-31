import re
from typing import List, Dict
from discogs_api import get_vinyl, get_cd, get_price

def remove_text_in_parentheses(text: str) -> str:
    """
        Removes text enclosed in parentheses from a given string.
        
        Args:
            text (str): The input string.
            
        Returns:
            str: The modified string with text inside parentheses removed.
    """
    text = re.sub(r'\(', ' (', text)
    text = re.sub(r'\([^)]*\)', '', text)
    return text

def remove_unwanted_characters(text: str) -> str:
    """
        Removes ", ', A, B, -, ~ and blank characters from a given string
        
        Args:
            text (str): The input string.
            
        Returns:
            str: The modified string with unwanted characters removed.
    """
    return text.replace('"', "").replace("'", "").replace("A", "").replace("B", "").replace(" ", "").replace("-", "").replace("~", "")

def contains_only_ascii_and_not_punctuation(text: str) -> bool:
    """
        Checks if a given string contains only ASCII characters and is not composed solely of punctuation.
        
        Args:
            text (str): The input string.
            
        Returns:
            bool: True if the string contains only ASCII characters and is not solely composed of punctuation; False otherwise.
    
    """
    punctuation = "<"'"'"'@:^`!#$%&*();?'\'[]{}=+,>"
    punctuation_regex = re.compile(f"^[a-zA-Z {re.escape(punctuation)}]*$")
    
    return not re.search(r'[^\u0000-\u007F]', text) and not punctuation_regex.match(text)

def get_discogs_data(text: str, type_record: str, discogs_token: str) -> Dict[str, str]:
    """
        Retrieves discogs data based on a given text and record type
        
        Args:
            text (str): The input text.
            type_record (str): The record type ("Vinyl" or "CD").
            discogs_token (str): The discogs token for authentication.
            
        Returns:
            Dict[str, str]: A dictionary containing discogs data.
    """
    discogs_data = {}

    if type_record in {"Vinyl", "Winyl"}:
        discogs_data = get_vinyl(text, discogs_token)
    elif type_record == "CD":
        discogs_data = get_cd(text, discogs_token)

    return discogs_data

def filter_discogs_data(discogs_data_list: List[Dict[str, str]], text: str, image_data: bool) -> List[Dict[str, str]]:
    """
        Filters discogs data based on specific criteria.
    
        Args:
            discogs_data_list (List[Dict[str, str]]): A list of discogs data dictionaries.
            text (str): The input text for filtering.
            image_data (bool): A flag indicating whether image data is being filtered.
            
        Retruns:
            List[Dict[str, str]]: A filtered list of discogs data dictionaries.
    """
    discogs_data_output = []

    for disc_data in discogs_data_list:
        if image_data:
            discogs_text = remove_unwanted_characters(disc_data['catno'])
            if text == discogs_text:
                discogs_data_output.append(disc_data)
                break
        else:
            discogs_data_output.append(disc_data)

    return discogs_data_output

def search_data(chunk: List[str], discogs_token: str, type_record: str, image_data: bool) -> List[dict[str, str]]:
    """
        Searches discogs data based on a given chunk of text, discogs token, record type, and image data flag.

        Args:
            chunk (List[str]): A list of text chunks.
            discogs_token (str): The discogs token for authentication.
            type_record (str): The record type ("Vinyl" or "CD").
            image_data (bool): A flag indicating whether image data is being searched.

        Returns:
            List[dict[str, str]]: A list of discogs data dictionaries that match the search criteria.
    """
    discogs_data_output = []
    discogs_data = {}

    for text in chunk:
        if 5 < len(text) < 50:
            if not image_data:
                text = remove_text_in_parentheses(text)

            if contains_only_ascii_and_not_punctuation(text):
                if image_data:
                    text = remove_unwanted_characters(text)
                
                discogs_data = get_discogs_data(text, type_record, discogs_token)

                if 'results' in discogs_data.keys():
                    discogs_data_output.extend(filter_discogs_data(discogs_data['results'], text, image_data))
                    
    return discogs_data_output

def remove_not_allowed_characters(text: str) -> str:
    """
        Remove characters that are not allowed on Allegro from a given string
        
        Args:
            text (str): The input string.
            
        Returns:
            str: The modified string with unwanted characters removed.
    """
    polish_chars_pattern = r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]'    
    ascii_pattern = r'[\x00-\x7F]'    
    pattern = f'{polish_chars_pattern}|{ascii_pattern}'
    
    matches = re.findall(pattern, text, flags=re.UNICODE)    
    cleaned_text = ''.join(matches)
    
    return cleaned_text

def preprocess_data(chunk: list, discogs_token: str) -> list:
    """
        Preprocesses the data in the chunk list and returns a list of discogs information dictionaries.

        Args:
            chunk (list): A list of data chunks.
            discogs_token (str): The discogs token for authentication.

        Returns:
            list: A list of discogs information dictionaries.
    """
    record_id, label, country, year, uri, genre, title, price, barcode = '-', '-', '-', '-', '-', '-', '-', '-', '-'
    community_want_have = {}
    discogs_information = []
    information = {"id": record_id, "label": label, "country": country, "year": year, "uri": f"https://www.discogs.com{uri}", "genre": genre, "title": title, "price": price, "barcode": barcode, "community": community_want_have}

    for result in chunk:
        if isinstance(result, dict):
            record_id = result['id']
            price = get_price(record_id, discogs_token)
            uri = result['uri']
            genre = result['genre'][0]
            title = remove_not_allowed_characters(result['title'])
            country = result.get('country', '-')
            year = result.get('year') or result.get('released') if (result.get('year') or result.get('released')) else '-'
            barcode = result.get('barcode', [''])[0].replace(" ", "") if result.get('barcode') else '-'
            label = result.get('label', [''])[0] + " | " + result.get('catno', '') if result.get('label') else '-'
            community_want_have = result['community']

        information = {"id": record_id, "label": label, "country": country, "year": year, "uri": f"https://www.discogs.com{uri}", "genre": genre, "title": title, "price": price, "barcode": barcode, 
        "community": community_want_have}
        discogs_information.append(information)

    return discogs_information




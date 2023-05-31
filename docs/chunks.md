Python scripts that preprocess data in chunks

remove_text_in_parentheses - removes text enclosed in parentheses from a given string.
- text (str): the input string.

remove_unwanted_characters - removes ", ', A, B, -, ~ and blank characters from a given string
- text (str): the input string.

contains_only_ascii_and_not_punctuation - checks if a given string contains only ASCII characters and is not composed solely of punctuation.
- text (str): the input string.

get_discogs_data - retrieves discogs data based on a given text and record type
- text (str): The input text.
- type_record (str): The record type ("Vinyl" or "CD").
- discogs_token (str): The discogs token for authentication.

filter_discogs_data - filters discogs data based on specific criteria.
- discogs_data_list (List[Dict[str, str]]): A list of discogs data dictionaries.
- text (str): The input text for filtering.
- image_data (bool): A flag indicating whether image data is being filtered.

search_data - searches the Discogs API for metadata associated with the input text chunks. Uses regular expressions to clean and filter the text data before making a call to either the "get_vinyl" or "get_cd" function (depending on the type of record specified) to retrieve search results from the Discogs API. The search results are filtered and returned as a list of dictionaries.
- chunk (List(str)): a list of text chunks
- discogs_token (str): a string containing the authentication token for the Discogs API
- type_record (str): a string indicating the type of record (either "Vinyl" or "CD")
- image_data (bool): a boolean indicating whether the data is an image

preprocess_data - takes a list of Discogs API search results and processes the data to extract relevant metadata. The function uses various string manipulation techniques to clean and format the metadata fields before adding them to a new dictionary. The final output is a list of dictionaries containing processed metadata for each item in the input search results.
- chunk (list): a list of dictionaries containing Discogs API search results
- discogs_token (str): a string containing the authentication token for the Discogs API

import multiprocessing
from typing import List, Dict
from chunks import search_data, preprocess_data
def search_data_parallel(text_from_image: List[str], discogs_token: str, type_record: str, image_data: bool) -> List[Dict[str, str]]:
    """
        Searches for data in parallel for the given text from images using multiprocessing.

        Args:
            text_from_image (List[str]): The list of text extracted from images.
            discogs_token (str): The token for the Discogs API.
            type_record (str): The type of record to search for.
            image_data (bool): Indicates whether to include image data in the search.

        Returns:
            List[Dict[str, str]]: The list of search results as dictionaries.
    """
    # Split the text_from_image list into chunks
    num_chunks = multiprocessing.cpu_count()
    chunk_size = len(text_from_image) // num_chunks
    if chunk_size == 0:
        chunk_size = 1
    chunks = [text_from_image[i:i+chunk_size] for i in range(0, len(text_from_image), chunk_size)]

    with multiprocessing.Pool() as pool:
        results = pool.starmap(search_data, [(chunk, discogs_token, type_record, image_data) for chunk in chunks])

    return [item for sublist in results for item in sublist]
        

def preprocess_data_parallel(text_from_image: str|list, credentials: dict, type_record: str, image_data: bool = True) -> List[Dict[str, str]]:
    """
        Preprocesses the data in parallel for the given text from images using multiprocessing.

        Args:
            text_from_image (str | list): The text extracted from images or a single text string.
            credentials (dict): The credentials containing the necessary information.
            type_record (str): The type of record to search for.
            image_data (bool, optional): Indicates whether to include image data in the search. Defaults to True.

        Returns:
            List[Dict[str, str]]: The preprocessed data as a list of dictionaries.
    """
    discogs_token = credentials["api_discogs_token"]

    # Clean up the input string
    if isinstance(text_from_image, str):
        text_from_image = text_from_image.replace("{", "").replace("}", "").split(",")

    # Search the Discogs API for vinyl records matching the input texts
    results = search_data_parallel(text_from_image, discogs_token, type_record, image_data)

    # Split the results list into chunks
    num_chunks = multiprocessing.cpu_count()
    chunk_size = len(results) // num_chunks
    if chunk_size == 0:
        chunk_size = 1
    chunks = [results[i:i+chunk_size] for i in range(0, len(results), chunk_size)]
    with multiprocessing.Pool() as pool:
        discogs_information = pool.starmap(preprocess_data, [(chunk, discogs_token) for chunk in chunks])

    return [item for sublist in discogs_information for item in sublist]

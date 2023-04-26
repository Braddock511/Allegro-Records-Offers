Python scripts that preprocess data in chunks

search_data - searches the Discogs API for metadata associated with the input text chunks. Uses regular expressions to clean and filter the text data before making a call to either the "get_vinyl" or "get_cd" function (depending on the type of record specified) to retrieve search results from the Discogs API. The search results are filtered and returned as a list of dictionaries.
- chunk: a list of text chunks
- discogs_token: a string containing the authentication token for the Discogs API
- type_record: a string indicating the type of record (either "Vinyl" or "CD")
- image_data: a boolean indicating whether the data is an image

preprocess_data - takes a list of Discogs API search results and processes the data to extract relevant metadata. The function uses various string manipulation techniques to clean and format the metadata fields before adding them to a new dictionary. The final output is a list of dictionaries containing processed metadata for each item in the input search results.
- chunk: a list of dictionaries containing Discogs API search results
- discogs_token: a string containing the authentication token for the Discogs API

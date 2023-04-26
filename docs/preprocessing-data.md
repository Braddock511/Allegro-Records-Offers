Python scripts that preprocessing data

search_data_parallel - takes a list of strings, each string containing text extracted from an image, and splits the list into chunks based on the number of available CPUs. It then uses multiprocessing to search the Discogs API for vinyl records matching the input texts, using the search_data function, and returns a list of dictionaries containing information about the matching records
- text_from_image (list): list of strings, each string containing text extracted from an image.
- discogs_token (str): containing the Discogs API token.
- type_record (str): specifying the type of record to search for in the Discogs database.
- image_data (boolean): value indicating whether or not image data is included in the search.

preprocess_data_parallel -  takes a string or list of strings containing text extracted from an image, cleans up the input string(s), and searches the Discogs API for vinyl records matching the input texts, using the search_data_parallel function. It then splits the results list into chunks based on the number of available CPUs, and uses multiprocessing to preprocess the data, using the preprocess_data function. Finally, it returns a list of dictionaries containing information about the matching records.
- text_from_image (str | list): string or list of strings, containing text extracted from an image.
- credentials (dictionary): credentials needed for the Discogs and ImageKit APIs.
- type_record (str): specifying the type of record to search for in the Discogs database (e.g., "vinyl").
- image_data (boolean): value indicating whether or not image data is included in the search.

remove_background - removes the background from an image specified by its URL, using the clear_image function, and uploads the cleared image to ImageKit, using the upload_file_imageKit function. It then returns the URL of the cleared image.
- image_url (str): URL of the image to remove the background from.
- credentials (dictionary): credentials needed for the ImageKit API.

get_cd_barcode - uploads the image to ImageKit, using the upload_file_imageKit function, and decodes the barcode from the image, using the pyzbar package. If a barcode is found in the image, it returns a tuple containing the decoded barcode and the URL of the original image. If no barcode is found, it returns an empty string and the URL of the original image.
image (str): base64 image file
credentials (dictionary): credentials needed for the ImageKit API.
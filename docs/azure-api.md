Python scripts that includes functions to interact with the Azure API

read_image - takes an image file path and credentials dictionary as input and returns a tuple containing a list of extracted text and the image URL
- image (str): base64 image file to be processed.
- credentials (dict): a dictionary containing credentials necessary to use the Azure Computer Vision API and ImageKit.

clear_image - takes an image URL and credentials dictionary as input and returns a string representing the result of applying background removal to the image
- image_url (str): a URL of the image to be processed.
- credentials (dict): a dictionary containing credentials necessary to use the Azure Computer Vision API and ImageKit.
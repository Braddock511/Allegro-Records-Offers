Python scripts that preprocessing images

read_image - Reads the text from an image using OCR and returns the extracted text and image URL.
- image (str): The image file or URL.
- credentials (Dict[str, str]): The credentials containing the necessary information.

preprocess_vinyl_images - Preprocesses vinyl images by reading the text from the images using OCR.
- images (List[str]): A list of image URLs.
- credentials (Dict[str, str]): The credentials containing the necessary information.

get_cd_barcode - Retrieves the CD barcode from an image.
- image (bytes): The image data in bytes.
- credentials (dict): The credentials containing the necessary informatio

preprocess_cd_images - Preprocesses CD images to extract barcode information
- image (bytes): The image data in bytes.
- credentials (dict): The credentials containing the necessary informatio

remove_background - Remove background from an image and upload the resulting image.
- image_url (str): URL of the image to remove the background from.
- credentials (Dict[str, str]): Credentials for image processing and uploading.
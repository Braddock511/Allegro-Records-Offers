import numpy as np
import requests
import base64
import asyncio
from PIL import Image
from pyzbar import pyzbar
from io import BytesIO
from typing import Dict
from rembg import remove
from imageKit_api import upload_file_imageKit

def resize_image(image_url: str, max_size_kb: int = 768) -> bytes:
    try:
        response = requests.get(image_url)
        image_bytes = response.content        
        img = Image.open(BytesIO(image_bytes))
        max_size_bytes = max_size_kb * 1024

        img_bytes = BytesIO()
        img.save(img_bytes, format="JPEG")
        current_size = len(img_bytes.getvalue())

        if current_size <= max_size_bytes:
            return base64.b64encode(img_bytes.getvalue())

        # Calculate the new quality to reduce the size
        quality = int((max_size_bytes / current_size) * 100)

        # Reduce the image quality to fit the size limit
        img = img.convert("RGB")
        img_bytes = BytesIO()
        img.save(img_bytes, format="JPEG", quality=quality)
        
        return base64.b64encode(img_bytes.getvalue())

    except Exception as e:
        return None

def read_image(image: str, credentials: Dict[str, str]) -> tuple[str, str]:
    """
        Reads the text from an image using OCR and returns the extracted text and image URL.

        Args:
            image (str): The image file or URL.
            credentials (Dict[str, str]): The credentials containing the necessary information.

        Returns:
            tuple[str, str]: The extracted text and image URL.
    """
    image_url = upload_file_imageKit(image, credentials)['url']
    resized_image = resize_image(image_url)
    resized_image_url = upload_file_imageKit(resized_image, credentials)['url']
    
    api_url = "https://api.ocr.space/parse/image"
    
    payload = {
        "apikey": credentials['api_ocr_space'],
        "language": "eng",
        "url": resized_image_url,
        "filetype": "URL",
    }

    response = requests.post(api_url, data=payload)
    result = response.json()

    # Extract the extracted text and image URL
    output_text = result.get("ParsedResults")[0].get("ParsedText").splitlines()
    
    return output_text, image_url

async def preprocess_vinyl_images(images: list, credentials: Dict[str, str]) -> list:
    """
        Preprocesses vinyl images by reading the text from the images using OCR.

        Args:
            images (List[str]): A list of image URLs.
            credentials (Dict[str, str]): The credentials containing the necessary information.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing the extracted text and image URL for each image.
    """
    # Read first image
    text_from_image_1, image_url_1 = await asyncio.to_thread(read_image, images[0], credentials)
    text_from_images = [{"text_from_image": text_from_image_1, "url": image_url_1}]
    # Other images
    other_image_tasks = [asyncio.to_thread(upload_file_imageKit, other_image, credentials) for other_image in images[1:]]
    other_image_urls = await asyncio.gather(*other_image_tasks)

    text_from_images.extend({"text_from_image": "{}", "url": other_image_url['url']} for other_image_url in other_image_urls)
    
    return text_from_images

def get_cd_barcode(image: bytes, credentials: dict) -> tuple[str, str]:
    """
        Retrieves the CD barcode from an image.

        Args:
            image (bytes): The image data in bytes.
            credentials (dict): The credentials containing the necessary information.

        Returns:
            Tuple[str, str]: A tuple containing the extracted barcode data and the image URL.
    """
    upload_image = upload_file_imageKit(image, credentials)
    image_url = upload_image['url']
    response = requests.get(image_url).content

    image = np.array(Image.open(BytesIO(response)).convert('RGB'))
    barcodes = pyzbar.decode(image)

    for barcode in barcodes:
        if data := barcode.data.decode("utf-8"):
             return data, image_url
    
    return "", image_url

async def preprocess_cd_images(images: list, credentials: Dict[str, str]) -> list:
    """
        Preprocesses CD images to extract barcode information.

        Args:
            images (List[bytes]): The CD images in bytes.
            credentials (dict): The credentials containing the necessary information.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing the extracted text and image URLs.
    """
    # Read second image 
    text_from_image, image_url_2 = await asyncio.to_thread(get_cd_barcode, images[1], credentials)

    # First image
    image_url_1 = await asyncio.to_thread(upload_file_imageKit, images[0], credentials)

    text_from_images = [
        {"text_from_image": "{}", "url": image_url_1['url']},
        {"text_from_image": text_from_image, "url": image_url_2},
    ]
    # Other images
    other_image_tasks = [asyncio.to_thread(upload_file_imageKit, other_image, credentials) for other_image in images[2:]]
    other_image_urls = await asyncio.gather(*other_image_tasks)

    text_from_images.extend({"text_from_image": "{}", "url": other_image_url['url']} for other_image_url in other_image_urls)
    
    return text_from_images

def remove_background(image_url: str, credentials: Dict[str, str]) -> str:
    """
        Remove background from an image and upload the resulting image.

        Args:
            image_url (str): URL of the image to remove the background from.
            credentials (Dict[str, str]): Credentials for image processing and uploading.

        Returns:
            str: URL of the uploaded image without the background.
    """
    response = requests.get(image_url)
    image_data = response.content

    # Process the image data to remove the background
    image_without_background = remove(image_data)
    image_without_background = base64.b64encode(image_without_background).decode('utf-8')

    upload_image = upload_file_imageKit(image_without_background, credentials)
    
    return upload_image['url']
    
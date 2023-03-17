from imagekitio import ImageKit

def upload_file_imageKit(image: str, credentials: list):
    imageKit_config = {
        "public_key": credentials[0],
        "private_key": credentials[1],
        "url_endpoint": credentials[2]
    }

    imagekit = ImageKit(**imageKit_config)

    result = imagekit.upload_file(file=image, file_name=f'{image[:10]}.png')

    return result.response_metadata.raw
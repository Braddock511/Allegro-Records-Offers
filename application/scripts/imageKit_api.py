from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

def upload_file_imageKit(image: str|bytes, credentials: dict[str, str]) -> dict[str, str]:
    imageKit_config = {
        "public_key": credentials["api_imagekit_id"],
        "private_key": credentials["api_imagekit_secret"],
        "url_endpoint": credentials["api_imagekit_endpoint"]
    }

    image_options = UploadFileRequestOptions(
        folder='/',
    )
    
    imagekit = ImageKit(**imageKit_config)

    result = imagekit.upload_file(file=image, file_name=f'{image[:10]}.png', options=image_options)
    return result.response_metadata.raw
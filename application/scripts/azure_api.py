import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from time import sleep
from imageKit_api import upload_file_imageKit

def read_image(image: str, credentials: dict) -> tuple[list, str]:
    subscription_key = credentials["api_azure_subscription_key"]
    endpoint = credentials["api_azure_endpoint"]

    # Create ComputerVisionClient object using credentials
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Upload image to ImageKit and get the URL
    image = upload_file_imageKit(image, credentials)
    read_image_url = image['url']

    # Submit image for OCR
    read_response = computervision_client.read(read_image_url,  raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Wait for OCR operation to complete
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        sleep(1)

    # Extract text from OCR result
    if read_result.status == OperationStatusCodes.succeeded:
        output_text = []
        for text_result in read_result.analyze_result.read_results:
            output_text += [line.text for line in text_result.lines]
    else:
        return ("Error", {"error": f"OCR operation did not succeed"})

    return output_text, read_image_url

def clear_image(image_url: str, credentials: dict) -> str:
    try:
        subscription_key = credentials["api_azure_subscription_key"]
        endpoint = credentials["api_azure_endpoint"]
        headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": subscription_key}

        response = requests.post(f"{endpoint}/computervision/imageanalysis:segment?api-version=2023-02-01-preview&mode=backgroundRemoval", headers=headers, json={"url": image_url})
        
        return response.content
    
    except Exception as e:
        return {"error": f"Error in clear_image: {e}"}
    
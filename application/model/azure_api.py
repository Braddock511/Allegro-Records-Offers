import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from time import sleep
from imageKit_api import upload_file_imageKit

def read_image(image: str, credentials: list):
    try:
        subscription_key = credentials[3]
        endpoint = credentials[4]

        # create ComputerVisionClient object using credentials
        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

        # upload image to ImageKit and get the URL
        image = upload_file_imageKit(image, credentials)
        read_image_url = image['url']

        # submit image for OCR
        read_response = computervision_client.read(read_image_url,  raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        # wait for OCR operation to complete
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            sleep(1)

        # extract text from OCR result
        if read_result.status == OperationStatusCodes.succeeded:
            output_text = []
            for text_result in read_result.analyze_result.read_results:
                output_text += [line.text for line in text_result.lines]
        else:
            print("OCR operation did not succeed")
            return None, None

        return output_text, read_image_url

    except Exception as e:
        print(f"Error in read_image: {e}")
        return None, None
    
def clear_image(image: str, credentials: list):
    try:
        subscription_key = credentials[3]
        endpoint = credentials[4]

        headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": subscription_key}
        response = requests.post(f"{endpoint}/computervision/imageanalysis:segment?api-version=2023-02-01-preview&mode=backgroundRemoval", headers=headers, json={"url": image})
        return response.content
    
    except Exception as e:
        print(f"Error in clear_image: {e}")
        return None
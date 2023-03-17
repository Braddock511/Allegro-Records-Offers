import unittest
from unittest.mock import MagicMock, patch
from application.model.preprocessing_data import search_data, preprocess_data
from application.model.imageKit_api import upload_file_imageKit
from application.model.discogs_api import get_vinyl, get_cd, get_price, get_tracklist

class Test(unittest.TestCase):
    
    def test_search_data_with_valid_data(self):
        data = ["E1 60439", "PCS 3062"]
        discogs_token = "token"
        type_record = "vinyl"
        image_data = False
        result = search_data(data, discogs_token, type_record, image_data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
    
    @patch('application.model.preprocessing_data.search_data')
    @patch('application.model.discogs_api.get_price')
    def test_preprocess_data_with_string_input(self, mock_get_price, mock_search_data):
        mock_get_price.return_value = "$10.00"
        mock_search_data.return_value = [{'id': '123', 'uri': '/release/123', 'genre': ['Rock'], 'title': 'Album Name', 'country': 'US', 'year': '1980', 'label': ['Label Name'], 'catno': '12345'}]

        data = "123, 456, 789"
        credentials = ["", "", "", "", "", "", "", "token"]
        output = preprocess_data(data, credentials)

        expected_output = {
            "url": "",
            "data": [
                {
                    "id": "123",
                    "label": "Label Name 12345",
                    "country": "US",
                    "year": "1980",
                    "uri": "https://www.discogs.com/release/123",
                    "genre": "Rock",
                    "title": "Album Name",
                    "price": "$10.00"
                },
                {
                    "id": "-",
                    "label": "-",
                    "country": "-",
                    "year": "-",
                    "uri": "-",
                    "genre": "-",
                    "title": "-",
                    "price": "-"
                },
                {
                    "id": "-",
                    "label": "-",
                    "country": "-",
                    "year": "-",
                    "uri": "-",
                    "genre": "-",
                    "title": "-",
                    "price": "-"
                }
            ]
        }

        self.assertEqual(output, expected_output)

    @patch('application.model.preprocessing_data.search_data')
    @patch('application.model.discogs_api.get_price')
    def test_preprocess_data_with_list_input(self, mock_get_price, mock_search_data):
        mock_get_price.return_value = "$10.00"
        mock_search_data.return_value = [{'id': '123', 'uri': '/release/123', 'genre': ['Rock'], 'title': 'Album Name', 'country': 'US', 'year': '1980', 'label': ['Label Name'], 'catno': '12345'}]

        data = ["123", "456", "789"]
        credentials = ["", "", "", "", "", "", "", "token"]
        output = preprocess_data(data, credentials)

        expected_output = {
            "url": "",
            "data": [
                {
                    "id": "123",
                    "label": "Label Name 12345",
                    "country": "US",
                    "year": "1980",
                    "uri": "https://www.discogs.com/release/123",
                    "genre": "Rock",
                    "title": "Album Name",
                    "price": "$10.00"
                },
                {
                    "id": "-",
                    "label": "-",
                    "country": "-",
                    "year": "-",
                    "uri": "-",
                    "genre": "-",
                    "title": "-",
                    "price": "-"
                },
                {
                    "id": "-",
                    "label": "-",
                    "country": "-",
                    "year": "-",
                    "uri": "-",
                    "genre": "-",
                    "title": "-",
                    "price": "-"
                }
            ]
        }

        self.assertEqual(output, expected_output)
    
    @patch('application.model.imageKit_api.ImageKit')
    def test_upload_file_imageKit(self, mock_ImageKit):
        credentials = ["my_public_key", "my_private_key", "my_url_endpoint"]
        image = "test_image.png"
        
        mock_upload = MagicMock()
        mock_upload.return_value = {"response_metadata": {"raw": "my_raw_response"}}
        mock_ImageKit.return_value.upload_file = mock_upload
        
        result = upload_file_imageKit(image, credentials)
        self.assertEqual(result, "my_raw_response")
        mock_ImageKit.assert_called_once_with(public_key="my_public_key", private_key="my_private_key", url_endpoint="my_url_endpoint")
        mock_upload.assert_called_once_with(file=image, file_name="my_image.png")

    @patch('application.model.discogs_api.get_vinyl')
    def test_get_vinyl(self, mock_requests_get):
        expected_response = {'results': [{'id': '123', 'title': 'Vinyl Record'}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_response
        mock_requests_get.return_value = mock_response

        discogs_token = 'some-token'
        query = 'Vinyl Record'

        response = get_vinyl(query, discogs_token)

        self.assertEqual(response, expected_response)
    
    @patch('application.model.discogs_api.get_cd')
    def test_get_cd(self, mock_requests_get):
        expected_response = {'results': [{'id': '456', 'title': 'CD'}]}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_response
        mock_requests_get.return_value = mock_response

        discogs_token = 'token'
        barcode = '1234567890'

        response = get_cd(barcode, discogs_token)

        self.assertEqual(response, expected_response)

    @patch('application.model.discogs_api.get_price')
    def test_get_price(self, mock_requests_get):
        expected_response = {'value': 20}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_response
        mock_requests_get.return_value = mock_response

        discogs_token = 'token'
        id = '789'

        response = get_price(id, discogs_token)

        self.assertEqual(response, expected_response)

    @patch('application.model.discogs_api.get_tracklist')
    def test_tracklist_found(self, mock_get):
        mock_response = {"tracklist": [
            {"position": "A1", "title": "Track 1"},
            {"position": "A2", "title": "Track 2"},
            {"position": "B1", "title": "Track 3"},
            {"position": "B2", "title": "Track 4"}
        ]}
        mock_get.return_value.json.return_value = mock_response
        discogs_token = "token"
        id = "id"

        expected_output = (
            "<p><b>LISTA UTWORÓW:</b></p>"
            "<p><b>A1. Track 1</b> | <b>A2. Track 2</b></p>"
            "<p><b>B1. Track 3</b> | <b>B2. Track 4</b></p>"
        )

        output = get_tracklist(id, discogs_token)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
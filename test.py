import unittest
from unittest.mock import MagicMock, patch
from application.model.preprocessing_data import search_data, preprocess_data
from application.model.imageKit_api import upload_file_imageKit
from application.model.discogs_api import get_vinyl, get_cd, get_price, get_tracklist
from application.api.database import post_credentials, get_credentials, post_data_image, get_data_image
from sqlalchemy.orm import Session

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

    @patch('application.api.database.create_engine')
    @patch('application.api.database.sessionmaker')
    def test_post_credentials(self, mock_sessionmaker, mock_create_engine):
        # Mock database session
        mock_session = MagicMock(spec=Session)
        mock_sessionmaker.return_value = mock_session
        
        # Mock SQLAlchemy engine
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        allegro_id = 'test_allegro_id'
        allegro_secret = 'test_allegro_secret'
        allegro_token = 'test_allegro_token'
        post_credentials(allegro_id, allegro_secret, allegro_token)
        
        # Assert that SQLAlchemy engine is created with the correct URL
        mock_create_engine.assert_called_once_with("postgresql://postgres:admin@localhost:5432/postgres")
        
        # Assert that SQLAlchemy session is created and used correctly
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch('application.api.database.create_engine')
    @patch('application.api.database.sessionmaker')
    def test_get_credentials(self, mock_sessionmaker, mock_create_engine):
        # Create a mock session
        mock_session = MagicMock(spec=Session)
        mock_session.return_value.query.return_value.order_by.return_value.limit.return_value.first.return_value = {
            "api_imagekit_id": "test_api_imagekit_id",
            "api_imagekit_secret": "test_api_imagekit_secret",
            "api_imagekit_endpoint": "test_api_imagekit_endpoint",
            "api_azure_subscription_key": "test_api_azure_subscription_key",
            "api_azure_endpoint": "test_api_azure_endpoint",
            "api_discogs_id": "test_api_discogs_id",
            "api_discogs_secret": "test_api_discogs_secret",
            "api_discogs_token": "test_api_discogs_token",
            "api_allegro_id": "test_api_allegro_id",
            "api_allegro_secret": "test_api_allegro_secret",
            "api_allegro_token": "test_api_allegro_token"
        }

        # Configure the mocks
        mock_sessionmaker.return_value = mock_session
        mock_create_engine.return_value = MagicMock()

        result = get_credentials()

        self.assertEqual(result, [
            "test_api_imagekit_id",
            "test_api_imagekit_secret",
            "test_api_imagekit_endpoint",
            "test_api_azure_subscription_key",
            "test_api_azure_endpoint",
            "test_api_discogs_id",
            "test_api_discogs_secret",
            "test_api_discogs_token",
            "test_api_allegro_id",
            "test_api_allegro_secret",
            "test_api_allegro_token"
        ])

    @patch('application.api.database.create_engine')
    @patch('application.api.database.sessionmaker')
    def test_post_data_image(self, mock_sessionmaker, mock_create_engine):
        data = [
            {'data': 'image_data_1', 'url': 'https://www.example.com/image_1.jpg'},
            {'data': 'image_data_2', 'url': 'https://www.example.com/image_2.jpg'},
            {'data': 'image_data_3', 'url': 'https://www.example.com/image_3.jpg'},
        ]
        
        # Mock the database dependencies
        mock_engine = mock_create_engine.return_value
        mock_session = mock_sessionmaker.return_value
        
        # Call the function
        post_data_image(data)
        
        # Assert the data has been added to the table
        mock_session.assert_called_once_with(bind=mock_engine)
        mock_session.return_value.add_all.assert_called_once_with([
            {"data":'image_data_1', "url":'https://www.example.com/image_1.jpg'},
            {"data":'image_data_2', "url":'https://www.example.com/image_2.jpg'},
            {"data":'image_data_3', "url":'https://www.example.com/image_3.jpg'},
        ])
        mock_session.return_value.commit.assert_called_once_with()
        mock_session.return_value.close.assert_called_once_with()
        
        # Clean up the database
        mock_session.return_value.query.return_value.delete.assert_called_once_with()
        mock_session.return_value.commit.assert_called_once_with()
        mock_session.return_value.close.assert_called_once_with()

    @patch('application.api.database.create_engine')
    @patch('application.api.database.sessionmaker')
    def test_get_data_image(self, mock_sessionmaker, mock_create_engine):
        #        # Create a mock session
        mock_session = MagicMock(spec=Session)
        mock_session.query.return_value.all.return_value = [{
            'data': ['data1', 'data2'],
            'url': ['url1', 'url2']
        }]

        # Configure the mocks
        mock_sessionmaker.return_value = mock_session
        mock_create_engine.return_value = MagicMock()

        expected_output = {
            'data': ['data1', 'data2'],
            'url': ['url1', 'url2']
        }
        
        result = get_data_image()

        self.assertEqual(result, expected_output)
        mock_session.execute.assert_called_with('TRUNCATE data_image')
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
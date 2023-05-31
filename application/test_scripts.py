import base64
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
import requests
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.main import app
from api.database import post_credentials, get_credentials, post_text_from_image, get_text_from_image, post_allegro_offers, get_allegro_offers, truncate_allegro_offers, truncate_allegro_payments
from scripts.allegro_api import get_my_offers, get_offer_info, create_offer, get_condition_and_carton, edit_description, get_payment_history, edit_images, swap_cartons
from scripts.discogs_api import get_vinyl, get_cd, get_price, get_tracklist, create_offer
from scripts.imageKit_api import upload_file_imageKit
from scripts.plots import annual_sale_barplot, create_genres_barplot
from scripts.preprocessing_data import search_data_parallel, preprocess_data_parallel
from scripts.chunks import search_data, preprocess_data
from scripts.preprocessing_image import read_image, preprocess_vinyl_images, get_cd_barcode, preprocess_cd_images, remove_background

Base = declarative_base()

class Credentials(Base):
        __tablename__ = "credentials"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)

        api_imagekit_id = Column(String)
        api_imagekit_secret = Column(String)
        api_imagekit_endpoint = Column(String)

        api_ocr_space = Column(String)

        api_discogs_token = Column(String)

        api_allegro_id = Column(String)
        api_allegro_secret = Column(String)
        api_allegro_token = Column(String)

class Image_Data(Base):
    __tablename__ = "image_data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text_from_image = Column(String)
    url = Column(String)

class AllegroOffers(Base):
    __tablename__ = "allegro_offers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    offer_id = Column(String)
    offer_data = Column(String)

class AllegroPayments(Base):
    __tablename__ = "allegro_payments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    payment = Column(String)

class Flags(Base):
    __tablename__ = "flags"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    load_offers = Column(Boolean)
    load_payment = Column(Boolean)

class TestDatabase:
    SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:admin@localhost:5432/postgres"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    def test_post_credentials(self):
        post_credentials("test_id", "test_secret", "test_token")

        row = self.session.query(Credentials).order_by(Credentials.id.desc()).first()

        assert row.api_allegro_id == "test_id"
        assert row.api_allegro_secret == "test_secret"
        assert row.api_allegro_token == "test_token"

    def test_get_credentials(self):
        result = get_credentials()

        assert result['api_allegro_id'] == "test_id"
        assert result['api_allegro_secret'] == "test_secret"
        assert result['api_allegro_token'] == "test_token"

    def test_post_text_from_image(self):
        text_from_images = [[{"text_from_image": "test", "url": "test.png"}, 
                            {"text_from_image": "", "url": "test.png"}, 
                            {"text_from_image": "", "url": "test.png"}],
                            [{"text_from_image": "test2", "url": "test2.png"}, 
                            {"text_from_image": "", "url": "test2.png"}, 
                            {"text_from_image": "", "url": "test2.png"}]]
        
        post_text_from_image(text_from_images)

        row = self.session.query(Image_Data).first()

        assert row.text_from_image == 'test'
        assert row.url == 'test.png'

    def test_get_text_from_image(self):
        result = get_text_from_image()

        assert result[0]['text_from_image'] == 'test'
        assert result[0]['url'] == 'test.png'
        
    def test_post_get_allegro_offers(self):
        allegro_offers = [{"id": '12456', "name": "test1"},
                          {"id": '92251', "name": "test2"},
                          {"id": '95253', "name": "test3"}]
        
        post_allegro_offers(allegro_offers)
        result = get_allegro_offers()

        assert isinstance(result[0], dict)
        
    def test_truncate_allegro_offers(self):
        truncate_allegro_offers()
        
        result = get_allegro_offers()
        
        assert result == []
        
    def test_truncate_allegro_payments(self):
        truncate_allegro_payments()
        
        result = truncate_allegro_payments()
        
        assert result is None

class TestAPI:
    client = TestClient(app)

    response = requests.get("https://ik.imagekit.io/jhddvvyeg/test.jpg?updatedAt=1685255855385")
    image_content = response.content
    vinyl_image = base64.b64encode(image_content).decode('utf-8')

    response = requests.get("https://ik.imagekit.io/jhddvvyeg/testCD.jpg?updatedAt=1685256086025")
    image_content = response.content
    cd_image = base64.b64encode(image_content).decode('utf-8')

    def test_read_vinyl_image(self):
        test_input = {
            "images": [TestAPI.vinyl_image, TestAPI.vinyl_image, TestAPI.vinyl_image],
        }

        response = TestAPI.client.post("/read-vinyl-image", json=test_input)

        assert response.status_code == 200
        
    def test_read_cd_image(self):
        test_input = {
            "images": [TestAPI.cd_image, TestAPI.cd_image, TestAPI.cd_image],
        }

        response = TestAPI.client.post("/read-vinyl-image", json=test_input)

        assert response.status_code == 200

    def test_discogs_information_image(self):
        payload = {
            "index": 0,
            "numberImages": 3,
            "typeRecord": "Vinyl",
        }

        response = TestAPI.client.post('/discogs-information-image', json=payload)

        assert response.status_code == 200

    def test_clear_image(self):
        test_input = {
            "image": TestAPI.vinyl_image
        }

        response = TestAPI.client.post("/clear-image", json=test_input)

        assert response.status_code == 200

    def test_discogs_info(self):
        test_input = {
            "index": 0,
            "allegroData": {
                "id": "12237324592"
            },
        }

        response = TestAPI.client.post("/discogs-information", json=test_input)

        assert response.status_code == 200

    def test_allegro_offers(self):
        test_data = {
            "limit": 10,
            "offset": 0,
            "typeOffer": "all",
            "typeRecord": "Vinyl",
            "genre": "all"
        }

        response = TestAPI.client.post("/allegro-offers", json=test_data)

        assert response.status_code == 200

    def test_allegro_offer(self):
        test_data = {
            "offerId": "12237324592"
        }

        response = TestAPI.client.post("/allegro-offer", json=test_data)

        assert response.status_code == 200

    def test_allegro_visitors_viewers(self):
        response = TestAPI.client.get("/allegro-visitors-viewers")

        assert response.status_code == 200

    def test_sale_barplot(self):
        response = TestAPI.client.get("/sale-barplot")

        assert response.status_code == 200
    
    def test_genre_barplot(self):
        response = TestAPI.client.get("/genre-barplot")

        assert response.status_code == 200
        
class TestAllegroApi:
    credentials = {"api_allegro_token": "", "api_discogs_token": ""}

    def test_get_my_offers(self):
        limit = 10
        offset = 0
        type_offer = "BUY_NOW"
        type_record = "Vinyl"
        genre = "rock"

        result = get_my_offers(TestAllegroApi.credentials, limit, offset, type_offer, type_record, genre)

        assert isinstance(result, dict)
        assert "items" in result
        assert len(result["items"]) == limit

    def test_get_offer_info(self):
        offer_id = 1234567890

        result = get_offer_info(TestAllegroApi.credentials, offer_id)

        assert isinstance(result, dict)
        assert "id" in result
        assert result["id"] == offer_id

    def test_get_condition_and_carton(self):
        offer_id = 1234567890
        condition, carton = get_condition_and_carton(TestAllegroApi.credentials, offer_id)

        assert isinstance(condition, str)
        assert isinstance(carton, str)
        assert condition != ''
        assert carton != ''

    def test_get_payment_history(self):
        limit = 10
        offset = 0

        result = get_payment_history(TestAllegroApi.credentials, limit, offset)

        assert "payments" in result
        assert "count" in result
        assert "totalCount" in result
        assert len(result["payments"]) <= limit
        assert result["count"] == len(result["payments"])
        assert result["totalCount"] >= result["count"]

    def test_create_offer(self):
        data = {
            "id": "26503601",
            "title": "Artist - Album",
            "label": "Label | 1234",
            "country": "US",
            "year": "1989",
            "genre": "Genre",
            "price": 99.99,
            "barcode": "Barcode"
        }
        carton = "Carton"
        condition = "Near Mint (NM or M-)"
        images = ["image1", "image2"]
        type_record = "Vinyl"
        clear = False
        
        with patch("module.get_tracklist") as mock_get_tracklist, \
            patch("module.get_my_offers") as mock_get_my_offers, \
            patch("module.get_offer_info") as mock_get_offer_info:
            
            # Set up the mocks
            mock_get_tracklist.return_value = "<p><b>LISTA UTWORÓW: -</b></p>"
            mock_get_my_offers.return_value = {"offers": [{"id": "123456789876"}]}
            mock_get_offer_info.return_value = {"payments": "Payments", "location": "Location"}
            
            result = create_offer(TestAllegroApi.credentials, data, carton, condition, images, type_record, clear)
            
            assert "name" in result.keys() 
            
    def test_edit_description(self):
        offer_id = "13565874294"
        images = ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]
        information = {"id": "26503601", "label": "Label | 1234", "country": "US", "year": "1989", "price": 99.99}
        result = edit_description(TestAllegroApi.credentials, offer_id, images, information)

        with patch("module.get_condition_and_carton") as mock_get_condition_and_carton, \
            patch("module.get_tracklist") as mock_get_tracklist, \
            patch("module.get_offer_info") as mock_get_offer_info:
            
            # Set up the mocks
            mock_get_condition_and_carton.assert_called_once_with(TestAllegroApi.credentials, offer_id)
            mock_get_offer_info.assert_called_once_with(TestAllegroApi.credentials, offer_id)
            mock_get_tracklist.assert_called_once_with("1", TestAllegroApi.credentials['api_discogs_token'])
            
            result = edit_description(TestAllegroApi.credentials, offer_id, images, information)
            
            assert "name" in result.keys() 
            
    def test_edit_images(self):
        offer_id = "13565874294"
        images = ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]
        
        result = edit_images(TestAllegroApi.credentials, offer_id, images)
        
        assert "name" in result.keys()

    def test_swap_cartons(self):
        change_carton = "A1"
        change_to_carton = "A2"
        result = swap_cartons(TestAllegroApi.credentials, change_carton, change_to_carton)

        assert result == "test.A2"

class TestDiscogsApi:
    discogs_token = ""

    def test_get_vinyl(self):
        query = "Nirvana"

        result = get_vinyl(query, TestDiscogsApi.discogs_token)

        assert isinstance(result, dict)

    def test_get_cd(self):
        query = "Metallica"

        result = get_cd(query, TestDiscogsApi.discogs_token)

        assert isinstance(result, dict)

    def test_get_price(self):
        id = "26503601"

        result = get_price(id, TestDiscogsApi.discogs_token)

        assert isinstance(result, dict)

    def test_get_trakclist(self):
        id = "26439602"

        result = get_tracklist(id, TestDiscogsApi.discogs_token)

        assert "<p><b>LISTA UTWORÓW: -</b></p>" in result
        
    def test_create_offer(self):
        listing_id = 2491654691
        condition = "Mint (M)"
        sleeve_condition = "Mint (M)"
        carton = "Test"
        price = 299.99
        
        result = create_offer(listing_id, condition, sleeve_condition, carton, price, TestDiscogsApi.discogs_token)
        
        assert "url" in result.keys()

class TestImageKitApi:
    credentials = {"api_imagekit_id": "", 
                   "api_imagekit_secret": "", 
                   "api_imagekit_endpoint": ""}
    
    response = requests.get("https://picsum.photos/200/300")
    image_content = response.content
    image = base64.b64encode(image_content).decode('utf-8')

    def test_upload_file_imageKit(self):
        result = upload_file_imageKit(TestImageKitApi.image, TestImageKitApi.credentials)

        assert isinstance(result, dict)
        assert result['url'].startswith("https://ik.imagekit.io/")

class TestPlots:
    credentials = {"api_imagekit_id": "", 
                   "api_imagekit_secret": "", 
                   "api_imagekit_endpoint": ""}

    def test_annual_sale_barplot(self):
        sales = [{"group": "INCOME", "occurredAt": "2022-01-01", "value": {"amount": "100"}},
                {"group": "EXPENSE", "occurredAt": "2022-02-01", "value": {"amount": "50"}},
                {"group": "INCOME", "occurredAt": "2022-03-01", "value": {"amount": "200"}}]
        
        result = annual_sale_barplot(TestPlots.credentials, sales)

        assert isinstance(result, str)
        assert result.startswith("https://ik.imagekit.io/")

    def test_create_genres_barplot(self):
        data = [
            {'category': {'id': '1410'}},
            {'category': {'id': '5639'}},
            {'category': {'id': '1410'}},
            {'category': {'id': '289'}},
            {'category': {'id': '5639'}},
            {'category': {'id': '1411'}},
            {'category': {'id': '1411'}},
            {'category': {'id': '1410'}},
            {'category': {'id': '289'}},
            {'category': {'id': '5639'}},
            {'category': {'id': '1411'}},
            {'category': {'id': '1411'}}
        ]

        result = create_genres_barplot(TestPlots.credentials, data)

        assert isinstance(result, str)
        assert result.startswith("https://ik.imagekit.io/")

class TestChunks:
    discogs_token = ""
    
    def test_search_data(self):
        input_data = ["Test1", "Test2", "Test3"]
        type_record = "Vinyl"
        image_data = True

        results = search_data(input_data, TestChunks.discogs_token, type_record, image_data)
        
        assert isinstance(results, list)
        assert all(isinstance(item, dict) for item in results)

    def test_preprocess_data(self):
        input_data = [
            {
                "id": 123,
                "uri": "/release/123",
                "genre": ["Rock"],
                "title": "Sample Album",
                "country": "USA",
                "year": 2021,
                "barcode": ["123456789"],
                "label": ["Sample Label"],
                "catno": "CAT001",
                "community": {"want": 10, "have": 5}
            }
        ]
        results = preprocess_data(input_data, TestChunks.discogs_token)

        assert isinstance(results, list)
        assert all(isinstance(item, dict) for item in results)

class TestPreprocessingData:
    credentials = {"api_discogs_token": "", 
                   "api_imagekit_id": "", 
                   "api_imagekit_secret": "", 
                   "api_imagekit_endpoint": ""}
            
    def test_search_data_parallel(self):
        # Test case 1: Text data - vinyl
        result = search_data_parallel(["Pink Floyd - The Dark Side Of The Moon"], TestPreprocessingData.credentials, "Vinyl", False)
        assert len(result) == 1
        assert result[0]['title'] == "The Dark Side Of The Moon"

        # Test case 2: Text data - cd
        result = search_data_parallel(["0602557156317"], TestPreprocessingData.credentials, "CD", False)
        assert len(result) == 1
        assert result[0]['title'] == "Hardwired...To Self-Destruct"

        # Test case 3: Image data - vinyl
        result = search_data_parallel(['JNYHUID MI SOYR', 'SIDE 1', 'LICENSEE TRADE MARK', 'sport (4:03)', 'GEMA', 'INAUTHORIZED PUBLIC PERFORMANCE BROAD', 'HAMBURG', '33', 'ATL 40 417', '1972 Atlantic Records', 'Klaus Doldinger', 'Except "Fairy Tale" - Trad. Adpt. By', 'Klaus Doldinger', 'All Titles Composed And Produced By', 'ATLANTIC', '4. Get Yourself A Second Passpo', '3. Fairy Tale (7:32)', '1. Mandragora (3:46)', '2. Nexus (5:23)', 'PASSPORT - SECOND PASSPORT', '40 417 -', 'STEREO', 'A ATLANTIC RECORDING CORP. U.S.A.', 'CTURER AND OF THE OWNER OF THE RECORD', 'ALL RIGHTS OF THE', 'BESSIE SMITH', 'AL STEWART', 'SPIRIT', "The World's Greatest Blues", '68258', 'MOONDOG', 'Singar', 'LEONARD COHEN', 'MOONDOG', 'POCO', 'The Bassie Smith Story Volumes 1-4', 'ARGENT', '52377/78/79/80', 'Argent', 'AMERICAN', 'KALEIDOSCOPE', 'Clear', '83729', 'The Family That Plays Together', '83523', 'argeac', '+', 'Spirit', '83278', 'Zero She Flies', '53848', '63241', "IT'S A", 'Love Chronicles', '83450', 'TIFUL DAY', '64082', 'Bedsitter', '53087', 'TREES', 'MILES DAVIS', 'ROCK WORKSHOP', 'bernice', '84005', 'Marrying Maiden', '64085', 'A Beautiful Day', '#3722', 'AMORY KANE', 'The Garden Of Jane Delawney', 'LAURA NYRO', '63837', 'BLACK WIDOW', 'on', 'AHAL', 'Rask Workshop', '64076', 'CEt', 'BOB DYLAN', 'REDBONE', 'SIM', 'GARFU', 'New York Tandeberry', 'L', 'Ch And The Thirteenth Confession 032', '63510', 'Nashville Skyline', 'Highway 61 Revisited', '88260', 'Giant Stop', 'lapisg it All Back Home', '83601', "The Netch'l blues", '82672', '82516', 'a Metal', '$8228', '83387', 'Just To Be There', 'CHAMBERS BROS', 'EVERLY', 'BROTHERS'], TestPreprocessingData.credentials, "Vinyl", True)
        assert len(result) == 1
        assert result[0]['title'] == "Passport - Second Passport"

        # Test case 4: Empty data
        result = search_data_parallel([""], TestPreprocessingData.credentials, "Vinyl", False)
        assert len(result) == 0
    
    def test_preprocess_data_parallel(self):
        # Test case 1: Image data
        input_text = "ATL40417"
        result = preprocess_data_parallel(input_text, TestPreprocessingData.credentials, "Vinyl")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]['title'] == "Second Passport"

        # Test case 2: Non-image data
        input_text = "Pink Floyd - The Dark Side Of The Moon"
        result = preprocess_data_parallel(input_text, TestPreprocessingData.credentials, "CD", False)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]['title'] == "The Dark Side Of The Moon"
        
class TestPreprocessingImage:
    response = requests.get("https://ik.imagekit.io/jhddvvyeg/test.jpg?updatedAt=1685255855385")
    image_content = response.content
    vinyl_image = base64.b64encode(image_content).decode('utf-8')
    
    credentials = {"api_discogs_token": "", 
                   "api_ocr_space": "",
                   "api_imagekit_id": "", 
                   "api_imagekit_secret": "", 
                   "api_imagekit_endpoint": ""}
    
    def test_read_image(self):
        text, image_url = read_image(TestPreprocessingImage.vinyl_image, TestPreprocessingImage.vinyl_image)

        assert isinstance(text, list)
        assert isinstance(image_url, str)

    async def test_preprocess_vinyl_images(self):
        images = [TestPreprocessingImage.vinyl_image, TestPreprocessingImage.vinyl_image, TestPreprocessingImage.vinyl_image]
        results = await preprocess_vinyl_images(images, TestPreprocessingImage.vinyl_image)

        assert isinstance(results, list)
        assert all(isinstance(item, dict) for item in results)
        
    def test_get_cd_barcode(self):
        text, image_url = get_cd_barcode(TestPreprocessingImage.vinyl_image, TestPreprocessingImage.vinyl_image)

        assert isinstance(text, list)
        assert isinstance(image_url, str)
        
    async def test_preprocess_vinyl_images(self):
        images = [TestPreprocessingImage.vinyl_image, TestPreprocessingImage.vinyl_image, TestPreprocessingImage.vinyl_image]
        results = await preprocess_cd_images(images, TestPreprocessingImage.vinyl_image)

        assert isinstance(results, list)
        assert all(isinstance(item, dict) for item in results)
        
    def test_remove_background(self):
        image_url = "https://ik.imagekit.io/jhddvvyeg/test.jpg?updatedAt=1685255855385"
        result = remove_background(image_url, TestPreprocessingImage.vinyl_image)

        assert isinstance(result, str)
        
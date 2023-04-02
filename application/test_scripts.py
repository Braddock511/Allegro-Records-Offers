import unittest
import base64
import io
from scripts.preprocessing_data import search_data, get_cd_barcode, preprocess_data, remove_background
from scripts.imageKit_api import upload_file_imageKit
from scripts.discogs_api import get_vinyl, get_cd, get_price, get_tracklist
from scripts.allegro_api import get_my_offers, get_offer_info, create_offer, get_condition_and_carton, edit_description, get_payment_history
from scripts.plots import annual_sale_barplot

class Test(unittest.TestCase):
    credentials = {"api_azure_subscription_key": "", "api_azure_endpoint": "", "api_imagekit_id": "", "api_imagekit_secret": "", "api_imagekit_endpoint": "", "api_discogs_token": "", "api_allegro_token": ""}
    
    def test_search_image_data(self):
        data = ['JNYHUIwdxaD sadMI SOYRcedas', 'SIDE asdad1']
        type_record = "Vinyl"
        image_data = True
        result = search_data(data, Test.credentials['discogs_token'], type_record, image_data)

        self.assertEqual(result[0]['country'], "Germany")
        self.assertEqual(result[0]['year'], "1972")
        self.assertEqual(result[0]['label'][0], "Atlantic")
        self.assertEqual(result[1]['country'], "US")
        self.assertEqual(result[1]['year'], "1960")
        self.assertEqual(result[1]['label'][0], "Cook")

    def test_search_image_data_wrong(self):
        data = ['JNYHUID MI SOYR', 'SIDE 1', 'LICENSEE TRADE MARK', 'sport (4:03)', 'GEMA', 'INAUTHORIZED PUBLIC PERFORMANCE BROAD', 'HAMBURG', '33', 'ATL 40 417', '1972 Atlantic Records', 'Klaus Doldinger', 'Except "Fairy Tale" - Trad. Adpt. By', 'Klaus Doldinger', 'All Titles Composed And Produced By', 'ATLANTIC', '4. Get Yourself A Second Passpo', '3. Fairy Tale (7:32)', '1. Mandragora (3:46)', '2. Nexus (5:23)', 'PASSPORT - SECOND PASSPORT', '40 417 -', 'STEREO', 'A ATLANTIC RECORDING CORP. U.S.A.', 'CTURER AND OF THE OWNER OF THE RECORD', 'ALL RIGHTS OF THE', 'BESSIE SMITH', 'AL STEWART', 'SPIRIT', "The World's Greatest Blues", '68258', 'MOONDOG', 'Singar', 'LEONARD COHEN', 'MOONDOG', 'POCO', 'The Bassie Smith Story Volumes 1-4', 'ARGENT', '52377/78/79/80', 'Argent', 'AMERICAN', 'KALEIDOSCOPE', 'Clear', '83729', 'The Family That Plays Together', '83523', 'argeac', '+', 'Spirit', '83278', 'Zero She Flies', '53848', '63241', "IT'S A", 'Love Chronicles', '83450', 'TIFUL DAY', '64082', 'Bedsitter', '53087', 'TREES', 'MILES DAVIS', 'ROCK WORKSHOP', 'bernice', '84005', 'Marrying Maiden', '64085', 'A Beautiful Day', '#3722', 'AMORY KANE', 'The Garden Of Jane Delawney', 'LAURA NYRO', '63837', 'BLACK WIDOW', 'on', 'AHAL', 'Rask Workshop', '64076', 'CEt', 'BOB DYLAN', 'REDBONE', 'SIM', 'GARFU', 'New York Tandeberry', 'L', 'Ch And The Thirteenth Confession 032', '63510', 'Nashville Skyline', 'Highway 61 Revisited', '88260', 'Giant Stop', 'lapisg it All Back Home', '83601', "The Netch'l blues", '82672', '82516', 'a Metal', '$8228', '83387', 'Just To Be There', 'CHAMBERS BROS', 'EVERLY', 'BROTHERS']
        type_record = "Vinyl"
        image_data = True
        result = search_data(data, Test.credentials['discogs_token'], type_record, image_data)

        self.assertEqual(result, [])

    def test_search_vinyl_data(self):
        data = ["E1 60439"]
        type_record = "Vinyl"
        image_data = False
        result = search_data(data, Test.credentials['discogs_token'], type_record, image_data)

        self.assertEqual(result[0]['country'], "US")
        self.assertEqual(result[0]['year'], "1986")
        self.assertEqual(result[0]['label'][0], "Elektra")
        self.assertEqual(result[1]['country'], "Canada")
        self.assertEqual(result[1]['year'], "1986")
        self.assertEqual(result[1]['label'][0], "Elektra")
    
    def test_search_vinyl_data_wrong(self):
        data = ["axsadasdE1 6asdasd0439"]
        type_record = "Vinyl"
        image_data = True
        result = search_data(data, Test.credentials['discogs_token'], type_record, image_data)

        self.assertEqual(result, [])

    def test_search_cd_data(self):
        data = ["88985479932"]
        type_record = "CD"
        image_data = False
        result = search_data(data, Test.credentials['discogs_token'], type_record, image_data)

        self.assertEqual(result[0]['country'], "Russia")
        self.assertEqual(result[0]['year'], "2017")
        self.assertEqual(result[0]['label'][0], "RCA")
        self.assertEqual(result[1]['country'], "Europe")
        self.assertEqual(result[1]['year'], "2017")
        self.assertEqual(result[1]['label'][0], "RCA")

    def test_search_cd_data_wrong(self):
        data = ["88985479932"]
        type_record = "CD"
        image_data = False
        result = search_data(data, Test.credentials['discogs_token'], type_record, image_data)

        self.assertEqual(result, [])

    def test_preprocess_data_vinyl(self):
        data = ["Passport - Second Passport.Ł13"]
        type_record = "Vinyl"
        url = ""
        image_data = False
        result = preprocess_data(data, Test.credentials, type_record, url, image_data)

        self.assertEqual(result[0]['country'], "Germany")
        self.assertEqual(result[0]['year'], "1972")
        self.assertEqual(result[0]['label'][0], "Atlantic")
        self.assertEqual(result[1]['country'], "US")
        self.assertEqual(result[1]['year'], "1960")
        self.assertEqual(result[1]['label'][0], "Cook")

    def test_preprocess_data_vinyl_wrong(self):
        data = ["becscdsd1as"]
        type_record = "Vinyl"
        url = ""
        image_data = False
        result = preprocess_data(data, Test.credentials, type_record, url, image_data)

        self.assertEqual(result, {"url": url, "data": []})        

    def test_preprocess_data_cd(self):
        data = ["88985479932"]
        type_record = "CD"
        url = ""
        image_data = False
        result = preprocess_data(data, Test.credentials, type_record, url, image_data)

        self.assertEqual(result['data'][0]['id'], 11330187)
        self.assertEqual(result['data'][0]['label'], "RCA | 88985479942")
        self.assertEqual(result['data'][0]['country'], "Europe")
        self.assertEqual(result['data'][0]['year'], "2017")
        self.assertEqual(result['data'][0]['uri'], "https://www.discogs.com/Paloma-Faith-The-Architect/release/11330187")
        self.assertEqual(result['data'][0]['genre'], "Pop")
        self.assertEqual(result['data'][0]['title'], "Paloma Faith - The Architect")
        self.assertEqual(list(result.keys()), ['Mint (M)', 'Near Mint (NM or M-)', 'Very Good Plus (VG+)', 'Very Good (VG)', 'Good Plus (G+)', 'Good (G)', 'Fair (F)', 'Poor (P)'])
        self.assertEqual(result['data'][0]['barcode'], "88985479942")

    def test_preprocess_data_cd_wrong(self):
        data = ["asv2d1dcs"]
        type_record = "CD"
        url = ""
        image_data = False
        result = preprocess_data(data, Test.credentials, type_record, url, image_data)

        self.assertEqual(result, {"url": url, "data": []})        

    def test_remove_background(self):
        image_url = "https://fastly.picsum.photos/id/30/1280/901.jpg?hmac=A_hpFyEavMBB7Dsmmp53kPXKmatwM05MUDatlWSgATE"
        result = remove_background(image_url, Test.credentials)

        self.assertNotEqual(result, image_url)

    def test_get_cd_barcode(self):
        with open(r'D:\plyty\E0\17_1.png', 'rb') as f:
            image_bytes = f.read()
            image = base64.b64encode(image_bytes)

        result, _ = get_cd_barcode(image, Test.credentials)
        
        self.assertEqual(result, "4050538283587")

    def test_upload_file_imageKit(self):
        with open(r'D:\plyty\E0\17_1.png', 'rb') as f:
            image_bytes = f.read()
            image = base64.b64encode(image_bytes)

        result = upload_file_imageKit(image, Test.credentials)

        self.assertEqual(result['fileType'], "image")

    def test_get_vinyl(self):
        query = "Passport - Second Passport"
        result = get_vinyl(query, Test.credentials['discogs_token'])

        self.assertEqual(result['results'][0]['country'], "Germany")
        self.assertEqual(result['results'][0]['year'], "1972")
        self.assertEqual(result['results'][0]['label'][0], "Atlantic")

    def test_get_vinyl_wrong(self):
        query = "asfgg2wdasx"
        result = get_vinyl(query, Test.credentials['discogs_token'])

        self.assertEqual(result['results'][0], {})

    def test_get_cd(self):
        barcode = "88985479932"
        result = get_cd(barcode, Test.credentials['discogs_token'])

        self.assertEqual(result['results'][0]['country'], "Europe")
        self.assertEqual(result['results'][0]['year'], "2017")
        self.assertEqual(result['results'][0]['label'][0], "RCA")

    def test_get_cd_wrong(self):
        barcode = "asfdgrwdaxsd"
        result = get_cd(barcode, Test.credentials['discogs_token'])

        self.assertEqual(result['results'][0], {})

    def test_get_price(self):
        id = "26182769"
        result = get_price(id, Test.credentials['discogs_token'])

        self.assertEqual(list(result.keys()), ['Mint (M)', 'Near Mint (NM or M-)', 'Very Good Plus (VG+)', 'Very Good (VG)', 'Good Plus (G+)', 'Good (G)', 'Fair (F)', 'Poor (P)'])

    def test_get_price_wrong(self):
        id = "dw1sas"
        result = get_price(id, Test.credentials['discogs_token'])

        self.assertEqual(result, {})

    def test_get_tracklist(self):
        id = "26182769"
        result = get_tracklist(id, Test.credentials['discogs_token'])

        self.assertEqual(result, "<p><b>LISTA UTWORÓW:</b></p><p><b>A1. Cracker Island</b> | <b>A2. Oil</b></p><p><b>A3. The Tired Influencer</b> | <b>A4. Tarantula</b></p><p><b>A5. Silent Running</b> | <b>B1. New Gold</b></p><p><b>B2. Baby Queen</b> | <b>B3. Tormenta</b></p><p><b>B4. Skinny Ape</b> | <b>B5. Posession Island</b></p>")

    def test_get_tracklist_wrong(self):
        id = "asdasd"
        result = get_tracklist(id, Test.credentials['discogs_token'])

        self.assertEqual(result, "<p><b>LISTA UTWORÓW: -</b></p>")

    def test_get_my_offers(self):
        limit = 1
        offset = 0
        type_offer = "Vinyl"
        genre = "all"
        result = get_my_offers(Test.credentials, limit, offset, type_offer, genre)

        self.assertIn("offers", result.keys())

    def test_get_my_offers_wrong(self):
        limit = 0
        offset = 0
        type_offer = "Vinyl"
        genre = "all"
        result = get_my_offers(Test.credentials, limit, offset, type_offer, genre)

        self.assertNotIn("offers", result.keys())

    def tesy_get_offer_info(self):
        offer_id = "1235676"
        result = get_offer_info(Test.credentials, offer_id)

        self.assertIn("name", result.keys())

    def tesy_get_offer_info_wrong(self):
        offer_id = "cdesda"
        result = get_offer_info(Test.credentials, offer_id)

        self.assertNotIn("name", result.keys())

    def test_create_offer(self):
        data = {"id": 123, "title": "test - title", "label": "test | label", "country": "test country", "year": 1998, "genre": "all", "price": 49.99, "barcode": 1234567890123}
        cartoon = "A1"
        condition = "Mint (M)"
        images = ["example.png", "example2.png", "example3.png"]
        type_record = "Vinyl"
        clear = False
        result = create_offer(Test.credentials, data, cartoon, condition, images, type_record, clear)

        self.assertIn("name", result.keys())

    def test_create_offer_wrong(self):
        data = {"id": 0, "title": "test - title", "label": "test | label", "country": "test country", "year": 1998, "genre": "", "price": "", "barcode": ""}
        cartoon = "A1"
        condition = "Mint (M)"
        images = ["example.png", "example2.png", "example3.png"]
        type_record = "Vinyl"
        clear = False
        result = create_offer(Test.credentials, data, cartoon, condition, images, type_record, clear)

        self.assertNotIn("name", result.keys())

    def test_get_condition_and_carton(self):
        offer_id = "1235676"
        result = get_condition_and_carton(Test.credentials, offer_id)

        conditions = ['M', 'MINT', '-M', 'M-', 'MINT-', '-MINT', 'MINT-.', '  MINT-', 'MINT, FOLIA', 'EX', 'EX+', 'EX++', 'EX-', 'EX.', 'EXCELLENT', 'VG', 'VG+', 'VG++','VG-', 'VERY GOOD', 'BARDZO DOBRY', 'BARDZO DOBRY.', 'G', 'GOOD', 'GOOD+', 'DOBRY', 'MINT-.DO UMYCIA', "MINT. NOWA ZAFOLIOWANA",'BARDZO DOBRY.PŁYTA DO UMYCIA', 'BARDZO DOBRY.DROBNE RYSKI', 'BARDZO DOBRY.DO UMYCIA']
        self.assertIn(result[0], conditions)
        self.assertIsInstance(result[1], str)

    def test_get_condition_and_carton_wrong(self):
        offer_id = "vfsadasd"
        result = get_condition_and_carton(Test.credentials, offer_id)

        conditions = ['M', 'MINT', '-M', 'M-', 'MINT-', '-MINT', 'MINT-.', '  MINT-', 'MINT, FOLIA', 'EX', 'EX+', 'EX++', 'EX-', 'EX.', 'EXCELLENT', 'VG', 'VG+', 'VG++','VG-', 'VERY GOOD', 'BARDZO DOBRY', 'BARDZO DOBRY.', 'G', 'GOOD', 'GOOD+', 'DOBRY', 'MINT-.DO UMYCIA', "MINT. NOWA ZAFOLIOWANA",'BARDZO DOBRY.PŁYTA DO UMYCIA', 'BARDZO DOBRY.DROBNE RYSKI', 'BARDZO DOBRY.DO UMYCIA']
        self.assertNotIn(result[0], conditions)
        self.assertNotIsInstance(result[1], str)

    def test_edit_description(self):
        offer_id = "1235676"
        images = ["example.png", "example2.png", "example3.png"]
        information = {"id": "5432134", "label": "test | label", "country": "test country", "year": 1978}
        result = edit_description(Test.credentials, offer_id, images, information)

        self.assertIn("name", result.keys())

    def test_edit_description_wrong(self):
        offer_id = "asdasd"
        images = ["example.png", "example2.png", "example3.png"]
        information = {"id": "5432134", "label": "test | label", "country": "test country", "year": 1978}
        result = edit_description(Test.credentials, offer_id, images, information)

        self.assertNotIn("name", result.keys())

    def test_edit_images(self):
        offer_id = "1235676"
        images = ["example.png", "example2.png", "example3.png"]
        result = edit_description(Test.credentials, offer_id, images)

        self.assertIn("name", result.keys())

    def test_edit_images_wrong(self):
        offer_id = "1235676"
        images = ["example.png", "example2.png", "example3.png"]
        result = edit_description(Test.credentials, offer_id, images)

        self.assertNotIn("name", result.keys())

    def test_allegro_sale(self):
        payments = []

        for i in range(10):
            payment_history = get_payment_history(Test.credentials, 100, 100*i)
            payments.append(payment_history['paymentOperations'])

        payments = sum(payments, [])
        
        self.assertIn("wallet1", payments[0].keys(), msg=payments[:100])

    def test_annual_sale_barplot(self):
        data = [{'type': '', 'group': '', 'wallet': {'paymentOperator': '', 'type': '', 'balance': {'amount': '', 'currency': ''}}, 'occurredAt': '', 'value': {'amount': '', 'currency': ''}, 'marketplaceId': '', 'payment': {'id': ''}, 'participant': {'id': '', 'companyName': None, 'login': '', 'firstName': '', 'lastName': '', 'address': {'street': '', 'city': '', 'postCode': ''}}}]
        result = annual_sale_barplot(Test.credentials, data)

        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()

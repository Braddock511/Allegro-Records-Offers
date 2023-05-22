from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from json import loads
import database as db
import allegro_api as allegro
from   preprocessing_image import read_image, remove_background
from   preprocessing_data import preprocess_data_parallel, get_cd_barcode
from   imageKit_api import upload_file_imageKit
from   plots import annual_sale_barplot, create_genres_barplot
from   discogs_api import create_offer

app = FastAPI()

# CORS middleware to allow requests from a specific origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/read-image")
async def read_image_data(request: Request):
    try:
        db.truncate_image_data()
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        images = response['images']
        type_record = response['typeRecord']
        number_images = response['numberImages']
        text_from_images = []

        for i in range(0, len(images), number_images):
            if type_record == "Vinyl":
                # Read first image
                image_1 = images[i]
                text_from_image_1, image_url_1 = read_image(image_1, credentials)
                text_from_images.append({"text_from_image": text_from_image_1, "url": image_url_1})

                # Other images
                for j in range(1, number_images):
                    other_image = images[i+j]
                    other_image_url = upload_file_imageKit(other_image, credentials)['url']
                    text_from_images.append({"text_from_image": "EMPTY", "url": other_image_url})

            elif type_record == "CD":
                # Read second image 
                image_2 = images[i+1]
                text_from_image, image_url_2 = get_cd_barcode(image_2, credentials)
                
                # Other images
                for j in range(number_images):
                    if j != 1:
                        other_image = images[i+j]
                        other_image_url = upload_file_imageKit(other_image, credentials)['url']
                        text_from_images.append({"text_from_image": "EMPTY", "url": other_image_url})

                    if j == 0:
                        text_from_images.append({"text_from_image": text_from_image, "url": image_url_2})

        db.post_text_from_image(text_from_images)

        return {"status": 200, "output": text_from_images}

    except Exception as e:
        return {"status": 404, "error": f"Exception in read_image: {str(e)}"}

@app.post("/clear-image")
async def clear_image(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        image = response['image']
        
        clear_image_url = remove_background(image, credentials)
        
        return {"status": 200, "output": clear_image_url}

    except Exception as e:
        return {"status": 404, "error": f"Exception in clear_image: {str(e)}"}

@app.post("/discogs-information")
async def discogs_info(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        record_id = response['id']
        allegro_data = response['allegroData']
        type_record = None
        offer_input_data = None
        
        if "offers" in allegro_data.keys():
            offers_info = allegro.get_offer_info(credentials, allegro_data['offers'][record_id]['id'])
        else:
            offers_info = allegro.get_offer_info(credentials, allegro_data['id'])
        
        parameters = offers_info['productSet'][0]['product']['parameters']
        for x in parameters:
            if x['name'] == 'Nośnik':
                type_record = x['values'][0]
                
        if type_record in {"Vinyl", "Winyl"}:
            name = offers_info['name']
            name = name.split(".")[0]
            name = name.split("(CD)")[0]
            offer_input_data = name
        elif type_record == "CD":
            parameters = offers_info['productSet'][0]['product']['parameters']
            
            for x in parameters:
                if x['name'] == 'EAN (GTIN)':
                    offer_input_data = x['values'][0]
        
        discogs_data = preprocess_data_parallel(offer_input_data, credentials, type_record, False)
            
        return {"status": 200, "offer": offers_info, "discogs": discogs_data}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in discogs_info: {str(e)}"}

@app.post("/discogs-information-image")
async def image_data(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        index = response['index']
        number_images = response['numberImages']
        type_record = response['typeRecord']
        discogs_data = []
        image_data = db.get_text_from_image()
        image_data = image_data[index:index+number_images]
        
        # Get data from discogs
        for data in image_data:
            text_from_image = data['text_from_image'] 
            url = data['url']
            
            if text_from_image == "EMPTY":
                discogs_data.append({"input_data": text_from_image, "information": "", "url": url})
            else:
                if type_record == "Vinyl":
                    information = preprocess_data_parallel(text_from_image, credentials, type_record)   
                elif type_record == "CD":
                    information = preprocess_data_parallel(text_from_image, credentials, type_record, False)
                
                discogs_data.append({"input_data": text_from_image, "information": information, "url": url})

        return {"status": 200, "output": discogs_data}

    except Exception as e:
        return {"status": 404, "error": f"Exception in image_data: {str(e)}"}

@app.get("/truncate")
async def truncate():
    try:
        db.truncate_image_data()

        return {"status": 200}
    except Exception as e:
        return {"status": 404, "error": f"Exception in image_data: {str(e)}"}


@app.post("/allegro-auth")
async def allegro_auth(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_id = response['client_id']
        user_secret = response['client_secret']
        token_url = allegro.allegro_verification(user_id, user_secret)

        return {"status": 200, "output": token_url}

    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_auth: {str(e)}"}

@app.post("/allegro-token")
async def allegro_token(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_id = response['client_id']
        user_secret = response['client_secret']
        device_code = response['device_code']
        user_token = allegro.get_allegro_token(user_id, user_secret, device_code)

        db.post_credentials(user_id, user_secret, user_token)

        return {"status": 200, "output": user_token}

    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_token: {str(e)}"}

@app.post("/allegro-edit-description")
async def edit_offer(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerId']
        images = response['images']
        new_data = response['data']

        result = allegro.edit_description(credentials, offer_id, images, new_data)

        return {"status": 200, "output": result}
        
    except Exception as e:
        return {"status": 404, "error": f"Exception in edit_offer: {str(e)}"}
    
@app.post("/allegro-edit-image")
async def edit_image(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerID']
        images = response['images']
        result = allegro.edit_images(credentials, offer_id, images)
        
        return {"status": 200, "output": result}

    except Exception as e:
        return {"status": 404, "error": f"Exception in edit-image: {str(e)}"}
    
@app.post("/allegro-listing")
async def allegro_listing(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        data = response['data']
        carton = response['carton']
        condition = response['condition']
        images = response['images']
        type_record = response['typeRecord']
        type_offer = response['typeOffer']
        duration = response['duration']
        clear = response['clear']
        credentials = db.get_credentials()

        result = allegro.create_offer(credentials, data, carton, condition, images, type_record, type_offer, duration, clear)

        return {"status": 200, "output": result}

    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_listing: {str(e)}"}

@app.post("/allegro-offers")
async def allegro_offers(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        limit = response['limit']
        offset = response['offset']
        type_offer = response['typeOffer']
        type_record = response['typeRecord']
        genre = response.get("genre", "all")
        
        offers = allegro.get_my_offers(credentials, limit, offset, type_offer, type_record, genre)
        return {"status": 200, "output": offers}

    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_offers: {str(e)}"}
    
@app.post("/allegro-offer")
async def allegro_offer(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerId']
        
        offers = allegro.get_offer_info(credentials, offer_id)
        
        return {"status": 200, "output": offers}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_offer: {str(e)}"}

@app.get("/store-all-offers")
async def store_all_offers():
    try:
        credentials = db.get_credentials()
        flags = db.get_flags()
        offers = []
        
        if not flags['load_offers']:
            i = 0
            
            while True:
                allegro_offers = allegro.get_my_offers(credentials, 1000, 1000*i, "all", "all", "all")
                offers.append(allegro_offers['offers'])

                if not allegro_offers['offers']:
                    break 
            
                i+=1

            offers = sum(offers, [])

            db.post_allegro_offers(offers)

        return {"status": 200, "output": offers}

    except Exception as e:
        return {"status": 404, "error": f"Exception in store_all_offers: {str(e)}"}

@app.get("/store-all-payments")
async def store_all_payments():
    try:
        credentials = db.get_credentials()
        flags = db.get_flags()
        payments = []
        if not flags['load_payment']:
            i = 0
            while True:
                
                payment_history = allegro.get_payment_history(credentials, 100, 100*i)
                payments.append(payment_history['paymentOperations'])

                if not payment_history['paymentOperations']:
                    break
                i+=1

            payments = sum(payments, [])

            db.post_payments(payments)

        return {"status": 200, "output": payments}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in store_all_payments: {str(e)}"}

@app.get("/allegro-visitors-viewers")
async def allegro_visitors_viewers():
    try:
        allegro_offers = db.get_allegro_offers()
        output_offers = []
        for offer in allegro_offers:
            offer = loads(offer['offer_data'])
            output_offers.append(offer)

        return {"status": 200, "output": output_offers}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_visitors_viewers: {str(e)}"}

@app.get("/sale-barplot")
async def sale_barplot():
    try:
        credentials = db.get_credentials()
        sales = db.get_payments()
        sale_barplot = annual_sale_barplot(credentials, sales)
        
        return {"status": 200, "output": sale_barplot}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in sale_barplot: {str(e)}"}
    
@app.get("/genre-barplot")
async def genre_barplot():
    try:
        credentials = db.get_credentials()
        allegro_offers = db.get_allegro_offers()
        output_offers = []
        for offer in allegro_offers:
            offer = loads(offer['offer_data'])
            output_offers.append(offer)

        genre_barplot = create_genres_barplot(credentials, output_offers)

        return {"status": 200, "output": genre_barplot}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in genre_barplot: {str(e)}"}

@app.get("/refresh-database")
async def refresh_database():
    try:
        db.truncate_allegro_offers()
        db.truncate_allegro_payments()
        db.post_false_flags()

        return {"status": 200}
    except Exception as e:
        return {"status": 404, "error": f"Exception in refresh_database: {str(e)}"}
    
@app.post("/discogs-listing")
async def discogs_listing(request: Request):
    try:
        credentials = db.get_credentials()
        discogs_token = credentials['api_discogs_token']
        response = loads((await request.body()).decode('utf-8'))
        listing_id = response['listing_id']
        media_condition = response['mediaCondition']
        sleeve_condition = response['sleeveCondition']
        carton = response['carton']
        price = response['price']

        result = create_offer(listing_id, media_condition, sleeve_condition, carton, price, discogs_token)

        return {"status": 200, "output": result}
    except Exception as e:
        return {"status": 404, "error": f"Exception in discogs_listing: {str(e)}"}
    
@app.post("/swap-cartons")
async def swap(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        swap_carton = response['swapCarton']
        with_carton = response['withCarton']

        result = allegro.swap_cartons(credentials, swap_carton, with_carton)

        return {"status": 200, "output": result}
    except Exception as e:
        return {"status": 404, "error": f"Exception in swap: {str(e)}"}
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from json import loads
import database as db
import allegro_api as allegro
from   preprocessing_image import preprocess_vinyl_images, preprocess_cd_images, remove_background
from   preprocessing_data import preprocess_data_parallel
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

@app.post("/read-vinyl-image")
async def read_vinyl_image(request: Request):
    try:
        db.truncate_image_data()
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        images = response['images']

        preprocess_tasks = [preprocess_vinyl_images(chunk_images, credentials) for chunk_images in images]
        text_from_images = await asyncio.gather(*preprocess_tasks)

        db.post_text_from_image(text_from_images)

        return {"status": 200, "output": text_from_images}

    except Exception as e:
        return {"status": 404, "error": f"Exception in read_vinyl_image: {str(e)}"}


@app.post("/read-cd-image")
async def read_cd_image(request: Request):
    try:
        db.truncate_image_data()
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        images = response['images']
        text_from_images = []
        
        preprocess_tasks = [preprocess_cd_images(chunk_images, credentials) for chunk_images in images]
        text_from_images = await asyncio.gather(*preprocess_tasks)
            
        db.post_text_from_image(text_from_images)

        return {"status": 200, "output": text_from_images}

    except Exception as e:
        return {"status": 404, "error": f"Exception in read_cd_image: {str(e)}"}

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
    """
        Endpoint that receives a POST request with data about an offer for a record. The function processes the data to extract the necessary information, and then queries the Discogs API to retrieve additional information about the record.

        Args:
            request (Request): The request object containing index of offers and information about the allegro offer. 

        Returns:
            dict: A dictionary containing the status, offer information, and Discogs data.
    """
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        index = response['index']
        allegro_data = response['allegroData']
        type_record = None
        offer_input_data = None
        
        if "offers" in allegro_data.keys():
            offer_info = allegro.get_offer_info(credentials, allegro_data['offers'][index]['id'])
        else:
            offer_info = allegro.get_offer_info(credentials, allegro_data['id'])
        
        parameters = offer_info['productSet'][0]['product']['parameters']
        for x in parameters:
            if x['name'] == 'Nośnik':
                type_record = x['values'][0]
                
        if type_record in {"Vinyl", "Winyl"}:
            name = offer_info['name']
            name = name.split(".")[0]
            name = name.split("(CD)")[0]
            offer_input_data = name
        elif type_record == "CD":
            parameters = offer_info['productSet'][0]['product']['parameters']
            
            for x in parameters:
                if x['name'] == 'EAN (GTIN)':
                    offer_input_data = x['values'][0]
        
        discogs_data = preprocess_data_parallel(offer_input_data, credentials, type_record, False)
            
        return {"status": 200, "offer": offer_info, "discogs": discogs_data}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in discogs_info: {str(e)}"}

@app.post("/discogs-information-image")
async def image_data(request: Request):
    """
        Get Discogs information for vinyl or CD records from image data.

        Args:
            request (Request): The request object containing index of offers, number images in one offer and type of record

        Returns:
            dict: A dictionary containing the status and Discogs data for the records.
    """
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

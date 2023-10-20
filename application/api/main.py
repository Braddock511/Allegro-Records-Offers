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
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        images = response['images']
        text_from_images = []
        db.delete_image_data(user_key)
        credentials = db.get_credentials(user_key)

        preprocess_tasks = [preprocess_vinyl_images(chunk_images, credentials) for chunk_images in images]
        text_from_images = await asyncio.gather(*preprocess_tasks)

        db.post_text_from_image(user_key, text_from_images)

        return {"status": 200, "output": text_from_images}

    except Exception as e:
        return {"status": 404, "error": f"Exception in read_vinyl_image: {str(e)}"}


@app.post("/read-cd-image")
async def read_cd_image(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        images = response['images']
        text_from_images = []
        db.delete_image_data(user_key)
        credentials = db.get_credentials(user_key)
        
        preprocess_tasks = [preprocess_cd_images(chunk_images, credentials) for chunk_images in images]
        text_from_images = await asyncio.gather(*preprocess_tasks)
            
        db.post_text_from_image(user_key, text_from_images)

        return {"status": 200, "output": text_from_images}

    except Exception as e:
        return {"status": 404, "error": f"Exception in read_cd_image: {str(e)}"}

@app.post("/clear-image")
async def clear_image(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        image = response['image']
        credentials = db.get_credentials(user_key)
        
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
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        index = response['index']
        allegro_data = response['allegroData']
        type_record = None
        offer_input_data = None
        credentials = db.get_credentials(user_key)
        
        if "offers" in allegro_data.keys():
            offer_info = allegro.get_offer_info(credentials, allegro_data['offers'][index]['id'])
        else:
            offer_info = allegro.get_offer_info(credentials, allegro_data['id'])
        
        parameters = offer_info['productSet'][0]['product']['parameters']
        for x in parameters:
            if x['name'] == 'Nośnik':
                type_record = x['values'][0]
            if x['name'] == 'EAN (GTIN)':
                offer_input_data = x['values'][0]                
                
        if type_record in {"Vinyl", "Winyl"}:
            name = offer_info['name']
            name = name.split(".")[0]
            name = name.split("(CD)")[0]
            offer_input_data = name

        information = preprocess_data_parallel(offer_input_data, credentials, type_record, False)
        discogs_data = [{"input_data": offer_input_data, "information": information, "url": ""}]

        return {"status": 200, "offer": offer_info, "output": discogs_data}
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
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        index = response['index']
        number_images = response['numberImages']
        type_record = response['typeRecord']
        credentials = db.get_credentials(user_key)
        image_data = db.get_text_from_image(user_key)
        image_data = image_data[index:index+number_images]
        discogs_data = []
        
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

@app.post("/discogs-information-new-search")
async def image_data(request: Request):
    response = loads((await request.body()).decode('utf-8'))
    user_key = response['userKey']
    new_search = response['newSearch']
    type_record = response.get('typeRecord', "")
    if not type_record:
        allegro_data = response['allegroData']
        parameters = allegro_data['productSet'][0]['product']['parameters']
        for x in parameters:
            if x['name'] == 'Nośnik':
                type_record = x['values'][0]
                
    credentials = db.get_credentials(user_key)
    information = preprocess_data_parallel(new_search, credentials, type_record, False)
    
    discogs_data = [{"input_data": new_search, "information": information, "url": ""} for _ in range(3)]

    return {"status": 200, "output": discogs_data}
       
    
@app.post("/clear-image-data")
async def clear_image_data(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        db.delete_image_data(user_key)

        return {"status": 200}
    except Exception as e:
        return {"status": 404, "error": f"Exception in clear_image_data: {str(e)}"}


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
        user_key = response['userKey']
        discogs_token = response['discogs_token']
        user_id = response['client_id']
        user_secret = response['client_secret']
        device_code = response['device_code']
        user_token = allegro.get_allegro_token(user_id, user_secret, device_code)

        check_user = db.post_credentials(user_key, discogs_token, user_id, user_secret, user_token)
        if check_user:
            return {"status": 200, "output": user_token}

        return {"status": 401, "output": "Unauthorized"}

    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_token: {str(e)}"}

@app.post("/allegro-edit-description")
async def edit_offer(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        offer_id = response['offerId']
        images = response['images']
        new_data = response['data']
        listing_similar = response['listing_similar']
        edit_description = response['editDescription']
        to_buy = response['toBuy']
        credentials = db.get_credentials(user_key)

        result = allegro.edit_description(credentials, offer_id, images, new_data, listing_similar, edit_description, to_buy)
        return {"status": 200, "output": result}
        
    except Exception as e:
        return {"status": 404, "error": f"Exception in edit_offer: {str(e)}"}
    
@app.post("/allegro-edit-image")
async def edit_image(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        offer_id = response['offerID']
        images = response['images']
        credentials = db.get_credentials(user_key)

        result = allegro.edit_images(credentials, offer_id, images)
        
        return {"status": 200, "output": result}

    except Exception as e:
        return {"status": 404, "error": f"Exception in edit-image: {str(e)}"}
    
@app.post("/allegro-listing")
async def allegro_listing(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        offer_data = response['offer_data']
        carton = response['carton']
        type_record = response['typeRecord']
        type_offer = response['typeOffer']
        duration = response['duration']
        clear = response['clear']
        credentials = db.get_credentials(user_key)

        result = allegro.create_offer(credentials, offer_data, carton, type_record, type_offer, duration, clear)

        return {"status": 200, "output": result}

    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_listing: {str(e)}"}

@app.post("/allegro-offers")
async def allegro_offers(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        limit = response['limit']
        offset = response['offset']
        type_offer = response['typeOffer']
        type_record = response['typeRecord']
        genre = response.get("genre", "all")
        credentials = db.get_credentials(user_key)
        
        offers = allegro.get_my_offers(credentials, limit, offset, type_offer, type_record, genre)
        return {"status": 200, "output": offers}

    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_offers: {str(e)}"}
    
@app.post("/allegro-offer")
async def allegro_offer(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        offer_id = response['offerId']
        credentials = db.get_credentials(user_key)
        
        offers = allegro.get_offer_info(credentials, offer_id)
        
        return {"status": 200, "output": offers}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_offer: {str(e)}"}

@app.post("/store-all-offers")
async def store_all_offers(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        credentials = db.get_credentials(user_key)
        flags = db.get_flags(user_key)
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

            db.post_allegro_offers(user_key, offers)

        return {"status": 200, "output": offers}

    except Exception as e:
        return {"status": 404, "error": f"Exception in store_all_offers: {str(e)}"}

@app.post("/store-all-payments")
async def store_all_payments(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        credentials = db.get_credentials(user_key)
        flags = db.get_flags(user_key)
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

            db.post_payments(user_key, payments)

        return {"status": 200, "output": payments}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in store_all_payments: {str(e)}"}

@app.post("/allegro-visitors-viewers")
async def allegro_visitors_viewers(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        allegro_offers = db.get_allegro_offers(user_key)
        output_offers = []
        for offer in allegro_offers:
            offer = loads(offer['offer_data'])
            output_offers.append(offer)

        return {"status": 200, "output": output_offers}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in allegro_visitors_viewers: {str(e)}"}

@app.post("/sale-barplot")
async def sale_barplot(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        credentials = db.get_credentials(user_key)
        sales = db.get_payments(user_key)
        sale_barplot = annual_sale_barplot(credentials, sales)
        
        return {"status": 200, "output": sale_barplot}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in sale_barplot: {str(e)}"}
    
@app.post("/genre-barplot")
async def genre_barplot(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        credentials = db.get_credentials(user_key)
        allegro_offers = db.get_allegro_offers(user_key)
        output_offers = []
        for offer in allegro_offers:
            offer = loads(offer['offer_data'])
            output_offers.append(offer)

        genre_barplot = create_genres_barplot(credentials, output_offers)

        return {"status": 200, "output": genre_barplot}
    
    except Exception as e:
        return {"status": 404, "error": f"Exception in genre_barplot: {str(e)}"}

@app.post("/refresh-database")
async def refresh_database(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        db.delete_allegro_offers(user_key)
        db.delete_allegro_payments(user_key)
        db.post_false_flags(user_key)

        return {"status": 200}
    except Exception as e:
        return {"status": 404, "error": f"Exception in refresh_database: {str(e)}"}
    
@app.post("/discogs-listing")
async def discogs_listing(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        discogs_token = credentials['api_discogs_token']
        listing_id = response['listing_id']
        media_condition = response['mediaCondition']
        sleeve_condition = response['sleeveCondition']
        carton = response['carton']
        price = response['price']
        credentials = db.get_credentials(user_key)

        result = create_offer(listing_id, media_condition, sleeve_condition, carton, price, discogs_token)

        return {"status": 200, "output": result}
    except Exception as e:
        return {"status": 404, "error": f"Exception in discogs_listing: {str(e)}"}
    
@app.post("/swap-all")
async def swap_all(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        swap_carton = response['swapCarton']
        with_carton = response['withCarton']
        credentials = db.get_credentials(user_key)

        result = allegro.swap_cartons(credentials, swap_carton, with_carton)

        return {"status": 200, "output": result}
    except Exception as e:
        return {"status": 404, "error": f"Exception in swap_all: {str(e)}"}
    
@app.post("/swap-specific")
async def swap_specific(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_key = response['userKey']
        swap_carton = response['swapCarton']
        with_carton = response['withCarton']
        offer_id = response['offerId']
        credentials = db.get_credentials(user_key)

        result = allegro.swap_specific_carton(credentials, swap_carton, with_carton, offer_id)

        return {"status": 200, "output": result}
    except Exception as e:
        return {"status": 404, "error": f"Exception in swap_specific: {str(e)}"}

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from json import loads
import database as db
import allegro_api as allegro
from  azure_api import read_image
from  preprocessing_data import preprocess_data, remove_background, get_cd_barcode
from  imageKit_api import upload_file_imageKit
from plots import annual_sale_barplot

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
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        images = response['images']
        type_record = response['typeRecord']
        number_images = response['numberImages']
        output = []

        for i in range(0, len(images), number_images):
            if type_record == "Vinyl":
                # Read first image
                image_1 = images[i]
                data_1, image_url_1 = read_image(image_1, credentials)
                output.append({"data": data_1, "url": image_url_1})

                # Other images
                for j in range(1, number_images):
                    other_image = images[i+j]
                    other_image_url = upload_file_imageKit(other_image, credentials)['url']

                    output.append({"data": "", "url": other_image_url})

            elif type_record == "CD":
                # Read second image 
                image_2 = images[i+1]
                data, image_url_2 = get_cd_barcode(image_2, credentials)
                
                # Other images
                for j in range(0, number_images-1):
                    other_image = images[i+j]
                    other_image_url = upload_file_imageKit(other_image, credentials)['url']

                    output.append({"data": "", "url": other_image_url})
                    if j == 0:
                        output.append({"data": data, "url": image_url_2})

        db.post_data_image(output)
        return {"success": 200}

    except Exception as e:
        return {"error": f"Exception in read_image: {str(e)}"}

@app.post("/clear-image")
async def clear_image(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        image = response['image']
        
        clear_image_url = remove_background(image, credentials)
        
        return clear_image_url

    except Exception as e:
        return {"error": f"Exception in clear_image: {str(e)}"}

@app.post("/discogs-information")
async def discogs_info(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        id = response['id']
        allegro_data = response['allegroData']
        type_record = response['typeRecord']

        if "offers" in allegro_data.keys():
            offers_info = allegro.get_offer_info(credentials, allegro_data['offers'][id]['id'])
        else:
            offers_info = allegro.get_offer_info(credentials, allegro_data['id'])
        output_data = None

        if type_record == "Vinyl":
            name = offers_info['name']
            name = name.split(".")[0]
            name = name.split("(CD)")[0]
            output_data = name
        elif type_record == "CD":
            parameters = offers_info['productSet'][0]['product']['parameters']
            for x in parameters:
                if x['name'] == 'EAN (GTIN)':
                    output_data = x['values'][0]
        
        discogs_data = preprocess_data(output_data, credentials, type_record, "", False)
            
        return {"offer": offers_info, "discogs": discogs_data}
    except Exception as e:
        return {"error": f"Exception in discogs_info: {str(e)}"}

@app.post("/discogs-information-image")
async def data_image(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        data_image = db.get_data_image()
        type_record = response['typeRecord']

        output_data = []    
        # Get data from discogs
        for data, url in zip(data_image['data'], data_image['url']):
            if not data:
                output_data.append({"input_data": data, "information": "", "url": url})
            else:
                if type_record == "Vinyl":
                    information = preprocess_data(data, credentials, type_record, url)
                elif type_record == "CD":
                    information = preprocess_data(data, credentials, type_record, url, False)
                output_data.append({"input_data": data,"information": information, "url": url})
        
        return output_data

    except Exception as e:
        return {"error": f"Exception in data_image: {str(e)}"}
    
@app.post("/allegro-auth")
async def allegro_auth(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_id = response['client_id']
        user_secret = response['client_secret']
        token_url = allegro.allegro_verification(user_id, user_secret)

        return token_url

    except Exception as e:
        return {"error": f"Exception in allegro_auth: {str(e)}"}

@app.post("/allegro-token")
async def allegro_token(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        user_id = response['client_id']
        user_secret = response['client_secret']
        device_code = response['device_code']
        user_token = allegro.get_allegro_token(user_id, user_secret, device_code)

        db.post_credentials(user_id, user_secret, user_token)

        return user_token

    except Exception as e:
        return {"error": f"Exception in allegro_token: {str(e)}"}

@app.post("/allegro-edit-offer")
async def edit_offer(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerId']
        images = response['images']
        new_data = response['data']

        result = allegro.edit_description(credentials, offer_id, images, new_data)

        return result
        
    except Exception as e:
        return {"error": f"Exception in edit_offer: {str(e)}"}
    
@app.post("/allegro-edit-image")
async def edit_image(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerID']
        images = response['images']
        result = allegro.edit_images(credentials, offer_id, images)
        
        return result

    except Exception as e:
        return {"error": f"Exception in edit-image: {str(e)}"}
    
@app.post("/allegro-listing")
async def allegro_listing(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        data = response['data']
        carton = response['carton']
        condition = response['condition']
        images = response['images']
        type = response['type']
        clear = response['clear']
        credentials = db.get_credentials()

        result = allegro.create_offer(credentials, data, carton, condition, images, type, clear)

        return result
    except Exception as e:
        return {"error": f"Exception in allegro_listing: {str(e)}"}

@app.post("/allegro-offers")
async def allegro_offers(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        limit = response['limit']
        offset = response['offset']
        type_offer = response['typeOffer']
        type_record = response['typeRecord']
        genre = response['genre'] if response['genre'] else 'all'
        
        offers = allegro.get_my_offers(credentials, limit, offset, type_offer, type_record, genre)
        
        return offers
    except Exception as e:
        return {"error": f"Exception in allegro_offers: {str(e)}"}
    
@app.post("/allegro-offer")
async def allegro_offer(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerId']
        
        offers = allegro.get_offer_info(credentials, offer_id)
        
        return offers
    except Exception as e:
        return {"error": f"Exception in allegro_offer: {str(e)}"}

@app.get("/allegro-visitors-viewers")
async def allegro_visitors_viewers():
    try:
        credentials = db.get_credentials()
        offers = []
        i = 0

        while True:
            vinyls = allegro.get_my_offers(credentials, 100, 1000*i, "all", "Vinyl", "all")
            cds = allegro.get_my_offers(credentials, 1000, 1000*i, "all", "CD", "all")
            offers.append(vinyls['offers'])
            offers.append(cds['offers'])

            if not vinyls['offers'] and not cds['offers']:
                break 
        
            i+=1

        offers = sum(offers, [])

        return offers

    except Exception as e:
        return {"error": f"Exception in allegro_visitors_viewers: {str(e)}"}
    
@app.get("/allegro-sale")
async def allegro_sale():
    try:
        credentials = db.get_credentials()
        offers = []
        i = 0

        while True:
            payment_history = allegro.get_payment_history(credentials, 100, 100*i)
            offers.append(payment_history['paymentOperations'])

            if not payment_history['paymentOperations']:
                break
            i+=1

        offers = sum(offers, [])

        return offers
    
    except Exception as e:
        return {"error": f"Exception in allegro_sale: {str(e)}"}
    
@app.get("/plots")
async def plots():
    try:
        credentials = db.get_credentials()
        data = await allegro_sale()
        bar_plot = annual_sale_barplot(credentials, data)
        
        return {"bar_plot": bar_plot}
    
    except Exception as e:
        return {"error": f"Exception in plots: {str(e)}"}
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from json import loads
import database as db
import allegro_api as allegro
from azure_api import read_image
from preprocessing_data import preprocess_data, remove_background
from imageKit_api import upload_file_imageKit

# getting the credentials

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
        output = []

        for i in range(0, len(images), 3):
            # read only the first image of every 3 images
            image = images[i]
            data, image_url = read_image(image, credentials)
            output.append({"data": data, "url": image_url})

            for j in range(2, 4):
                image = images[j+i-1]
                image_url = upload_file_imageKit(image, credentials)['url']
                output.append({"data": "", "url": image_url})

        db.post_data_image(output)

        return {"success": 200}

    except Exception as e:
        return {"error": f"Exception in read_image: {str(e)}"}

@app.get("/data-image")
async def data_image():
    try:
        credentials = db.get_credentials()
        data_image = db.get_data_image()

        output_data = []    
        for data, url in zip(data_image['data'], data_image['url']):
            if not data:
                output_data.append({"information": "", "url": url})
            else:
                information = preprocess_data(data, credentials, "vinyl", url)
                output_data.append({"information": information, "url": url})
                
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
    
@app.post("/allegro-listing")
async def allegro_listing(request: Request):
    try:
        response = loads((await request.body()).decode('utf-8'))
        data = response['data']
        cartoon = response['cartoon']
        condition = response['condition']
        images = response['images']
        credentials = db.get_credentials()

        allegro.create_offer_vinyl(credentials, data, cartoon, condition, images)

        return {"success": 200}
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
        genre = response['genre']
        
        offers = allegro.get_my_offers(credentials, limit, offset, type_offer, type_record, genre)
        
        return offers
    except Exception as e:
        return {"error": f"Exception in allegro_offers: {str(e)}"}
    
@app.post("/discogs-information")
async def discogs_info(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        id = response['id']
        allegro_data = response['allegroData']
        type_record = response['typeRecord']

        offers_info = allegro.get_offer_info(credentials, allegro_data['offers'][id]['id'])
        output_data = None

        if type_record == "vinyl":
            output_data = offers_info['name']
        elif type_record == "cd":
            parameters = offers_info['productSet'][0]['product']['parameters']
            for x in parameters:
                if x['name'] == 'EAN (GTIN)':
                    output_data = x['values'][0]
        
        discogs_data = preprocess_data(output_data, credentials, type_record, "", False)
            
        return {"offer": offers_info, "discogs": discogs_data}
    except Exception as e:
        return {"error": f"Exception in discogs_info: {str(e)}"}
    
@app.post("/edit-offer")
async def edit_offer(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerId']
        images = response['images']
        new_data = response['data'][0]

        allegro.edit_description(credentials, offer_id, images, new_data)

        return {"success": 200}
        
    except Exception as e:
        return {"error": f"Exception in edit_offer: {str(e)}"}
    
@app.get("/allegro-stats")
async def allegro_stats():
    try:
        credentials = db.get_credentials()
        offers = []
        i = 0

        while True:
            vinyls = allegro.get_my_offers(credentials, 100, 1000*i, "all", "vinyl", "all")
            cds = allegro.get_my_offers(credentials, 1000, 1000*i, "all", "cd", "all")
            offers.append(vinyls['offers'])
            offers.append(cds['offers'])

            if not vinyls['offers'] and not cds['offers']:
                break 
        
            i+=1

        offers = sum(offers, [])

        return offers

    except Exception as e:
        return {"error": f"Exception in allegro_stats: {str(e)}"}

@app.post("/clear-image")
async def clear_image(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        images = response['images']
        
        clear_image_url = remove_background(images[0], credentials)
        
        return clear_image_url

    except Exception as e:
        return {"error": f"Exception in clear_image: {str(e)}"}

@app.post("/edit-image")
async def edit_image(request: Request):
    try:
        credentials = db.get_credentials()
        response = loads((await request.body()).decode('utf-8'))
        offer_id = response['offerID']
        images = response['images']
        allegro.edit_images(credentials, offer_id, images)
        
        return {"succes": 200}

    except Exception as e:
        return {"error": f"Exception in edit-image: {str(e)}"}
Custom API to connect to Vue

read_image_data - endpoint that receives a POST request with image data in the request body. The endpoint reads the images, extracts text from them, and stores the extracted text and image URLs in a database.
- request with a JSON object in the request body containing the following keys:
    - images (list): base64-encoded images.
    - typeRecord (str): specifying the type of record being processed (either "Vinyl" or "CD").
    - numberImages (int): specifying the number of images per record.

clear_image - endpoint that receives a POST request with image data in the request body. The endpoint removes the background from the image using the remove_background() function, and returns the URL of the resulting image.
- request with a JSON object in the request body containing the following keys:
    - images (list): base64-encoded images.

discogs_info - endpoint that receives a POST request with data about an offer for a music record. The function processes the data to extract the necessary information, and then queries the Discogs API to retrieve additional information about the record. The resulting data is returned as a JSON object.
- request with a JSON object in the request body containing the following keys:
    - index (str): representing the index of offers
    - allegroData (dictionary): information about the offer.

image_data - endpoint /discogs-information-image that takes in a POST request with JSON data. The endpoint retrieves image data from a database, processes the data using a pre-trained machine learning model, and returns the processed data in JSON format.
- request with a JSON object in the request body containing the following keys:
    - index (int): representing the starting index of the images to be retrieved from the database.
    - numberImages (int): number images in one offer
    - typeRecord (dictionary): type of the record, either "Vinyl" or "CD".

truncate - endpoint that truncate image data table

allegro_auth - responsible for handling requests to authenticate and authorize an Allegro API client. When a POST request is sent to this endpoint, the code extracts the client ID and client secret from the request body, calls the allegro_verification function to get an authorization URL, and returns it to the caller.
- request with a JSON object in the request body containing the following keys:
    - client_id (str): The client ID of the Allegro API client.
    - client_secret (str): The client secret of the Allegro API client.

allegro_token - request that takes in a Request object. This route is used to get an Allegro token from the user credentials and device code. The user credentials and device code are received in the request body in the form of JSON data. Once the token is obtained, it is saved to the database using the db.post_credentials function. The response of this route is a JSON object containing the status code and the output.
- request with a JSON object in the request body containing the following keys:
    - client_id (str): The client ID of the Allegro API client.
    - client_secret (str): The client secret of the Allegro API client.
    - device_code (str): device code for the user.

edit_offer - ndpoint that allows the user to edit an existing offer on Allegro, a Polish online marketplace. The endpoint takes the offer ID, a list of images, and new data as input. The images parameter is a list of base64 encoded strings representing the new images to be uploaded. The new_data parameter is a dictionary containing the new offer data to be updated.
- request with a JSON object in the request body containing the following keys:
    - offerId: (str) The unique identifier of the offer to be edited.
    - images: (list) A list of base64 encoded strings representing the new images to be uploaded.
    - data: (dict) A dictionary containing the new offer data to be updated.

edit_image - endpoint allows editing the images of an offer in the Allegro
- request with a JSON object in the request body containing the following keys:
    - offerID: The ID of the offer to edit.
    - images: A list of dictionaries representing the images to upload. Each dictionary contains the following keys:
        - url: The URL of the image to upload.
        - filename: The filename of the image to upload.

allegro_listing - endpoint for creating a new listing on the Allegro
- request with a JSON object in the request body containing the following keys:
    - data: a dictionary containing details about the listing, such as title, description, price, and shipping options.
    - carton (str): marking of the physical carton
    - condition (str): condition of disc
    - images (list): image URLs for the listing.
    - type_offer (str): type of offer - buy now or auction
    - type_record (str): type of recors - vinyl or cd
    - duration (str): duration of the listing (in days).
    - clear (boolean): whether to remove the background of the image

allegro_offers - retrieve a list of the authenticated user's offers on the Allegro
- request with a JSON object in the request body containing the following keys:
    - limit (int): how many offers
    - offset (int): which offer to start with
    - type_offer (str): type of offer - buy now or auction
    - type_record (str): type of recors - vinyl or cd
    - genre (str): type of genre, list of categories - https://allegro.pl/kategoria/muzyka?string=muzyka

allegro_offer - endpoint allows the user to retrieve information about an offer on Allegro, using the offer_id provided in the request.
- request with a JSON object in the request body containing the following keys:
    - offer_id (int): the unique identifier of the product offer.

store_all_offers - endpoint is responsible for retrieving all offers listed by the user and store them in a database. The offers are retrieved from the Allegro API by making multiple requests with 1000 offers per request. The response is combined into a single list and then stored in the database.    

store_all_payments - endpoint is responsible for retrieving all payments listed by the user and store them in a database. The payments are retrieved from the Allegro API by making multiple requests with 100 offers per request. The response is combined into a single list and then stored in the database.    

allegro_visitors_viewers - retrieve all Allegro offers stored in a database and returns them as a list of Python dictionaries. 

sale_barplot - returns a bar plot of the annual sales from Allegro.

genre_barplot - returns a bar plot that shows the number of offers per music genre on the Allegro.

refresh_database - refreshing infromation about offers and payments from Allegro

discogs_listing - endpoint creates a new offer on Discogs
- request with a JSON object in the request body containing the following keys:
    - listing_id (str): ID of the Discogs listing to use as a basis for the new offer.
    - mediaCondition (str): condition of the media (e.g., "Mint", "Very Good", etc.).
    - sleeveCondition (str): condition of the sleeve (e.g., "Mint", "Very Good", etc.).
    - carton (str): marking of the physical carton
    - price (float): price of record
    - discogs_token (str): discogs API token to use for authentication.
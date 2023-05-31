Python scripts that includes functions to interact with the Allegro API

allegro_verification - sends a request to Allegro to verify the client ID and client secret. 
- client_id (str): client id from allegro api
- client_secret (str): client key from allegro api

get_allegro_token - uses the device code obtained from the previous function to get an access token. 
- client_id (str): client id from allegro api
- client_secret (str): client key from allegro api
- device_code (str): secret code from allegro api (value taken from allegro_verification)

get_my_offers - return active sale offers from the user's Allegro account. 
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- limit (int): how many offers
- offset (int): which offer to start with
- type_offer (str): type of offer - buy now or auction
- type_record (str): type of recors - vinyl or cd
- genre (str): type of genre, list of categories - https://allegro.pl/kategoria/muzyka?string=muzyka

get_offer_info - return specific information about a product offer on Allegro.
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- offer_id (int): the unique identifier of the product offer.

handle_allegro_errors - Handles errors returned by the Allegro API during product offers processing.
- data (dict): Containing product information.
- result (dict): Containing the result returned by the Allegro API.
- credentials (dict): contains the Allegro API token needed to authenticate the request.

create_offer - creating an offer on the Allegro platform for either a Vinyl or CD record.
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- discogs_data (dict): information about record from discogs
- carton (str): marking of the physical carton
- condition (str): condition of disc
- images (list): images of record
- type_offer (str): type of offer - buy now or auction
- type_record (str): type of recors - vinyl or cd
- duration (str): duration of offer
- clear (boolean): If the clear parameter is set to True, the function removes the background of the first image in the images list using another function remove_background()

get_condition_and_carton - return condition of disc and marking of the physical carton from offer description
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- offer_id (int): the unique identifier of the product offer.

edit_description - edits the description of an existing offer on Allegro
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- offer_id (int): the unique identifier of the product offer.
- images (list): images of record
- new_information (dict): information about record from discogs

edit_images - edits the images of an existing offer on Allegro
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- offer_id (int): the unique identifier of the product offer.
- images (list): images of record

get_payment_history - retrieves payment history from Allegro
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- limit (int): how many offers
- offset (int): which offer to start with

swap_cartons - swaps the carton name in Allegro offers with a new carton name.
- credentials (dict): contains the Allegro API token needed to authenticate the request.
- change_carton (str): The old carton name to be replaced.
- change_to_carton (str): The new carton name to replace with.
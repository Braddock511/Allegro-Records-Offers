Python scripts that includes functions to interact with the PostgreSQL database

post_credentials - insert user credentials to database
- allegro_id (str): client id from allegro api
- allegro_secret (str): client key from allegro api
- allegro_token (str): token from allegro api

get_credentials - retrieve credentials from database.

post_text_from_image - insert text from image into database
- text_from_images (list): text from records images

get_text_from_image - retrieve image text from database.

truncate_image_data - truncate image data table

post_allegro_offers - insert allegro offers into database
- offers (list): offers from allegro

get_allegro_offers - retrieve allegro offers from database.

post_payments - insert allegro payments into database
- payments (list): payments from allegro

get_payments - retrieve allegro payments from database.

post_false_flags - insert false flags into the database, which inform that offers and payments from Allegro have not been added to the database

get_flags()- retrieve flags from database.

truncate_allegro_offers - truncate allegro offers table

truncate_allegro_payments - truncate allegro payments table
Python scripts that includes functions to interact with the Discogs API

get_vinyl - returns a JSON object containing search results for the given query. The results include information about the artist, title, label, and format of the vinyl records.
- query (str) - A search query for vinyl records.
- discogs_token (str) - A Discogs authentication token.

get_cd - returns a JSON object containing search results for the CD with the given barcode. The results include information about the artist, title, label, and format of the CD
- barcode (str) - The barcode of a CD.
- discogs_token (str) - A Discogs authentication token.

get_price - returns a JSON object containing price suggestions for the given release ID. The results include the median, minimum, and maximum prices for the release in the Discogs marketplace.
- id (str) - The Discogs release ID of a vinyl record or CD.
- discogs_token (str) - A Discogs authentication token.

get_tracklist - returns a formatted HTML string containing the tracklist for the given release ID. The tracklist includes the position and title of each track on the release.
- id (str) - The Discogs release ID of a vinyl record or CD.
- discogs_token (str) - A Discogs authentication token.

create_offer - creates a new offer on the Discogs marketplace for the given vinyl record or CD. The offer includes information about the release ID, condition, sleeve condition, location, and price. The function returns a JSON object containing information about the new offer.
- listing_id (int) - The Discogs listing ID of the vinyl record or CD to create an offer for.
- condition (str) - The condition of the vinyl record or CD.
- sleeve_condition (str) - The condition of the sleeve for the vinyl record or CD.
- carton (str) - The location of the vinyl record or CD.
- price (float) - The price for the vinyl record or CD.
- discogs_token (str) - A Discogs authentication token.
import requests

def get_vinyl(query: str, discogs_token: str) -> dict[str, str]:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com/database/search?query={query}&format=lp&type=release"

    response = requests.get(url, headers=headers)

    return response.json()


def get_cd(barcode: str, discogs_token: str) -> dict[str, str]:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com/database/search?barcode={barcode}&format=cd&type=release"

    response = requests.get(url, headers=headers)

    return response.json()

def get_price(id: str, discogs_token: str) -> dict[str, str]:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com//marketplace/price_suggestions/{id}"

    response = requests.get(url, headers=headers)

    return response.json()

def get_tracklist(id: str, discogs_token: str) -> str:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com/releases/{id}"

    response = requests.get(url, headers=headers)

    try:
        tracklist = response.json()['tracklist']
        tracks = "<p><b>LISTA UTWORÓW:</b></p>"
        paragraph = []
        outtrack = ""
        
        for track in tracklist:
            if 'sub_tracks' in list(track.keys()):
                for sub_track in track['sub_tracks']:
                    outtrack = f"<b>{sub_track['position']}. {sub_track['title']}</b>"
                    
            else:
                outtrack = f"<b>{track['position']}. {track['title']}</b>"

            paragraph.append(outtrack)

            if len(paragraph) == 2:
                output = " | ".join(paragraph)
                tracks += f"<p>{output}</p>"
                paragraph.clear()

        tracks = tracks.replace("&", " ")

        return tracks
    
    except KeyError:
        return "<p><b>LISTA UTWORÓW: -</b></p>"

def create_offer(listing_id: int, condition: str, sleeve_condition: str, carton: str, price: float, discogs_token: str) -> dict[str, str]:
    offer = {
        "listing_id": listing_id,
        "release_id": listing_id,
        "condition": condition,
        "sleeve_condition": sleeve_condition,
        "price": price,
        "location": carton
    }
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com//marketplace/listings"
    response = requests.post(url, headers=headers, json=offer)

    return response.json()

import requests
from typing import Dict

def get_vinyl(query: str, discogs_token: str) -> Dict[str, str]:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com/database/search?query={query}&format=lp&type=release"

    response = requests.get(url, headers=headers)

    return response.json()


def get_cd(barcode: str, discogs_token: str) -> Dict[str, str]:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com/database/search?barcode={barcode}&format=cd&type=release"

    response = requests.get(url, headers=headers)

    return response.json()

def get_price(id: str, discogs_token: str) -> Dict[str, str]:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com//marketplace/price_suggestions/{id}"

    response = requests.get(url, headers=headers)

    return response.json()

def get_tracklist(id: str, discogs_token: str) -> str:
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = f"https://api.discogs.com/releases/{id}"
    
    try:
        response = requests.get(url, headers=headers)
        tracklist = response.json()['tracklist']
        tracks = []
        outtrack = ""

        for track in tracklist:
            if 'sub_tracks' in track:
                # If 'sub_tracks' exist, iterate through them
                for sub_track in track['sub_tracks']:
                    outtrack = f"<b>{sub_track['position']}. {sub_track['title']}</b>"
                    tracks.append(outtrack)
            else:
                # If no 'sub_tracks', process the track itself
                outtrack = f"<b>{track['position']}. {track['title']}</b>"
                tracks.append(outtrack)

        formatted_tracks = ["<p><b>LISTA UTWORÓW:</b></p>"]
        for i in range(0, len(tracks), 2):
            pair = " | ".join(tracks[i:i + 2])
            formatted_tracks.append(f"<p>{pair}</p>")
        output = "".join(formatted_tracks)
        
        return output.replace("&", " ")
    
    except KeyError:
        return "<p><b>LISTA UTWORÓW: -</b></p>"

def create_offer(listing_id: int, condition: str, sleeve_condition: str, carton: str, price: float, discogs_token: str) -> Dict[str, str]:
    offer = {
        "listing_id": listing_id,
        "release_id": listing_id,
        "condition": condition,
        "sleeve_condition": sleeve_condition,
        "price": price,
        "location": carton
    }
    headers = {"Authorization": f"Discogs token={discogs_token}", "Content-Type": "application/json"}
    url = "https://api.discogs.com//marketplace/listings"
    response = requests.post(url, headers=headers, json=offer)

    return response.json()

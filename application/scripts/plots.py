import seaborn as sns
import matplotlib.pyplot as plt
import base64
import os
import json
from datetime import datetime
from imageKit_api import upload_file_imageKit

def annual_sale_barplot(credentials: dict, sales: list) -> str:
    dates = {}
    prices = {}

    # Sorting prices by month
    for sale in sales:
        sale = json.loads(sale)
        if sale['group'] == "INCOME":
            date = datetime.strptime(sale['occurredAt'][:7], '%Y-%m')
            price = float(sale['value']['amount'])

            if date in prices:
                prices[date] += price
            else:
                dates[date] = date
                prices[date] = price

    output = {"date": [date.strftime('%Y-%m') for date in dates.values()][:12][::-1], "price": [round(price, 0) for price in prices.values()][:12][::-1]}

    sns.set_style("whitegrid")
    sns.set_palette("pastel")

    plt.figure(figsize=(20, 10))
    plot = sns.barplot(data=output, x="date", y="price", color='green')

    plt.title("Income in given months", fontsize=18)
    plt.xlabel("Months", fontsize=14)
    plt.ylabel("Income in PLN", fontsize=14)

    # Add price above each bar
    for i, bar in enumerate(plot.containers):
        price = output["price"][i]
        plot.bar_label(bar, label=f"{price:.2f}", label_type="edge", fontsize=14)

    # Upload plot to imagekit 
    if not os.path.exists("temp"):
        os.mkdir("temp")

    plt.savefig("temp/sale_barplot.png", bbox_inches="tight")

    with open('temp/sale_barplot.png', 'rb') as f:
        image_bytes = f.read()
        image = base64.b64encode(image_bytes)

    image_url = upload_file_imageKit(image, credentials)

    return image_url['url']

def create_genres_barplot(credentials: dict, offers: list) -> str:
    categories = {1410: 'ballad', 1411: 'blues', 5639: 'ethno', 1145: 'country', 5638: 'dance', 5626: 'kids', 289: 'jazz', 5625: 'carols', 260981: 'metal', 10830: 'alternative', 261112: 'electronic', 322237: 'film', 286: 'classical', 261156: 'opera', 261039: 'pop', 261040: 'rap', 1413: 'reggae', 261043: 'rock', 5623: "rock'n'roll", 261041: 'single', 1419: 'compilations', 1420: 'soul', 321961: 'synth-pop', 293: 'other', 9531: 'sets', 1361: 'ballad', 261036: 'blues', 261100: 'folk, world & country', 261035: 'dance', 89757: 'disco', 261128: 'metal', 261111: 'electronic', 9536: 'classical', 89751: 'religious', 261042: 'new', 9537: 'opera', 261044: 'hip-hop', 5607: 'carols', 261110: 'rock', 5605: "rock'n'roll", 322236: 'single', 261102: 'compilations', 181: 'soul', 321960: 'synth-pop', 191: 'other', 9530: 'sets'}
    genres = [categories.get(int(offer['category']['id'])) for offer in offers]
    genres = sorted(genres, key=lambda x: genres.count(x), reverse=True)

    sns.set_style("whitegrid")
    sns.set_palette("pastel")

    plt.figure(figsize=(20, 10))
    plot = sns.countplot(x=genres, color='green')
    plot.set_xticklabels(plot.get_xticklabels(), rotation=45, ha="right")

    plt.title("Number of genres in offers", fontsize=18)
    plt.xlabel("Genre", fontsize=14)

    for bar in plot.containers:
        plot.bar_label(bar, label_type='edge', fontsize=12, padding=5)

    # Upload plot to imagekit 
    if not os.path.exists("temp"):
        os.mkdir("temp")
        
    plt.savefig("temp/genres_barplot.png", bbox_inches="tight")

    with open('temp/genres_barplot.png', 'rb') as f:
        image_bytes = f.read()
        image = base64.b64encode(image_bytes)

    image_url = upload_file_imageKit(image, credentials)

    return image_url['url']
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import os
import json
import pandas as pd
from datetime import datetime
from imageKit_api import upload_file_imageKit

def annual_sale_barplot(credentials: dict, sales: list) -> str:
    """
    Generates a bar plot of annual sales using the provided credentials and sales data.

    Args:
        credentials (dict): The credentials containing the necessary information.
        sales (list): The list of sales data from allegro.

    Returns:
        str: The URL of the generated bar plot image.
    """
    dates = []
    prices = []
    
    # Sorting prices by month
    for sale in sales:
        sale = json.loads(sale)
        if sale['group'] == "INCOME":
            date = datetime.strptime(sale['occurredAt'][:7], '%Y-%m')
            price = float(sale['value']['amount'])

            if date not in dates:
                dates.append(date)
                prices.append(price)
            else:
                index = dates.index(date)
                prices[index] += price

    df = pd.DataFrame({"date": dates, "price": prices})
    df["date"] = df["date"].dt.strftime('%Y-%m')  
    df = df.sort_values(by="date").tail(12).reset_index(drop=True)

    sns.set_style("whitegrid")
    sns.set_palette("pastel")

    plt.figure(figsize=(20, 10))
    plot = sns.barplot(data=df, x="date", y="price", color='green')

    plt.title("Income in given months", fontsize=18)
    plt.xlabel("Months", fontsize=14)
    plt.ylabel("Income in PLN", fontsize=14)

    # Add price above each bar
    for i, bar in enumerate(plot.containers):
        price = df["price"][i]
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
    """
    Generates a bar plot of the number of genres in the offers

    Args:
        credentials (dict): The credentials containing the necessary information.
        offers (list): The list of offers data.

    Returns:
        str: The URL of the generated bar plot image.
    """
    categories = {1410: 'Ballad', 1411: 'Blues', 1145: "Country", 5638: 'Dance', 0: 'Disco', 5639: 'Ethno, Folk, World music', 5626: 'For kids', 289: 'Jazz', 5625: 'Carols', 260981: 'Metal', 10830: 'Alternative', 261112: 'Electronic', 322237: 'Film', 286: 'Classical', 261156: 'Opera', 261039: 'Pop', 261040: 'Rap, Hip-Hop', 1413: 'Reggae', 261043: 'Rock', 5623: "Rock'n'roll", 261041: 'Single', 284: 'New sounds', 1419: 'Compilations', 1420: 'Soul', 321961: 'Synth-pop', 293: 'Other', 9531: 'Sets',
                  1361: 'Ballad', 261036: 'Blues', 1143: "Country", 261035: 'Dance', 89757: 'Disco', 261100: "Ethno, Folk, World music", 261028: "For kids", 260: 'Jazz', 5607: 'Carols', 261128: 'Metal', 261029: 'Alternative', 261111: 'Electronic', 322237: 'Film', 9536: 'Classical', 9537: 'Opera', 261127: 'Pop', 261044: 'Rap, Hip-Hop', 182: 'Reggae', 261110: 'Rock', 5605: "Rock'n'roll", 322236: 'Single', 261042: 'New sounds', 261102: 'Compilations', 181: 'Soul', 321960: 'Synth-pop', 9530: 'Sets', 191: 'Other', 89751: 'Religious', }

    df = pd.DataFrame({"genre": [categories.get(int(offer['category']['id'])) for offer in offers]})
    
    sns.set_style("whitegrid")
    sns.set_palette("pastel")

    plt.figure(figsize=(20, 10))
    plot = sns.countplot(data=df, x="genre", color='green', order=df['genre'].value_counts().index)
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

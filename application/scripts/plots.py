import seaborn as sns
import matplotlib.pyplot as plt
import base64
import os
from datetime import datetime
from imageKit_api import upload_file_imageKit

def annual_sale_barplot(credentials: dict, data: list):
    dates = {}
    prices = {}

    # Sorting prices by month
    for sale in data:
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
    plt.savefig("temp/output.png", bbox_inches="tight")

    with open('temp/output.png', 'rb') as f:
        image_bytes = f.read()
        image = base64.b64encode(image_bytes)

    image_url = upload_file_imageKit(image, credentials)

    return image_url['url']
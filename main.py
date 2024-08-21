# using base conda env

# Imports
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import pprint
import os
import json


# function to scrape data from website
# returns a list of dictionaries that contain all needed data for analysis.


def get_data():
    dict_list = []

    urls_list = [
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$1",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$2",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$3",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$5",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$10",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$20",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$30",
    ]

    # urls_list = ["https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$1"]
    for url in urls_list:
        response = get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        main = soup.select("#global-content > div > div > div > div")[0]
        for table in main.find_all("div", recursive=False):
            game_name = table.select("div > header > div > a")[0].text
            game_price = table.select("div > header > div > p:nth-child(2)")[
                0
            ].text  # need to sperate price out of the data
            data_table = pd.read_html(str(table.select("div > table")[0]))
            # print((data_table[0]))
            Last_day = table.select("div > header > div > p:nth-child(3)")[0].text
            dictionary = {
                "date": datetime.today().strftime("%m/%d/%Y"),
                "game_name": game_name,
                "game_price": game_price,
                "data_table": data_table[0].to_dict("records"),
                "Last_day": Last_day,
            }
            dict_list.append(dictionary)
    return dict_list


# to do: add mongo db for all data
#       Add time stamp for each data
#       do calculations


if __name__ == "__main__":
    x = get_data()
    for y in x:
        print(y["data_table"])

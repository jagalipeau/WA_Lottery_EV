# using base conda env

# Imports
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import Mongo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import warnings

# Muting FutureWarnings
warnings.simplefilter(action="ignore", category=FutureWarning)


def get_data():

    # Setting up selenium
    options = webdriver.SafariOptions()

    # Empty list to store finished dictionaries
    dict_list = []

    # List of URLS where games are located. One url for each price of scrtacher
    urls_list = [
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$1",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$2",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$3",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$5",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$10",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$20",
        "https://www.walottery.com/Scratch/TopPrizesRemaining.aspx?price=$30",
    ]

    # Looping through each url and downloaded html
    for url in urls_list:
        response = get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        main = soup.select("#global-content > div > div > div > div")[0]
        # Looping through each html table that exists in the download html above
        for table in main.find_all("div", recursive=False):

            game_price = table.select("div > header > div > p:nth-child(2)")[
                0
            ].text  # need to sperate price out of the data
            data_table = pd.read_html(str(table.select("div > table")[0]))
            # print((data_table[0]))
            Last_day = table.select("div > header > div > p:nth-child(3)")[0].text

            game_id = table.select("div > header > div > p:nth-child(2)")[0].text[-4:]
            game_name = f'{table.select("div > header > div > a")[0].text} ({game_id})'
            # --- Begin selenium scraping. tickets sold is rendered not in the source code.
            url = f"https://www.walottery.com/Scratch/Explorer.aspx?id={game_id}"
            driver = webdriver.Safari(options=options)
            driver.get(url)
            wait = WebDriverWait(driver, 30)
            # Waiting until the tickets sold appears
            r = wait.until(
                lambda driver: driver.find_element(
                    By.XPATH,
                    '//*[@id="global-content"]/section[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/p[1]/strong',
                ).text
                != "N/A"
            )
            r = driver.find_element(
                By.XPATH,
                '//*[@id="global-content"]/section[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/p[1]/strong',
            )
            tickets_sold = int(r.text.replace(",", ""))
            driver.quit()

            # --------------------------------------------------------------------
            # Creating dictionary for each game
            dictionary = {
                "date": datetime.today().strftime("%m/%d/%Y"),
                "game_name": game_name,
                "game_price": game_price,
                "data_table": data_table[0].to_dict("records"),
                "Last_day": Last_day,
                "tickets_sold": tickets_sold,
            }
            print("table")
            dict_list.append(dictionary)
        print("url")
    # returns a list of dictionaries
    return dict_list


# Returns Noithing. Adds to the Mongo DB the expected value for each game.
def calculate(documents):
    # Uncomment below to use every single game instead of ones passed to it
    # documents = Mongo.read_raw()
    EV_dict_list = []
    # Iterating through each of the games that is passed in
    for doc in documents:
        try:
            df = pd.DataFrame(doc["data_table"])
            tickets_sold = doc["tickets_sold"]
            ticket_price = float(doc["game_price"].split()[0].replace("$", ""))
            new_prize_amount = "0"
            new_total_prizes = tickets_sold - sum(df["Total Prizes"])
            new_prizes_remaining = new_total_prizes - sum(df["Prizes Remaining"])
            new_prizes_paid = new_total_prizes - new_prizes_remaining
            zero_row = {
                "Prize Amount": new_prize_amount,
                "Total Prizes": new_total_prizes,
                "Prizes Paid": new_prizes_paid,
                "Prizes Remaining": new_prizes_remaining,
            }
            df["Prize Amount"] = (
                df["Prize Amount"].str.replace("$", "").str.replace(",", "")
            )
            df.loc[len(df)] = zero_row

            df["Probabilty"] = df["Prizes Remaining"] / sum(df["Prizes Remaining"])

            df["Prize Amount"] = pd.to_numeric(df["Prize Amount"])

            df["Expected Value"] = df["Prize Amount"] * df["Probabilty"]

            EV = sum(df["Expected Value"]) - ticket_price
            print(f"{doc['game_name']} on {doc['date']} has an EV of {EV}")

            # Adding it to the database
            EV_dict = {
                "game_name": doc["game_name"],
                "date": doc["date"],
                "EV": EV,
                "ticket_price": ticket_price,
                "tickets_sold": tickets_sold,
                "data_table": df.to_dict("records"),
            }
            EV_dict_list.append(EV_dict)
        except:
            print(f"{doc['game_name']} on {doc['date']} -- Failed")

    Mongo.update(new_data=EV_dict_list, collectionName="EV_data")
    return None


if __name__ == "__main__":
    if Mongo.is_database_running() == True:
        data_full = get_data()
        Mongo.update(data_full, collectionName="full_data")
        calculate(data_full)

    # calculate()

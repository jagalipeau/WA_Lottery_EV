import pandas as pd
import streamlit as st
import pymongo
import matplotlib.pyplot as plt


client = pymongo.MongoClient("mongodb://mongoadmin:pass@localhost:27017/")
database = client["Wa_Lotto"]
collection = database["EV_data"]


allData = pd.DataFrame(list(collection.find()))


def ts():
    xAxis = st.sidebar.selectbox(
        "Select an x-Axis",
        ("date", "ticket_price", "tickets_sold"),
        index=None,
        placeholder="Select contact method...",
    )
    if xAxis == "date":
        game_name = st.sidebar.selectbox("Select a game", allData["game_name"].unique())
        plotData = allData[allData["game_name"] == game_name]
        st.title(
            f"EV vs Date on {game_name}",
        )
        st.line_chart(
            data=plotData,
            x=xAxis,
            y="EV",
        )

    elif xAxis == "ticket_price":
        date = st.sidebar.selectbox("Select a date", allData["date"].unique())
        plotData = allData[allData["date"] == date]
        st.title(f"EV vs {xAxis} on {date}")
        st.line_chart(
            data=plotData,
            x=xAxis,
            y="EV",
        )
        groups = plotData.groupby(xAxis)["EV"].apply(list)
        print(groups)
        fig, ax = plt.subplots()
        ax.violinplot(groups, showmeans=True)

        # Add labels and title
        ax.set_xlabel("Ticket Price")
        ax.set_ylabel("EV")
        ax.set_title(f"Violin Plot of EV by Ticket Price for {date}")
        ax.grid(True, axis="y", linestyle="--", color="gray", alpha=0.7)

        st.pyplot(fig)

    elif xAxis == "tickets_sold":
        st.title("EV vs Tickets Sold")
        st.bar_chart(
            data=allData,
            x=xAxis,
            y="EV",
        )
    else:
        st.error("Please select an option to the left")
    return None


def DF(allData):
    col1, col2, col4, col5 = st.columns([0.25, 0.25, 0.25, 0.25])
    name = col1.selectbox(
        "Select a Game Name", allData["game_name"].unique(), index=None
    )
    if name:
        allData = allData[allData["game_name"] == name]

    date = col2.selectbox("Select a Date", allData["date"].unique(), index=None)
    if date:
        allData = allData[allData["date"] == date]

    ticket_price = col4.selectbox(
        "Select a ticket price", allData["ticket_price"].unique(), index=None
    )
    if ticket_price:
        allData = allData[allData["ticket_price"] == ticket_price]

    tickets_sold = col5.selectbox(
        "Select how many tickets sold", allData["tickets_sold"].unique(), index=None
    )
    if tickets_sold:
        allData = allData[allData["tickets_sold"] == tickets_sold]

    st.dataframe(
        allData.drop(columns=["data_table", "_id"], inplace=False),
        hide_index=True,
        width=1000,
    )

    return None


type = st.sidebar.radio("Select type of display", ["Plot", "Dataframe"])

if type == "Plot":
    ts()
else:
    DF(allData)

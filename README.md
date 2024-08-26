# **WA_lotto_scratcher**

### Introduction

---

This is a Python project that scrapes lottery data and calculates winning numbers.

### Purpose Statement

---

The goal of this project is to provide a simple way to scrape lottery data and calculate expected value for each ticket.

### File Structure

---

- `main.py`: This is the entry point of the project. It scrapes lottery data and calculates expected value.
- `notify.py`: This file contains functions to send notifications in case a scratcher goes positive (i.e., wins).
- `Mongo.py`: This is used to communicate with the Mongo Database.

### Dependencies

---

- beatifulsoup4
- requests
- pandas
- datetime
- Pymongo
- selenium

### Installation

---

1. Clone the repository using `git clone`.
2. Install the required libraries using pip (`pip install beautifulsoup4 requests pandas datetime pymongo selenium`).
3. Run the project using Python (`python main.py`).

### Usage

---

Run `python main.py` to scrape lottery data and calculate winning numbers.

### Side Notes

---

- Must have a MONGODB database setup. This is connected to a localhost docker instance (easiest way).
- Selenium is using Safari. Can change this on line 56. webdriver.Chrome() or whatever browser you prefer.

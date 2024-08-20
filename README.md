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
- `games/`: This directory stores time-series files for each scratcher, making it easier to analyze and visualize the data using pandas.

### Dependencies

---

- beatifulsoup4
- requests
- pandas
- datetime

### Installation

---

1. Clone the repository using `git clone`.
2. Install the required libraries using pip (`pip install beautifulsoup4 requests pandas datetime`).
3. Run the project using Python (`python main.py`).

### Usage

---

Run `python main.py` to scrape lottery data and calculate winning numbers.

### Contributing

---

Feel free to contribute to this project by submitting pull requests or issues.

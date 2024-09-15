# Nepse Stock Price History Scraper

This Python script scrapes historical stock price data from [ShareSansar](https://www.sharesansar.com/) for a specified company using Selenium and BeautifulSoup.

## Features

- Automatically scrapes price history data for a given stock symbol.
- Uses Selenium for navigating the web and BeautifulSoup for parsing the HTML.
- Automatically handles pagination.
- Exports the scraped data to a CSV file.

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver (managed automatically by `webdriver_manager`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/nepse-price-history-scraper.git
   cd nepse-price-history-scraper

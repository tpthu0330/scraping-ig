# Instagram Data Crawler

This Python script allows you to crawl and extract data from an Instagram account within a specified date range. The extracted data, including post URLs, content, likes, comments, and timestamps, is then saved to an Excel file.

## Features

- Extracts Instagram post data using a provided account URL
- Allows specifying a date range to filter posts
- Saves the extracted data to an Excel file for further analysis

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `BeautifulSoup` library (from `bs4`)
- `lxml` parser
- `re` library
- `pickle` library

You can install the required libraries using pip:

```bash
pip install requests pandas beautifulsoup4 lxml
```

## Usage

### 1. Prepare Instagram Cookies

Ensure you have the Instagram cookies saved in a `.pkl` file named `insta_cookies_<email>.pkl` where `<email>` is the email associated with the Instagram account.

### 2. Run the Script

Execute the script and provide the necessary inputs when prompted:

```bash
python instagram_data_crawler.py
```

You will be prompted to enter:
- Instagram account URL
- Start date (in `YYYY-MM-DD` format)
- End date (in `YYYY-MM-DD` format)

### 3. Output

The script will output an Excel file named `insta_data.xlsx` containing the Instagram data within the specified date range.

## Functions

### `get_insta_cookies(email)`

Loads Instagram cookies from a pickle file.

- **Parameters**: 
  - `email` (str): The email associated with the Instagram account.
- **Returns**: 
  - `dict`: A dictionary containing the cookies for the Instagram session.

### `id_account(acc_url)`

Extracts the Instagram account ID from the provided URL.

- **Parameters**: 
  - `acc_url` (str): The URL of the Instagram account.
- **Returns**: 
  - `str`: The extracted Instagram account ID.

### `crawl_insta(acc_url, start_date, end_date)`

Crawls Instagram posts from the provided account URL within a specified date range.

- **Parameters**: 
  - `acc_url` (str): The URL of the Instagram account.
  - `start_date` (str): The start date in `YYYY-MM-DD` format.
  - `end_date` (str): The end date in `YYYY-MM-DD` format.
- **Returns**: 
  - `list`: A list of dictionaries containing Instagram post data.

### `save_to_excel(data, file_name)`

Saves the crawled Instagram data to an Excel file.

- **Parameters**: 
  - `data` (list): List of dictionaries containing Instagram data.
  - `file_name` (str): The name of the Excel file to save.
- **Returns**: 
  - `None`

## Disclaimer
This script was written in 2022, and Instagram's website structure or API may have changed since then. 
As a result, the script might not function as intended or may require modifications to work with the current Instagram setup.

## Acknowledgments

- The script utilizes the `requests` library for HTTP requests.
- `BeautifulSoup` is used for parsing HTML content.
- `pandas` is employed for data manipulation and saving to Excel.

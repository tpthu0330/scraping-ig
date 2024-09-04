import requests
import json
from datetime import datetime
import pickle
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_insta_cookies(email):
    """
    Load Instagram cookies from a pickle file and return them as a dictionary.

    Parameters:
    email (str): The email associated with the Instagram account.

    Returns:
    dict: A dictionary containing the cookies for the Instagram session.
    """
    # Initialize an empty dictionary to hold the cookies
    cookies = {}
    # Load cookies from a pickle file specific to the provided email
    insta_cookies = pickle.load(open("insta_cookies_" + email + ".pkl", "rb"))
    # Write to dictionary
    for cookie in insta_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies

# Load cookies for a specific Instagram account
insta_cookie = get_insta_cookies('shuashuafall')

def id_account(acc_url):
    """
    Extract Instagram account ID from the account URL using a regular expression.

    Parameters:
    acc_url (str): Instagram account URL.

    Returns:
    str: The extracted account ID.
    """
    # Get Instagram page content
    insta_acc = requests.get(acc_url, cookies = insta_cookie)
    soup = BeautifulSoup(insta_acc.content, 'lxml')
    # Find script containing 'window._sharedData'
    script_list = soup.find_all('script', attrs={'type':"text/javascript"})
    output_id_list = [element for element in script_list if 'window._sharedData' in element.text]
    # Extract account ID using regex
    script = output_id_list[0]
    id_insta = re.findall(r"profilePage_(\d+)", script.text)
    return id_insta[0]

def crawl_insta(acc_url, start_date, end_date):
    """
    Crawl Instagram posts within a specified date range.

    Parameters:
    acc_url (str): Instagram account URL.
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    list: Filtered list of posts within the date range.
    """
    end_cursor = "" # Initialize cursor for pagination
    id = id_account(acc_url) # Get Instagram account ID

    # Define the API URL for querying Instagram data
    api_url = 'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A12%2C%22after%22%3A%22{}%22%7D'
        
    output = [] # Initialize list to store output data
    flag = True # Control flag for looping

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    while flag == True:
        # Send request to Instagram API
        response = requests.get(api_url.format(id, end_cursor), cookies = insta_cookie)
        print(response.url) # Print API request URL

        # Parse JSON response
        insta_json = json.loads(response.content.decode("utf-8"))
        list_photos = insta_json['data']['user']['edge_owner_to_timeline_media']['edges']
        
        # Process each photo
        for photo in list_photos:
            row = {}
            row['url'] = 'https://instagram.com/p/'+photo['node']['shortcode']
            row['like'] = photo['node']['edge_media_preview_like']['count']
            row['comment'] = photo['node']['edge_media_to_comment']['count']
            row['date'] = datetime.fromtimestamp(photo['node']['taken_at_timestamp'])
            # Extract content if available
            try:
                row['content'] = photo['node']['edge_media_to_caption']['edges'][0]['node']['text']
            except IndexError:
                row['content'] = ""
            # Check date to decide if crawling should stop
            if row['date'] < start_date:
                flag = False
                break
                print('Limit')
            output.append(row)

        # Update cursor for next page
        end_cursor = insta_json['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    
    # Update cursor for next page
    return list(filter(lambda x: (x['date'] < end_date), output))

def save_to_excel(data, file_name):
    """
    Save Instagram data to an Excel file.

    Parameters:
    data (list): List of dictionaries containing Instagram data.
    file_name (str): Name of the Excel file to save.

    Returns:
    None
    """
    # Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to an Excel file
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")


def main():
    """
    Main function to execute the Instagram data crawling and saving process.

    Returns:
    None
    """
    # Get user input for Instagram URL, start date, and end date
    ig_url = input("Enter the Instagram account URL: ")
    ig_start_date = input("Enter the start date (YYYY-MM-DD): ")
    ig_end_date = input("Enter the end date (YYYY-MM-DD): ")

    # Crawl Instagram data using user inputs
    ig_info = crawl_insta(ig_url, ig_start_date, ig_end_date)

    # Save the crawled data to an Excel file
    save_to_excel(ig_info, 'insta_data.xlsx')

# Run the main function
if __name__ == "__main__":
    main()

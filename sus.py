import requests
from fake_useragent import UserAgent
import time
import random
import os

# Function to read proxies from a text file
def get_proxies_from_file(file_path):
    """
    Reads proxies from a text file, one per line.
    Returns a list of proxies.
    """
    if not os.path.exists(file_path):
        print(f"Error: Proxy file not found at '{file_path}'")
        return []
    with open(file_path, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

# Path to your proxy text file
proxy_file = 'working_proxies.txt'  # Make sure this file exists in the same directory
proxy_list = get_proxies_from_file(proxy_file)

if not proxy_list:
    print("No proxies found. The script will exit.")
    exit()

session = requests.Session()

# Common headers for the requests
headers = {
    'User-Agent': UserAgent().firefox,  # Use fake_useragent to get a realistic user agent
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain',
    'Origin': 'https://www.flipkart.com',
    'Referer': 'https://www.google.com',
    'Server': 'cloudflare'
}

# The range of pages you want to scrape
# This will download pages from 1 to 20
start_page = 21
end_page = 39 

for i in range(start_page, end_page):
    # Select a random proxy from the list for each request
    proxy = random.choice(proxy_list)
    proxies = {
        'http': proxy
    }
    
    # Generate a random delay
    k = random.uniform(2.001, 11.177)

    url = f"https://www.flipkart.com/motorola-edge-60-fusion-5g-pantone-slipstream-256-gb/product-reviews/itm8553dc1ee56ee?pid=MOBH9ARFZHXSRYMA&lid=LSTMOBH9ARFZHXSRYMAF5I7OY&marketplace=FLIPKART&page={i}"
    
    print(f"Scraping page {i} with proxy: {proxy}")
    try:
        # Introduce a delay before each request
        time.sleep(k)
        r = session.get(url, proxies=proxies, headers=headers, timeout=10) # Added a timeout for robustness
        r.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Save the content to a file
        with open(f"file{i}.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"Successfully downloaded page {i} to file{i}.html")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while scraping page {i} using proxy {proxy}: {e}")
    
    print("-" * 50)
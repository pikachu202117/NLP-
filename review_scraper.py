import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_reviews(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all review containers
    review_containers = soup.find_all('div', class_='cPHDOP col-12-12')
    
    reviews_data = []
    
    for container in review_containers:
        review_data = {}
        
        # Rating (XQDdHH Ga3i8K)
        rating_elem = container.find('div', class_='XQDdHH Ga3i8K')
        if rating_elem:
            review_data['XQDdHH_Ga3i8K_rating'] = rating_elem.get_text(strip=True)
        
        # Rating category (z9E0IG)
        rating_category = container.find('p', class_='z9E0IG')
        if rating_category:
            review_data['z9E0IG_rating_category'] = rating_category.get_text(strip=True)
        
        # Review text (ZmyHeo)
        review_text_container = container.find('div', class_='ZmyHeo')
        if review_text_container:
            # Get all text from the container
            review_text = review_text_container.get_text(separator=' ', strip=True)
            # Remove "READ MORE" if present
            review_text = re.sub(r'\s*READ MORE\s*', '', review_text)
            review_data['ZmyHeo_review_text'] = review_text
        
        # Reviewer name (_2NsDsF AwS1CA)
        reviewer_name = container.find('p', class_='_2NsDsF AwS1CA')
        if reviewer_name:
            review_data['_2NsDsF_AwS1CA_reviewer_name'] = reviewer_name.get_text(strip=True)
        
        # Reviewer details (MztJPv)
        reviewer_details = container.find('p', class_='MztJPv')
        if reviewer_details:
            review_data['MztJPv_reviewer_details'] = reviewer_details.get_text(strip=True)
        
        # Review date (_2NsDsF - second occurrence)
        date_elements = container.find_all('p', class_='_2NsDsF')
        if len(date_elements) > 1:
            review_data['_2NsDsF_review_date'] = date_elements[-1].get_text(strip=True)
        
        # Helpful votes (tl9VpF - thumbs up)
        vote_elements = container.find_all('span', class_='tl9VpF')
        if len(vote_elements) >= 1:
            review_data['tl9VpF_thumbs_up'] = vote_elements[0].get_text(strip=True)
        if len(vote_elements) >= 2:
            review_data['tl9VpF_thumbs_down'] = vote_elements[1].get_text(strip=True)
        
        # Only add non-empty reviews
        if review_data:
            reviews_data.append(review_data)
    
    return pd.DataFrame(reviews_data)

def scrape_from_url(url, headers=None):
    """
    Scrape reviews from a URL
    """
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return scrape_reviews(response.text)

def scrape_from_file(file_path):
    """
    Scrape reviews from HTML file
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    return scrape_reviews(html_content)


if __name__ == "__main__":
    all_files_df = []
file_names = ['file.html', 'file1.html'] + [f'file{i}.html' for i in range(2, 19)] # You can adjust the range as needed.

for file_name in file_names:
    try:
        df = scrape_from_file(file_name)
        if not df.empty:
            all_files_df.append(df)
        else:
            print(f"No reviews found in '{file_name}', adding an empty record.")
            empty_df = pd.DataFrame([{'name': 'N/A', 'rating': 'N/A', 'review_title': 'N/A', 'review_description': 'N/A', 'likes': '0', 'dislikes': '0'}])
            all_files_df.append(empty_df)
    except FileNotFoundError:
        print(f"File '{file_name}' not found, skipping.")
        # As per your request, if a file is not found, the record would be empty.
        # We can add an empty DataFrame or an empty record.
        empty_df = pd.DataFrame([{'name': 'N/A', 'rating': 'N/A', 'review_title': 'N/A', 'review_description': 'N/A', 'likes': '0', 'dislikes': '0'}])
        all_files_df.append(empty_df)


# Consolidate all dataframes into a single dataframe
consolidated_df = pd.concat(all_files_df, ignore_index=True)

# Display results
print(f"Scraped {len(consolidated_df)} records in total.")
print("\nColumn names:")
for col in consolidated_df.columns:
    print(f"- {col}")

print("\nFirst few rows:")
print(consolidated_df.head())

# Save to CSV
consolidated_df.to_csv('scraped_reviews.csv', index=False)
print("\nData saved to 'scraped_reviews.csv'")

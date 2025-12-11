from bs4 import BeautifulSoup
import csv

# Your modification to read the file from disk is correct.
html_content = ""
with open("file.html", "r") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

reviews = soup.find_all('div', class_='_2nQpl_')
extracted_data = []

for review in reviews:
    try:
        # Extract reviewer name
        name = review.find('p', class_='_2sc7ZR _2V5EHH').text.strip()
        
        # Extract rating
        rating_container = review.find('div', class_='_3LWZlK _1BLPMq')
        rating = rating_container.text.strip() if rating_container else "N/A"
        
        # Extract review title
        title = review.find('p', class_='_2-N8zT').text.strip()
        
        # Extract review description
        description_container = review.find('div', class_='t-ZTKy')
        # The description is inside a nested div
        description = description_container.find('div').text.strip() if description_container and description_container.find('div') else "N/A"
        
        # Extract likes and dislikes
        likes_dislikes_container = review.find('div', class_='_1G6s-')
        likes_dislikes = likes_dislikes_container.find_all('span', class_='_1H-LsS') if likes_dislikes_container else []
        likes = likes_dislikes[0].text.strip() if len(likes_dislikes) > 0 else '0'
        dislikes = likes_dislikes[1].text.strip() if len(likes_dislikes) > 1 else '0'

        # Add the extracted data to our list
        extracted_data.append({
            'name': name,
            'rating': rating,
            'review_title': title,
            'review_description': description,
            'likes': likes,
            'dislikes': dislikes
        })
    except AttributeError:
        # Skip if a review element is missing parts
        continue

# Define the CSV file name and headers
csv_file = 'review_data.csv'
fieldnames = ['name', 'rating', 'review_title', 'review_description', 'likes', 'dislikes']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(extracted_data)

print(f"Data successfully extracted and saved to {csv_file}")

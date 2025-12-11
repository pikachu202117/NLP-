import pandas as pd
import os

# Read data1.csv to get the URLs
try:
    df_data1 = pd.read_csv("data1.csv")
    urls = df_data1.iloc[:, 0].tolist()
except FileNotFoundError:
    print("Error: data1.csv not found.")
    exit()

# Define the range of review files to process
start_index = 9
end_index = 14
review_files = [f'scraped_reviews{i}.csv' for i in range(start_index, end_index + 1)]

# Check if review files exist
missing_files = [file for file in review_files if not os.path.exists(file)]
if missing_files:
    print("Error: The following review files are missing:")
    for file in missing_files:
        print(f" - {file}")
    print("Please provide these files and run the script again.")
else:
    for i in range(start_index, end_index + 1):
        review_file_name = f'scraped_reviews{i}.csv'
        url_index = i - start_index

        if url_index < len(urls):
            url = urls[url_index]
            try:
                parts = url.strip('/').split('/')
                model_name = parts[-3]

                df_reviews = pd.read_csv(review_file_name)
                df_reviews['model_name'] = model_name

                df_reviews.to_csv(review_file_name, index=False)
                print(f"Successfully processed {review_file_name}. 'model_name' column added with value '{model_name}'.")

            except IndexError:
                print(f"Could not extract model name from URL: {url} for file {review_file_name}. Skipping...")
            except Exception as e:
                print(f"An error occurred while processing {review_file_name}: {e}")
        else:
            print(f"Not enough URLs in data1.csv to process all review files. Skipping {review_file_name}...")

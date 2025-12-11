import pandas as pd
import os

def consolidate_and_filter_csvs(output_filename='consolidated_reviews.csv'):
    # Define the columns to be extracted, based on my previous HTML scraping.
    # These column names are derived from the classes found in the HTML which i have downloaded using requests.
    columns_to_extract = {
        'XQDdHH_Ga3i8K_rating': 'rating',
        'z9E0IG_rating_category': 'review_title',
        'ZmyHeo_review_text': 'review_description',
        '_2NsDsF_AwS1CA_reviewer_name': 'reviewer_name',
        'MztJPv_reviewer_details': 'reviewer_details',
        '_2NsDsF_review_date': 'review_date',
        'tl9VpF_thumbs_up': 'likes',
        'tl9VpF_thumbs_down': 'dislikes',
        'mobile' : 'model_name',
	'model_name' : 'model_name'
    }

    all_dataframes = []
    
    # Iterate through the range of files specified
    for i in range(1, 14): # Loop from 1 to 10
        filename = f'scraped_reviews{i}.csv'
        
        if os.path.exists(filename):
            print(f"Processing file: {filename}")
            try:
                df = pd.read_csv(filename)
                existing_cols_to_extract = {col: new_name for col, new_name in columns_to_extract.items() if col in df.columns}
                
                if existing_cols_to_extract:
                    # Select the specified columns and rename them
                    extracted_df = df[list(existing_cols_to_extract.keys())].rename(columns=existing_cols_to_extract)
                    all_dataframes.append(extracted_df)
                else:
                    print(f"Warning: No specified columns found in {filename}.")
            except pd.errors.EmptyDataError:
                print(f"Warning: {filename} is empty. Skipping.")
            except Exception as e:
                print(f"An error occurred while reading {filename}: {e}")
        else:
            print(f"File not found: {filename}. Ignoring as requested.")

    if all_dataframes:
        consolidated_df = pd.concat(all_dataframes, ignore_index=True)
        consolidated_df.to_csv(output_filename, index=False)
        print(f"\nSuccessfully consolidated data into '{output_filename}'")
        print(f"Total rows in consolidated file: {len(consolidated_df)}")
        print("\nColumns in final CSV:")
        print(consolidated_df.columns.tolist())
    else:
        print("\nNo data to consolidate. No valid files were found or processed.")

if __name__ == "__main__":
    consolidate_and_filter_csvs()

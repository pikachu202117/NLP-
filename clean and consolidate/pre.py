import pandas as pd
import re

def preprocess_reviews(df):
    print("Step 1: Removing emojis from text columns...")
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE)

    # Apply the regex to all columns with 'object' (string) data type
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).apply(lambda x: emoji_pattern.sub(r'', x))
    
    print("Emojis removed.")
    print("-" * 50)

    print("Step 2: Dropping records with more than one null value...")
    total_columns = len(df.columns)
    
    # Drop rows where the number of non-null values is less than (total_columns - 1)
    original_row_count = len(df)
    df.dropna(thresh=total_columns - 1, inplace=True)
    
    print(f"Dropped {original_row_count - len(df)} records. {len(df)} records remaining.")
    print("-" * 50)


    print("Step 3: Imputing missing ratings with the average...")
    if 'rating' in df.columns:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        # Calculate the mean of the existing ratings, excluding NaN values
        average_rating = df['rating'].mean()
        
        if pd.notna(average_rating):
            # Fill any missing values in the 'rating' column with the average
            df['rating'] = df['rating'].fillna(average_rating)
            print(f"Missing ratings imputed with the average: {average_rating:.2f}")
        else:
            print("Warning: Could not calculate average rating. No values were imputed.")
    else:
        print("Warning: 'rating' column not found in the DataFrame. Skipping imputation.")
    
    print("-" * 50)
    
    return df

df = pd.read_csv('consolidated_reviews.csv')

print("Original DataFrame:")
print(df)
print("\n" + "="*50 + "\n")

preprocessed_df = preprocess_reviews(df.copy())

print("\n" + "="*50 + "\n")
print("Preprocessed DataFrame:")
print(preprocessed_df)
preprocessed_df.to_csv("cleaned.csv")

import os
import pandas as pd
from scripts.consolidate_data import consolidate_excel_files_to_csv
from scripts.parse_data import clean_data, restructure_data
from scripts.features import add_match_features

# Define key file paths
BASE_DIR = '/Users/swagner/VSCode/Tennis_Prediction/src'
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONSOLIDATED_CSV = os.path.join(DATA_DIR, 'consolidated_data.csv')
FINAL_OUTPUT_CSV = os.path.join(DATA_DIR, 'final_output_with_elo.csv')

def main():
    # Step 1: Consolidate Excel files to CSV
    print("🔄 Consolidating Excel files...")
    consolidate_excel_files_to_csv(DATA_DIR, CONSOLIDATED_CSV)

    # Step 2: Clean Data
    print("🧹 Cleaning data...")
    cleaned_df = clean_data(CONSOLIDATED_CSV)

    # Step 3: Restructure Data using cleaned_df directly
    print("🔀 Restructuring data...")
    restructured_df = restructure_data(cleaned_df)

    # Step 4: Add all feature columns
    print("📈 Generating match features...")
    restructured_df, _, _ = add_match_features(restructured_df)

    # Step 5: Save final dataset
    restructured_df.to_csv(FINAL_OUTPUT_CSV, index=False)
    print(f"✅ Final dataset saved to: {FINAL_OUTPUT_CSV}")

if __name__ == "__main__":
    main()

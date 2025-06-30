import os
from scripts.consolidate_data import consolidate_excel_files_to_csv
from scripts.parse_data import clean_data, restructure_data
from scripts.elo import calculate_elo
import pandas as pd

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

    # Step 3: Restructure Data
    print("🔀 Restructuring data...")
    restructured_df = restructure_data(CONSOLIDATED_CSV)

    # Step 4: Calculate ELO and enhance dataset
    print("📈 Calculating ELO ratings...")
    player_elo = {}
    elo_ratings_1 = []
    elo_ratings_2 = []

    for _, row in restructured_df.iterrows():
        p1, p2 = row['player_1'], row['player_2']
        win = row['Winner']
        elo_ratings_1.append(player_elo.get(p1, 1500))
        elo_ratings_2.append(player_elo.get(p2, 1500))
        player_elo = calculate_elo(player_elo, p1, p2, p1 if win == "player_1" else p2)

    restructured_df['elo_player_1'] = elo_ratings_1
    restructured_df['elo_player_2'] = elo_ratings_2

    # Step 5: Save final dataset
    restructured_df.to_csv(FINAL_OUTPUT_CSV, index=False)
    print(f"✅ Final dataset saved to: {FINAL_OUTPUT_CSV}")

if __name__ == "__main__":
    main()

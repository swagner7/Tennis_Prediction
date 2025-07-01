import os
import pandas as pd
from scripts.consolidate_data import consolidate_excel_files_to_csv
from scripts.parse_data import clean_data, restructure_data
from scripts.elo import calculate_elo

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

    # Step 3: Restructure Data using cleaned_df instead of CSV
    print("🔀 Restructuring data...")
    cleaned_df.to_csv("src/data/cleaned_temp.csv", index=False)  # Save interim clean file
    restructured_df = restructure_data("src/data/cleaned_temp.csv")

    # Step 4: Calculate ELO and enhance dataset
    print("📈 Calculating ELO ratings...")
    player_elo = {}
    surface_elo = {}
    elo_ratings_1 = []
    elo_ratings_2 = []
    surface_elo_1 = []
    surface_elo_2 = []

    for _, row in restructured_df.iterrows():
        p1, p2 = row['player_1'], row['player_2']
        win = row['Winner']
        winner_name = p1 if win == "player_1" else p2
        surface = row.get('Surface', 'Unknown')

        # General Elo
        elo_ratings_1.append(player_elo.get(p1, 1500))
        elo_ratings_2.append(player_elo.get(p2, 1500))
        player_elo = calculate_elo(player_elo, p1, p2, winner_name)

        # Surface-specific Elo
        surface_elo.setdefault(surface, {})
        surface_dict = surface_elo[surface]
        surface_elo_1.append(surface_dict.get(p1, 1500))
        surface_elo_2.append(surface_dict.get(p2, 1500))
        surface_elo[surface] = calculate_elo(surface_dict, p1, p2, winner_name)

    # Add Elo columns to final dataset
    restructured_df['elo_player_1'] = elo_ratings_1
    restructured_df['elo_player_2'] = elo_ratings_2
    restructured_df['surface_elo_player_1'] = surface_elo_1
    restructured_df['surface_elo_player_2'] = surface_elo_2

    # Step 5: Save final dataset
    restructured_df.to_csv(FINAL_OUTPUT_CSV, index=False)
    print(f"✅ Final dataset saved to: {FINAL_OUTPUT_CSV}")

if __name__ == "__main__":
    main()

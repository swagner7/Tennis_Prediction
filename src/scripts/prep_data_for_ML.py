import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    """
    Load the engineered tennis match dataset, clean and extract features for ML model training.

    This function:
    - Loads the final output CSV with all enriched features
    - Drops rows with missing values (for modeling compatibility)
    - Defines the binary target variable: 1 if player_1 wins, else 0
    - Selects feature columns: Elo ratings, recent form, opponent strength, and rest days
    - Saves two files:
        - X.csv: features for modeling
        - y.csv: binary target labels

    Output files are saved in the '../data/' directory.
    """
    df = pd.read_csv('../data/final_output_with_elo.csv')

    # Drop any rows with missing values (or handle differently if needed)
    df = df.dropna()

    # Define target and features
    y = (df['Winner'] == 'player_1').astype(int)
    feature_cols = [col for col in df.columns if col.startswith(('elo_', 'form', 'avg_opp', 'days_since'))]

    X = df[feature_cols]

    # Save feature and target datasets
    X.to_csv('../data/X.csv', index=False)
    y.to_csv('../data/y.csv', index=False)
    print("✅ Prepared X.csv and y.csv for ML modeling")

if __name__ == '__main__':
    main()

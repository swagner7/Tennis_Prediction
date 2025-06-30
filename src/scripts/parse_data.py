import pandas as pd
import numpy as np

def clean_data(csv_path):
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['Winner', 'Loser'])  # Ensure both columns exist
    return df

def restructure_data(csv_path):
    """
    Load tennis match data and restructure it to have 'player_1', 'player_2', and 'winner' columns,
    while preserving match metadata columns.

    Parameters:
        csv_path (str): Path to the input CSV file with 'winner' and 'loser' columns.

    Returns:
        pd.DataFrame: Restructured match data with metadata.
    """
    df = pd.read_csv(csv_path)

    metadata_cols = ['Location', 'Tournament', 'Date', 'Series', 'Court', 'Best of']

    def randomize_players(row):
        if np.random.rand() > 0.5:
            return pd.Series({
                'player_1': row['Winner'],
                'player_2': row['Loser'],
                'Winner': 'player_1',
                **{col: row[col] for col in metadata_cols if col in row}
            })
        else:
            return pd.Series({
                'player_1': row['Loser'],
                'player_2': row['Winner'],
                'Winner': 'player_2',
                **{col: row[col] for col in metadata_cols if col in row}
            })

    restructured_df = df.apply(randomize_players, axis=1)
    restructured_df.to_csv("restructured_df.csv", index=False)
    return restructured_df

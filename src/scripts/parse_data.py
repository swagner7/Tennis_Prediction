import pandas as pd
import numpy as np

def clean_data(csv_path):
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['Winner', 'Loser'])  # Ensure both columns exist
    df = df[df['Comment'] == 'Completed'] # Filter for completed matches
    return df

def restructure_data(df):
    """
    Restructure a cleaned DataFrame to have 'player_1', 'player_2', and 'winner' columns,
    while preserving match metadata.

    Parameters:
        df (pd.DataFrame): Cleaned match data with 'winner' and 'loser' columns.

    Returns:
        pd.DataFrame: Restructured match data with metadata.
    """
    metadata_cols = ['Location', 'Tournament', 'Date', 'Series', 'Court', 'Best of', 'Surface', 'Round']

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

    return df.apply(randomize_players, axis=1)

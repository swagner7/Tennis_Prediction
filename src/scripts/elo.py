import os
import pandas as pd

# Define the folder containing the Excel files and the output CSV file
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
output_csv = os.path.join(data_folder, 'consolidated_data.csv')

def calculate_elo(player_elo, player1, player2, winner, k=32):
    """
    Update ELO ratings based on match results.
    :param player_elo: Dictionary of player ELO ratings.
    :param player1: Name of Player 1.
    :param player2: Name of Player 2.
    :param winner: Name of the winner.
    :param k: K-factor for ELO calculation.
    :return: Updated player_elo dictionary.
    """
    # Initialize ELO ratings if players are not in the dictionary
    player_elo.setdefault(player1, 1500)
    player_elo.setdefault(player2, 1500)

    # Calculate expected scores
    expected1 = 1 / (1 + 10 ** ((player_elo[player2] - player_elo[player1]) / 400))
    expected2 = 1 / (1 + 10 ** ((player_elo[player1] - player_elo[player2]) / 400))

    # Update ELO ratings based on the match result
    if winner == player1:
        player_elo[player1] += k * (1 - expected1)
        player_elo[player2] += k * (0 - expected2)
    elif winner == player2:
        player_elo[player1] += k * (0 - expected1)
        player_elo[player2] += k * (1 - expected2)

    return player_elo
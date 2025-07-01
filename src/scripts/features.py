import pandas as pd
from datetime import datetime
from scripts.elo import calculate_elo

def add_match_features(df, player_elo=None, surface_elo=None):
    """
    Enrich match data with player and match-specific features useful for ML predictions.

    Features added:
        - elo_player_1 / elo_player_2: General Elo rating at match time
        - surface_elo_player_1 / _2: Elo specific to surface (Clay, Grass, etc.)
        - days_since_1 / _2: Days since last match for each player
        - form5_1 / _2: Win rate over last 5 matches
        - form10_1 / _2: Win rate over last 10 matches
        - avg_opp5_1 / _2: Avg opponent Elo over last 5 matches
        - avg_opp10_1 / _2: Avg opponent Elo over last 10 matches
    """
    player_elo = player_elo or {}
    surface_elo = surface_elo or {}

    # Historical tracking
    last_match_date = {}
    recent_results = {}
    recent_opponent_elo = {}

    # Feature containers
    days_since_1 = []
    days_since_2 = []
    form5 = []
    form10 = []
    avg_opp5 = []
    avg_opp10 = []
    elo_ratings_1 = []
    elo_ratings_2 = []
    surface_elo_1 = []
    surface_elo_2 = []

    for _, row in df.iterrows():
        date = pd.to_datetime(row['Date'])
        p1, p2 = row['player_1'], row['player_2']
        win = row['Winner']
        winner_name = p1 if win == "player_1" else p2
        surface = row.get('Surface', 'Unknown')

        # 🗓️ Days since last match per player
        def compute_days(player):
            if player in last_match_date:
                delta = (date - last_match_date[player]).days
            else:
                delta = None
            last_match_date[player] = date
            return delta

        days_since_1.append(compute_days(p1))
        days_since_2.append(compute_days(p2))

        # 📊 General Elo before match
        current_elo1 = player_elo.get(p1, 1500)
        current_elo2 = player_elo.get(p2, 1500)
        elo_ratings_1.append(current_elo1)
        elo_ratings_2.append(current_elo2)

        # 🧱 Surface-specific Elo before match
        surface_elo.setdefault(surface, {})
        surface_dict = surface_elo[surface]
        surface_elo_1.append(surface_dict.get(p1, 1500))
        surface_elo_2.append(surface_dict.get(p2, 1500))

        # 📈 Recent form and average opponent Elo
        def update_player_stats(player, won, opp_elo):
            recent_results.setdefault(player, [])
            recent_opponent_elo.setdefault(player, [])
            if won is not None:
                recent_results[player].append(1 if won else 0)
                recent_opponent_elo[player].append(opp_elo)

            form_5 = sum(recent_results[player][-5:]) / min(5, len(recent_results[player]))
            form_10 = sum(recent_results[player][-10:]) / min(10, len(recent_results[player]))
            avg_5 = sum(recent_opponent_elo[player][-5:]) / min(5, len(recent_opponent_elo[player]))
            avg_10 = sum(recent_opponent_elo[player][-10:]) / min(10, len(recent_opponent_elo[player]))
            return form_5, form_10, avg_5, avg_10

        f5_1, f10_1, a5_1, a10_1 = update_player_stats(p1, win == 'player_1', current_elo2)
        f5_2, f10_2, a5_2, a10_2 = update_player_stats(p2, win == 'player_2', current_elo1)

        form5.append((f5_1, f5_2))
        form10.append((f10_1, f10_2))
        avg_opp5.append((a5_1, a5_2))
        avg_opp10.append((a10_1, a10_2))

        # 🔄 Update Elo ratings (after match)
        player_elo = calculate_elo(player_elo, p1, p2, winner_name)
        surface_elo[surface] = calculate_elo(surface_dict, p1, p2, winner_name)

    # Assign features to dataframe
    df['elo_player_1'] = elo_ratings_1
    df['elo_player_2'] = elo_ratings_2
    df['surface_elo_player_1'] = surface_elo_1
    df['surface_elo_player_2'] = surface_elo_2
    df['days_since_1'] = days_since_1
    df['days_since_2'] = days_since_2
    df[['form5_1','form5_2']] = pd.DataFrame(form5, index=df.index)
    df[['form10_1','form10_2']] = pd.DataFrame(form10, index=df.index)
    df[['avg_opp5_1','avg_opp5_2']] = pd.DataFrame(avg_opp5, index=df.index)
    df[['avg_opp10_1','avg_opp10_2']] = pd.DataFrame(avg_opp10, index=df.index)

    return df, player_elo, surface_elo

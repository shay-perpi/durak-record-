from collections import Counter
from app.db import get_players

def fetch_player_statistics():
    """
    Fetch and calculate statistics for all players.
    Returns:
        dict: A dictionary containing player statistics.
    """
    players = get_players()
    player_stats = {player["name"]: {"total_losses": 0, "evening_losses": 0, "round_losses": 0} for player in players}

    # Fetch data from Firestore (this part is a placeholder for live queries)
    # Example structure:
    # evening_data = db.collection("evenings").stream()
    # round_data = db.collection("rounds").stream()

    # For now, we’ll return placeholder data
    return player_stats

def prepare_statistics_for_visualization(stats):
    """
    Prepare statistics for graphical representation.
    Args:
        stats (dict): Player statistics.
    Returns:
        dict: Prepared data for charts and graphs.
    """
    losses = {player: data["total_losses"] for player, data in stats.items()}
    return losses

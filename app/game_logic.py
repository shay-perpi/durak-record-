from collections import Counter

def determine_round_loser(losses, players):
    """
    Identify the player with 5 losses in a round.
    """
    for player in players:
        if losses[player] >= 5:
            return player
    return None

def determine_evening_loser(round_losers):
    """
    Determine the evening loser based on the rounds lost.
    Arguments:
        round_losers (list): List of players who lost rounds in the evening.
    Returns:
        str: The name of the evening loser.
    """
    if not round_losers:
        return None
    count = Counter(round_losers)
    return count.most_common(1)[0][0]

def reset_losses(players):
    """
    Reset all players' loss counts for a new game.
    """
    return {player: 0 for player in players}


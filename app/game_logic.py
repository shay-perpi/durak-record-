from collections import Counter

def determine_round_loser(losses, players):
    """
    Determine the round loser based on the losses.
    Arguments:
        losses (dict): Dictionary of players and their loss counts.
        players (list): List of all active players.
    Returns:
        str: The name of the round loser.
    """
    for player in players:
        if losses.get(player, 0) >= 5:
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
    Reset loss counts for all players at the end of a round or evening.
    Arguments:
        players (list): List of player names.
    Returns:
        dict: A reset dictionary with players' loss counts set to 0.
    """
    return {player: 0 for player in players}

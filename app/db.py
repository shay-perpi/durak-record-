import firebase_admin
from firebase_admin import credentials, firestore

# Firestore initialization
def initialize_db():
    """
    Initialize the Firestore connection using service account credentials.
    Replace 'path/to/your/firebase/credentials.json' with the actual path.
    """
    try:
        cred = credentials.Certificate("path/to/your/firebase/credentials.json")
        firebase_admin.initialize_app(cred)
    except ValueError:
        # Firebase already initialized
        pass

def get_players():
    """
    Fetch all players from the Firestore 'players' collection.
    Returns a list of player dictionaries.
    """
    db = firestore.client()
    players = db.collection('players').stream()
    return [{**doc.to_dict(), 'id': doc.id} for doc in players]

def log_round_loss(loser_name, manual_end=False):
    """
    Record a round loss in the Firestore 'rounds' collection.
    Arguments:
        loser_name (str): Name of the player who lost.
        manual_end (bool): Whether the round ended manually.
    """
    db = firestore.client()
    db.collection('rounds').add({
        'date': firestore.SERVER_TIMESTAMP,
        'loser': loser_name,
        'manual_end': manual_end
    })

def finalize_evening(round_losers, evening_loser):
    """
    Finalize an evening in the Firestore 'evenings' collection.
    Arguments:
        round_losers (list): List of players who lost rounds in the evening.
        evening_loser (str): Name of the player who lost the most rounds.
    """
    db = firestore.client()
    db.collection('evenings').add({
        'date': firestore.SERVER_TIMESTAMP,
        'round_losers': round_losers,
        'evening_loser': evening_loser
    })

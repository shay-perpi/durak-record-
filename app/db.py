import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate("durak-record-firebase-adminsdk-olf7r-295d46a304.json")  # Update the path
    firebase_admin.initialize_app(cred)

def get_firestore_client():
    """
    Returns a Firestore client instance.
    """
    return firestore.client()

# Firestore initialization
def initialize_db():
    """
    Initialize the Firestore connection using service account credentials.
    Replace 'path/to/your/firebase/credentials.json' with the actual path.
    """
    try:
        cred = credentials.Certificate("durak-record-firebase-adminsdk-olf7r-295d46a304.json")
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


def log_round_loss(loser_name, manual_end=False):
    """
    Record a round loss or early game ending in Firestore.
    """
    db = firestore.client()
    db.collection('games').add({
        'loser': loser_name,
        'manual_end': manual_end,
        'players': st.session_state.selected_players,
        'losses': st.session_state.losses,
        'timestamp': firestore.SERVER_TIMESTAMP
    })


# Fetch All Players
def get_all_players():
    db = firestore.client()
    players_ref = db.collection("players")
    players = players_ref.stream()

    return [
        {"id": player.id, "name": player.to_dict().get("name"), "score": player.to_dict().get("score", 0)}
        for player in players
    ]


# Add a New Player
def add_player(name):
    db = firestore.client()
    db.collection("players").add({"name": name, "score": 0})


# Update Scores
def update_score(players, scores):
    db = firestore.client()
    for player in players:
        player_id = player["id"]
        current_score = scores[player["name"]]
        db.collection("players").document(player_id).update({"score": current_score})


# Fetch Statistics
def get_statistics():
    db = firestore.client()

    round_losses = db.collection("rounds").stream()
    evening_losses = db.collection("evenings").stream()
    results = db.collection("results").stream()

    return {
        "round_losses": [{"player_name": r.to_dict()["player_name"], "losses": r.to_dict()["losses"]} for r in round_losses],
        "evening_losses": [{"evening_date": e.to_dict()["date"], "losses": e.to_dict()["losses"]} for e in evening_losses],
        "results": [{"player_name": r.to_dict()["player_name"], "losses": r.to_dict()["losses"]} for r in results],
    }
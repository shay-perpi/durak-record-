import streamlit as st
from app.db import get_players, log_round_loss, finalize_evening
from app.game_logic import determine_round_loser, determine_evening_loser, reset_losses

# Persistent variables
if "losses" not in st.session_state:
    st.session_state.losses = {}
if "round_losers" not in st.session_state:
    st.session_state.round_losers = []

def render_home():
    """
    Render the home page where players can be managed.
    """
    st.title("Durak Record - Home")
    st.markdown("Welcome to Durak Record! Use the sidebar to navigate.")

def render_game():
    """
    Render the game page to track ongoing games.
    """
    st.title("Current Game")
    st.markdown("Track losses and rounds here.")

    # Load players from Firestore
    players = get_players()
    player_names = [player["name"] for player in players]

    # Display players and losses
    if not player_names:
        st.warning("No players found. Add players from the database.")
        return

    st.subheader("Player Losses")
    for player in player_names:
        if player not in st.session_state.losses:
            st.session_state.losses[player] = 0
        st.text(f"{player}: {st.session_state.losses[player]} losses")

    # Record a loss
    st.subheader("Add a Loss")
    selected_player = st.selectbox("Select a player to add a loss:", player_names)
    if st.button("Add Loss"):
        st.session_state.losses[selected_player] += 1
        st.success(f"Added a loss to {selected_player}.")
        round_loser = determine_round_loser(st.session_state.losses, player_names)
        if round_loser:
            st.session_state.round_losers.append(round_loser)
            st.success(f"{round_loser} has lost the round!")
            log_round_loss(round_loser)
            st.session_state.losses = reset_losses(player_names)

    # Option to end the evening manually
    if st.button("End Evening"):
        evening_loser = determine_evening_loser(st.session_state.round_losers)
        if evening_loser:
            finalize_evening(st.session_state.round_losers, evening_loser)
            st.success(f"The evening loser is {evening_loser}.")
            st.session_state.round_losers = []

def render_statistics():
    """
    Render the statistics page.
    """
    st.title("Statistics")
    st.markdown("View historical statistics about game losses.")

    # Example: Placeholder for statistics
    st.info("Statistics coming soon! Stay tuned for detailed graphs and tables.")

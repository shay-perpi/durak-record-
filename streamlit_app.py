import streamlit as st
from app.ui_components import render_game, render_statistics, render_player_management
from app.db import get_all_players

# Initialize Streamlit App
st.sidebar.title("Durak Record")
page = st.sidebar.radio("Navigation", ["Game", "Statistics", "Manage Players"])

# State Initialization
if "selected_players" not in st.session_state:
    st.session_state.selected_players = []

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "game_active" not in st.session_state:
    st.session_state.game_active = False

# Navigation
if page == "Game":
    players = get_all_players()

    if not st.session_state.game_active:
        st.header("Select Players for the Game")
        selected_names = st.multiselect(
            "Choose players to include in the game:",
            [player["name"] for player in players]
        )
        if st.button("Start Game"):
            if selected_names:
                st.session_state.selected_players = [
                    player for player in players if player["name"] in selected_names
                ]
                st.session_state.scores = {player["name"]: 0 for player in st.session_state.selected_players}
                st.session_state.game_active = True
            else:
                st.warning("Please select at least one player to start the game.")

    if st.session_state.game_active:
        render_game(st.session_state.selected_players, st.session_state.scores)

elif page == "Statistics":
    render_statistics()

elif page == "Manage Players":
    render_player_management()

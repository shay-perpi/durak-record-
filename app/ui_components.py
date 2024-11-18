import streamlit as st
import pandas as pd
import plotly.express as px
from app.db import update_score, get_statistics, add_player


def render_game(selected_players, scores):
    st.title("Durak Game")
    st.subheader("Manage the current game and player scores.")

    for player in selected_players:
        name = player["name"]
        col_left, col_mid, col_right = st.columns([1, 2, 1])

        with col_mid:
            st.markdown(f"<h2 style='text-align: center;'>{name}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>{scores[name]}</h3>", unsafe_allow_html=True)

        with col_right:
            if st.button(f"Raise ({name})", key=f"raise_{name}"):
                scores[name] += 1

        with col_left:
            if st.button(f"Decrease ({name})", key=f"decrease_{name}"):
                scores[name] = max(0, scores[name] - 1)

    if any(score == 5 for score in scores.values()):
        st.warning("A player has reached 5 losses. End the game?")
        if st.button("End Game"):
            st.success("Game Over. Results recorded.")
            update_score(selected_players, scores)
            reset_game()

    if st.button("End Game Early"):
        st.info("Game ended early and recorded.")
        update_score(selected_players, scores)
        reset_game()


def reset_game():
    st.session_state.selected_players = []
    st.session_state.scores = {}
    st.session_state.game_active = False


def render_statistics():
    import pandas as pd
    import plotly.express as px
    import streamlit as st
    from app.db import get_statistics

    st.title("Durak Game Statistics")
    stats = get_statistics()

    # Pie Chart: Loss Percentage by Rounds
    st.markdown("### Loss Percentage by Rounds")
    round_losses_df = pd.DataFrame(stats.get("round_losses", []))

    if not round_losses_df.empty:
        pie_chart = px.pie(
            round_losses_df,
            names="player_name",
            values="losses",
            title="Round Loss Percentage",
        )
        st.plotly_chart(pie_chart, use_container_width=True)
    else:
        st.info("No data available for round losses.")

    # Bar Chart: Losses by Evenings
    st.markdown("### Losses by Evenings")
    evening_losses_df = pd.DataFrame(stats.get("evening_losses", []))

    if not evening_losses_df.empty:
        bar_chart = px.bar(
            evening_losses_df,
            x="evening_date",
            y="losses",
            labels={"evening_date": "Evening", "losses": "Total Losses"},
            title="Losses by Evenings",
        )
        st.plotly_chart(bar_chart, use_container_width=True)
    else:
        st.info("No data available for evening losses.")

    # Table: Player Loss Summary
    st.markdown("### Player Loss Summary")
    results_df = pd.DataFrame(stats.get("results", []))

    if not results_df.empty:
        st.table(results_df)
    else:
        st.info("No data available for player loss summary.")


def render_player_management():
    st.title("Manage Players")
    st.subheader("Add a New Player")

    new_player_name = st.text_input("Player Name")
    if st.button("Add Player"):
        if new_player_name.strip():
            add_player(new_player_name.strip())
            st.success(f"Player '{new_player_name}' added successfully.")
        else:
            st.error("Player name cannot be empty.")

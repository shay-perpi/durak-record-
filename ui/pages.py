import streamlit as st
from app.ui_components import render_home, render_game, render_statistics

def main():
    """
    Main function to render the Streamlit app with navigation.
    """
    st.sidebar.title("Durak Record")
    page = st.sidebar.radio("Navigate", ["Home", "Game", "Statistics"])

    if page == "Home":
        render_home()
    elif page == "Game":
        render_game()
    elif page == "Statistics":
        render_statistics()

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from datetime import date

# Set page configuration
st.set_page_config(page_title="Cycling Club Tracker", page_icon="🚴")

# Initialize data in session state if it doesn't exist
if 'rides' not in st.session_state:
    st.session_state.rides = pd.DataFrame(columns=["Date", "Member", "KM"])

st.title("🚴 Cycling Club KM Tracker")

# --- Sidebar: Log a New Ride ---
st.sidebar.header("Log a Ride")
member_name = st.sidebar.text_input("Member Name")
km_ridden = st.sidebar.number_input("Kilometers Ridden", min_value=0.1, step=0.1)
ride_date = st.sidebar.date_input("Date of Ride", date.today())

if st.sidebar.button("Add Ride"):
    if member_name:
        new_ride = pd.DataFrame({"Date": [ride_date], "Member": [member_name], "KM": [km_ridden]})
        st.session_state.rides = pd.concat([st.session_state.rides, new_ride], ignore_index=True)
        st.sidebar.success(f"Added {km_ridden}km for {member_name}!")
    else:
        st.sidebar.error("Please enter a name.")

# --- Main Dashboard ---
tab1, tab2 = st.tabs(["🏆 Leaderboard", "📜 Recent Rides"])

with tab1:
    st.subheader("Club Leaderboard")
    if not st.session_state.rides.empty:
        # Group by member and sum KM
        leaderboard = st.session_state.rides.groupby("Member")["KM"].sum().sort_values(ascending=False).reset_index()
        
        # Display as a bar chart and table
        st.bar_chart(leaderboard.set_index("Member"))
        st.dataframe(leaderboard, use_container_width=True)
    else:
        st.info("No rides logged yet. Use the sidebar to add the first one!")

with tab2:
    st.subheader("All Logged Activities")
    if not st.session_state.rides.empty:
        st.dataframe(st.session_state.rides.sort_values("Date", ascending=False), use_container_width=True)
        
        # Option to clear data
        if st.button("Clear All Data"):
            st.session_state.rides = pd.DataFrame(columns=["Date", "Member", "KM"])
            st.rerun()

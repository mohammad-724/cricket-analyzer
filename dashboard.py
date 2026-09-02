import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Define Database Path
DB_PATH = 'data/cricket_analysis.db'

# Helper function to run SQL queries and return DataFrames
def load_data(query):
    if not os.path.exists(DB_PATH):
        st.error("Database not found! Please run setup_db.py first.")
        return pd.DataFrame()
        
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 2. Set up the Streamlit Page
st.set_page_config(page_title="Cricket Performance Analyzer", layout="wide")
st.title("🏏 Cricket Performance Dashboard")
st.write("Welcome to the interactive cricket data analyzer.")

# 3. Sidebar for Navigation
st.sidebar.header("Navigation")
analysis_type = st.sidebar.radio(
    "Choose a view:",
    ["Top Toss Winners", "Raw Data Explorer"]
)

# 4. Render Layout based on Selection
if analysis_type == "Top Toss Winners":
    st.subheader("Top 5 Teams by Toss Wins")
    
    query = """
        SELECT toss_winner, COUNT(*) as toss_wins 
        FROM matches 
        GROUP BY toss_winner 
        ORDER BY toss_wins DESC 
        LIMIT 5;
    """
    
    df = load_data(query)
    
    if not df.empty:
        # Display data as a table alongside the chart using columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Data Table")
            st.dataframe(df, use_container_width=True)
            
        with col2:
            st.write("### Bar Chart")
            fig, ax = plt.subplots()
            ax.bar(df['toss_winner'], df['toss_wins'], color='#1f77b4')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)

elif analysis_type == "Raw Data Explorer":
    st.subheader("Explore Matches Table")
    
    query = "SELECT * FROM matches LIMIT 50;"
    df = load_data(query)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
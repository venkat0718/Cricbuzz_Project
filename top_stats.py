import streamlit as st
import requests
import pandas as pd
from urllib.parse import quote

# ---------------- Setup ----------------
st.set_page_config(page_title="🏏 Cricbuzz LiveStats", layout="wide")

# ✅ Direct API Key (no .env needed)
API_KEY = "08efb2192fmsh6c8b42b60b9495fp142a78jsn3a4095e1f60e"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

# ---------------- Global CSS ----------------
st.markdown("""
    <style>
    h1, h2, h3, h4, h5 { font-family: "Segoe UI", sans-serif !important; font-weight: 600 !important; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; padding-top: 20px; }
    div[data-testid="stDataFrame"] table { border: 1px solid #ddd; border-radius: 5px; }
    .stMarkdown p { font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

# ---------------- Helper Functions ----------------
def search_players(query):
    query_encoded = quote(query)
    url = f"{BASE_URL}/stats/v1/player/search?plrN={query_encoded}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
        return {}

def get_player_details(player_id):
    url = f"{BASE_URL}/stats/v1/player/{player_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
        return {}

def get_player_stats(player_id, stat_type="batting"):
    url = f"{BASE_URL}/stats/v1/player/{player_id}/{stat_type}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
        return {}

def parse_stats_table(stats_json, drop_columns=None):
    if not stats_json or "headers" not in stats_json or "values" not in stats_json:
        return pd.DataFrame()
    headers = stats_json["headers"]
    rows = [row["values"] for row in stats_json["values"]]
    df = pd.DataFrame(rows, columns=headers)
    if drop_columns:
        df = df.drop(columns=drop_columns, errors="ignore")
    return df

# ---------------- Sidebar ----------------
st.sidebar.title("ℹ About")
st.sidebar.markdown("""
Cricbuzz LiveStats Dashboard  
Built with Streamlit + Cricbuzz API, this app lets you explore:

✅ Real-time Player Profiles  
✅ ICC Rankings (Clean Card Design)  
✅ Batting & Bowling Stats  
""")

# ---------------- Main Page ----------------
st.title("🏏 Player Stats & ICC Rankings")
player_name = st.text_input("🔍 Enter player name (e.g. Virat Kohli, Joe Root):")

if player_name:
    results = search_players(player_name)

    if "player" in results and results["player"]:
        player_options = {p["name"]: p for p in results["player"]}
        selected_name = st.selectbox("Select a player:", list(player_options.keys()))
        selected_player = player_options[selected_name]

        tabs = st.tabs(["📌 Profile", "🏏 Batting Stats", "🎯 Bowling Stats"])

        # ---------------- Profile Tab ----------------
        with tabs[0]:
            st.subheader(f"{selected_player['name']} ({selected_player['teamName']})")
            details = get_player_details(selected_player["id"])
            st.write(f"📅 DOB: {selected_player.get('dob', 'N/A')}")
            st.write(f"🧢 Role: {details.get('role', 'N/A')}")
            st.write(f"🏏 Batting Style: {details.get('bat', 'N/A')}")
            st.write(f"⚾ Bowling Style: {details.get('bowl', 'N/A')}")
            st.write(f"🌍 Birth Place: {details.get('birthPlace', 'N/A')}")
            st.write(f"👤👤👤 Teams: {details.get('teams', 'N/A')}")

            # ---------------- ICC Rankings ----------------
            if "rankings" in details and details["rankings"]:
                st.subheader("🏆 ICC Rankings")
                rankings = details["rankings"]

                col1, col2, col3 = st.columns(3)

                def styled_metric(title, value):
                    try:
                        rank_int = int(value)
                    except:
                        rank_int = None
                    color = "#F5F5F5"
                    if rank_int is not None:
                        if rank_int <= 5:
                            color = "#A8E6CF"
                        elif rank_int <= 10:
                            color = "#FFD3B6"
                    return f"""
                    <div style='background-color:{color};padding:10px;
                                border-radius:10px;margin:5px;
                                text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1);'>
                        <h5 style='margin-bottom:5px;font-size:14px;'>{title}</h5>
                        <h3 style='margin:0;font-size:18px;color:#333;'>{value}</h3>
                    </div>
                    """

                with col1:
                    st.markdown("### 🏏 Batting")
                    for k, v in rankings.get("bat", {}).items():
                        if "DiffRank" not in k:
                            label = k.replace("odi", "ODI ").replace("test", "Test ").replace("t20", "T20 ").replace("Rank", " Rank").replace("Best", " Best")
                            st.markdown(styled_metric(label.strip(), v), unsafe_allow_html=True)

                with col2:
                    st.markdown("### ⚾ Bowling")
                    for k, v in rankings.get("bowl", {}).items():
                        if "DiffRank" not in k:
                            label = k.replace("odi", "ODI ").replace("test", "Test ").replace("t20", "T20 ").replace("Rank", " Rank").replace("Best", " Best")
                            st.markdown(styled_metric(label.strip(), v), unsafe_allow_html=True)

                with col3:
                    st.markdown("### 🏏⚾ All-Rounder")
                    for k, v in rankings.get("all", {}).items():
                        if "DiffRank" not in k:
                            label = k.replace("odi", "ODI ").replace("test", "Test ").replace("t20", "T20 ").replace("Rank", " Rank").replace("Best", " Best")
                            st.markdown(styled_metric(label.strip(), v), unsafe_allow_html=True)

        # ---------------- Batting Stats Tab ----------------
        with tabs[1]:
            st.subheader("🏏 Batting Stats")
            batting_stats = get_player_stats(selected_player["id"], "batting")
            df_bat = parse_stats_table(batting_stats, drop_columns=["400"])
            if not df_bat.empty:
                st.dataframe(df_bat, use_container_width=True)
            else:
                st.warning("No batting stats available.")

        # ---------------- Bowling Stats Tab ----------------
        with tabs[2]:
            st.subheader("☄ Bowling Stats")
            bowling_stats = get_player_stats(selected_player["id"], "bowling")
            df_bowl = parse_stats_table(bowling_stats, drop_columns=["10w"])
            if not df_bowl.empty:
                st.dataframe(df_bowl, use_container_width=True)
            else:
                st.warning("No bowling stats available.")
    else:
        st.warning("⚠ No players found. Try another name.")

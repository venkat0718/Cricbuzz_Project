import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 🔑 Direct API Key (no dotenv, no .env file needed)
CRICBUZZ_API_KEY = "08efb2192fmsh6c8b42b60b9495fp142a78jsn3a4095e1f60e"
CRICBUZZ_HOST = "cricbuzz-cricket.p.rapidapi.com"

class CricbuzzAPI:
    def _init(self):   # ✅ fixed typo (_init → _init_)
        self.headers = {
            "x-rapidapi-key": CRICBUZZ_API_KEY,
            "x-rapidapi-host": CRICBUZZ_HOST
        }
        self.base_url = "https://cricbuzz-cricket.p.rapidapi.com"

    def get_live_matches(self):
        """Fetch all live matches"""
        try:
            url = f"{self.base_url}/matches/v1/live"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"⚠ Error fetching live matches: {e}")
            return None

    def get_scorecard(self, match_id: str):
        """Fetch detailed scorecard by matchId"""
        try:
            url = f"{self.base_url}/mcenter/v1/{match_id}/scard"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"⚠ Error fetching scorecard: {e}")
            return None


def format_time(epoch_ms):
    """Convert epoch ms to human-readable format"""
    try:
        return datetime.fromtimestamp(int(epoch_ms) / 1000).strftime("%d %b %Y, %I:%M %p")
    except:
        return "N/A"


def show_innings_scorecard(api: CricbuzzAPI, match_id: str):
    """Display batting & bowling scorecard for selected match"""
    data = api.get_scorecard(match_id)
    if not data or "scorecard" not in data:
        st.warning("⚠ No scorecard data available.")
        return

    for i, innings in enumerate(data["scorecard"], start=1):
        st.subheader(f"📊 Inning {i} - {innings.get('batteamname', '')}")

        # 🏏 Batting Table
        batsmen_list = [
            {
                "Batsman": b.get("name", ""),
                "Runs": b.get("runs", 0),
                "Balls": b.get("balls", 0),
                "4s": b.get("fours", 0),
                "6s": b.get("sixes", 0),
                "SR": b.get("strkrate", 0),
                "Out": b.get("outdec", "")
            }
            for b in innings.get("batsman", [])
        ]
        batsmen_df = pd.DataFrame(batsmen_list)
        if not batsmen_df.empty:
            st.write("### 🏏 Batting")
            st.dataframe(batsmen_df, use_container_width=True)

        # 🎯 Bowling Table
        bowlers_list = [
            {
                "Bowler": bl.get("name", ""),
                "Overs": bl.get("overs", 0),
                "Maidens": bl.get("maidens", 0),
                "Runs": bl.get("runs", 0),
                "Wickets": bl.get("wickets", 0),
                "Economy": bl.get("economy", 0)
            }
            for bl in innings.get("bowler", [])
        ]
        bowlers_df = pd.DataFrame(bowlers_list)
        if not bowlers_df.empty:
            st.write("### ☄ Bowling")
            st.dataframe(bowlers_df, use_container_width=True)

        st.markdown("---")


def show_live_matches():
    """Main function to display live matches"""
    st.title("🏏 Cricbuzz LiveStats - Live Matches")
    st.caption("📡 Real-time cricket updates with stats & scorecards")

    api = CricbuzzAPI()
    data = api.get_live_matches()

    if not data:
        st.warning("⚠ No live matches available right now.")
        return

    series_options = {}
    for type_match in data.get("typeMatches", []):
        match_type = type_match.get("matchType", "Unknown")
        for series in type_match.get("seriesMatches", []):
            series_info = series.get("seriesAdWrapper", {})
            if "matches" in series_info:
                series_name = series_info.get("seriesName", "Unknown Series")
                key = f"{series_name} ({match_type})"
                series_options[key] = series_info["matches"]

    if not series_options:
        st.warning("⚠ No active series at the moment.")
        return

    selected_series = st.selectbox("🛑LIVE 🎞🎥 Select a Live Series", list(series_options.keys()))
    matches = series_options[selected_series]

    for match in matches:
        match_info = match.get("matchInfo", {})
        match_score = match.get("matchScore", {})

        team1 = match_info.get("team1", {}).get("teamName", "Team 1")
        team2 = match_info.get("team2", {}).get("teamName", "Team 2")
        match_id = match_info.get("matchId", "")

        st.subheader(f"🆚 {team1} vs {team2}")
        st.write(f"Match: {match_info.get('matchDesc', '')} ({match_info.get('matchFormat', '')})")
        st.write(f"Status: {match_info.get('status', '')}")
        st.write(f"State: {match_info.get('stateTitle', '')}")

        venue = match_info.get("venueInfo", {})
        st.write(f"Venue: {venue.get('ground', '')}, {venue.get('city', '')}")
        st.write(f"Start Time: {format_time(match_info.get('startDate'))}")
        st.write(f"End Time: {format_time(match_info.get('endDate'))}")

        # Show Team Scores
        if "team1Score" in match_score:
            t1 = match_info.get("team1", {}).get("teamSName", "Team 1")
            t1_inn = match_score.get("team1Score", {}).get("inngs1", {})
            st.success(f"{t1}: {t1_inn.get('runs', 0)}/{t1_inn.get('wickets', 0)} "
                       f"in {t1_inn.get('overs', 0)} overs")

        if "team2Score" in match_score:
            t2 = match_info.get("team2", {}).get("teamSName", "Team 2")
            t2_inn = match_score.get("team2Score", {}).get("inngs1", {})
            st.success(f"{t2}: {t2_inn.get('runs', 0)}/{t2_inn.get('wickets', 0)} "
                       f"in {t2_inn.get('overs', 0)} overs")

        # Button to show detailed scorecard
        if st.button(f"📑 View Scorecard - {team1} vs {team2}", key=f"btn_{match_id}"):
            show_innings_scorecard(api, match_id)

        st.markdown("---")


# ✅ About Section
st.sidebar.title("ℹ About")
st.sidebar.markdown("""
Cricbuzz LiveStats Dashboard  
Built with Streamlit + Cricbuzz API, this app lets you explore:
- ✅ Real-time Live Matches  
- ✅ Series & Match Info  
- ✅ Batting & Bowling Scorecards  
""")

# ✅ Fix main entry
if __name__ == "__main__":
    show_live_matches()

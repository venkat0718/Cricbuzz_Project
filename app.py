import streamlit as st
from datetime import datetime

st.set_page_config(page_title="🏏 Cricbuzz LiveStats", layout="wide")

# ---------- CUSTOM STYLING ----------
page_bg = """
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background-color: #f5f7fa;
    background-size: cover;
}

/* Gradient Title */
.main-title {
    font-size: 55px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #FF6F61, #FFD700, #1E90FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.4);
    margin-bottom: -5px;
}

.sub-title {
    font-size: 22px;
    text-align: center;
    color: #444;
    font-weight: 600;
    margin-bottom: 30px;
}

/* Metric Cards */
.metric-box {
    background: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    color: #222;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.1);
}
.metric-box:hover {
    transform: scale(1.05);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
}
.metric-icon img {
    width: 60px;
    margin-bottom: 8px;
}
.metric-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 5px;
}
.metric-value {
    font-size: 22px;
    font-weight: 700;
    color: #FF6F61;
}

/* Section Style */
.section {
    background: white;
    padding: 30px;
    border-radius: 18px;
    margin-top: 20px;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.1);
}

/* Footer */
.footer {
    text-align: center;
    font-size: 14px;
    color: #555;
    margin-top: 40px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🏏 Cricbuzz LiveStats</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-Time Cricket Insights & SQL-Based Analytics</div>', unsafe_allow_html=True)

# ---------- SUMMARY CARDS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="metric-box">
            <div class="metric-icon">
                <img src="https://img.icons8.com/color/96/combo-chart--v1.png"/>
            </div>
            <div class="metric-title">Total Matches</div>
            <div class="metric-value">1,500+</div>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="metric-box">
            <div class="metric-icon">
                <img src="https://img.icons8.com/color/96/cricket.png"/>
            </div>
            <div class="metric-title">Players</div>
            <div class="metric-value">1,200+</div>
        </div>
        """, unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="metric-box">
            <div class="metric-icon">
                <img src="https://img.icons8.com/color/96/globe-earth.png"/>
            </div>
            <div class="metric-title">Countries</div>
            <div class="metric-value">20+</div>
        </div>
        """, unsafe_allow_html=True
    )

# ---------- PROJECT OVERVIEW ----------
st.markdown(
    """
    <div class="section">
    <h3>🎯 Project Overview</h3>
    <p><b>Cricbuzz LiveStats</b> is your one-stop cricket analytics dashboard powered by Cricbuzz API & SQL.</p>
    <ul>
        <li>⚡ Real-time match data from <b>Cricbuzz API</b></li>
        <li>🧮 25 SQL-based analytical queries</li>
        <li>📊 Player & Team performance dashboards</li>
        <li>🛠 CRUD operations for database management</li>
    </ul>
    <p>This project is designed for <b>Sports Analysts, Broadcasters, Fantasy Platforms, and Learners</b>.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- USE CASES + IMAGE ----------
col1, col2 = st.columns([1,1])

with col1:
    st.markdown(
        """
        <div class="section">
        <h3>💼 Business Use Cases</h3>
        <ul>
            <li>📺 <b>Sports Media</b> – Live insights for commentary</li>
            <li>🎮 <b>Fantasy Cricket</b> – Stats for fantasy team building</li>
            <li>📈 <b>Analytics Firms</b> – Data-driven predictions</li>
            <li>🎓 <b>Education</b> – SQL & data science practice</li>
            <li>🎲 <b>Betting & Prediction</b> – Outcome analysis</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.image("https://pngimg.com/d/cricket_PNG95.png", width=350)

# ---------- NAVIGATION HINT ----------
st.info("👉 Use the **sidebar** to explore Live Matches, Player Stats, SQL Analytics, and CRUD Operations")

# ---------- FOOTER ----------
st.markdown(
    f"""
    <div class="footer">
    🚀 Created by <b>Venkat Subramaniam </b> • Powered by <b>Streamlit, SQL & Cricbuzz API</b><br>
    📅 Last Updated: {datetime.today().strftime('%B %d, %Y')}
    </div>
    """,
    unsafe_allow_html=True
)

# pages/crud_operations.py
import os
import pandas as pd
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# ===============================
# ENV + DB
# ===============================
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "rudra")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Rudra0718")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

# ===============================
# PAGE CONFIG + CSS
# ===============================
st.set_page_config(page_title="🏏 CRUD – Players", layout="wide")
st.title("🏏 CRUD Operations — Players")
st.caption("Manage player master data (add, update, delete, view).")

st.markdown("""
<style>
div[data-testid="stCaptionContainer"] p {font-size:18px !important;color:#333 !important;font-weight:600 !important;}
div.stButton > button, button[data-testid="stFormSubmitButton"]{
  background-color:#4a66d5 !important;color:#fff !important;font-weight:700 !important;border-radius:8px !important;
  height:42px !important; width:180px !important; border:none !important;
}
div.stButton > button:hover, button[data-testid="stFormSubmitButton"]:hover{background-color:#3b53b0 !important;}
</style>
""", unsafe_allow_html=True)

# ===============================
# HELPERS
# ===============================
@st.cache_data(ttl=60)
def fetch_teams():
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT team_id, team_name, country FROM teams ORDER BY team_name;")
        return cur.fetchall()

@st.cache_data(ttl=60)
def fetch_players_min():
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT player_id, full_name FROM players ORDER BY full_name;")
        return cur.fetchall()

def fetch_player(player_id: int):
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT player_id, full_name, nick_name, role, batting_style, bowling_style,
                   COALESCE(is_keeper,false) AS is_keeper,
                   COALESCE(is_captain,false) AS is_captain,
                   team_id
            FROM players
            WHERE player_id=%s
        """, (player_id,))
        return cur.fetchone()

def upsert_player(row: dict, mode: str):
    with get_conn() as conn, conn.cursor() as cur:
        if mode == "insert":
            cur.execute("""
                INSERT INTO players
                  (player_id, full_name, nick_name, role, batting_style, bowling_style,
                   is_keeper, is_captain, team_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (player_id) DO NOTHING
            """, (
                row["player_id"], row["full_name"], row["nick_name"], row["role"],
                row["batting_style"], row["bowling_style"], row["is_keeper"],
                row["is_captain"], row["team_id"]
            ))
        else:
            cur.execute("""
                UPDATE players
                SET full_name=%s, nick_name=%s, role=%s, batting_style=%s, bowling_style=%s,
                    is_keeper=%s, is_captain=%s, team_id=%s
                WHERE player_id=%s
            """, (
                row["full_name"], row["nick_name"], row["role"], row["batting_style"],
                row["bowling_style"], row["is_keeper"], row["is_captain"],
                row["team_id"], row["player_id"]
            ))
        conn.commit()

def delete_player(player_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM players WHERE player_id=%s", (player_id,))
        conn.commit()

def view_players_df():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
              p.player_id,
              p.full_name,
              COALESCE(p.nick_name,'—') AS nick_name,
              COALESCE(t.team_name,'—') AS team_name,
              COALESCE(t.country,'—') AS country,
              COALESCE(p.role,'—') AS role,
              COALESCE(p.batting_style,'—') AS batting_style,
              COALESCE(p.bowling_style,'—') AS bowling_style,
              COALESCE(p.is_keeper,false) AS is_keeper,
              COALESCE(p.is_captain,false) AS is_captain,
              p.team_id
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.player_id;
        """)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        return pd.DataFrame(rows, columns=cols)

# ===============================
# TABS
# ===============================
tab_add, tab_update, tab_delete, tab_view = st.tabs(["➕ Add","✏️ Update","🗑 Delete","📊 View"])

# ---------------- Add ----------------
with tab_add:
    with st.form("add_form", clear_on_submit=True):
        st.subheader("➕ Add New Player")
        c1, c2 = st.columns(2)
        with c1:
            player_id = st.number_input("Player ID (BIGINT, must be unique)", min_value=1, step=1)
            full_name = st.text_input("Full Name")
            nick_name = st.text_input("Nick Name", value="")
            role      = st.text_input("Role (Batsman/Bowler/All-rounder)", value="")
        with c2:
            batting_style = st.text_input("Batting Style", value="")
            bowling_style = st.text_input("Bowling Style", value="")
            is_keeper     = st.checkbox("Is Wicket-Keeper?", value=False)
            is_captain    = st.checkbox("Is Captain?", value=False)

        teams = fetch_teams()
        team_map = {"— (no team)": None}
        for t in teams:
            team_map[f"{t['team_name']} ({t['country']})"] = t["team_id"]
        team_label = st.selectbox("Team", list(team_map.keys()))
        team_id = team_map[team_label]

        add_btn = st.form_submit_button("✅ Add Player")
        if add_btn:
            if not player_id or not str(full_name).strip():
                st.error("Player ID and Full Name are required.")
            else:
                try:
                    upsert_player({
                        "player_id": int(player_id),
                        "full_name": full_name.strip(),
                        "nick_name": (nick_name or "").strip(),
                        "role": (role or "").strip(),
                        "batting_style": (batting_style or "").strip(),
                        "bowling_style": (bowling_style or "").strip(),
                        "is_keeper": bool(is_keeper),
                        "is_captain": bool(is_captain),
                        "team_id": team_id
                    }, mode="insert")
                    st.success(f"🎉 Added player '{full_name}' (ID {int(player_id)})")
                    fetch_players_min.clear()  # refresh cache
                except Exception as e:
                    st.error(f"Insert failed: {e}")

# ---------------- Update ----------------
with tab_update:
    st.subheader("✏️ Update Player")
    plist = fetch_players_min()
    if not plist:
        st.info("No players found to update.")
    else:
        display = [f"{p['full_name']} (ID {p['player_id']})" for p in plist]
        pick = st.selectbox("Select Player", display)
        sel_id = int(pick.rsplit("ID", 1)[1].strip(") ").strip())
        current = fetch_player(sel_id)

        if current:
            with st.form("upd_form", clear_on_submit=False):
                c1, c2 = st.columns(2)
                with c1:
                    full_name = st.text_input("Full Name", value=current["full_name"] or "")
                    nick_name = st.text_input("Nick Name", value=current["nick_name"] or "")
                    role      = st.text_input("Role", value=current["role"] or "")
                with c2:
                    batting_style = st.text_input("Batting Style", value=current["batting_style"] or "")
                    bowling_style = st.text_input("Bowling Style", value=current["bowling_style"] or "")
                    is_keeper     = st.checkbox("Is Wicket-Keeper?", value=current["is_keeper"])
                    is_captain    = st.checkbox("Is Captain?", value=current["is_captain"])

                teams = fetch_teams()
                team_map = {"— (no team)": None}
                for t in teams:
                    team_map[f"{t['team_name']} ({t['country']})"] = t["team_id"]

                # Preselect current team label
                rev_map = {v: k for k, v in team_map.items()}
                pre_label = rev_map.get(current["team_id"], "— (no team)")
                team_label = st.selectbox("Team", list(team_map.keys()), index=list(team_map.keys()).index(pre_label))
                team_id = team_map[team_label]

                upd_btn = st.form_submit_button("🔄 Update Player")
                if upd_btn:
                    try:
                        upsert_player({
                            "player_id": sel_id,
                            "full_name": full_name.strip(),
                            "nick_name": (nick_name or "").strip(),
                            "role": (role or "").strip(),
                            "batting_style": (batting_style or "").strip(),
                            "bowling_style": (bowling_style or "").strip(),
                            "is_keeper": bool(is_keeper),
                            "is_captain": bool(is_captain),
                            "team_id": team_id
                        }, mode="update")
                        st.success(f"✅ Updated player (ID {sel_id})")
                        fetch_players_min.clear()  # refresh cache
                    except Exception as e:
                        st.error(f"Update failed: {e}")

# ---------------- Delete ----------------
with tab_delete:
    st.subheader("🗑 Delete Player")
    plist = fetch_players_min()
    if not plist:
        st.info("No players to delete.")
    else:
        display = [f"{p['full_name']} (ID {p['player_id']})" for p in plist]
        pick = st.selectbox("Select Player to Delete", display)
        sel_id = int(pick.rsplit("ID", 1)[1].strip(") ").strip())
        confirm = st.checkbox("I understand this will permanently delete the player.", value=False)
        if st.button("🚨 Delete Player"):
            if not confirm:
                st.error("Please tick the confirmation box.")
            else:
                try:
                    delete_player(sel_id)
                    st.success(f"❌ Deleted player ID {sel_id}")
                    fetch_players_min.clear()  # refresh cache
                except Exception as e:
                    st.error(f"Delete failed: {e}")

# ---------------- View ----------------
with tab_view:
    st.subheader("📊 Player Records")
    try:
        df = view_players_df()
        if df.empty:
            st.warning("No records found.")
        else:
            st.dataframe(df, width="stretch", height=440)
    except Exception as e:
        st.error(f"Query failed: {e}")

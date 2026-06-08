import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="MLB Statzzz",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #111118;
    --bg-card: #16161f;
    --bg-hover: #1e1e2a;
    --accent-green: #00e676;
    --accent-yellow: #ffd600;
    --accent-red: #ff1744;
    --accent-orange: #ff6d00;
    --accent-blue: #2979ff;
    --text-primary: #f0f0f8;
    --text-secondary: #8888aa;
    --text-muted: #555570;
    --border: #222233;
    --border-bright: #333355;
}

* { font-family: 'Inter', sans-serif; }
.stApp { background: var(--bg-primary); color: var(--text-primary); }
.block-container { padding: 1rem 2rem; max-width: 100%; }

/* Hide streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Header */
.app-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 0 16px;
    border-bottom: 1px solid var(--border-bright);
    margin-bottom: 20px;
}
.app-logo {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #00e676, #2979ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-subtitle {
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500;
}

/* Game selector tabs */
.game-tabs {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}
.game-tab {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 14px;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-secondary);
    transition: all 0.2s;
}
.game-tab:hover, .game-tab.active {
    border-color: var(--accent-blue);
    color: var(--text-primary);
    background: var(--bg-hover);
}

/* Section headers */
.section-header {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--text-secondary);
    margin: 24px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Score badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-elite { background: rgba(0,230,118,0.15); color: #00e676; border: 1px solid rgba(0,230,118,0.3); }
.badge-high { background: rgba(41,121,255,0.15); color: #2979ff; border: 1px solid rgba(41,121,255,0.3); }
.badge-moderate { background: rgba(255,214,0,0.15); color: #ffd600; border: 1px solid rgba(255,214,0,0.3); }
.badge-avoid { background: rgba(255,23,68,0.15); color: #ff1744; border: 1px solid rgba(255,23,68,0.3); }

/* Data table */
.stat-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    margin-bottom: 32px;
}
.stat-table th {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 12px;
    text-align: center;
    border-bottom: 1px solid var(--border-bright);
    white-space: nowrap;
}
.stat-table th:first-child { text-align: left; }
.stat-table td {
    padding: 10px 12px;
    text-align: center;
    border-bottom: 1px solid var(--border);
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}
.stat-table td:first-child {
    text-align: left;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
}
.stat-table tr:hover td { background: var(--bg-hover); }

/* Color cells */
.cell-green { background: rgba(0,230,118,0.12); color: #00e676; font-weight: 700; }
.cell-yellow { background: rgba(255,214,0,0.12); color: #ffd600; font-weight: 700; }
.cell-red { background: rgba(255,23,68,0.12); color: #ff1744; font-weight: 700; }
.cell-orange { background: rgba(255,109,0,0.12); color: #ff6d00; font-weight: 700; }
.cell-neutral { color: var(--text-primary); }

/* Top pitchers card */
.pitcher-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
}

/* Input styling */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border-bright) !important;
    color: var(--text-primary) !important;
}
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border-color: var(--border-bright) !important;
    color: var(--text-primary) !important;
}

/* Metric cards */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 24px;
}
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}
.metric-label {
    font-size: 0.65rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
}

/* Nav tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary);
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--text-secondary);
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.82rem;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

/* Trend arrows */
.trend-up { color: #00e676; }
.trend-down { color: #ff1744; }
.trend-flat { color: #ffd600; }

/* Team badge */
.team-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 700;
    font-size: 0.85rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── SCORING FUNCTIONS ──────────────────────────────────────────────────────────
def calc_hr_score(barrel, fb, p_barrel, p_fb):
    try: return round((barrel*55)+(p_barrel*30)+(fb*10)+(p_fb*5), 1)
    except: return 0

def calc_hit_score(ld, p_ld):
    try: return round((ld*70)+(p_ld*30), 1)
    except: return 0

def calc_swstr_score(hitter_swstr, pitcher_swstr):
    try: return round((hitter_swstr*60)+(pitcher_swstr*40), 1)
    except: return 0

def calc_zone_fit(zone_contact, p_chase, h_chase):
    try: return round((zone_contact*5)+(p_chase*3)+(h_chase*2), 1)
    except: return 0

def calc_master(hr, hit, swstr, zone):
    try: return round((hr*0.35)+(hit*0.25)+(swstr*0.25)+(zone*0.15), 1)
    except: return 0

def hr_likelihood(score, barrel):
    if barrel < 5: return "❌ Avoid"
    if score >= 2000: return "🔥 Elite Spot"
    if score >= 1500: return "🟢 High Likelihood"
    if score >= 1000: return "🟡 Moderate"
    return "❌ Avoid"

def hit_likelihood(score):
    if score >= 2800: return "⚾ Base Hit Machine"
    if score >= 2000: return "🟢 Good Contact Spot"
    if score >= 1400: return "🟡 Moderate Contact"
    return "❌ Low Contact"

def play_fade(master, barrel):
    if barrel < 5: return "❌ Fade - Low Power"
    if master >= 1500: return "🔥 Strong Play"
    if master >= 1200: return "🟢 Lean Play"
    if master >= 900: return "🟡 Neutral"
    return "❌ Fade"

def color_val(val, thresholds, reverse=False):
    """Returns CSS class based on value thresholds [green, yellow, red]"""
    if val is None or val == "": return "cell-neutral"
    try:
        v = float(val)
        g, y, r = thresholds
        if not reverse:
            if v >= g: return "cell-green"
            if v >= y: return "cell-yellow"
            if v <= r: return "cell-red"
        else:
            if v <= g: return "cell-green"
            if v <= y: return "cell-yellow"
            if v >= r: return "cell-red"
        return "cell-neutral"
    except: return "cell-neutral"

def render_cell(val, css_class="cell-neutral", fmt=None):
    if val is None or val == "": return '<td class="cell-neutral">—</td>'
    try:
        display = f"{float(val):.1f}" if fmt == "f1" else \
                  f"{float(val):.3f}" if fmt == "f3" else \
                  f"{float(val):.0f}" if fmt == "f0" else str(val)
    except: display = str(val)
    return f'<td class="{css_class}">{display}</td>'

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "hitters" not in st.session_state:
    st.session_state.hitters = pd.DataFrame(columns=[
        "Name","Team","Barrel%","HardHit%","FB%","LD%","Chase%",
        "LA","AvgEV","ISO","SwStr%","ZoneContact%","xwOBA",
        "PulledBrl%","BrlBIP%","SweetSpot%","Last14AVG","Last14HH%"
    ])

if "pitchers" not in st.session_state:
    st.session_state.pitchers = pd.DataFrame(columns=[
        "Name","Team","BarrelAllowed%","FBAllowed%","HR9","LDAllowed%",
        "ChaseAllowed%","EVAllowed","LAAllowed","SwStr%Induced","Zone%",
        "Last14ERA","Last14HHAllowed%"
    ])

if "matchups" not in st.session_state:
    st.session_state.matchups = pd.DataFrame(columns=[
        "Hitter","Pitcher","Game"
    ])

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div>
        <div class="app-logo">⚾ MLB Statzzz</div>
        <div class="app-subtitle">Daily Matchup Intelligence Board</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN TABS ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Daily Board", "🔧 Manage Data", "⚾ Pitchers", "📥 Import"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DAILY BOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    if st.session_state.matchups.empty or st.session_state.hitters.empty:
        st.markdown("""
        <div style="text-align:center; padding: 80px 0; color: #555570;">
            <div style="font-size: 4rem; margin-bottom: 16px;">⚾</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #8888aa; margin-bottom: 8px;">No matchups loaded yet</div>
            <div style="font-size: 0.85rem;">Go to <strong>Manage Data</strong> to add hitters, pitchers, and matchups</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        hitters_df = st.session_state.hitters.set_index("Name")
        pitchers_df = st.session_state.pitchers.set_index("Name")
        matchups_df = st.session_state.matchups

        # Group by game
        games = matchups_df["Game"].unique() if "Game" in matchups_df.columns else ["All Games"]

        # Game selector
        selected_game = st.selectbox("🎮 Select Game", ["All Games"] + list(games), label_visibility="collapsed")

        filtered = matchups_df if selected_game == "All Games" else matchups_df[matchups_df["Game"] == selected_game]

        # Build results
        rows = []
        for _, m in filtered.iterrows():
            h_name = m["Hitter"]
            p_name = m["Pitcher"]
            game = m.get("Game", "")

            h = hitters_df.loc[h_name] if h_name in hitters_df.index else None
            p = pitchers_df.loc[p_name] if p_name in pitchers_df.index else None

            if h is None or p is None: continue

            def g(df, col, default=0):
                try: return float(df[col]) if col in df.index else default
                except: return default

            barrel = g(h,"Barrel%"); fb = g(h,"FB%"); ld = g(h,"LD%")
            chase = g(h,"Chase%"); la = g(h,"LA"); ev = g(h,"AvgEV")
            iso = g(h,"ISO"); swstr = g(h,"SwStr%"); zc = g(h,"ZoneContact%")
            xwoba = g(h,"xwOBA"); pulledbrl = g(h,"PulledBrl%")
            brlbip = g(h,"BrlBIP%"); sweet = g(h,"SweetSpot%")
            hh = g(h,"HardHit%")

            p_barrel = g(p,"BarrelAllowed%"); p_fb = g(p,"FBAllowed%")
            p_ld = g(p,"LDAllowed%"); p_chase = g(p,"ChaseAllowed%")
            p_swstr = g(p,"SwStr%Induced"); p_zone = g(p,"Zone%")
            p_ev = g(p,"EVAllowed"); p_la = g(p,"LAAllowed")

            hr_s = calc_hr_score(barrel, fb, p_barrel, p_fb)
            hit_s = calc_hit_score(ld, p_ld)
            swstr_s = calc_swstr_score(swstr, p_swstr)
            zone_s = calc_zone_fit(zc, p_chase, chase)
            master_s = calc_master(hr_s, hit_s, swstr_s, zone_s)
            hr_lik = hr_likelihood(hr_s, barrel)
            hit_lik = hit_likelihood(hit_s)
            pf = play_fade(master_s, barrel)

            rows.append({
                "Hitter": h_name, "Pitcher": p_name, "Game": game,
                "Team": h.get("Team","") if hasattr(h,"get") else h["Team"] if "Team" in h.index else "",
                "Matchup": round(master_s,1),
                "Zone Fit": round(zone_s,1),
                "HR Form": hr_lik,
                "kHR": round(hr_s,1),
                "ISO": iso, "xwOBA": xwoba,
                "SwStr%": swstr, "PulledBrl%": pulledbrl,
                "Brl/BIP%": brlbip, "SweetSpot%": sweet,
                "FB%": fb, "HH%": hh, "LA": la,
                "Hit Score": hit_s, "Hit Like": hit_lik,
                "Play/Fade": pf, "Master": master_s,
                "_barrel": barrel
            })

        if not rows:
            st.warning("No matching hitter/pitcher data found. Check your data entries.")
        else:
            results_df = pd.DataFrame(rows).sort_values("Matchup", ascending=False)

            # Summary metrics
            strong = len(results_df[results_df["Play/Fade"].str.contains("Strong", na=False)])
            lean = len(results_df[results_df["Play/Fade"].str.contains("Lean", na=False)])
            fade = len(results_df[results_df["Play/Fade"].str.contains("Fade", na=False)])
            avg_master = results_df["Master"].mean()

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="metric-value" style="color:#00e676">{strong}</div>
                    <div class="metric-label">🔥 Strong Plays</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#2979ff">{lean}</div>
                    <div class="metric-label">🟢 Lean Plays</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#ff1744">{fade}</div>
                    <div class="metric-label">❌ Fades</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#ffd600">{avg_master:.0f}</div>
                    <div class="metric-label">Avg Master Score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Group by game for display
            for game_name, group in results_df.groupby("Game") if "Game" in results_df.columns else [("All", results_df)]:
                st.markdown(f'<div class="section-header">⚾ {game_name}</div>', unsafe_allow_html=True)

                html = """<table class="stat-table"><thead><tr>
                    <th>Hitter</th><th>vs Pitcher</th>
                    <th>Matchup</th><th>Zone Fit</th><th>HR Form</th><th>kHR</th>
                    <th>ISO</th><th>xwOBA</th><th>SwStr%</th>
                    <th>PulledBrl%</th><th>Brl/BIP%</th><th>SweetSpot%</th>
                    <th>FB%</th><th>HH%</th><th>LA</th><th>Play/Fade</th>
                </tr></thead><tbody>"""

                for _, row in group.iterrows():
                    pf = row["Play/Fade"]
                    pf_class = "cell-green" if "Strong" in pf else \
                               "cell-green" if "Lean" in pf else \
                               "cell-yellow" if "Neutral" in pf else "cell-red"

                    hr_class = "cell-green" if "Elite" in row["HR Form"] or "High" in row["HR Form"] else \
                               "cell-yellow" if "Moderate" in row["HR Form"] else "cell-red"

                    html += f"""<tr>
                        <td style="font-weight:700">{row['Hitter']}</td>
                        <td style="color:#8888aa;font-size:0.75rem">{row['Pitcher']}</td>
                        {render_cell(row['Matchup'], color_val(row['Matchup'],[1500,1200,900]), "f0")}
                        {render_cell(row['Zone Fit'], color_val(row['Zone Fit'],[400,300,200]), "f0")}
                        <td class="{hr_class}" style="font-size:0.75rem">{row['HR Form']}</td>
                        {render_cell(row['kHR'], color_val(row['kHR'],[2000,1500,1000]), "f0")}
                        {render_cell(row['ISO'], color_val(row['ISO'],[0.2,0.15,0.1]), "f3")}
                        {render_cell(row['xwOBA'], color_val(row['xwOBA'],[0.38,0.32,0.28]), "f3")}
                        {render_cell(row['SwStr%'], color_val(row['SwStr%'],[25,18,12]), "f1")}
                        {render_cell(row['PulledBrl%'], color_val(row['PulledBrl%'],[15,10,5]), "f1")}
                        {render_cell(row['Brl/BIP%'], color_val(row['Brl/BIP%'],[12,8,4]), "f1")}
                        {render_cell(row['SweetSpot%'], color_val(row['SweetSpot%'],[35,28,20]), "f1")}
                        {render_cell(row['FB%'], color_val(row['FB%'],[35,28,20]), "f1")}
                        {render_cell(row['HH%'], color_val(row['HH%'],[50,40,30]), "f1")}
                        {render_cell(row['LA'], color_val(row['LA'],[12,8,4]), "f1")}
                        <td class="{pf_class}" style="font-size:0.75rem;font-weight:700">{pf}</td>
                    </tr>"""

                html += "</tbody></table>"
                st.markdown(html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MANAGE DATA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Add Hitter</div>', unsafe_allow_html=True)
        with st.form("add_hitter"):
            h_name = st.text_input("Hitter Name")
            h_team = st.text_input("Team")
            c1, c2, c3 = st.columns(3)
            with c1:
                h_barrel = st.number_input("Barrel%", 0.0, 100.0, 0.0, step=0.1)
                h_hh = st.number_input("Hard Hit%", 0.0, 100.0, 0.0, step=0.1)
                h_fb = st.number_input("FB%", 0.0, 100.0, 0.0, step=0.1)
                h_ld = st.number_input("LD%", 0.0, 100.0, 0.0, step=0.1)
                h_chase = st.number_input("Chase%", 0.0, 100.0, 0.0, step=0.1)
                h_la = st.number_input("Launch Angle", -30.0, 60.0, 0.0, step=0.1)
            with c2:
                h_ev = st.number_input("Avg EV", 0.0, 120.0, 0.0, step=0.1)
                h_iso = st.number_input("ISO", 0.0, 1.0, 0.0, step=0.001, format="%.3f")
                h_swstr = st.number_input("SwStr%", 0.0, 100.0, 0.0, step=0.1)
                h_zc = st.number_input("Zone Contact%", 0.0, 100.0, 0.0, step=0.1)
                h_xwoba = st.number_input("xwOBA", 0.0, 1.0, 0.0, step=0.001, format="%.3f")
            with c3:
                h_pbrl = st.number_input("PulledBrl%", 0.0, 100.0, 0.0, step=0.1)
                h_brlbip = st.number_input("Brl/BIP%", 0.0, 100.0, 0.0, step=0.1)
                h_sweet = st.number_input("SweetSpot%", 0.0, 100.0, 0.0, step=0.1)
                h_l14avg = st.number_input("Last 14 AVG", 0.0, 1.0, 0.0, step=0.001, format="%.3f")
                h_l14hh = st.number_input("Last 14 HH%", 0.0, 100.0, 0.0, step=0.1)

            if st.form_submit_button("➕ Add Hitter", use_container_width=True):
                if h_name:
                    new_row = {
                        "Name": h_name, "Team": h_team,
                        "Barrel%": h_barrel, "HardHit%": h_hh, "FB%": h_fb,
                        "LD%": h_ld, "Chase%": h_chase, "LA": h_la,
                        "AvgEV": h_ev, "ISO": h_iso, "SwStr%": h_swstr,
                        "ZoneContact%": h_zc, "xwOBA": h_xwoba,
                        "PulledBrl%": h_pbrl, "BrlBIP%": h_brlbip,
                        "SweetSpot%": h_sweet, "Last14AVG": h_l14avg,
                        "Last14HH%": h_l14hh
                    }
                    existing = st.session_state.hitters
                    existing = existing[existing["Name"] != h_name]
                    st.session_state.hitters = pd.concat([existing, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"✅ {h_name} added!")

    with col2:
        st.markdown('<div class="section-header">Add Matchup</div>', unsafe_allow_html=True)
        with st.form("add_matchup"):
            hitter_names = st.session_state.hitters["Name"].tolist() if not st.session_state.hitters.empty else []
            pitcher_names = st.session_state.pitchers["Name"].tolist() if not st.session_state.pitchers.empty else []

            m_hitter = st.selectbox("Hitter", [""] + hitter_names)
            m_pitcher = st.selectbox("Pitcher", [""] + pitcher_names)
            m_game = st.text_input("Game (e.g. BOS vs TB)")

            if st.form_submit_button("➕ Add Matchup", use_container_width=True):
                if m_hitter and m_pitcher:
                    new_match = {"Hitter": m_hitter, "Pitcher": m_pitcher, "Game": m_game}
                    existing = st.session_state.matchups
                    existing = existing[~((existing["Hitter"]==m_hitter)&(existing["Pitcher"]==m_pitcher))]
                    st.session_state.matchups = pd.concat([existing, pd.DataFrame([new_match])], ignore_index=True)
                    st.success(f"✅ {m_hitter} vs {m_pitcher} added!")

        st.markdown('<div class="section-header">Current Hitters</div>', unsafe_allow_html=True)
        if not st.session_state.hitters.empty:
            st.dataframe(
                st.session_state.hitters[["Name","Team","Barrel%","HardHit%","FB%","LD%","xwOBA"]],
                use_container_width=True, hide_index=True
            )
            if st.button("🗑️ Clear All Hitters"):
                st.session_state.hitters = pd.DataFrame(columns=st.session_state.hitters.columns)
                st.rerun()

        st.markdown('<div class="section-header">Current Matchups</div>', unsafe_allow_html=True)
        if not st.session_state.matchups.empty:
            st.dataframe(st.session_state.matchups, use_container_width=True, hide_index=True)
            if st.button("🗑️ Clear All Matchups"):
                st.session_state.matchups = pd.DataFrame(columns=st.session_state.matchups.columns)
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PITCHERS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="section-header">Add Pitcher</div>', unsafe_allow_html=True)
        with st.form("add_pitcher"):
            p_name = st.text_input("Pitcher Name")
            p_team = st.text_input("Team")
            p_barrel = st.number_input("Barrel Allowed%", 0.0, 100.0, 0.0, step=0.1)
            p_fb = st.number_input("FB Allowed%", 0.0, 100.0, 0.0, step=0.1)
            p_hr9 = st.number_input("HR/9", 0.0, 10.0, 0.0, step=0.01, format="%.2f")
            p_ld = st.number_input("LD Allowed%", 0.0, 100.0, 0.0, step=0.1)
            p_chase = st.number_input("Chase Allowed%", 0.0, 100.0, 0.0, step=0.1)
            p_ev = st.number_input("EV Allowed", 0.0, 120.0, 0.0, step=0.1)
            p_la = st.number_input("LA Allowed", -30.0, 60.0, 0.0, step=0.1)
            p_swstr = st.number_input("SwStr% Induced", 0.0, 100.0, 0.0, step=0.1)
            p_zone = st.number_input("Zone%", 0.0, 100.0, 0.0, step=0.1)
            p_era14 = st.number_input("Last 14 ERA", 0.0, 20.0, 0.0, step=0.01, format="%.2f")
            p_hh14 = st.number_input("Last 14 HH Allowed%", 0.0, 100.0, 0.0, step=0.1)

            if st.form_submit_button("➕ Add Pitcher", use_container_width=True):
                if p_name:
                    new_p = {
                        "Name": p_name, "Team": p_team,
                        "BarrelAllowed%": p_barrel, "FBAllowed%": p_fb,
                        "HR9": p_hr9, "LDAllowed%": p_ld,
                        "ChaseAllowed%": p_chase, "EVAllowed": p_ev,
                        "LAAllowed": p_la, "SwStr%Induced": p_swstr,
                        "Zone%": p_zone, "Last14ERA": p_era14,
                        "Last14HHAllowed%": p_hh14
                    }
                    existing = st.session_state.pitchers
                    existing = existing[existing["Name"] != p_name]
                    st.session_state.pitchers = pd.concat([existing, pd.DataFrame([new_p])], ignore_index=True)
                    st.success(f"✅ {p_name} added!")

    with col2:
        st.markdown('<div class="section-header">Top Slate Pitchers</div>', unsafe_allow_html=True)
        if not st.session_state.pitchers.empty:
            pdf = st.session_state.pitchers.copy()

            html = """<table class="stat-table"><thead><tr>
                <th>Pitcher</th><th>Team</th>
                <th>Barrel Allowed%</th><th>FB Allowed%</th><th>HR/9</th>
                <th>LD Allowed%</th><th>Chase Allowed%</th>
                <th>EV Allowed</th><th>LA Allowed</th>
                <th>SwStr% Induced</th><th>Zone%</th>
            </tr></thead><tbody>"""

            for _, row in pdf.iterrows():
                html += f"""<tr>
                    <td style="font-weight:700">{row['Name']}</td>
                    <td style="color:#8888aa">{row.get('Team','')}</td>
                    {render_cell(row['BarrelAllowed%'], color_val(row['BarrelAllowed%'],[12,8,5],reverse=True), "f1")}
                    {render_cell(row['FBAllowed%'], color_val(row['FBAllowed%'],[35,28,20]), "f1")}
                    {render_cell(row['HR9'], color_val(row['HR9'],[1.5,1.2,0.8],reverse=True), "f2")}
                    {render_cell(row['LDAllowed%'], color_val(row['LDAllowed%'],[25,20,15],reverse=True), "f1")}
                    {render_cell(row['ChaseAllowed%'], color_val(row['ChaseAllowed%'],[35,28,22]), "f1")}
                    {render_cell(row['EVAllowed'], color_val(row['EVAllowed'],[92,89,86],reverse=True), "f1")}
                    {render_cell(row['LAAllowed'], color_val(row['LAAllowed'],[18,12,8]), "f1")}
                    {render_cell(row['SwStr%Induced'], color_val(row['SwStr%Induced'],[28,20,14]), "f1")}
                    {render_cell(row['Zone%'], color_val(row['Zone%'],[50,45,40]), "f1")}
                </tr>"""

            html += "</tbody></table>"
            st.markdown(html, unsafe_allow_html=True)

            if st.button("🗑️ Clear All Pitchers"):
                st.session_state.pitchers = pd.DataFrame(columns=st.session_state.pitchers.columns)
                st.rerun()
        else:
            st.info("No pitchers added yet. Use the form to add pitchers.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — IMPORT (CSV)
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Import from CSV</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#8888aa; font-size:0.85rem; margin-bottom:16px;">
    Upload a CSV file to bulk import hitters, pitchers, or matchups.<br>
    Make sure your CSV headers match the column names exactly.
    </div>
    """, unsafe_allow_html=True)

    import_type = st.radio("Import type", ["Hitters", "Pitchers", "Matchups"], horizontal=True)
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head(), use_container_width=True)
            if st.button("✅ Confirm Import"):
                if import_type == "Hitters":
                    st.session_state.hitters = pd.concat([st.session_state.hitters, df], ignore_index=True).drop_duplicates("Name")
                elif import_type == "Pitchers":
                    st.session_state.pitchers = pd.concat([st.session_state.pitchers, df], ignore_index=True).drop_duplicates("Name")
                else:
                    st.session_state.matchups = pd.concat([st.session_state.matchups, df], ignore_index=True)
                st.success(f"✅ {len(df)} {import_type} imported!")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

    st.markdown('<div class="section-header">Export Data</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if not st.session_state.hitters.empty:
            st.download_button("📥 Export Hitters", st.session_state.hitters.to_csv(index=False), "hitters.csv", "text/csv")
    with col2:
        if not st.session_state.pitchers.empty:
            st.download_button("📥 Export Pitchers", st.session_state.pitchers.to_csv(index=False), "pitchers.csv", "text/csv")
    with col3:
        if not st.session_state.matchups.empty:
            st.download_button("📥 Export Matchups", st.session_state.matchups.to_csv(index=False), "matchups.csv", "text/csv")

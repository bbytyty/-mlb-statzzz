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
    --accent-blue: #2979ff;
    --text-primary: #f0f0f8;
    --text-secondary: #8888aa;
    --border: #222233;
    --border-bright: #333355;
}
* { font-family: 'Inter', sans-serif; }
.stApp { background: var(--bg-primary); color: var(--text-primary); }
.block-container { padding: 1rem 2rem; max-width: 100%; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
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
.rank-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--border);
    color: var(--text-secondary);
    font-size: 0.65rem;
    font-weight: 700;
    margin-right: 8px;
}
.rank-1 { background: rgba(255,214,0,0.2); color: #ffd600; }
.rank-2 { background: rgba(192,192,192,0.2); color: #c0c0c0; }
.rank-3 { background: rgba(205,127,50,0.2); color: #cd7f32; }
.cell-green { background: rgba(0,230,118,0.12); color: #00e676; font-weight: 700; }
.cell-yellow { background: rgba(255,214,0,0.12); color: #ffd600; font-weight: 700; }
.cell-red { background: rgba(255,23,68,0.12); color: #ff1744; font-weight: 700; }
.cell-orange { background: rgba(255,109,0,0.12); color: #ff6d00; font-weight: 700; }
.cell-neutral { color: var(--text-primary); }
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
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── GITHUB DATA URLS ───────────────────────────────────────────────────────────
GITHUB_RAW = "https://raw.githubusercontent.com/bbytyty/-mlb-statzzz/main"
HITTERS_URL = f"{GITHUB_RAW}/hitters_today.csv"
PITCHERS_URL = f"{GITHUB_RAW}/pitchers_today.csv"
MATCHUPS_URL = f"{GITHUB_RAW}/matchups_today.csv"

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_github_data():
    try:
        hitters = pd.read_csv(HITTERS_URL)
        pitchers = pd.read_csv(PITCHERS_URL)
        matchups = pd.read_csv(MATCHUPS_URL)
        return hitters, pitchers, matchups
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

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

def calc_khr(barrel, pulled_brl, hh, fb, iso):
    """KHR = Pure power profile score independent of matchup"""
    try: return round((barrel*40)+(pulled_brl*25)+(hh*15)+(fb*10)+(iso*1000), 1)
    except: return 0

def khr_rating(score):
    if score >= 2500: return "🔥 Elite KHR"
    if score >= 2000: return "🟢 High KHR"
    if score >= 1500: return "🟡 Moderate KHR"
    return "❌ Low KHR"

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

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
hitters_df, pitchers_df, matchups_df = load_github_data()
h_count = len(hitters_df)
p_count = len(pitchers_df)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="app-header">
    <div>
        <div class="app-logo">⚾ MLB Statzzz</div>
        <div class="app-subtitle">Daily Matchup Intelligence Board</div>
    </div>
    <div style="margin-left:auto; display:flex; gap:16px; align-items:center;">
        <div style="text-align:center;">
            <div style="font-size:1.4rem;font-weight:800;color:#00e676">{h_count}</div>
            <div style="font-size:0.6rem;color:#8888aa;text-transform:uppercase;letter-spacing:1px">Hitters</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:1.4rem;font-weight:800;color:#2979ff">{p_count}</div>
            <div style="font-size:0.6rem;color:#8888aa;text-transform:uppercase;letter-spacing:1px">Pitchers</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN TABS ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Daily Board", "💣 KHR Rankings", "⚾ Pitchers"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DAILY BOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    if hitters_df.empty or matchups_df.empty:
        st.markdown("""
        <div style="text-align:center; padding: 80px 0; color: #555570;">
            <div style="font-size: 4rem; margin-bottom: 16px;">⚾</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #8888aa; margin-bottom: 8px;">Loading data from GitHub...</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        h_idx = hitters_df.set_index("Name")
        p_idx = pitchers_df.set_index("Name")
        games = matchups_df["Game"].unique() if "Game" in matchups_df.columns else ["All Games"]
        selected_game = st.selectbox("🎮 Filter by Game", ["All Games"] + list(games), label_visibility="collapsed")
        filtered = matchups_df if selected_game == "All Games" else matchups_df[matchups_df["Game"] == selected_game]

        rows = []
        for _, m in filtered.iterrows():
            h_name = m["Hitter"]
            p_name = m["Pitcher"]
            game = m.get("Game", "")
            h = h_idx.loc[h_name] if h_name in h_idx.index else None
            p = p_idx.loc[p_name] if p_name in p_idx.index else None
            if h is None or p is None: continue

            def g(df, col, default=0):
                try: return float(df[col]) if col in df.index else default
                except: return default

            barrel=g(h,"Barrel%"); fb=g(h,"FB%"); ld=g(h,"LD%")
            chase=g(h,"Chase%"); la=g(h,"LA"); ev=g(h,"AvgEV")
            iso=g(h,"ISO"); swstr=g(h,"SwStr%"); zc=g(h,"ZoneContact%")
            xwoba=g(h,"xwOBA"); pulledbrl=g(h,"PulledBrl%")
            brlbip=g(h,"BrlBIP%"); sweet=g(h,"SweetSpot%")
            hh=g(h,"HardHit%")

            p_barrel=g(p,"BarrelAllowed%"); p_fb=g(p,"FBAllowed%")
            p_ld=g(p,"LDAllowed%"); p_chase=g(p,"ChaseAllowed%")
            p_swstr=g(p,"SwStr%Induced"); p_zone=g(p,"Zone%")
            p_csw=g(p,"CSW%")

            hr_s=calc_hr_score(barrel,fb,p_barrel,p_fb)
            hit_s=calc_hit_score(ld,p_ld)
            swstr_s=calc_swstr_score(swstr,p_swstr)
            zone_s=calc_zone_fit(zc,p_chase,chase)
            master_s=calc_master(hr_s,hit_s,swstr_s,zone_s)
            khr_s=calc_khr(barrel,pulledbrl,hh,fb,iso)
            khr_rat=khr_rating(khr_s)
            hr_lik=hr_likelihood(hr_s,barrel)
            hit_lik=hit_likelihood(hit_s)
            pf=play_fade(master_s,barrel)

            rows.append({
                "Hitter":h_name,"Pitcher":p_name,"Game":game,
                "Matchup":round(master_s,1),"Zone Fit":round(zone_s,1),
                "HR Form":hr_lik,"kHR":round(hr_s,1),
                "KHR Score":round(khr_s,1),"KHR Rating":khr_rat,
                "ISO":iso,"xwOBA":xwoba,"SwStr%":swstr,
                "PulledBrl%":pulledbrl,"Brl/BIP%":brlbip,
                "SweetSpot%":sweet,"FB%":fb,"HH%":hh,"LA":la,
                "CSW%":p_csw,"Hit Like":hit_lik,
                "Play/Fade":pf,"Master":master_s,"_barrel":barrel
            })

        if not rows:
            st.warning("No matching data found!")
        else:
            results_df = pd.DataFrame(rows).sort_values("Matchup", ascending=False)
            strong=len(results_df[results_df["Play/Fade"].str.contains("Strong",na=False)])
            lean=len(results_df[results_df["Play/Fade"].str.contains("Lean",na=False)])
            fade=len(results_df[results_df["Play/Fade"].str.contains("Fade",na=False)])
            avg_master=results_df["Master"].mean()

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

            groups = results_df.groupby("Game") if "Game" in results_df.columns else [("All",results_df)]
            for game_name, group in groups:
                st.markdown(f'<div class="section-header">⚾ {game_name}</div>', unsafe_allow_html=True)
                html = """<table class="stat-table"><thead><tr>
                    <th>#</th><th>Hitter</th><th>vs Pitcher</th>
                    <th>Matchup</th><th>KHR Score</th><th>KHR Rating</th>
                    <th>Zone Fit</th><th>HR Form</th><th>kHR</th>
                    <th>ISO</th><th>xwOBA</th><th>SwStr%</th>
                    <th>PulledBrl%</th><th>Brl/BIP%</th><th>SweetSpot%</th>
                    <th>FB%</th><th>HH%</th><th>LA</th><th>CSW%</th><th>Play/Fade</th>
                </tr></thead><tbody>"""

                for rank,(_, row) in enumerate(group.iterrows(),1):
                    pf=row["Play/Fade"]
                    pf_class="cell-green" if "Strong" in pf or "Lean" in pf else \
                              "cell-yellow" if "Neutral" in pf else "cell-red"
                    hr_class="cell-green" if "Elite" in row["HR Form"] or "High" in row["HR Form"] else \
                              "cell-yellow" if "Moderate" in row["HR Form"] else "cell-red"
                    khr_class="cell-green" if "Elite" in row["KHR Rating"] or "High" in row["KHR Rating"] else \
                               "cell-yellow" if "Moderate" in row["KHR Rating"] else "cell-red"
                    rank_class=f"rank-{rank}" if rank<=3 else ""

                    html+=f"""<tr>
                        <td><span class="rank-num {rank_class}">{rank}</span></td>
                        <td style="font-weight:700">{row['Hitter']}</td>
                        <td style="color:#8888aa;font-size:0.75rem">{row['Pitcher']}</td>
                        {render_cell(row['Matchup'],color_val(row['Matchup'],[1500,1200,900]),"f0")}
                        {render_cell(row['KHR Score'],color_val(row['KHR Score'],[2500,2000,1500]),"f0")}
                        <td class="{khr_class}" style="font-size:0.75rem">{row['KHR Rating']}</td>
                        {render_cell(row['Zone Fit'],color_val(row['Zone Fit'],[400,300,200]),"f0")}
                        <td class="{hr_class}" style="font-size:0.75rem">{row['HR Form']}</td>
                        {render_cell(row['kHR'],color_val(row['kHR'],[2000,1500,1000]),"f0")}
                        {render_cell(row['ISO'],color_val(row['ISO'],[0.2,0.15,0.1]),"f3")}
                        {render_cell(row['xwOBA'],color_val(row['xwOBA'],[0.38,0.32,0.28]),"f3")}
                        {render_cell(row['SwStr%'],color_val(row['SwStr%'],[25,18,12]),"f1")}
                        {render_cell(row['PulledBrl%'],color_val(row['PulledBrl%'],[15,10,5]),"f1")}
                        {render_cell(row['Brl/BIP%'],color_val(row['Brl/BIP%'],[12,8,4]),"f1")}
                        {render_cell(row['SweetSpot%'],color_val(row['SweetSpot%'],[35,28,20]),"f1")}
                        {render_cell(row['FB%'],color_val(row['FB%'],[35,28,20]),"f1")}
                        {render_cell(row['HH%'],color_val(row['HH%'],[50,40,30]),"f1")}
                        {render_cell(row['LA'],color_val(row['LA'],[12,8,4]),"f1")}
                        {render_cell(row['CSW%'],color_val(row['CSW%'],[30,25,20]),"f1")}
                        <td class="{pf_class}" style="font-size:0.75rem;font-weight:700">{pf}</td>
                    </tr>"""

                html+="</tbody></table>"
                st.markdown(html,unsafe_allow_html=True)

    if st.button("🔄 Refresh Data from GitHub"):
        st.cache_data.clear()
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — KHR RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">💣 KHR Power Rankings — Pure HR Profile</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#8888aa;font-size:0.85rem;margin-bottom:16px;">
    KHR ranks hitters by pure power profile regardless of matchup.<br>
    Formula: <strong>(Barrel% × 40) + (PulledBrl% × 25) + (HardHit% × 15) + (FB% × 10) + (ISO × 1000)</strong>
    </div>
    """, unsafe_allow_html=True)

    if hitters_df.empty:
        st.info("No hitter data loaded.")
    else:
        khr_rows = []
        for _, h in hitters_df.iterrows():
            def gh(col, default=0):
                try: return float(h[col]) if col in h.index else default
                except: return default

            barrel=gh("Barrel%"); pulledbrl=gh("PulledBrl%")
            hh=gh("HardHit%"); fb=gh("FB%"); iso=gh("ISO")
            xwoba=gh("xwOBA"); ev=gh("AvgEV"); la=gh("LA")
            sweet=gh("SweetSpot%"); brlbip=gh("BrlBIP%")

            khr_s=calc_khr(barrel,pulledbrl,hh,fb,iso)
            khr_rat=khr_rating(khr_s)

            khr_rows.append({
                "Hitter":h["Name"],"Team":h.get("Team",""),
                "KHR Score":round(khr_s,1),"KHR Rating":khr_rat,
                "Barrel%":barrel,"PulledBrl%":pulledbrl,
                "HardHit%":hh,"FB%":fb,"ISO":iso,
                "xwOBA":xwoba,"EV":ev,"LA":la,
                "SweetSpot%":sweet,"Brl/BIP%":brlbip
            })

        khr_df = pd.DataFrame(khr_rows).sort_values("KHR Score", ascending=False)

        html = """<table class="stat-table"><thead><tr>
            <th>#</th><th>Hitter</th><th>Team</th>
            <th>KHR Score</th><th>KHR Rating</th>
            <th>Barrel%</th><th>PulledBrl%</th>
            <th>HardHit%</th><th>FB%</th><th>ISO</th>
            <th>xwOBA</th><th>EV</th><th>LA</th>
            <th>SweetSpot%</th><th>Brl/BIP%</th>
        </tr></thead><tbody>"""

        for rank,(_, row) in enumerate(khr_df.iterrows(),1):
            khr_class="cell-green" if "Elite" in row["KHR Rating"] or "High" in row["KHR Rating"] else \
                       "cell-yellow" if "Moderate" in row["KHR Rating"] else "cell-red"
            rank_class=f"rank-{rank}" if rank<=3 else ""

            html+=f"""<tr>
                <td><span class="rank-num {rank_class}">{rank}</span></td>
                <td style="font-weight:700">{row['Hitter']}</td>
                <td style="color:#8888aa;font-size:0.75rem">{row['Team']}</td>
                {render_cell(row['KHR Score'],color_val(row['KHR Score'],[2500,2000,1500]),"f0")}
                <td class="{khr_class}" style="font-size:0.75rem;font-weight:700">{row['KHR Rating']}</td>
                {render_cell(row['Barrel%'],color_val(row['Barrel%'],[15,10,5]),"f1")}
                {render_cell(row['PulledBrl%'],color_val(row['PulledBrl%'],[15,10,5]),"f1")}
                {render_cell(row['HardHit%'],color_val(row['HardHit%'],[50,40,30]),"f1")}
                {render_cell(row['FB%'],color_val(row['FB%'],[35,28,20]),"f1")}
                {render_cell(row['ISO'],color_val(row['ISO'],[0.2,0.15,0.1]),"f3")}
                {render_cell(row['xwOBA'],color_val(row['xwOBA'],[0.38,0.32,0.28]),"f3")}
                {render_cell(row['EV'],color_val(row['EV'],[92,89,86]),"f1")}
                {render_cell(row['LA'],color_val(row['LA'],[12,8,4]),"f1")}
                {render_cell(row['SweetSpot%'],color_val(row['SweetSpot%'],[35,28,20]),"f1")}
                {render_cell(row['Brl/BIP%'],color_val(row['Brl/BIP%'],[12,8,4]),"f1")}
            </tr>"""

        html+="</tbody></table>"
        st.markdown(html,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PITCHERS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Top Slate Pitchers</div>', unsafe_allow_html=True)
    if pitchers_df.empty:
        st.info("No pitcher data loaded.")
    else:
        html="""<table class="stat-table"><thead><tr>
            <th>Pitcher</th><th>Team</th>
            <th>Barrel Allowed%</th><th>FB Allowed%</th><th>HR/9</th>
            <th>LD Allowed%</th><th>Chase Allowed%</th>
            <th>EV Allowed</th><th>LA Allowed</th>
            <th>SwStr% Induced</th><th>Zone%</th><th>CSW%</th>
        </tr></thead><tbody>"""

        for _,row in pitchers_df.iterrows():
            html+=f"""<tr>
                <td style="font-weight:700">{row['Name']}</td>
                <td style="color:#8888aa">{row.get('Team','')}</td>
                {render_cell(row['BarrelAllowed%'],color_val(row['BarrelAllowed%'],[12,8,5],reverse=True),"f1")}
                {render_cell(row['FBAllowed%'],color_val(row['FBAllowed%'],[35,28,20]),"f1")}
                {render_cell(row['HR9'],color_val(row['HR9'],[1.5,1.2,0.8],reverse=True),"f2")}
                {render_cell(row['LDAllowed%'],color_val(row['LDAllowed%'],[25,20,15],reverse=True),"f1")}
                {render_cell(row['ChaseAllowed%'],color_val(row['ChaseAllowed%'],[35,28,22]),"f1")}
                {render_cell(row['EVAllowed'],color_val(row['EVAllowed'],[92,89,86],reverse=True),"f1")}
                {render_cell(row['LAAllowed'],color_val(row['LAAllowed'],[18,12,8]),"f1")}
                {render_cell(row['SwStr%Induced'],color_val(row['SwStr%Induced'],[28,20,14]),"f1")}
                {render_cell(row['Zone%'],color_val(row['Zone%'],[50,45,40]),"f1")}
                {render_cell(row['CSW%'],color_val(row['CSW%'],[30,25,20]),"f1")}
            </tr>"""

        html+="</tbody></table>"
        st.markdown(html,unsafe_allow_html=True)

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

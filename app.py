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
    grid-template-columns: repeat(5, 1fr);
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

GITHUB_RAW = "https://raw.githubusercontent.com/bbytyty/-mlb-statzzz/main"
HITTERS_URL = f"{GITHUB_RAW}/hitters_today.csv"
PITCHERS_URL = f"{GITHUB_RAW}/pitchers_today.csv"
MATCHUPS_URL = f"{GITHUB_RAW}/matchups_today.csv"

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
def platoon_bonus(bats, throws):
    """Platoon advantage multiplier"""
    try:
        b = str(bats).strip().upper()
        t = str(throws).strip().upper()
        if b == "S": return 1.05
        if b == "R" and t == "L": return 1.10
        if b == "L" and t == "R": return 1.10
        return 1.0
    except: return 1.0

def calc_hr_score(barrel, fb, p_barrel, p_fb, bats, throws):
    try:
        base = (barrel*55)+(p_barrel*30)+(fb*10)+(p_fb*5)
        return round(base * platoon_bonus(bats, throws), 1)
    except: return 0

def calc_hit_score(ld, p_ld, sweet, xwoba, swstr):
    """Improved hit score using SweetSpot% and xwOBA"""
    try:
        return round((ld*35)+(p_ld*20)+(sweet*25)+(xwoba*200)-(swstr*8), 1)
    except: return 0

def calc_doubles_score(ld, oppo, sweet, p_ld, fb):
    """Doubles score based on LD%, Oppo%, SweetSpot%"""
    try:
        return round((ld*35)+(oppo*25)+(sweet*20)+(p_ld*15)+(fb*5), 1)
    except: return 0

def calc_swstr_score(hitter_swstr, pitcher_swstr):
    try: return round((hitter_swstr*60)+(pitcher_swstr*40), 1)
    except: return 0

def calc_zone_fit(zone_contact, p_chase, h_chase):
    try: return round((zone_contact*5)+(p_chase*3)+(h_chase*2), 1)
    except: return 0

def auto_form(last14_avg, last14_hh, xwoba, hh, barrel):
    """Auto calculate form from last 14 days vs season stats"""
    try:
        score = 5  # start neutral
        # Last 14 AVG vs season xBA
        if last14_avg > 0:
            if last14_avg >= 0.320: score += 2
            elif last14_avg >= 0.280: score += 1
            elif last14_avg <= 0.200: score -= 2
            elif last14_avg <= 0.240: score -= 1
        # Last 14 HH% vs season HH%
        if last14_hh > 0 and hh > 0:
            diff = last14_hh - hh
            if diff >= 10: score += 2
            elif diff >= 5: score += 1
            elif diff <= -10: score -= 2
            elif diff <= -5: score -= 1
        return max(1, min(10, score))
    except: return 5

def calc_form_score(form):
    try: return round(float(form) * 100, 1)
    except: return 500

def form_arrow(form):
    try:
        f = float(form)
        if f >= 8: return "🔥"
        if f >= 7: return "↑"
        if f >= 5: return "→"
        if f >= 3: return "↓"
        return "❄️"
    except: return "→"

def calc_master(hr, hit, swstr, zone, p_csw, form):
    try:
        form_s = calc_form_score(form)
        base = (hr*0.30)+(hit*0.20)+(swstr*0.20)+(zone*0.15)+(form_s*0.15)
        if p_csw >= 32: penalty = 0.85
        elif p_csw >= 30: penalty = 0.90
        elif p_csw >= 28: penalty = 0.95
        else: penalty = 1.0
        return round(base * penalty, 1)
    except: return 0

def calc_khr(barrel, pulled_brl, hh, fb, iso):
    try: return round((barrel*40)+(pulled_brl*25)+(hh*15)+(fb*10)+(iso*1000), 1)
    except: return 0

def khr_rating(score):
    if score >= 2500: return "🔥 Elite KHR"
    if score >= 2000: return "🟢 High KHR"
    if score >= 1500: return "🟡 Moderate KHR"
    return "❌ Low KHR"

def hr_likelihood(score, barrel, ev=88, form=5):
    if barrel < 3 and ev < 93 and form < 7: return "❌ Avoid"
    if score >= 2000: return "🔥 Elite Spot"
    if score >= 1500: return "🟢 High Likelihood"
    if score >= 1000: return "🟡 Moderate"
    return "❌ Avoid"

def hit_likelihood(score):
    if score >= 2200: return "🔥 Hit Lock"
    if score >= 1800: return "🟢 Good Contact"
    if score >= 1400: return "🟡 Moderate Contact"
    return "❌ Low Contact"

def doubles_likelihood(score):
    if score >= 2500: return "🔥 Double Lock"
    if score >= 2100: return "🟢 Double Play"
    if score >= 1700: return "🟡 Double Lean"
    return "❌ Low"

def hit_play_fade(hit_score, form):
    try: f = float(form)
    except: f = 5
    if hit_score >= 2200 and f >= 6: return "🔥 Hit Lock"
    if hit_score >= 1800 and f >= 5: return "🟢 Hit Play"
    if hit_score >= 1400: return "🟡 Hit Lean"
    return "❌ Skip Hit"

def doubles_play_fade(doubles_score, oppo, ld, form):
    """Strict doubles prediction — needs high Oppo% AND high LD%"""
    try: f = float(form)
    except: f = 5
    # Must have BOTH high oppo% and high ld% to qualify
    if oppo < 25 or ld < 22: return "❌ Skip"
    if doubles_score >= 2500 and f >= 7: return "🔥 Double Lock"
    if doubles_score >= 2200 and f >= 6: return "🟢 Double Play"
    if doubles_score >= 1900 and f >= 5: return "🟡 Double Lean"
    return "❌ Skip"

def hr_play_fade(master, barrel, p_csw, form, bats, throws, ev=88, bbe=100):
    try: f = float(form)
    except: f = 5
    platoon = platoon_bonus(bats, throws)
    # Small sample warning — under 20 BBE
    if bbe < 20: return "⚠️ Small Sample"
    if barrel < 3 and ev < 93 and form < 7: return "❌ Fade HR"
    if p_csw >= 32 and f < 6: return "⚠️ K Risk"
    if master >= 1500 and f >= 6 and platoon > 1.0: return "🔥 HR Lock"
    if master >= 1500 and f >= 6: return "🔥 HR Play"
    if master >= 1500: return "🟡 HR Lean"
    if master >= 1200: return "🟡 HR Lean"
    return "❌ Fade HR"

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

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Daily Board", "🔥 HR Props", "🎯 Hit Props", "📐 Doubles", "💣 KHR Rankings"])

def build_rows(filtered, h_idx, p_idx):
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
        def gs(df, col, default=""):
            try: return str(df[col]) if col in df.index else default
            except: return default

        barrel=g(h,"Barrel%"); fb=g(h,"FB%"); ld=g(h,"LD%")
        chase=g(h,"Chase%"); la=g(h,"LA"); ev=g(h,"AvgEV")
        iso=g(h,"ISO"); swstr=g(h,"SwStr%"); zc=g(h,"ZoneContact%")
        xwoba=g(h,"xwOBA"); pulledbrl=g(h,"PulledBrl%")
        brlbip=g(h,"BrlBIP%"); sweet=g(h,"SweetSpot%")
        hh=g(h,"HardHit%"); oppo=g(h,"Oppo%")
        last14_avg=g(h,"Last14AVG",0)
        last14_hh=g(h,"Last14HH%",0)
        manual_form=g(h,"Form",0)
        # Use manual form if set, otherwise auto-calculate
        if manual_form > 0:
            form = manual_form
        else:
            form = auto_form(last14_avg, last14_hh, xwoba, hh, barrel)
        bats=gs(h,"Bats","R")

        p_barrel=g(p,"BarrelAllowed%"); p_fb=g(p,"FBAllowed%")
        p_ld=g(p,"LDAllowed%"); p_chase=g(p,"ChaseAllowed%")
        p_swstr=g(p,"SwStr%Induced"); p_zone=g(p,"Zone%")
        p_csw=g(p,"CSW%")
        throws=gs(p,"Throws","R")

        platoon = platoon_bonus(bats, throws)
        platoon_str = "✅ Platoon" if platoon > 1.0 else "—"

        hr_s=calc_hr_score(barrel,fb,p_barrel,p_fb,bats,throws)
        hit_s=calc_hit_score(ld,p_ld,sweet,xwoba,swstr)
        dbl_s=calc_doubles_score(ld,oppo,sweet,p_ld,fb)
        swstr_s=calc_swstr_score(swstr,p_swstr)
        zone_s=calc_zone_fit(zc,p_chase,chase)
        master_s=calc_master(hr_s,hit_s,swstr_s,zone_s,p_csw,form)
        khr_s=calc_khr(barrel,pulledbrl,hh,fb,iso)
        khr_rat=khr_rating(khr_s)
        hr_lik=hr_likelihood(hr_s,barrel,ev,form)
        hit_lik=hit_likelihood(hit_s)
        dbl_lik=doubles_likelihood(dbl_s)
        hr_pf=hr_play_fade(master_s,barrel,p_csw,form,bats,throws,ev,bbe)
        hit_pf=hit_play_fade(hit_s,form)
        dbl_pf=doubles_play_fade(dbl_s,oppo,ld,form)
        f_arrow=form_arrow(form)

        rows.append({
            "Hitter":h_name,"Pitcher":p_name,"Game":game,
            "Bats":bats,"Throws":throws,"Platoon":platoon_str,
            "Matchup":round(master_s,1),"Zone Fit":round(zone_s,1),
            "HR Form":hr_lik,"kHR":round(hr_s,1),
            "KHR Score":round(khr_s,1),"KHR Rating":khr_rat,
            "Hit Score":round(hit_s,1),"Hit Like":hit_lik,
            "Doubles Score":round(dbl_s,1),"Doubles Like":dbl_lik,
            "HR Play":hr_pf,"Hit Play":hit_pf,"Doubles Play":dbl_pf,
            "Form":form,"Form Arrow":f_arrow,
            "ISO":iso,"xwOBA":xwoba,"SwStr%":swstr,
            "PulledBrl%":pulledbrl,"Brl/BIP%":brlbip,
            "SweetSpot%":sweet,"FB%":fb,"HH%":hh,"LA":la,
            "LD%":ld,"Oppo%":oppo,"CSW%":p_csw,
            "Master":master_s,"_barrel":barrel
        })
    return rows

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DAILY BOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    if hitters_df.empty or matchups_df.empty:
        st.markdown("""
        <div style="text-align:center; padding: 80px 0;">
            <div style="font-size: 4rem;">⚾</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #8888aa;">Loading data from GitHub...</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        h_idx = hitters_df.set_index("Name")
        p_idx = pitchers_df.set_index("Name")
        games = matchups_df["Game"].unique()
        selected_game = st.selectbox("🎮 Filter by Game", ["All Games"] + list(games), label_visibility="collapsed")
        filtered = matchups_df if selected_game == "All Games" else matchups_df[matchups_df["Game"] == selected_game]
        rows = build_rows(filtered, h_idx, p_idx)

        if not rows:
            st.warning("No matching data found!")
        else:
            results_df = pd.DataFrame(rows).sort_values("Matchup", ascending=False)
            hr_plays=len(results_df[results_df["HR Play"].str.contains("HR Play|HR Lock",na=False)])
            hit_plays=len(results_df[results_df["Hit Play"].str.contains("Hit Lock|Hit Play",na=False)])
            dbl_plays=len(results_df[results_df["Doubles Play"].str.contains("Double Lock|Double Play",na=False)])
            k_risks=len(results_df[results_df["HR Play"].str.contains("K Risk",na=False)])
            avg_master=results_df["Master"].mean()

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="metric-value" style="color:#00e676">{hr_plays}</div>
                    <div class="metric-label">🔥 HR Plays</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#2979ff">{hit_plays}</div>
                    <div class="metric-label">🎯 Hit Plays</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#ffd600">{dbl_plays}</div>
                    <div class="metric-label">📐 Double Plays</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#ff6d00">{k_risks}</div>
                    <div class="metric-label">⚠️ K Risks</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color:#8888aa">{avg_master:.0f}</div>
                    <div class="metric-label">Avg Score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            groups = results_df.groupby("Game")
            for game_name, group in groups:
                st.markdown(f'<div class="section-header">⚾ {game_name}</div>', unsafe_allow_html=True)
                html = """<table class="stat-table"><thead><tr>
                    <th>#</th><th>Hitter</th><th>vs Pitcher</th>
                    <th>Platoon</th><th>Form</th><th>Matchup</th>
                    <th>HR Play</th><th>Hit Play</th><th>Doubles</th>
                    <th>KHR</th><th>ISO</th><th>xwOBA</th>
                    <th>LD%</th><th>Oppo%</th><th>Sweet%</th><th>HH%</th><th>CSW%</th>
                </tr></thead><tbody>"""

                for rank,(_, row) in enumerate(group.iterrows(),1):
                    hr_pf=row["HR Play"]
                    hit_pf=row["Hit Play"]
                    dbl_pf=row["Doubles Play"]
                    hr_class="cell-green" if "Lock" in hr_pf or "HR Play" in hr_pf else \
                              "cell-orange" if "K Risk" in hr_pf else \
                              "cell-yellow" if "Lean" in hr_pf else "cell-red"
                    hit_class="cell-green" if "Lock" in hit_pf or "Hit Play" in hit_pf else \
                               "cell-yellow" if "Lean" in hit_pf else "cell-red"
                    dbl_class="cell-green" if "Lock" in dbl_pf or "Double Play" in dbl_pf else \
                               "cell-yellow" if "Lean" in dbl_pf else "cell-red"
                    khr_class="cell-green" if "Elite" in row["KHR Rating"] or "High" in row["KHR Rating"] else \
                               "cell-yellow" if "Moderate" in row["KHR Rating"] else "cell-red"
                    rank_class=f"rank-{rank}" if rank<=3 else ""
                    form_val=row["Form"]
                    try:
                        f=float(form_val)
                        form_color="#00e676" if f>=7 else "#ffd600" if f>=5 else "#ff1744"
                    except: form_color="#ffd600"
                    platoon_color="#00e676" if row["Platoon"]=="✅ Platoon" else "#555570"

                    html+=f"""<tr>
                        <td><span class="rank-num {rank_class}">{rank}</span></td>
                        <td style="font-weight:700">{row['Hitter']}<br><span style="font-size:0.65rem;color:#8888aa">{row['Bats']}HB</span></td>
                        <td style="color:#8888aa;font-size:0.75rem">{row['Pitcher']}<br><span style="font-size:0.65rem">{row['Throws']}HP</span></td>
                        <td style="color:{platoon_color};font-weight:700;font-size:0.75rem">{row['Platoon']}</td>
                        <td style="color:{form_color};font-weight:700">{row['Form Arrow']} {form_val}</td>
                        {render_cell(row['Matchup'],color_val(row['Matchup'],[1500,1200,900]),"f0")}
                        <td class="{hr_class}" style="font-size:0.72rem;font-weight:700">{hr_pf}</td>
                        <td class="{hit_class}" style="font-size:0.72rem;font-weight:700">{hit_pf}</td>
                        <td class="{dbl_class}" style="font-size:0.72rem;font-weight:700">{dbl_pf}</td>
                        {render_cell(row['KHR Score'],color_val(row['KHR Score'],[2500,2000,1500]),"f0")}
                        {render_cell(row['ISO'],color_val(row['ISO'],[0.2,0.15,0.1]),"f3")}
                        {render_cell(row['xwOBA'],color_val(row['xwOBA'],[0.38,0.32,0.28]),"f3")}
                        {render_cell(row['LD%'],color_val(row['LD%'],[25,20,15]),"f1")}
                        {render_cell(row['Oppo%'],color_val(row['Oppo%'],[30,25,18]),"f1")}
                        {render_cell(row['SweetSpot%'],color_val(row['SweetSpot%'],[35,28,20]),"f1")}
                        {render_cell(row['HH%'],color_val(row['HH%'],[50,40,30]),"f1")}
                        {render_cell(row['CSW%'],color_val(row['CSW%'],[30,25,20]),"f1")}
                    </tr>"""

                html+="</tbody></table>"
                st.markdown(html,unsafe_allow_html=True)

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HR PROPS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">🔥 HR Props — Platoon + Barrel + Form</div>', unsafe_allow_html=True)
    if not hitters_df.empty and not matchups_df.empty:
        h_idx = hitters_df.set_index("Name")
        p_idx = pitchers_df.set_index("Name")
        all_rows = build_rows(matchups_df, h_idx, p_idx)
        if all_rows:
            hr_df = pd.DataFrame(all_rows)
            hr_df = hr_df[~hr_df["HR Play"].str.contains("Fade HR$", na=False)]
            hr_df = hr_df.sort_values("KHR Score", ascending=False)

            html = """<table class="stat-table"><thead><tr>
                <th>#</th><th>Hitter</th><th>vs Pitcher</th><th>Game</th>
                <th>Platoon</th><th>Form</th><th>HR Play</th>
                <th>KHR Score</th><th>Matchup</th>
                <th>Barrel%</th><th>PulledBrl%</th><th>HH%</th><th>ISO</th><th>CSW%</th>
            </tr></thead><tbody>"""

            for rank,(_, row) in enumerate(hr_df.iterrows(),1):
                hr_pf=row["HR Play"]
                hr_class="cell-green" if "Lock" in hr_pf or "HR Play" in hr_pf else \
                          "cell-orange" if "K Risk" in hr_pf else "cell-yellow"
                rank_class=f"rank-{rank}" if rank<=3 else ""
                form_val=row["Form"]
                try:
                    f=float(form_val)
                    form_color="#00e676" if f>=7 else "#ffd600" if f>=5 else "#ff1744"
                except: form_color="#ffd600"
                platoon_color="#00e676" if row["Platoon"]=="✅ Platoon" else "#555570"

                html+=f"""<tr>
                    <td><span class="rank-num {rank_class}">{rank}</span></td>
                    <td style="font-weight:700">{row['Hitter']}</td>
                    <td style="color:#8888aa;font-size:0.75rem">{row['Pitcher']}</td>
                    <td style="color:#8888aa;font-size:0.72rem">{row['Game']}</td>
                    <td style="color:{platoon_color};font-weight:700;font-size:0.75rem">{row['Platoon']}</td>
                    <td style="color:{form_color};font-weight:700">{row['Form Arrow']} {form_val}</td>
                    <td class="{hr_class}" style="font-size:0.72rem;font-weight:700">{hr_pf}</td>
                    {render_cell(row['KHR Score'],color_val(row['KHR Score'],[2500,2000,1500]),"f0")}
                    {render_cell(row['Matchup'],color_val(row['Matchup'],[1500,1200,900]),"f0")}
                    {render_cell(row['_barrel'],color_val(row['_barrel'],[15,10,5]),"f1")}
                    {render_cell(row['PulledBrl%'],color_val(row['PulledBrl%'],[15,10,5]),"f1")}
                    {render_cell(row['HH%'],color_val(row['HH%'],[50,40,30]),"f1")}
                    {render_cell(row['ISO'],color_val(row['ISO'],[0.2,0.15,0.1]),"f3")}
                    {render_cell(row['CSW%'],color_val(row['CSW%'],[30,25,20]),"f1")}
                </tr>"""

            html+="</tbody></table>"
            st.markdown(html,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — HIT PROPS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">🎯 Hit Props — SweetSpot% + xwOBA + Form</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#8888aa;font-size:0.85rem;margin-bottom:16px;">
    NO barrel% cutoff — contact hitters included!<br>
    Formula: (LD%×35) + (P_LD%×20) + (SweetSpot%×25) + (xwOBA×200) - (SwStr%×8)
    </div>
    """, unsafe_allow_html=True)
    if not hitters_df.empty and not matchups_df.empty:
        h_idx = hitters_df.set_index("Name")
        p_idx = pitchers_df.set_index("Name")
        all_rows = build_rows(matchups_df, h_idx, p_idx)
        if all_rows:
            hit_df = pd.DataFrame(all_rows)
            hit_df = hit_df[hit_df["Hit Play"].str.contains("Hit Lock|Hit Play|Hit Lean", na=False)]
            hit_df = hit_df.sort_values("Hit Score", ascending=False)

            html = """<table class="stat-table"><thead><tr>
                <th>#</th><th>Hitter</th><th>vs Pitcher</th><th>Game</th>
                <th>Platoon</th><th>Form</th><th>Hit Play</th><th>Hit Score</th>
                <th>LD%</th><th>SweetSpot%</th><th>xwOBA</th><th>SwStr%</th><th>CSW%</th>
            </tr></thead><tbody>"""

            for rank,(_, row) in enumerate(hit_df.iterrows(),1):
                hit_pf=row["Hit Play"]
                hit_class="cell-green" if "Lock" in hit_pf or "Hit Play" in hit_pf else "cell-yellow"
                rank_class=f"rank-{rank}" if rank<=3 else ""
                form_val=row["Form"]
                try:
                    f=float(form_val)
                    form_color="#00e676" if f>=7 else "#ffd600" if f>=5 else "#ff1744"
                except: form_color="#ffd600"
                platoon_color="#00e676" if row["Platoon"]=="✅ Platoon" else "#555570"

                html+=f"""<tr>
                    <td><span class="rank-num {rank_class}">{rank}</span></td>
                    <td style="font-weight:700">{row['Hitter']}</td>
                    <td style="color:#8888aa;font-size:0.75rem">{row['Pitcher']}</td>
                    <td style="color:#8888aa;font-size:0.72rem">{row['Game']}</td>
                    <td style="color:{platoon_color};font-weight:700;font-size:0.75rem">{row['Platoon']}</td>
                    <td style="color:{form_color};font-weight:700">{row['Form Arrow']} {form_val}</td>
                    <td class="{hit_class}" style="font-size:0.72rem;font-weight:700">{hit_pf}</td>
                    {render_cell(row['Hit Score'],color_val(row['Hit Score'],[2200,1800,1400]),"f0")}
                    {render_cell(row['LD%'],color_val(row['LD%'],[25,20,15]),"f1")}
                    {render_cell(row['SweetSpot%'],color_val(row['SweetSpot%'],[35,28,20]),"f1")}
                    {render_cell(row['xwOBA'],color_val(row['xwOBA'],[0.38,0.32,0.28]),"f3")}
                    {render_cell(row['SwStr%'],color_val(row['SwStr%'],[25,18,12]),"f1")}
                    {render_cell(row['CSW%'],color_val(row['CSW%'],[30,25,20]),"f1")}
                </tr>"""

            html+="</tbody></table>"
            st.markdown(html,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DOUBLES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">📐 Doubles Props — LD% + Oppo% + SweetSpot%</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#8888aa;font-size:0.85rem;margin-bottom:16px;">
    Doubles predicted by line drives + opposite field tendency + sweet spot contact.<br>
    Formula: (LD%×35) + (Oppo%×25) + (SweetSpot%×20) + (P_LD%×15) + (FB%×5)
    </div>
    """, unsafe_allow_html=True)
    if not hitters_df.empty and not matchups_df.empty:
        h_idx = hitters_df.set_index("Name")
        p_idx = pitchers_df.set_index("Name")
        all_rows = build_rows(matchups_df, h_idx, p_idx)
        if all_rows:
            dbl_df = pd.DataFrame(all_rows)
            dbl_df = dbl_df[dbl_df["Doubles Play"].str.contains("Double Lock|Double Play|Double Lean", na=False)]
            dbl_df = dbl_df.sort_values("Doubles Score", ascending=False)

            html = """<table class="stat-table"><thead><tr>
                <th>#</th><th>Hitter</th><th>vs Pitcher</th><th>Game</th>
                <th>Form</th><th>Doubles Play</th><th>Doubles Score</th>
                <th>LD%</th><th>Oppo%</th><th>SweetSpot%</th><th>FB%</th><th>xwOBA</th>
            </tr></thead><tbody>"""

            for rank,(_, row) in enumerate(dbl_df.iterrows(),1):
                dbl_pf=row["Doubles Play"]
                dbl_class="cell-green" if "Lock" in dbl_pf or "Double Play" in dbl_pf else "cell-yellow"
                rank_class=f"rank-{rank}" if rank<=3 else ""
                form_val=row["Form"]
                try:
                    f=float(form_val)
                    form_color="#00e676" if f>=7 else "#ffd600" if f>=5 else "#ff1744"
                except: form_color="#ffd600"

                html+=f"""<tr>
                    <td><span class="rank-num {rank_class}">{rank}</span></td>
                    <td style="font-weight:700">{row['Hitter']}</td>
                    <td style="color:#8888aa;font-size:0.75rem">{row['Pitcher']}</td>
                    <td style="color:#8888aa;font-size:0.72rem">{row['Game']}</td>
                    <td style="color:{form_color};font-weight:700">{row['Form Arrow']} {form_val}</td>
                    <td class="{dbl_class}" style="font-size:0.72rem;font-weight:700">{dbl_pf}</td>
                    {render_cell(row['Doubles Score'],color_val(row['Doubles Score'],[2200,1800,1400]),"f0")}
                    {render_cell(row['LD%'],color_val(row['LD%'],[25,20,15]),"f1")}
                    {render_cell(row['Oppo%'],color_val(row['Oppo%'],[30,25,18]),"f1")}
                    {render_cell(row['SweetSpot%'],color_val(row['SweetSpot%'],[35,28,20]),"f1")}
                    {render_cell(row['FB%'],color_val(row['FB%'],[35,28,20]),"f1")}
                    {render_cell(row['xwOBA'],color_val(row['xwOBA'],[0.38,0.32,0.28]),"f3")}
                </tr>"""

            html+="</tbody></table>"
            st.markdown(html,unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — KHR RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">💣 KHR Power Rankings</div>', unsafe_allow_html=True)
    if not hitters_df.empty:
        khr_rows = []
        for _, h in hitters_df.iterrows():
            def gh(col, default=0):
                try: return float(h[col]) if col in h.index else default
                except: return default
            barrel=gh("Barrel%"); pulledbrl=gh("PulledBrl%")
            hh=gh("HardHit%"); fb=gh("FB%"); iso=gh("ISO")
            xwoba=gh("xwOBA"); ev=gh("AvgEV"); la=gh("LA")
            form=gh("Form",5)
            khr_s=calc_khr(barrel,pulledbrl,hh,fb,iso)
            khr_rat=khr_rating(khr_s)
            f_arrow=form_arrow(form)
            khr_rows.append({
                "Hitter":h["Name"],"Team":h.get("Team",""),
                "Form":form,"Form Arrow":f_arrow,
                "KHR Score":round(khr_s,1),"KHR Rating":khr_rat,
                "Barrel%":barrel,"PulledBrl%":pulledbrl,
                "HardHit%":hh,"FB%":fb,"ISO":iso,
                "xwOBA":xwoba,"EV":ev,"LA":la,
            })

        khr_df = pd.DataFrame(khr_rows).sort_values("KHR Score", ascending=False)
        html = """<table class="stat-table"><thead><tr>
            <th>#</th><th>Hitter</th><th>Team</th><th>Form</th>
            <th>KHR Score</th><th>KHR Rating</th>
            <th>Barrel%</th><th>PulledBrl%</th>
            <th>HardHit%</th><th>FB%</th><th>ISO</th>
            <th>xwOBA</th><th>EV</th><th>LA</th>
        </tr></thead><tbody>"""

        for rank,(_, row) in enumerate(khr_df.iterrows(),1):
            khr_class="cell-green" if "Elite" in row["KHR Rating"] or "High" in row["KHR Rating"] else \
                       "cell-yellow" if "Moderate" in row["KHR Rating"] else "cell-red"
            rank_class=f"rank-{rank}" if rank<=3 else ""
            form_val=row["Form"]
            try:
                f=float(form_val)
                form_color="#00e676" if f>=7 else "#ffd600" if f>=5 else "#ff1744"
            except: form_color="#ffd600"

            html+=f"""<tr>
                <td><span class="rank-num {rank_class}">{rank}</span></td>
                <td style="font-weight:700">{row['Hitter']}</td>
                <td style="color:#8888aa;font-size:0.75rem">{row['Team']}</td>
                <td style="color:{form_color};font-weight:700">{row['Form Arrow']} {form_val}</td>
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
            </tr>"""

        html+="</tbody></table>"
        st.markdown(html,unsafe_allow_html=True)

    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="MLB Statzzz", page_icon="⚾", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
:root {
    --bg: #080810;
    --bg2: #0f0f1a;
    --bg3: #161625;
    --border: #1e1e35;
    --border2: #2a2a45;
    --text: #e8e8f5;
    --muted: #6666aa;
    --green: #00ff88;
    --yellow: #ffcc00;
    --orange: #ff8800;
    --red: #ff3355;
    --blue: #4488ff;
    --purple: #aa44ff;
}
* { font-family: 'Space Grotesk', sans-serif; box-sizing: border-box; }
.stApp { background: var(--bg); color: var(--text); }
.block-container { padding: 1.5rem 2rem; max-width: 100%; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }

/* HEADER */
.header { 
    border-bottom: 1px solid var(--border2);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}
.logo { 
    font-size: 1.8rem; 
    font-weight: 700; 
    letter-spacing: -0.5px;
    color: var(--text);
}
.logo span { color: var(--green); }
.tagline { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; }
.meta { font-size: 0.75rem; color: var(--muted); font-family: 'Space Mono', monospace; text-align: right; }

/* SCORE FORMULA BOX */
.formula-box {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
    font-size: 0.78rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
}
.formula-box strong { color: var(--text); }

/* SECTION HEADERS */
.section-label {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--muted);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* PLAYER CARDS */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 12px;
    margin-bottom: 2.5rem;
}
.player-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    position: relative;
    transition: border-color 0.2s;
}
.player-card:hover { border-color: var(--border2); }
.card-rank {
    position: absolute;
    top: 10px;
    right: 12px;
    font-size: 0.65rem;
    font-family: 'Space Mono', monospace;
    color: var(--muted);
}
.card-rank.top1 { color: var(--green); font-weight: 700; }
.card-rank.top3 { color: var(--yellow); }
.player-name { font-size: 1rem; font-weight: 600; margin-bottom: 2px; }
.player-meta { font-size: 0.72rem; color: var(--muted); margin-bottom: 10px; }
.score-bar-wrap { margin-bottom: 10px; }
.score-label { display: flex; justify-content: space-between; margin-bottom: 4px; }
.score-name { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); }
.score-val { font-size: 0.78rem; font-family: 'Space Mono', monospace; font-weight: 700; }
.score-bar { height: 5px; border-radius: 3px; background: var(--border); overflow: hidden; }
.score-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }
.reasons { margin-top: 10px; border-top: 1px solid var(--border); padding-top: 8px; }
.reason-row { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; font-size: 0.72rem; }
.reason-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.platoon-badge {
    display: inline-block;
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.3);
    color: var(--green);
    font-size: 0.6rem;
    padding: 1px 6px;
    border-radius: 3px;
    font-weight: 600;
    letter-spacing: 1px;
    margin-left: 6px;
}
.form-badge {
    display: inline-block;
    font-size: 0.65rem;
    padding: 1px 6px;
    border-radius: 3px;
    margin-left: 4px;
}
.form-hot { background: rgba(255,136,0,0.15); color: var(--orange); border: 1px solid rgba(255,136,0,0.3); }
.form-up { background: rgba(0,255,136,0.1); color: var(--green); border: 1px solid rgba(0,255,136,0.2); }
.form-neutral { background: rgba(102,102,170,0.15); color: var(--muted); border: 1px solid var(--border); }
.form-down { background: rgba(255,51,85,0.1); color: var(--red); border: 1px solid rgba(255,51,85,0.2); }
.small-sample { background: rgba(255,136,0,0.1); color: var(--orange); border: 1px solid rgba(255,136,0,0.3); font-size: 0.6rem; padding: 1px 6px; border-radius: 3px; margin-left: 6px; }

/* HEATMAP CELLS */
.heat-grid { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.heat-cell { 
    padding: 3px 8px; 
    border-radius: 4px; 
    font-size: 0.68rem; 
    font-family: 'Space Mono', monospace;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 60px;
}
.heat-label { font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; margin-bottom: 1px; }
.heat-val { font-weight: 700; }
.heat-green { background: rgba(0,255,136,0.12); color: var(--green); }
.heat-yellow { background: rgba(255,204,0,0.12); color: var(--yellow); }
.heat-orange { background: rgba(255,136,0,0.12); color: var(--orange); }
.heat-red { background: rgba(255,51,85,0.12); color: var(--red); }
.heat-neutral { background: var(--bg3); color: var(--muted); }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background: var(--bg2); border-radius: 8px; padding: 4px; gap: 2px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: var(--muted); border-radius: 6px; font-size: 0.82rem; font-weight: 500; }
.stTabs [aria-selected="true"] { background: var(--bg3) !important; color: var(--text) !important; }

/* SELECTBOX */
.stSelectbox > div > div { background: var(--bg2); border-color: var(--border2); color: var(--text); }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── DATA ───────────────────────────────────────────────────────────────────────
GITHUB_RAW = "https://raw.githubusercontent.com/bbytyty/-mlb-statzzz/main"

@st.cache_data(ttl=300)
def load_data():
    try:
        h = pd.read_csv(f"{GITHUB_RAW}/hitters_today.csv")
        p = pd.read_csv(f"{GITHUB_RAW}/pitchers_today.csv")
        m = pd.read_csv(f"{GITHUB_RAW}/matchups_today.csv")
        return h, p, m
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

hitters_df, pitchers_df, matchups_df = load_data()

# ── SCORING ENGINE ─────────────────────────────────────────────────────────────
def g(df, col, default=0):
    try: return float(df[col]) if col in df.index else default
    except: return default

def gs(df, col, default=""):
    try: return str(df[col]) if col in df.index else default
    except: return default

def platoon_bonus(bats, throws):
    b, t = str(bats).strip().upper(), str(throws).strip().upper()
    if b == "S": return 1.05
    if (b == "R" and t == "L") or (b == "L" and t == "R"): return 1.10
    return 1.0

def hr_score_100(barrel, pulled_brl, fb, iso, xslg, hh, la, ev, p_barrel, p_fb, p_hr9, bats, throws, form, bbe):
    """
    HR Score (0-100)
    Barrel%       × 2.5  = max 37.5  (15% barrel = elite)
    PulledBrl%    × 0.8  = max 20.0
    FB%           × 0.25 = max 8.75
    ISO           × 50   = max 10.0
    HardHit%      × 0.15 = max 7.5
    LA bonus      sweet spot 10-25° = +5
    P_Barrel      × 0.5  = max 7.5   (pitcher gives up barrels)
    Platoon       × 1.05-1.10 multiplier
    Form          adjustment ±5
    """
    if bbe < 20: return None  # small sample
    raw = (barrel * 2.5) + (pulled_brl * 0.8) + (fb * 0.25) + (iso * 50) + (hh * 0.15) + (p_barrel * 0.5)
    if 10 <= la <= 25: raw += 5
    raw *= platoon_bonus(bats, throws)
    try:
        f = float(form)
        raw += (f - 5) * 1.5
    except: pass
    return max(0, min(100, round(raw, 1)))

def hit_score_100(xba, ld, p_ld, sweet, swstr, xwoba, form, p_csw):
    """
    Hit Score (0-100)
    xBA           × 200  = max 70   (.350 xBA = elite)
    LD%           × 0.5  = max 12.5
    P_LD%         × 0.3  = max 9
    SweetSpot%    × 0.2  = max 7
    SwStr% penalty× -0.3 = up to -9
    CSW% penalty  if >30 = -5
    Form boost    ±4
    """
    raw = (xba * 200) + (ld * 0.5) + (p_ld * 0.3) + (sweet * 0.2) - (swstr * 0.3)
    if p_csw >= 32: raw -= 8
    elif p_csw >= 30: raw -= 5
    elif p_csw >= 28: raw -= 3
    try:
        f = float(form)
        raw += (f - 5) * 0.8
    except: pass
    return max(0, min(100, round(raw, 1)))

def double_score_100(ld, oppo, sweet, ev, xslg, p_ld, fb, form):
    """
    Double Score (0-100)
    LD%           × 0.8  = max 20
    Oppo%         × 0.7  = max 21
    SweetSpot%    × 0.5  = max 17.5
    EV bonus      >92mph = +8, >89 = +4
    xSLG          × 40   = max 14 (doubles need xSLG not just power)
    P_LD%         × 0.3  = max 9
    Form          ±3
    """
    if oppo < 22 or ld < 20: return 0  # must be oppo/LD hitter
    raw = (ld * 0.8) + (oppo * 0.7) + (sweet * 0.5) + (xslg * 40) + (p_ld * 0.3)
    if ev >= 92: raw += 8
    elif ev >= 89: raw += 4
    try:
        f = float(form)
        raw += (f - 5) * 0.6
    except: pass
    return max(0, min(100, round(raw, 1)))

def xbh_score_100(ev, sweet, xslg, hh, ld, fb, iso, form):
    """
    XBH Score (0-100) - combines HR and double potential
    EV            × 0.6  = max ~55
    SweetSpot%    × 0.4  = max 14
    xSLG          × 30   = max ~12
    HardHit%      × 0.15 = max ~7
    ISO           × 30   = max ~9
    Form          ±3
    """
    raw = (ev * 0.6 - 50) + (sweet * 0.4) + (xslg * 30) + (hh * 0.15) + (iso * 30)
    try:
        f = float(form)
        raw += (f - 5) * 0.6
    except: pass
    return max(0, min(100, round(raw, 1)))

def score_color(score):
    if score is None: return "heat-neutral", "—"
    if score >= 75: return "heat-green", f"{score:.0f}"
    if score >= 55: return "heat-yellow", f"{score:.0f}"
    if score >= 35: return "heat-orange", f"{score:.0f}"
    return "heat-red", f"{score:.0f}"

def bar_color(score):
    if score is None: return "#333355", 0
    if score >= 75: return "#00ff88", score
    if score >= 55: return "#ffcc00", score
    if score >= 35: return "#ff8800", score
    return "#ff3355", score

def form_badge(form):
    try:
        f = float(form)
        if f >= 8: return f'<span class="form-badge form-hot">🔥 {f:.0f}</span>'
        if f >= 7: return f'<span class="form-badge form-up">↑ {f:.0f}</span>'
        if f >= 5: return f'<span class="form-badge form-neutral">→ {f:.0f}</span>'
        return f'<span class="form-badge form-down">↓ {f:.0f}</span>'
    except: return ''

def heat_class(val, thresholds):
    try:
        v = float(val)
        if v >= thresholds[0]: return "heat-green"
        if v >= thresholds[1]: return "heat-yellow"
        if v >= thresholds[2]: return "heat-orange"
        return "heat-red"
    except: return "heat-neutral"

def build_player_data():
    if hitters_df.empty or pitchers_df.empty or matchups_df.empty:
        return []
    h_idx = hitters_df.set_index("Name")
    p_idx = pitchers_df.set_index("Name")
    rows = []
    for _, m in matchups_df.iterrows():
        h_name, p_name = m["Hitter"], m["Pitcher"]
        game = m.get("Game", "")
        if h_name not in h_idx.index or p_name not in p_idx.index: continue
        h, p = h_idx.loc[h_name], p_idx.loc[p_name]

        barrel=g(h,"Barrel%"); fb=g(h,"FB%"); ld=g(h,"LD%")
        hh=g(h,"HardHit%"); la=g(h,"LA"); ev=g(h,"AvgEV")
        iso=g(h,"ISO"); swstr=g(h,"SwStr%"); xwoba=g(h,"xwOBA")
        pulledbrl=g(h,"PulledBrl%"); brlbip=g(h,"BrlBIP%")
        sweet=g(h,"SweetSpot%"); oppo=g(h,"Oppo%"); pull=g(h,"FB%")
        xba=g(h,"xwOBA")*0.75  # approximate xBA from xwOBA
        xslg=xwoba*1.4  # approximate xSLG
        form=g(h,"Form",5); bats=gs(h,"Bats","R")
        bbe=g(h,"BBE",100); zc=g(h,"ZoneContact%")
        chase=g(h,"Chase%")

        p_barrel=g(p,"BarrelAllowed%"); p_fb=g(p,"FBAllowed%")
        p_ld=g(p,"LDAllowed%"); p_csw=g(p,"CSW%")
        p_hr9=g(p,"HR9"); throws=gs(p,"Throws","R")
        p_chase=g(p,"ChaseAllowed%")

        platoon = platoon_bonus(bats, throws)
        has_platoon = platoon > 1.0

        hr_s = hr_score_100(barrel,pulledbrl,fb,iso,xslg,hh,la,ev,p_barrel,p_fb,p_hr9,bats,throws,form,bbe)
        hit_s = hit_score_100(xba,ld,p_ld,sweet,swstr,xwoba,form,p_csw)
        dbl_s = double_score_100(ld,oppo,sweet,ev,xslg,p_ld,fb,form)
        xbh_s = xbh_score_100(ev,sweet,xslg,hh,ld,fb,iso,form)

        # Build reasons
        hr_reasons = []
        if barrel >= 15: hr_reasons.append(("green", f"Elite barrel rate {barrel:.1f}%"))
        elif barrel >= 10: hr_reasons.append(("yellow", f"Good barrel rate {barrel:.1f}%"))
        if pulledbrl >= 15: hr_reasons.append(("green", f"Pulls {pulledbrl:.1f}% of barrels"))
        if hh >= 50: hr_reasons.append(("green", f"{hh:.1f}% hard hit rate"))
        if has_platoon: hr_reasons.append(("green", "Platoon advantage"))
        if p_barrel >= 12: hr_reasons.append(("yellow", f"Pitcher allows {p_barrel:.1f}% barrels"))
        if float(form) >= 7: hr_reasons.append(("orange", f"Trending up (form {form})"))
        if bbe < 20: hr_reasons.append(("orange", f"Small sample ({bbe:.0f} BBE)"))

        hit_reasons = []
        if xwoba >= 0.38: hit_reasons.append(("green", f"Elite xwOBA {xwoba:.3f}"))
        if ld >= 25: hit_reasons.append(("green", f"{ld:.1f}% line drive rate"))
        if sweet >= 35: hit_reasons.append(("green", f"{sweet:.1f}% sweet spot contact"))
        if swstr <= 15: hit_reasons.append(("green", f"Low whiff rate {swstr:.1f}%"))
        if p_csw >= 30: hit_reasons.append(("red", f"Tough pitcher CSW {p_csw:.1f}%"))
        if float(form) >= 7: hit_reasons.append(("orange", "Hot recent form"))

        rows.append({
            "name": h_name, "pitcher": p_name, "game": game,
            "bats": bats, "throws": throws, "platoon": has_platoon,
            "form": form, "bbe": bbe,
            "barrel": barrel, "pulledbrl": pulledbrl, "hh": hh,
            "fb": fb, "la": la, "ev": ev, "iso": iso,
            "sweet": sweet, "ld": ld, "oppo": oppo,
            "xwoba": xwoba, "swstr": swstr, "p_csw": p_csw,
            "hr_score": hr_s, "hit_score": hit_s,
            "dbl_score": dbl_s, "xbh_score": xbh_s,
            "hr_reasons": hr_reasons, "hit_reasons": hit_reasons,
        })
    return rows

def render_card(row, score_key, score_label, reasons_key, rank):
    score = row[score_key]
    if score is None: score = 0
    bar_c, bar_w = bar_color(score)
    rank_class = "top1" if rank == 1 else "top3" if rank <= 3 else ""
    platoon_html = '<span class="platoon-badge">PLATOON</span>' if row["platoon"] else ""
    small_sample = f'<span class="small-sample">⚠️ {row["bbe"]:.0f} BBE</span>' if row["bbe"] < 20 else ""
    form_html = form_badge(row["form"])

    reasons_html = ""
    for color, text in row.get(reasons_key, [])[:4]:
        dot_color = {"green":"#00ff88","yellow":"#ffcc00","orange":"#ff8800","red":"#ff3355"}.get(color,"#6666aa")
        reasons_html += f'<div class="reason-row"><div class="reason-dot" style="background:{dot_color}"></div><span style="color:#aaaacc">{text}</span></div>'

    # Heatmap cells
    cells = []
    if score_key == "hr_score":
        cells = [
            ("Barrel", f"{row['barrel']:.1f}%", heat_class(row['barrel'],[15,10,6])),
            ("PullBrl", f"{row['pulledbrl']:.1f}%", heat_class(row['pulledbrl'],[15,10,5])),
            ("HH%", f"{row['hh']:.1f}%", heat_class(row['hh'],[50,40,30])),
            ("FB%", f"{row['fb']:.1f}%", heat_class(row['fb'],[35,28,20])),
            ("EV", f"{row['ev']:.0f}", heat_class(row['ev'],[93,90,87])),
        ]
    elif score_key == "hit_score":
        cells = [
            ("xwOBA", f"{row['xwoba']:.3f}", heat_class(row['xwoba'],[0.38,0.32,0.27])),
            ("LD%", f"{row['ld']:.1f}%", heat_class(row['ld'],[25,20,15])),
            ("Sweet%", f"{row['sweet']:.1f}%", heat_class(row['sweet'],[35,28,20])),
            ("SwStr%", f"{row['swstr']:.1f}%", heat_class(100-row['swstr'],[85,82,78])),
            ("CSW%", f"{row['p_csw']:.1f}%", heat_class(35-row['p_csw'],[10,6,2])),
        ]
    elif score_key == "dbl_score":
        cells = [
            ("LD%", f"{row['ld']:.1f}%", heat_class(row['ld'],[25,20,15])),
            ("Oppo%", f"{row['oppo']:.1f}%", heat_class(row['oppo'],[30,25,18])),
            ("Sweet%", f"{row['sweet']:.1f}%", heat_class(row['sweet'],[35,28,20])),
            ("EV", f"{row['ev']:.0f}", heat_class(row['ev'],[93,90,87])),
            ("xwOBA", f"{row['xwoba']:.3f}", heat_class(row['xwoba'],[0.38,0.32,0.27])),
        ]
    else:  # xbh
        cells = [
            ("EV", f"{row['ev']:.0f}", heat_class(row['ev'],[93,90,87])),
            ("Sweet%", f"{row['sweet']:.1f}%", heat_class(row['sweet'],[35,28,20])),
            ("HH%", f"{row['hh']:.1f}%", heat_class(row['hh'],[50,40,30])),
            ("ISO", f"{row['iso']:.3f}", heat_class(row['iso'],[0.20,0.15,0.10])),
            ("Barrel", f"{row['barrel']:.1f}%", heat_class(row['barrel'],[15,10,6])),
        ]

    heat_html = "".join([f'<div class="heat-cell {c}"><div class="heat-label">{l}</div><div class="heat-val">{v}</div></div>' for l,v,c in cells])

    return f"""
    <div class="player-card">
        <div class="card-rank {rank_class}">#{rank}</div>
        <div class="player-name">{row['name']}{platoon_html}{small_sample}</div>
        <div class="player-meta">vs {row['pitcher']} · {row['game']} · {row['bats']}HB vs {row['throws']}HP {form_html}</div>
        <div class="score-bar-wrap">
            <div class="score-label">
                <span class="score-name">{score_label}</span>
                <span class="score-val" style="color:{bar_c}">{score:.0f}</span>
            </div>
            <div class="score-bar"><div class="score-fill" style="width:{bar_w}%;background:{bar_c}"></div></div>
        </div>
        <div class="heat-grid">{heat_html}</div>
        {f'<div class="reasons">{reasons_html}</div>' if reasons_html else ''}
    </div>
    """

# ── HEADER ─────────────────────────────────────────────────────────────────────
h_count = len(hitters_df) if not hitters_df.empty else 0
p_count = len(pitchers_df) if not pitchers_df.empty else 0
games_count = len(matchups_df["Game"].unique()) if not matchups_df.empty else 0

st.markdown(f"""
<div class="header">
    <div>
        <div class="logo">⚾ MLB <span>Statzzz</span></div>
        <div class="tagline">Daily Matchup Intelligence</div>
    </div>
    <div class="meta">
        {h_count} hitters · {p_count} pitchers · {games_count} games<br>
        Scores 0–100 · Higher = better matchup
    </div>
</div>
""", unsafe_allow_html=True)

# ── FORMULA BOX ────────────────────────────────────────────────────────────────
with st.expander("📐 How scores are calculated"):
    st.markdown("""
    **HR Score (0–100)**
    `Barrel%×2.5 + PulledBrl%×0.8 + FB%×0.25 + ISO×50 + HH%×0.15 + P_Barrel×0.5 + LA_bonus(+5 if 10-25°) × Platoon × Form_adj`

    **Hit Score (0–100)**
    `xBA×200 + LD%×0.5 + P_LD%×0.3 + SweetSpot%×0.2 - SwStr%×0.3 - CSW_penalty + Form_adj`

    **Double Score (0–100)**
    `LD%×0.8 + Oppo%×0.7 + SweetSpot%×0.5 + xSLG×40 + P_LD%×0.3 + EV_bonus + Form_adj`
    *Requires Oppo% ≥ 22% AND LD% ≥ 20%*

    **XBH Score (0–100)**
    `(EV×0.6-50) + SweetSpot%×0.4 + xSLG×30 + HH%×0.15 + ISO×30 + Form_adj`

    **Platoon bonus:** RHB vs LHP or LHB vs RHP = ×1.10 · Switch = ×1.05
    **Form adjustment:** Score 8–10 = +4.5 · Score 7 = +3 · Score 5–6 = 0 · Score 3–4 = −3
    """)

# ── BUILD DATA ─────────────────────────────────────────────────────────────────
all_players = build_player_data()

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🚀 HR Targets", "🎯 Hit Targets", "⚡ XBH Targets", "📐 Double Targets"])

games = sorted(set(r["game"] for r in all_players)) if all_players else []
selected_game = st.selectbox("Filter by game", ["All Games"] + games, label_visibility="collapsed")

def filtered_sorted(players, score_key, top_n=10):
    filtered = players if selected_game == "All Games" else [p for p in players if p["game"] == selected_game]
    valid = [p for p in filtered if p[score_key] is not None and p[score_key] > 0]
    return sorted(valid, key=lambda x: x[score_key], reverse=True)[:top_n]

with tab1:
    top = filtered_sorted(all_players, "hr_score", 10)
    if top:
        html = '<div class="section-label">Top 10 HR Candidates Today</div>'
        html += '<div class="cards-grid">'
        for i, r in enumerate(top):
            html += render_card(r, "hr_score", "HR Score", "hr_reasons", i+1)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No data loaded yet.")

with tab2:
    top = filtered_sorted(all_players, "hit_score", 10)
    if top:
        html = '<div class="section-label">Top 10 Hit Candidates Today</div>'
        html += '<div class="cards-grid">'
        for i, r in enumerate(top):
            html += render_card(r, "hit_score", "Hit Score", "hit_reasons", i+1)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

with tab3:
    top = filtered_sorted(all_players, "xbh_score", 10)
    if top:
        html = '<div class="section-label">Top 10 Extra Base Hit Candidates Today</div>'
        html += '<div class="cards-grid">'
        for i, r in enumerate(top):
            html += render_card(r, "xbh_score", "XBH Score", "hr_reasons", i+1)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

with tab4:
    top = filtered_sorted(all_players, "dbl_score", 10)
    if top:
        html = '<div class="section-label">Top 10 Double Candidates Today</div>'
        html += '<div class="cards-grid">'
        for i, r in enumerate(top):
            html += render_card(r, "dbl_score", "Double Score", "hit_reasons", i+1)
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

if st.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

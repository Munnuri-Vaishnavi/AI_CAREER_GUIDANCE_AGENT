import streamlit as st
import json
import time
import threading
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career Guidance Agent — AP & Telangana",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load data ───────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def load_10th_data():
    with open(DATA_DIR / "opportunities_10th.json",encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_inter_data():
    with open(DATA_DIR / "opportunities_inter.json",encoding="utf-8") as f:
        return json.load(f)

data_10th = load_10th_data()
data_inter = load_inter_data()

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Main container */
.main .block-container {
    padding-top: 1rem;
    max-width: 1100px;
}

/* App header */
.app-header {
    background: linear-gradient(135deg, #1E3A5F 0%, #2563EB 100%);
    color: white;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 2rem;
}
.app-header h1 { font-size: 2rem; font-weight: 700; margin: 0; }
.app-header p { font-size: 1rem; opacity: 0.85; margin-top: 0.5rem; }

/* Level selector cards */
.level-card {
    background: white;
    border: 2px solid #E2E8F0;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.level-card:hover {
    border-color: #2563EB;
    box-shadow: 0 8px 30px rgba(37,99,235,0.15);
    transform: translateY(-3px);
}
.level-card .icon { font-size: 3rem; margin-bottom: 0.75rem; }
.level-card h2 { font-size: 1.3rem; font-weight: 700; color: #1E3A5F; margin: 0; }
.level-card p { font-size: 0.875rem; color: #64748B; margin: 0.4rem 0 0; }

/* Opportunity category cards */
.cat-header {
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
}
.cat-header:hover { opacity: 0.9; }

/* Opportunity detail card */
.opp-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}
.opp-card h4 { color: #1E3A5F; font-size: 1.05rem; margin-bottom: 0.5rem; }
.opp-card .badge {
    display: inline-block;
    background: #EEF2FF;
    color: #3730A3;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
}
.opp-card .badge-green {
    background: #ECFDF5;
    color: #065F46;
}
.opp-card .badge-orange {
    background: #FFFBEB;
    color: #92400E;
}
.opp-card .badge-red {
    background: #FEF2F2;
    color: #991B1B;
}

/* Link chips */
.link-chip {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
    font-size: 0.78rem;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
    text-decoration: none;
}

/* Step indicator */
.step-bar {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}
.step {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
}
.step.active { background: #2563EB; color: white; }
.step.done { background: #059669; color: white; }
.step.pending { background: #E2E8F0; color: #94A3B8; }
.step-line { width: 40px; height: 2px; background: #E2E8F0; align-self: center; border-radius: 2px; }
.step-line.done { background: #059669; }

/* Form sections */
.form-section {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.form-section h3 { color: #1E3A5F; font-size: 1rem; font-weight: 700; margin-bottom: 1rem; }

/* Progress steps */
.progress-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 0.9rem;
    font-weight: 500;
}
.progress-step.done { background: #ECFDF5; color: #065F46; }
.progress-step.active { background: #EFF6FF; color: #1D4ED8; }
.progress-step.pending { background: #F8FAFC; color: #94A3B8; }

/* Guidance output */
.guidance-container {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 2rem;
    line-height: 1.75;
}

/* Summary banner */
.summary-banner {
    background: linear-gradient(135deg, #059669, #0891B2);
    color: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Download button */
.download-section {
    background: #1E3A5F;
    color: white;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin-top: 1.5rem;
}

/* Stream selector */
.stream-pill {
    display: inline-block;
    padding: 0.5rem 1.25rem;
    border-radius: 25px;
    border: 2px solid #E2E8F0;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.15s;
    margin: 4px;
}
.stream-pill.selected {
    background: #2563EB;
    border-color: #2563EB;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ──────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "home",       # home | explore | form | processing | results
        "level": None,           # "10th Completed" | "Inter Completed"
        "stream": None,
        "profile": {},
        "guidance_data": None,
        "pdf_bytes": None,
        "active_category": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Navigation helpers ──────────────────────────────────────────────────────
def go(screen): st.session_state.screen = screen; st.rerun()

# ── Step indicator ──────────────────────────────────────────────────────────
def render_steps(current):
    steps = ["Choose Level", "Explore", "Your Details", "Guidance"]
    screen_order = ["home", "explore", "form", "processing", "results"]
    idx = screen_order.index(current) if current in screen_order else 0

    html = '<div class="step-bar">'
    for i, s in enumerate(steps):
        si = i + 1
        if i < idx:
            cls = "done"
            icon = "✓"
        elif i == idx or (current == "processing" and i == 2):
            cls = "active"
            icon = str(si)
        else:
            cls = "pending"
            icon = str(si)
        html += f'<div class="step {cls}" title="{s}">{icon}</div>'
        if i < len(steps) - 1:
            line_cls = "done" if i < idx - 1 else ""
            html += f'<div class="step-line {line_cls}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
def screen_home():
    st.markdown("""
    <div class="app-header">
        <h1>🎓 Career Guidance Agent</h1>
        <p>Personalised career roadmap for every student — no opportunity missed</p>
    </div>
    """, unsafe_allow_html=True)

    render_steps("home")

    st.markdown("### Select your education level to begin")
    st.markdown(" ")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        if st.button("🎒  10th Completed", use_container_width=True, key="btn_10th",
                     help="Explore all paths after completing 10th standard"):
            st.session_state.level = "10th Completed"
            st.session_state.stream = None
            go("explore")
        st.markdown("""
        <div style="text-align:center; color:#64748B; font-size:0.875rem; margin-top:0.5rem;">
        15+ career paths • Polytechnic • ITI • RGUKT • Defence • Govt Jobs
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🎓  Inter Completed", use_container_width=True, key="btn_inter",
                     help="Explore all paths after completing Intermediate / 12th"):
            st.session_state.level = "Inter Completed"
            go("stream_select")
        st.markdown("""
        <div style="text-align:center; color:#64748B; font-size:0.875rem; margin-top:0.5rem;">
        Engineering • Medical • CA • Law • Defence • Banking • Civil Services
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Career Paths", "25+", "Comprehensive")
    c2.metric("Official Sites", "30+", "Live Data")
    c3.metric("Scholarships", "20+", "All Categories")
    c4.metric("Govt Job Paths", "15+", "AP & TS Focus")

# ══════════════════════════════════════════════════════════════════════════════
# STREAM SELECT (for Inter students)
# ══════════════════════════════════════════════════════════════════════════════
def screen_stream_select():
    st.markdown("""
    <div class="app-header">
        <h1>🎓 Inter Completed — Select Your Stream</h1>
        <p>Choose your stream to see relevant opportunities</p>
    </div>
    """, unsafe_allow_html=True)

    streams = {
        "MPC": {"icon": "📐", "desc": "Maths, Physics, Chemistry — Engineering, Sciences, Architecture"},
        "BiPC": {"icon": "🧬", "desc": "Biology, Physics, Chemistry — Medical, Pharmacy, Nursing"},
        "MEC": {"icon": "📊", "desc": "Maths, Economics, Commerce — CA, Finance, Law, Business"},
        "CEC": {"icon": "💼", "desc": "Civics, Economics, Commerce — Commerce, Banking, Law"},
        "HEC": {"icon": "📚", "desc": "History, Economics, Civics — Civil Services, Law, Humanities"},
        "Vocational": {"icon": "🛠️", "desc": "Vocational Groups — Skill-based careers, B.Voc programs"},
    }

    st.markdown("#### Select your Intermediate stream:")
    cols = st.columns(3)
    for i, (stream, info) in enumerate(streams.items()):
        with cols[i % 3]:
            if st.button(f"{info['icon']}  {stream}", key=f"stream_{stream}",
                         use_container_width=True):
                st.session_state.stream = stream
                go("explore")
            st.caption(info["desc"])

    st.markdown("---")
    if st.button("← Back", key="back_from_stream"):
        go("home")

# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — EXPLORE ALL OPPORTUNITIES
# ══════════════════════════════════════════════════════════════════════════════

def render_opportunity_card_10th(category: dict):
    """Render a single 10th opportunity category with expandable details."""
    cat_id = category["id"]
    title = category["title"]
    icon = category.get("icon", "📌")
    color = category.get("color", "#2563EB")
    summary = category.get("summary", "")

    with st.expander(f"{icon}  {title}", expanded=False):
        st.markdown(f'<p style="color:{color}; font-weight:600;">{summary}</p>',
                    unsafe_allow_html=True)

        # Intermediate groups have sub-groups
        if cat_id == "intermediate" and "groups" in category:
            tabs = st.tabs([g["name"].split("—")[0].strip() for g in category["groups"]])
            for i, group in enumerate(category["groups"]):
                with tabs[i]:
                    _render_inter_group(group)
            return

        # Other categories
        _render_general_category_10th(category)

def _render_inter_group(group: dict):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**🎯 Target:** {group.get('target', '')}")
        st.markdown(f"**⏱ Duration:** {group.get('duration', '')}")
        st.markdown(f"**✅ Eligibility:** {group.get('eligibility', '')}")

        boards = group.get("boards", [])
        if boards:
            st.markdown("**📋 Boards:**")
            for b in boards:
                st.markdown(f"&nbsp;&nbsp;• {b}")

    with col2:
        exams = group.get("competitive_exams", [])
        if exams:
            st.markdown("**📝 Entrance Exams:**")
            for e in exams:
                st.markdown(
                    f'&nbsp;&nbsp;• **{e["name"]}** — {e["for"]} '
                    f'<a href="https://{e["site"]}" target="_blank" class="link-chip">{e["site"]}</a>',
                    unsafe_allow_html=True
                )

    st.markdown("**🎓 Further Education:**")
    st.markdown("  " + "  •  ".join(group.get("further_education", [])))

    colleges = group.get("top_colleges_ap_ts", [])
    if colleges:
        st.markdown("**🏛️ Top Colleges (AP & Telangana):**")
        cols = st.columns(2)
        for j, c in enumerate(colleges):
            cols[j % 2].markdown(f"• {c}")

    govt = group.get("govt_jobs_after", [])
    if govt:
        st.markdown("**🏛️ Government Job Options:**")
        st.markdown("  " + "  •  ".join(govt))

    scholarships = group.get("scholarships", [])
    if scholarships:
        st.markdown("**💰 Scholarships:**")
        for s in scholarships:
            st.markdown(f"• {s}")

def _render_general_category_10th(cat: dict):
    """Render polytechnic, ITI, RGUKT, defence, govt jobs etc."""

    # Duration / eligibility at top
    if "duration" in cat:
        st.markdown(f"**⏱ Duration:** {cat['duration']}")
    if "eligibility" in cat:
        st.markdown(f"**✅ Eligibility:** {cat['eligibility']}")
    if "fee" in cat:
        st.info(f"💰 **Fee:** {cat['fee']}")

    col1, col2 = st.columns(2)

    with col1:
        # Entrance exams
        exams = cat.get("entrance_exams", [])
        if exams:
            st.markdown("**📝 Entrance Exams:**")
            for e in exams:
                st.markdown(
                    f'• **{e["name"]}** — {e.get("details", "")} '
                    f'<a href="https://{e["site"]}" target="_blank">🔗 {e["site"]}</a>',
                    unsafe_allow_html=True
                )

        # Single entrance exam
        if "entrance_exam" in cat:
            e = cat["entrance_exam"]
            st.markdown(f'**📝 Entrance:** {e["name"]} — {e.get("details", "")} '
                        f'<a href="https://{e["site"]}" target="_blank">🔗</a>',
                        unsafe_allow_html=True)

        # Trades / courses / branches
        for key, label in [("trades", "Trades"), ("branches", "Branches"),
                            ("courses", "Courses"), ("entries_after_10th", "Entry Options")]:
            items = cat.get(key, [])
            if items:
                st.markdown(f"**📋 {label}:**")
                if isinstance(items[0], dict):
                    for item in items:
                        name = item.get("name", "")
                        dur = item.get("duration", "")
                        demand = item.get("demand", "")
                        extra = f" ({dur})" if dur else ""
                        badge = f" 🔥 {demand}" if demand else ""
                        eligibility = item.get("eligibility", "")
                        elig_text = f" — {eligibility}" if eligibility else ""
                        st.markdown(f"• **{name}**{extra}{badge}{elig_text}")
                else:
                    cols = st.columns(2)
                    for j, it in enumerate(items):
                        cols[j % 2].markdown(f"• {it}")

    with col2:
        # Further education
        further = cat.get("further_education", [])
        if further:
            st.markdown("**🎓 Further Education:**")
            for f in further:
                st.markdown(f"• {f}")

        # Govt jobs
        govt = cat.get("govt_jobs", cat.get("govt_jobs_after", []))
        if govt:
            st.markdown("**🏛️ Government Jobs:**")
            if isinstance(govt, list):
                for g in govt:
                    if isinstance(g, dict):
                        st.markdown(f'• **{g["name"]}** <a href="https://{g["site"]}" target="_blank">🔗</a>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"• {g}")

        # Benefits (RGUKT etc)
        benefits = cat.get("benefits", [])
        if benefits:
            st.markdown("**🌟 Benefits:**")
            for b in benefits:
                st.markdown(f"• {b}")

        # Campuses
        campuses = cat.get("campuses", [])
        if campuses:
            st.markdown("**🏛️ Campuses:**")
            for c in campuses:
                st.markdown(
                    f'• **{c["name"]}** — {c["location"]} '
                    f'<a href="https://{c["site"]}" target="_blank">🔗</a>',
                    unsafe_allow_html=True
                )

    # Official sites always at bottom
    sites = cat.get("official_sites", [])
    if sites:
        st.markdown("**🌐 Official Websites:**")
        links = "  ".join([f'<a href="https://{s}" target="_blank" class="link-chip">🔗 {s}</a>' for s in sites])
        st.markdown(links, unsafe_allow_html=True)

    # Scholarships section
    if cat.get("id") == "scholarships_10th":
        _render_scholarships_section(cat)

def _render_scholarships_section(cat: dict):
    """Special rendering for scholarships."""
    tab_ap, tab_ts, tab_central, tab_pvt = st.tabs(
        ["AP Government", "TS Government", "Central Government", "Private"])

    with tab_ap:
        for s in cat.get("ap_scholarships", []):
            with st.container():
                st.markdown(f"**💰 {s['name']}**")
                st.markdown(f"Benefit: {s['benefit']}")
                st.markdown(f"Eligibility: {s.get('eligibility', '')}")
                st.markdown(f'🔗 <a href="https://{s["site"]}" target="_blank">{s["site"]}</a>',
                            unsafe_allow_html=True)
                st.divider()

    with tab_ts:
        for s in cat.get("ts_scholarships", []):
            st.markdown(f"**💰 {s['name']}**")
            st.markdown(f"Benefit: {s['benefit']}")
            st.markdown(f"Eligibility: {s.get('eligibility', '')}")
            st.markdown(f'🔗 <a href="https://{s["site"]}" target="_blank">{s["site"]}</a>',
                        unsafe_allow_html=True)
            st.divider()

    with tab_central:
        for s in cat.get("central_scholarships", []):
            st.markdown(f"**💰 {s['name']}**")
            st.markdown(f"Benefit: {s['benefit']}")
            st.markdown(f"Eligibility: {s.get('eligibility', '')}")
            st.markdown(f'🔗 <a href="https://{s["site"]}" target="_blank">{s["site"]}</a>',
                        unsafe_allow_html=True)
            st.divider()

    with tab_pvt:
        for s in cat.get("private_scholarships", []):
            st.markdown(f"**💰 {s['name']}**")
            st.markdown(f'🔗 <a href="https://{s["site"]}" target="_blank">{s["site"]}</a>',
                        unsafe_allow_html=True)
            st.divider()

def render_inter_stream_opportunities(stream: str):
    """Render opportunities for a specific inter stream."""
    stream_data = data_inter["streams"].get(stream, {})
    categories = stream_data.get("categories", [])

    if not categories:
        st.warning(f"Stream data for {stream} not found.")
        return

    st.markdown(f"### Opportunities for {stream_data.get('label', stream)}")

    for cat in categories:
        with st.expander(f"{cat.get('icon', '📌')}  {cat['title']}", expanded=False):
            col1, col2 = st.columns(2)
            color = cat.get("color", "#2563EB")
            st.markdown(f'<p style="color:{color}; font-weight:600;">{cat.get("summary", "")}</p>',
                        unsafe_allow_html=True)

            if "eligibility" in cat:
                st.markdown(f"**✅ Eligibility:** {cat['eligibility']}")

            with col1:
                exams = cat.get("entrance_exams", [])
                if exams:
                    st.markdown("**📝 Entrance Exams:**")
                    for e in exams:
                        details = e.get("details", "") or e.get("cutoff_general", "")
                        st.markdown(
                            f'• **{e["name"]}** — {details} '
                            f'<a href="https://{e["site"]}" target="_blank">🔗</a>',
                            unsafe_allow_html=True
                        )

                if "entrance_exam" in cat:
                    e = cat["entrance_exam"]
                    st.markdown(
                        f'**📝 Entrance:** {e["name"]} '
                        f'<a href="https://{e["site"]}" target="_blank">🔗</a>',
                        unsafe_allow_html=True
                    )

                courses = cat.get("courses", [])
                if courses:
                    st.markdown("**📋 Courses:**")
                    for c in courses:
                        if isinstance(c, dict):
                            dur = f" ({c.get('duration', '')})" if c.get('duration') else ""
                            st.markdown(f"• **{c['name']}**{dur}")
                        else:
                            st.markdown(f"• {c}")

                if "exams" in cat:
                    st.markdown("**📝 Exams to Target:**")
                    for e in cat["exams"]:
                        st.markdown(
                            f'• **{e["name"]}** — {e.get("details", "")} '
                            f'<a href="https://{e["site"]}" target="_blank">🔗</a>',
                            unsafe_allow_html=True
                        )

            with col2:
                colleges_ap = cat.get("top_colleges_ap_ts", cat.get("top_colleges", []))
                if colleges_ap:
                    st.markdown("**🏛️ Top Colleges:**")
                    for c in colleges_ap[:6]:
                        if isinstance(c, dict):
                            t = c.get("type", "")
                            site = c.get("site", "")
                            link = f' <a href="https://{site}" target="_blank">🔗</a>' if site else ""
                            badge = f' `{t}`' if t else ""
                            st.markdown(f"• **{c['name']}**{badge}{link}", unsafe_allow_html=True)
                        else:
                            st.markdown(f"• {c}")

                further = cat.get("further_education", [])
                if further:
                    st.markdown("**🎓 Further Education:**")
                    for f in further:
                        st.markdown(f"• {f}")

                govt = cat.get("govt_jobs", cat.get("govt_jobs_after", []))
                if govt:
                    st.markdown("**🏛️ Government Jobs:**")
                    for g in govt:
                        if isinstance(g, dict):
                            st.markdown(
                                f'• **{g["name"]}** <a href="https://{g["site"]}" target="_blank">🔗</a>',
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(f"• {g}")

            if "salary_outlook" in cat:
                s = cat["salary_outlook"]
                c1, c2, c3 = st.columns(3)
                c1.metric("Entry Level", s.get("entry", ""))
                c2.metric("3 Years", s.get("3_years", ""))
                c3.metric("5 Years", s.get("5_years", ""))

    # Common opportunities for all inter students
    st.markdown("---")
    st.markdown("### 🌟 Common Opportunities (All Inter Students)")

    common = data_inter.get("common_for_all_inter", {})

    with st.expander("🪖 Defence After Inter", expanded=False):
        entries = common.get("defence", {}).get("entries", [])
        for e in entries:
            stream_req = e.get("stream", "")
            badge = f" *({stream_req})*" if stream_req else ""
            st.markdown(
                f'• **{e["name"]}**{badge} — {e.get("details", "")} '
                f'<a href="https://{e["site"]}" target="_blank">🔗 {e["site"]}</a>',
                unsafe_allow_html=True
            )

    with st.expander("💰 Scholarships for Inter Students", expanded=False):
        sch = common.get("scholarships_inter", {})
        _render_scholarships_section(sch)

    with st.expander("🏛️ Civil Services Foundation — Start Now", expanded=False):
        cs = common.get("civil_services_foundation", {})
        st.info(cs.get("message", ""))
        for r in cs.get("resources", []):
            st.markdown(f'🔗 <a href="https://{r}" target="_blank">{r}</a>', unsafe_allow_html=True)

    with st.expander("🏦 Banking Preparation Foundation", expanded=False):
        bk = common.get("banking_foundation", {})
        st.info(bk.get("message", ""))
        for e in bk.get("exams", []):
            st.markdown(
                f'• **{e["name"]}** <a href="https://{e["site"]}" target="_blank">🔗</a>',
                unsafe_allow_html=True
            )

def screen_explore():
    level = st.session_state.level
    stream = st.session_state.stream

    st.markdown(f"""
    <div class="app-header">
        <h1>📚 All Opportunities After {level}</h1>
        <p>{'Stream: ' + stream if stream else 'Explore every path available to you — click any card to expand details'}</p>
    </div>
    """, unsafe_allow_html=True)

    render_steps("explore")

    # Top action buttons
    col_back, col_fwd = st.columns([1, 3])
    with col_back:
        if st.button("← Back", key="back_explore"):
            if level == "Inter Completed":
                go("stream_select")
            else:
                go("home")
    with col_fwd:
        if st.button("I've explored — Take me to personalised guidance →",
                     key="go_form", type="primary"):
            go("form")

    st.markdown("---")
    st.info("💡 **Tip:** Click any card below to expand and see full details — exam dates, eligibility, official links, colleges, scholarships and more.")

    if level == "10th Completed":
        categories = data_10th.get("categories", [])
        for cat in categories:
            render_opportunity_card_10th(cat)
    else:
        render_inter_stream_opportunities(stream)

    st.markdown("---")
    col_back2, col_fwd2 = st.columns([1, 3])
    with col_back2:
        if st.button("← Back", key="back_explore2"):
            go("stream_select" if level == "Inter Completed" else "home")
    with col_fwd2:
        if st.button("Proceed to Personalised Guidance →",
                     key="go_form2", type="primary"):
            go("form")

# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 3 — PERSONAL DETAILS FORM
# ══════════════════════════════════════════════════════════════════════════════

AP_TS_DISTRICTS = sorted([
    # Telangana
    "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon",
    "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar",
    "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad", "Mahabubnagar",
    "Mancherial", "Medak", "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool",
    "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
    "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet", "Suryapet",
    "Vikarabad", "Wanaparthy", "Warangal Rural", "Warangal Urban",
    "Yadadri Bhuvanagiri",
    # Andhra Pradesh
    "Alluri Sitharama Raju", "Anakapalli", "Anantapur", "Annamayya",
    "Bapatla", "Chittoor", "Dr B.R. Ambedkar Konaseema", "East Godavari",
    "Eluru", "Guntur", "Kakinada", "Krishna", "Kurnool", "Nandyal",
    "NTR (Vijayawada)", "Palnadu", "Parvathipuram Manyam", "Prakasam",
    "Sri Balaji (Tirupati)", "Sri Sathya Sai", "Srikakulam", "Tirupati",
    "Visakhapatnam", "Vizianagaram", "West Godavari", "YSR Kadapa",
    # Other states
    "Other — Please specify in additional info"
])

INTERESTS = [
    "Maths and Problem Solving",
    "Physics and Science Experiments",
    "Biology and Living Things",
    "Computers and Programming",
    "Electronics and Circuits",
    "Business and Entrepreneurship",
    "Finance and Accounting",
    "Medicine and Healthcare",
    "Law and Justice",
    "Arts and Design",
    "Writing and Literature",
    "Teaching and Explaining",
    "Helping and Social Service",
    "Agriculture and Nature",
    "Mechanical and Automobile",
    "Construction and Architecture",
    "Defence and Police Service",
    "Sports and Physical Fitness",
    "Music and Performing Arts",
    "Research and Experiments",
]

def screen_form():
    level = st.session_state.level
    stream = st.session_state.stream

    st.markdown(f"""
    <div class="app-header">
        <h1>📝 Your Personal Profile</h1>
        <p>Tell us about yourself so we can guide you like a real counsellor</p>
    </div>
    """, unsafe_allow_html=True)

    render_steps("form")

    with st.form("student_profile_form"):
        # Basic info
        st.markdown("#### 👤 Basic Information")
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name *", placeholder="e.g. Ravi Kumar")
        gender = c2.selectbox("Gender *", ["Male", "Female", "Prefer not to say"])

        c3, c4 = st.columns(2)
        marks = c3.number_input(
            f"{'10th' if level == '10th Completed' else '12th/Inter'} Percentage *",
            min_value=0.0, max_value=100.0, value=65.0, step=0.5
        )
        state_choice = c4.selectbox("State", ["Telangana", "Andhra Pradesh", "Other State"])

        c5, c6 = st.columns(2)
        district = c5.selectbox("District *", AP_TS_DISTRICTS)
        school_type = c6.selectbox("School/College Type", ["Government", "Private", "Aided"])

        st.markdown("---")
        st.markdown("#### 🏷️ Category & Background")
        c7, c8 = st.columns(2)
        caste = c7.selectbox("Caste Category *", ["OC (Open Category)", "BC-A", "BC-B", "BC-C", "BC-D", "BC-E", "SC", "ST", "EWS", "Minority"])
        income = c8.selectbox("Family Annual Income *", [
            "Below Rs 50,000",
            "Rs 50,000 — Rs 1,00,000",
            "Rs 1,00,000 — Rs 2,50,000",
            "Rs 2,50,000 — Rs 5,00,000",
            "Rs 5,00,000 — Rs 10,00,000",
            "Above Rs 10,00,000"
        ])

        st.markdown("---")
        st.markdown("#### 🎯 Your Interests & Aptitudes")
        st.caption("Select all that apply — the more you select, the better we can guide you")

        cols = st.columns(2)
        selected_interests = []
        for i, interest in enumerate(INTERESTS):
            if cols[i % 2].checkbox(interest, key=f"interest_{i}"):
                selected_interests.append(interest)

        st.markdown("---")
        st.markdown("#### 💬 Anything Else?")
        additional = st.text_area(
            "Tell us more about yourself, specific goals, any constraints, or questions",
            placeholder="e.g. I want to become a doctor but NEET is tough. My family can only afford government college. I am also interested in computers...",
            height=100
        )

        st.markdown("---")
        submitted = st.form_submit_button(
            "🚀  Get My Personalised Career Guidance",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
                return
            if not selected_interests:
                st.warning("Please select at least one interest for better guidance.")

            st.session_state.profile = {
                "name": name.strip(),
                "level": level,
                "stream": stream or "N/A",
                "marks": marks,
                "gender": gender,
                "district": district,
                "state": state_choice,
                "school_type": school_type,
                "caste": caste,
                "income": income,
                "interests": selected_interests,
                "additional_info": additional.strip(),
            }
            go("processing")

    if st.button("← Back to Explore All Opportunities", key="back_form"):
        go("explore")

# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 4 — PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def screen_processing():
    profile = st.session_state.profile

    st.markdown(f"""
    <div class="app-header">
        <h1>🤖 AI Agent Working for You</h1>
        <p>Analysing your profile and searching live data — please wait...</p>
    </div>
    """, unsafe_allow_html=True)

    render_steps("processing")

    st.markdown(f"### Hello {profile.get('name', 'Student')}! Generating your personalised career guidance...")

    progress_steps = [
        ("📋", "Reading and analysing your complete profile"),
        ("🔍", "Searching latest exam notifications and cutoffs"),
        ("🏛️", "Finding top colleges matching your marks"),
        ("💰", "Checking scholarships you qualify for"),
        ("🏢", "Identifying government job opportunities"),
        ("🗺️", "Building your personalised career roadmap"),
        ("📄", "Preparing your detailed guidance report"),
    ]

    progress_container = st.container()
    status_text = st.empty()

    with progress_container:
        placeholders = []
        for icon, text in progress_steps:
            p = st.empty()
            p.markdown(
                f'<div class="progress-step pending">⏳ {icon} {text}...</div>',
                unsafe_allow_html=True
            )
            placeholders.append((p, icon, text))

    def update_ui_step(idx):
        for i, (p, icon, text) in enumerate(placeholders):
            if i < idx:
                p.markdown(
                    f'<div class="progress-step done">✅ {icon} {text}</div>',
                    unsafe_allow_html=True
                )
            elif i == idx:
                p.markdown(
                    f'<div class="progress-step active">🔄 {icon} {text}...</div>',
                    unsafe_allow_html=True
                )

    # Run agent
    from agent import get_career_guidance
    from pdf_generator import generate_pdf_report

    step_counter = [0]

    def progress_cb(msg):
        update_ui_step(step_counter[0])
        step_counter[0] += 1
        status_text.info(f"⏳ {msg}")

    try:
        guidance_data = get_career_guidance(profile, progress_callback=progress_cb)
        # Mark all done
        for i in range(len(placeholders)):
            update_ui_step(len(placeholders))

        status_text.success("✅ Guidance generation complete!")

        # Generate PDF
        with st.spinner("Generating your PDF report..."):
            pdf_bytes = generate_pdf_report(guidance_data)

        st.session_state.guidance_data = guidance_data
        st.session_state.pdf_bytes = pdf_bytes
        time.sleep(1)
        go("results")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API keys in .env file and try again.")
        if st.button("← Try Again"):
            go("form")

# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 5 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════

def screen_results():
    guidance_data = st.session_state.guidance_data
    pdf_bytes = st.session_state.pdf_bytes
    profile = guidance_data.get("profile", {})
    guidance_text = guidance_data.get("guidance", "")

    st.markdown(f"""
    <div class="app-header">
        <h1>🎯 Your Career Guidance Report</h1>
        <p>Personalised for {profile.get('name', 'you')} | {profile.get('level', '')}
        {' — ' + profile.get('stream', '') if profile.get('stream') != 'N/A' else ''}</p>
    </div>
    """, unsafe_allow_html=True)

    render_steps("results")

    # Download button at top
    col1, col2 = st.columns([3, 1])
    with col2:
        if pdf_bytes:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"career_guidance_{profile.get('name', 'student').replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

    # Profile summary strip
    st.markdown(
    f"""
    <div class="summary-banner">
        Student: {profile.get('name')} |
        Level: {profile.get('level')} |
        {f"Stream: {profile.get('stream')} |" if profile.get('stream') != 'N/A' else ''}
        Marks: {profile.get('marks')}% |
        District: {profile.get('district')} |
        Category: {profile.get('caste')}
    </div>
    """,
    unsafe_allow_html=True
)
    # Guidance text
    st.markdown("### 📋 Your Complete Career Guidance")
    st.markdown('<div class="guidance-container">', unsafe_allow_html=True)
    st.markdown(guidance_text)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download at bottom too
    st.markdown("---")
    if pdf_bytes:
        st.markdown("### 📥 Download Your Complete PDF Report")
        st.info("Your full career roadmap report with all opportunities, action plans, exam calendar, and scholarships is ready.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download PDF Career Report",
                data=pdf_bytes,
                file_name=f"career_guidance_{profile.get('name', 'student').replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

    st.markdown("---")
    cola, colb, colc = st.columns(3)
    with cola:
        if st.button("🔄 Start Over", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            go("home")
    with colb:
        if st.button("✏️ Update My Profile", use_container_width=True):
            go("form")
    with colc:
        if st.button("📚 Explore Opportunities Again", use_container_width=True):
            go("explore")

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════

screen = st.session_state.screen

if screen == "home":
    screen_home()
elif screen == "stream_select":
    screen_stream_select()
elif screen == "explore":
    screen_explore()
elif screen == "form":
    screen_form()
elif screen == "processing":
    screen_processing()
elif screen == "results":
    screen_results()
else:
    screen_home()



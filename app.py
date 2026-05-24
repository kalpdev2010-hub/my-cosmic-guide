import streamlit as st
import datetime
import requests

# Permanent custom birth chart coordinates
MY_PROFILE = {
    "ascendant_lagna": "Pisces",
    "birth_nakshatra": "Ardra",
    "moon_sign": "Gemini"
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", 
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

TARABALA_MATRIX = {
    1: {"name": "Janma Tara (Volatile)", "status": "❌ Avoid", "vibe": "Focus on routine care; avoid major physical operations or high-stakes initiations."},
    2: {"name": "Sampat Tara (Prosperous)", "status": "🟢 Exceptional", "vibe": "Elite alignment for wealth generation, asset purchases, and financial trading."},
    3: {"name": "Vipat Tara (High Risk)", "status": "❌ Critical Alert", "vibe": "High risk of sudden operational setbacks. Postpone contract signatures."},
    4: {"name": "Kshema Tara (Protected)", "status": "🟢 Highly Secure", "vibe": "Safe, shielded window. Excellent for logistical planning and travel execution."},
    5: {"name": "Pratyak Tara (Obstacles)", "status": "❌ Minor Delays", "vibe": "Expect unexpected administrative friction. Double-check fine print details."},
    6: {"name": "Sadhana Tara (Success)", "status": "🟢 Elite Success", "vibe": "Outstanding frequency for closing sales and launching code upgrades."},
    7: {"name": "Naidhana Tara (Terminal)", "status": "❌ Deep Restriction", "vibe": "Strict boundary control needed. Postpone any high-stakes transactions."},
    8: {"name": "Mitra Tara (Harmonious)", "status": "🟢 Very Favorable", "vibe": "Highly supportive for strategic meetings, mediation, and client relationship upgrades."},
    9: {"name": "Param Mitra Tara (Supreme)", "status": "👑 Maximum Alignment", "vibe": "Flawless astronomical window for securing lifetime business partnerships."}
}

PLANET_THEMES = {
    "Sunday": {"planet": "Sun", "emoji": "☀️", "color": "#FF8C00", "bg": "#2b1a00", "vibe": "Pure Vitality & Leadership Aura Active"},
    "Monday": {"planet": "Moon", "emoji": "🌙", "color": "#A9A9A9", "bg": "#131822", "vibe": "Fluid Intuition & Emotional Clarity Active"},
    "Tuesday": {"planet": "Mars", "emoji": "💥", "color": "#FF4500", "bg": "#2b0b00", "vibe": "High-Drive Execution & Tactical Focus Active"},
    "Wednesday": {"planet": "Mercury", "emoji": "🌿", "color": "#00FF7F", "bg": "#00240f", "vibe": "Sharp Communication & Analytical Edge Active"},
    "Thursday": {"planet": "Jupiter", "emoji": "👑", "color": "#FFD700", "bg": "#2b2500", "vibe": "Supreme Wisdom & Massive Fortune Expansion Active"},
    "Friday": {"planet": "Venus", "emoji": "💎", "color": "#FF69B4", "bg": "#2b001a", "vibe": "Creative Masterclass & Asset Harmony Active"},
    "Saturday": {"planet": "Saturn", "emoji": "🪐", "color": "#4682B4", "bg": "#0d1b2a", "vibe": "Deep Focus, Structure & Discipline Active"}
}

DAILY_STYLE_LOOKUP = {
    "Monday": {"color": "White, Silver, or Cream", "grooming": "✅ Safe for hair & nail cutting.", "task": "Routed excess funds toward liquid capital holdings."},
    "Tuesday": {"color": "Bright Red or Coral", "grooming": "❌ Avoid cutting hair or nails today (Mars energy).", "task": "Held firm boundaries against issuing new loans or debt liabilities."},
    "Wednesday": {"color": "Green or Pastel Shades", "grooming": "✅ Excellent day for grooming and personal care.", "task": "Audited active commercial contract terms or asset accounts."},
    "Thursday": {"color": "Golden Yellow or Saffron", "grooming": "⚠️ Avoid major haircuts to preserve Jupiter energy.", "task": "Verified allocation targets for compounding long-term assets (SIPs/ETFs)."},
    "Friday": {"color": "Clean White or Off-White", "grooming": "✅ Perfect for aesthetic grooming and spa routines.", "task": "Reviewed frontend performance metrics or creative UI adjustments."},
    "Saturday": {"color": "Black, Dark Blue, or Charcoal", "grooming": "❌ Strictly avoid hair and nail cutting today.", "task": "Dedicated execution strictly to structural backend cleanup or logistics data."},
    "Sunday": {"color": "Orange, Ruby Red, or Gold", "grooming": "Neutral day. Keep grooming minimal.", "task": "Completed an audit on asset balances and configured the upcoming weekly goals."}
}

MACRO_DATA = {
    "Weekly": {
        "job": {"good": "Strong communication surge early in the week; excellent for pitches, team syncs, and client updates.", "bad": "Friction during backend data updates mid-week. Keep file logs clean and backup assets."},
        "finance": {"good": "Liquid capital flow is stable; good for handling immediate operational invoices.", "bad": "Avoid quick retail overspending or speculative trading on Thursday afternoon."},
        "health": {"good": "High mental clarity and focus profiles for strategic tasks.", "bad": "Minor sleep inconsistencies. Reduce late-night display usage."},
        "relationship": {"good": "Supportive configurations for immediate professional and creative partnerships.", "bad": "Miscommunications possible under pressure. Verify instructions clearly."}
    },
    "Monthly": {
        "job": {"good": "Excellent phase for updating digital frameworks, frontend optimization, and performance tracking.", "bad": "Expect short-term delays from external vendors or regulatory steps."},
        "finance": {"good": "Strong returns on systemic investments (SIPs/ETFs) and structured savings fields.", "bad": "Check auto-renewals and hidden software subscription leakages."},
        "health": {"good": "Ideal month to establish solid nutritional and cardiovascular discipline.", "bad": "High mental load can induce eye strain or posture fatigue. Set screen breaks."},
        "relationship": {"good": "Great for collaborative work configurations and professional network visibility.", "bad": "Keep workspace discussions clear and separate from emotional assumptions."}
    },
    "Quarterly": {
        "job": {"good": "Major expansion capabilities. Excellent window for infrastructure upgrades and launching products.", "bad": "High competitive pressure in the market requires tight data security protocols."},
        "finance": {"good": "Opportunities to structure long-term commercial assets or capitalize on older investments.", "bad": "Avoid over-leveraging on fresh capital loans or massive commercial liabilities."},
        "health": {"good": "Vibrant physical recovery phases and strength gains under structured routines.", "bad": "Watch out for seasonal shifts causing digestive slowing or minor joint stiffness."},
        "relationship": {"good": "Alignments favor deep, long-range planning with primary key partners.", "bad": "Ensure legal agreements or divisions of responsibilities are explicit."}
    },
    "6 Months": {
        "job": {"good": "Transit support favors massive professional evolution, systemic restructuring, and scaling platforms.", "bad": "Hidden internal friction from old operational backlogs. Resolve database technical debt early."},
        "finance": {"good": "Substantial foundational asset growth. Excellent for structural corporate planning.", "bad": "Rahu/Ketu transits require total caution regarding opaque contracts or non-verified capital pools."},
        "health": {"good": "High nervous system resilience and stamina recovery windows.", "bad": "Do not skip regular health checkpoints or stress auditing metrics."},
        "relationship": {"good": "Excellent period to solidify your inner circle and eliminate distracting associations.", "bad": "Opaque communication blocks can create minor trust delays if not handled directly."}
    },
    "Yearly": {
        "job": {"good": "Foundational transit window for establishing market dominance, authority, and high-tier licensing upgrades.", "bad": "Saturn in the house of expenditure demands meticulous attention to commercial overhead costs."},
        "finance": {"good": "Major accumulation pathways open through disciplined, compounding asset vehicles.", "bad": "Strictly ban speculative or high-volatility financial exposure to preserve core wealth blocks."},
        "health": {"good": "Strong physical alignment when backed by long-term wellness frameworks.", "bad": "Prone to burnout from over-working. Enforce strict, non-negotiable downtime boundaries."},
        "relationship": {"good": "Major stabilizing energy for lifelong personal and professional bonds.", "bad": "Avoid business partnerships where roles and fiscal splits are not audited by a third party."}
    }
}

def get_live_nakshatra_and_tarabala(target_date):
    try:
        url = f"https://api.vedastro.org/api/Calculate/MoonConstellation/Location/25.2048,55.2708/Time/12:00/{target_date.strftime('%d-%m-%Y')}/+04:00"
        res = requests.get(url, timeout=4).json()
        current_star = res["Payload"]["Name"]
        if current_star not in NAKSHATRAS: raise Exception()
    except:
        base_date = datetime.date(2026, 5, 18)
        days_elapsed = (target_date - base_date).days
        current_star = NAKSHATRAS[(7 + days_elapsed) % 27]
    birth_idx = NAKSHATRAS.index(MY_PROFILE["birth_nakshatra"])
    curr_idx = NAKSHATRAS.index(current_star)
    star_distance = (curr_idx - birth_idx) % 27
    return current_star, TARABALA_MATRIX[(star_distance % 9) + 1]

# Advanced Multi-Sector Target Prediction Engine
def get_advanced_predictions(day_name, status_str):
    if "Exceptional" in status_str or "Supreme" in status_str or "Success" in status_str:
        return {
            "career": "🟢 **High Momentum:** Saturn transiting 10th from your Moon rewards precision logistics. Exalted Jupiter triggers clean strategic clarity. Execute platforms upgrades, update theme code structures, or deploy marketing modifications during peak hours.",
            "finance": "🟢 **Compounding Peak:** Excellent alignment for tracking Systematic Investment Plans (SIPs) or long-term fund positioning. A supportive window to audit structural cash reserves or route incoming revenue safely.",
            "health": "🟢 **Vital Recovery:** Jupiter casts its protective 9th aspect back onto your physical body (1st house). Immune vectors are boosted. High physical endurance window; execute demanding operational workflows confidently."
        }
    elif "Avoid" in status_str or "Alert" in status_str or "Restriction" in status_str:
        return {
            "career": "❌ **Consolidation Required:** Ambient friction could cause server delays or communicative bottlenecks with external distribution setups. Dedicate energy strictly to resolving technical debt, archiving old files, or sorting inventory frameworks.",
            "finance": "❌ **Defensive Posture:** Keep core capital reserves insulated. Postpone heavy initial investments into completely unverified commercial vendor frameworks or launching complex structural debts today.",
            "health": "⚠️ **Energy Drain Warning:** Saturn hovering in your 1st house can trigger physical fatigue or screen eye strain under heavy pressure. Set mandatory screen breaks and enforce firm boundary lines around sleep."
        }
    else:
        return {
            "career": "🟡 **Linear Progression:** Stable parameters for processing standard e-commerce tasks, coordinating client reports, and checking frontend analytics. Intuition is well-balanced for long-range optimization planning.",
            "finance": "🟡 **Stable Balance:** Safe configuration for micro-budget adjustments or routine banking transfers. Maintain your default compounding strategies; avoid quick high-risk retail speculation positions.",
            "health": "🟡 **Grounded Vitality:** Standard respiratory and nervous system stability. Keep posture aligned during long table sessions and maintain your standard hydration index."
        }

def get_dubai_rahu_kaal(day_name, target_date):
    try:
        url = f"https://api.sunrise-sunset.org/json?lat=25.2048&lng=55.2708&date={target_date.strftime('%Y-%m-%d')}&formatted=0"
        response = requests.get(url, timeout=4).json()
        if response["status"] == "OK":
            sunrise_local = datetime.datetime.fromisoformat(response["results"]["sunrise"]) + datetime.timedelta(hours=4)
            sunset_local = datetime.datetime.fromisoformat(response["results"]["sunset"]) + datetime.timedelta(hours=4)
        else: raise Exception()
    except:
        today_mid = datetime.datetime.combine(target_date, datetime.time(0, 0))
        sunrise_local = today_mid + datetime.timedelta(hours=6)
        sunset_local = today_mid + datetime.timedelta(hours=18, minutes=30)
    daylight_duration = sunset_local - sunrise_local
    start_time = sunrise_local + ((daylight_duration / 8) * {"Monday": 1, "Saturday": 2, "Friday": 3, "Wednesday": 4, "Thursday": 5, "Tuesday": 6, "Sunday": 7}.get(day_name, 0))
    return start_time.strftime("%I:%M %p"), (start_time + (daylight_duration / 8)).strftime("%I:%M %p")

def get_detailed_decision_matrix(day_name):
    matrix = {
        "Monday": {"wealth": "🟢 **Good:** Micro-investments or routing funds to liquid assets. Avoid risky speculative trading.", "business": "🟢 **Favorable:** Great for team coordination and creative brainstorming. Trust your gut.", "travel": "🟢 **Safe:** Peaceful short-distance transits.", "health": "🟡 **Neutral:** Prioritize hydration and rest.", "legal": "❌ **Avoid:** Do not execute adversarial legal settlements today."},
        "Tuesday": {"wealth": "❌ **Restriction:** Avoid signing major loan frameworks or lending capital.", "business": "🟢 **High Power:** Perfect for audits, technical execution, and operations maintenance.", "travel": "🟡 **Caution:** Keep transits brief and highly structured.", "health": "🟢 **Excellent:** High energy window. Ideal for medical adjustments.", "legal": "🟢 **Favorable:** Strong configuration for filing updates and formal contractual disputes."},
        "Wednesday": {"wealth": "🟢 **Auspicious:** Excellent for asset adjustments and checking account setups.", "business": "🟢 **Excellent:** Maximum commercial alignment for contract signing and marketing rollout.", "travel": "🟢 **Highly Favorable:** Top alignment for commercial logistics and inventory transit.", "health": "🟢 **Good:** Great day for neurological wellness, yoga, breathing exercises, and dietary adjustments.", "legal": "🟢 **Favorable:** Ideal for registration filings and partnership reviews."},
        "Thursday": {"wealth": "🟢 **Supreme Alignment:** Premier window for mutual fund review, long-term asset positioning, and setting strategic investments.", "business": "🟢 **Supreme Alignment:** Perfect for high-level meetings, system design, and launching major expansion steps.", "travel": "🟢 **Favorable:** Supports executive or commercial transit.", "health": "🟢 **Good:** Highly favorable for beginning systematic dietary regimens.", "legal": "🟢 **Excellent:** Exceptional protection for regulatory compliance reviews."},
        "Friday": {"wealth": "🟡 **Neutral:** Safe for regular budgeting; avoid allocating massive capital to heavy industrial stocks.", "business": "🟢 **Favorable:** Exceptional for front-facing marketing, PR events, and UI/UX reviews.", "travel": "🟢 **Safe:** Smooth, stress-free travel profiles.", "health": "🟡 **Neutral:** Rest up and avoid heavy, dense meals.", "legal": "🟡 **Neutral:** Safe for standard document processing."},
        "Saturday": {"wealth": "🟡 **Caution:** Avoid volatile trades. Favorable for physical assets or equipment purchases.", "business": "🟢 **Productive:** Lock down backend processing, data cleanups, and logistical maintenance.", "travel": "❌ **Avoid:** Postpone long personal journeys to bypass unexpected delays.", "health": "🟡 **Caution:** Watch joint strain. Excellent for deep rest cycles.", "legal": "🟡 **Neutral:** Slow movement; use strictly to review structural fine-print clauses."},
        "Sunday": {"wealth": "🟢 **Favorable:** Perfect window for asset audits and long-term asset balancing.", "business": "🟢 **High Alignment:** Elite configuration for corporate structuring and launching upcoming workflows.", "travel": "🟢 **Good:** Permanent, energetic transit windows.", "health": "🟢 **Excellent:** Excellent vitality indices.", "legal": "🟢 **Favorable:** Auspicious for managing governmental licensing or certificates."}
    }
    return matrix.get(day_name, matrix["Sunday"])

def get_hora_vibe(hora_planet):
    vibes = {"Jupiter": "🌟 **Auspicious Hour (Supreme):** Perfect for high-value financial actions, long-term investments, meeting mentors, and major decisions.", "Mercury": "🧠 **Intellectual Hour (Highly Productive):** Prime for signing contracts, sending key updates, coding, and analytical reviews.", "Venus": "🎨 **Creative Hour (Smooth):** Great for visual design, client relationship management, and personal comfort items.", "Moon": "🌊 **Intuitive Hour (Fluid):** Ideal for team alignment, conceptual brainstorming, and liquid capital shifts.", "Sun": "👑 **Authority Hour (Powerful):** Top configuration for leadership execution and connecting with executive decision-makers.", "Mars": "⚡ **Aggressive Hour (Volatile):** Best for auditing bugs and immediate execution. **Avoid** taking new liabilities or initiating sensitive arguments.", "Saturn": "⏳ **Delay Hour (Restrictive):** Focus purely on server maintenance, data archiving, and systemic admin processing. **Avoid** project kickoffs."}
    return vibes.get(hora_planet, "")

def calculate_hora_sequence(day_name):
    order = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    day_lords = {"Sunday": "Sun", "Monday": "Moon", "Tuesday": "Mars", "Wednesday": "Mercury", "Thursday": "Jupiter", "Friday": "Venus", "Saturday": "Saturn"}
    start_index = order.index(day_lords[day_name])
    return [(f"{(6 + i) % 24:02d}:00 - {(7 + i) % 24:02d}:00", order[(start_index + i) % 7]) for i in range(24)]

# Mobile UI Layout Configuration
st.set_page_config(page_title="Cosmic Guide", page_icon="🌙", layout="centered")

if "selected_date" not in st.session_state: 
    st.session_state.selected_date = datetime.date.today()

target_date = st.session_state.selected_date
day_name = target_date.strftime("%A")
theme = PLANET_THEMES[day_name]

# Global Custom Color CSS Injection
st.markdown(f"<style>.stApp {{background: linear-gradient(180deg, {theme['bg']} 0%, #0e1117 100%) !important; background-attachment: fixed !important;}}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 26px; font-weight: bold; margin-bottom: 0px; text-align: center;'>🔱 My Daily Cosmic Guide</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 13px; color: #808495; margin-top: 2px; margin-bottom: 10px;'>Lagna: Pisces | Birth Star: Ardra | Rashi: Gemini</p>", unsafe_allow_html=True)

view_mode = st.radio("Select View Mode:", ["☀️ Daily Engine", "🌌 Macro Horizons"], horizontal=True)

st.write("---")

if view_mode == "☀️ Daily Engine":
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Yesterday", use_container_width=True): st.session_state.selected_date = datetime.date.today() - datetime.timedelta(days=1)
    with col2:
        if st.button("☀️ Today", use_container_width=True): st.session_state.selected_date = datetime.date.today()
    with col3:
        if st.button("➡️ Tomorrow", use_container_width=True): st.session_state.selected_date = datetime.date.today() + datetime.timedelta(days=1)

    calendar_date = st.date_input("Or look up an alternative date:", value=st.session_state.selected_date)
    if calendar_date != st.session_state.selected_date: st.session_state.selected_date = calendar_date

    target_date = st.session_state.selected_date
    day_name = target_date.strftime("%A")
    theme = PLANET_THEMES[day_name]
    style_info = DAILY_STYLE_LOOKUP[day_name]
    current_star, tarabala = get_live_nakshatra_and_tarabala(target_date)
    rahu_start, rahu_end = get_dubai_rahu_kaal(day_name, target_date)
    
    # Generate Advanced Multi-Sector Predictions
    preds = get_advanced_predictions(day_name, tarabala["status"])

    st.markdown(f'<div style="background-color: {theme["bg"]}; border-left: 5px solid {theme["color"]}; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);"><span style="font-size: 24px; float: right;">{theme["emoji"]}</span><h3 style="margin: 0; color: {theme["color"]}; font-size: 15px; font-weight: bold; letter-spacing: 0.5px;">DAY INFLUENCER: {theme["planet"].upper()}</h3><p style="margin: 5px 0 0 0; color: #ffffff; font-size: 13px; font-style: italic; opacity: 0.9;">{theme["vibe"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background-color: #0b1511; border-left: 5px solid #00FF7F; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);"><span style="font-size: 18px; float: right;">✨</span><h3 style="margin: 0; color: #00FF7F; font-size: 14px; font-weight: bold;">STAR TIMING: {current_star.upper()} ({tarabala["status"]})</h3><p style="margin: 3px 0 0 0; color: #ffffff; font-size: 13px; font-weight: bold;">{tarabala["name"]}</p><p style="margin: 3px 0 0 0; color: #cccccc; font-size: 12px; opacity: 0.85;">{tarabala["vibe"]}</p></div>', unsafe_allow_html=True)
    
    # RESTORED / UPGRADED: Unified Gochar Target Predictions Section
    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>🔮 Gochar Forecast (Predictions)</h2>", unsafe_allow_html=True)
    with st.expander("💼 Career Prediction", expanded=True):
        st.write(preds["career"])
    with st.expander("💰 Finance Prediction", expanded=False):
        st.write(preds["finance"])
    with st.expander("🏥 Health Prediction", expanded=False):
        st.write(preds["health"])
        
    st.error(f"🛑 **Critical Restriction Window (Dubai):** Avoid executing high-stakes business deals today during **Rahu Kaal: {rahu_start} - {rahu_end}**.")

    # Interactive Checklist Scorecard Module
    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>📊 Daily Alignment Scorecard</h2>", unsafe_allow_html=True)
    
    d_key = target_date.strftime("%Y%m%d")
    c1 = st.checkbox(f"Wore matching apparel frequencies ({style_info['color']})", key=f"c1_{d_key}")
    c2 = st.checkbox(f"Complied with daily personal care directives ({style_info['grooming'].split('.')[0]})", key=f"c2_{d_key}")
    c3 = st.checkbox(f"Executed specific core asset mandate: {style_info['task']}", key=f"c3_{d_key}")
    c4 = st.checkbox(f"Safely circumnavigated Dubai Rahu Kaal window boundary limits", key=f"c4_{d_key}")
    
    completed = sum([c1, c2, c3, c4])
    score_pct = int((completed / 4) * 100)
    
    st.progress(completed / 4)
    if score_pct == 100:
        st.success("🏆 **Flawless Harmonization!** You are completely aligned with the planetary currents today.")
    else:
        st.caption(f"Current alignment score index: **{score_pct}%**")

    st.write("---")

    st.markdown(f"<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>✨ Decision Matrix for {day_name}</h2>", unsafe_allow_html=True)
    decisions = get_detailed_decision_matrix(day_name)

    with st.expander("🎨 Styling & Clothing Color", expanded=False): st.info(f"**Recommended Colors for {day_name}:**\n\n{style_info['color']}")
    with st.expander("💇‍♂️ Personal Care & Grooming", expanded=False): st.warning(f"**Grooming Directives:**\n\n{style_info['grooming']}")
    with st.expander("💰 Wealth & Investments", expanded=False): st.write(decisions["wealth"])
    with st.expander("💼 Business & Career", expanded=False): st.write(decisions["business"])
    with st.expander("✈️ Travel & Relocation", expanded=False): st.write(decisions["travel"])
    with st.expander("🏥 Health & Medical", expanded=False): st.write(decisions["health"])
    with st.expander("⚖️ Property & Legal", expanded=False): st.write(decisions["legal"])

    st.write("---")
    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 10px; margin-bottom: 5px;'>⏰ Hourly Time Planner (Hora)</h2>", unsafe_allow_html=True)
    hora_list = calculate_hora_sequence(day_name)
    local_now = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    selected_slot = st.selectbox("Choose a time block to inspect:", options=[f"{s[0]} (Ruled by {s[1]})" for s in hora_list], index=(local_now.hour - 6) % 24)
    st.info(get_hora_vibe(selected_slot.split("Ruled by ")[1].replace(")", "")))

else:
    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 0px; margin-bottom: 5px;'>🌌 Long-Range Macro Architecture</h2>", unsafe_allow_html=True)
    horizon = st.selectbox("Choose Time Horizon Window:", ["Weekly", "Monthly", "Quarterly", "6 Months", "Yearly"])
    
    data = MACRO_DATA[horizon]
    sectors = [
        {"name": "💼 Job & Career", "key": "job"},
        {"name": "💰 Finance & Wealth", "key": "finance"},
        {"name": "🏥 Health & Wellness", "key": "health"},
        {"name": "🤝 Relationships & Alliances", "key": "relationship"}
    ]
    
    for s in sectors:
        st.markdown(f"<h3 style='font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>{s['name']}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: #111622; padding: 12px; border-radius: 8px; box-shadow: 0px 2px 6px rgba(0,0,0,0.2);">
            <p style="margin: 0px 0px 6px 0px; font-size: 13px; color: #00FF7F;">🟢 <b>Favorable (Good):</b> {data[s['key']]['good']}</p>
            <p style="margin: 0; font-size: 13px; color: #FF4500;">❌ <b>Caution (Bad):</b> {data[s['key']]['bad']}</p>
        </div>
        """, unsafe_allow_html=True)

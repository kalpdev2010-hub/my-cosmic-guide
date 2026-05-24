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

# Restored Core Grooming & Appearance Engine
DAILY_STYLE_LOOKUP = {
    "Monday": {"color": "White, Silver, or Cream", "grooming": "✅ Safe for hair & nail cutting."},
    "Tuesday": {"color": "Bright Red or Coral", "grooming": "❌ Avoid cutting hair or nails today (Mars energy)."},
    "Wednesday": {"color": "Green or Pastel Shades", "grooming": "✅ Excellent day for grooming and personal care."},
    "Thursday": {"color": "Golden Yellow or Saffron", "grooming": "⚠️ Avoid major haircuts to preserve Jupiter energy."},
    "Friday": {"color": "Clean White or Off-White", "grooming": "✅ Perfect for aesthetic grooming and spa routines."},
    "Saturday": {"color": "Black, Dark Blue, or Charcoal", "grooming": "❌ Strictly avoid hair and nail cutting today."},
    "Sunday": {"color": "Orange, Ruby Red, or Gold", "grooming": "Neutral day. Keep grooming minimal."}
}

def get_live_nakshatra_and_tarabala(target_date):
    try:
        url = f"https://api.vedastro.org/api/Calculate/MoonConstellation/Location/25.2048,55.2708/Time/12:00/{target_date.strftime('%d-%m-%Y')}/+04:00"
        res = requests.get(url, timeout=4).json()
        current_star = res["Payload"]["Name"]
        if current_star not in NAKSHATRAS:
            raise Exception()
    except:
        base_date = datetime.date(2026, 5, 18)
        days_elapsed = (target_date - base_date).days
        current_star = NAKSHATRAS[(7 + days_elapsed) % 27]

    birth_idx = NAKSHATRAS.index(MY_PROFILE["birth_nakshatra"])
    curr_idx = NAKSHATRAS.index(current_star)
    
    star_distance = (curr_idx - birth_idx) % 27
    tarabala_score = (star_distance % 9) + 1
    return current_star, TARABALA_MATRIX[tarabala_score]

def get_dubai_rahu_kaal(day_name, target_date):
    try:
        url = f"https://api.sunrise-sunset.org/json?lat=25.2048&lng=55.2708&date={target_date.strftime('%Y-%m-%d')}&formatted=0"
        response = requests.get(url, timeout=4).json()
        if response["status"] == "OK":
            sunrise_local = datetime.datetime.fromisoformat(response["results"]["sunrise"]) + datetime.timedelta(hours=4)
            sunset_local = datetime.datetime.fromisoformat(response["results"]["sunset"]) + datetime.timedelta(hours=4)
        else:
            raise Exception()
    except:
        today_mid = datetime.datetime.combine(target_date, datetime.time(0, 0))
        sunrise_local = today_mid + datetime.timedelta(hours=6)
        sunset_local = today_mid + datetime.timedelta(hours=18, minutes=30)

    daylight_duration = sunset_local - sunrise_local
    part_duration = daylight_duration / 8
    rahu_order = {"Monday": 1, "Saturday": 2, "Friday": 3, "Wednesday": 4, "Thursday": 5, "Tuesday": 6, "Sunday": 7}
    
    target_part = rahu_order.get(day_name, 0)
    start_time = sunrise_local + (part_duration * target_part)
    end_time = start_time + part_duration
    return start_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p")

def get_detailed_decision_matrix(day_name):
    matrix = {
        "Monday": {"wealth": "🟢 **Good:** Micro-investments or routing funds to liquid assets. Avoid risky speculative trading.", "business": "🟢 **Favorable:** Great for team coordination and creative brainstorming. Trust your gut.", "travel": "🟢 **Safe:** Peaceful short-distance transits.", "health": "🟡 **Neutral:** Prioritize hydration and rest.", "legal": "❌ **Avoid:** Do not execute adversarial legal settlements today."},
        "Tuesday": {"wealth": "❌ **Restriction:** Avoid signing major loan frameworks or lending capital.", "business": "🟢 **High Power:** Perfect for audits, technical execution, and operations maintenance.", "travel": "🟡 **Caution:** Keep transits brief and highly structured.", "health": "🟢 **Excellent:** High energy window. Ideal for medical adjustments.", "legal": "🟢 **Favorable:** Strong configuration for filing updates and formal contractual disputes."},
        "Wednesday": {"wealth": "🟢 **Auspicious:** Excellent for asset adjustments and checking account setups.", "business": "🟢 **Excellent:** Maximum commercial alignment for contract signing and marketing rollout.", "travel": "🟢 **Highly Favorable:** Top alignment for commercial logistics and inventory transit.", "health": "🟢 **Good:** Great day for neurological wellness, yoga, breathing exercises, and dietary adjustments.", "legal": "🟢 **Favorable:** Ideal for registration filings and partnership reviews."},
        "Thursday": {"wealth": "🟢 **Supreme Alignment:** Premier window for mutual fund review, long-term asset positioning, and setting strategic investments.", "business": "🟢 **Supreme Alignment:** Perfect for high-level meetings, system design, and launching major expansion steps.", "travel": "🟢 **Favorable:** Supports executive or commercial transit.", "health": "🟢 **Good:** Highly favorable for beginning systematic dietary regimens.", "legal": "🟢 **Excellent:** Exceptional protection for regulatory compliance reviews."},
        "Friday": {"wealth": "🟡 **Neutral:** Safe for regular budgeting; avoid allocating massive capital to heavy industrial stocks.", "business": "🟢 **Favorable:** Exceptional for front-facing marketing, PR events, and UI/UX reviews.", "travel": "🟢 **Safe:** Smooth, stress-free travel profiles.", "health": "🟡 **Neutral:** Rest up and avoid heavy, dense meals.", "legal": "🟡 **Neutral:** Safe for standard document processing."},
        "Saturday": {"wealth": "🟡 **Caution:** Avoid volatile trades. Favorable for physical assets or equipment purchases.", "business": "🟢 **Productive:** Lock down backend processing, data cleanups, and logistical maintenance.", "travel": "❌ **Avoid:** Postpone long personal journeys to bypass unexpected delays.", "health": "🟡 **Caution:** Watch joint strain. Excellent for deep rest cycles.", "legal": "🟡 **Neutral:** Slow movement; use strictly to review structural fine-print clauses."},
        "Sunday": {"wealth": "🟢 **Favorable:** Perfect window for asset audits and long-term asset balancing.", "business": "🟢 **High Alignment:** Elite configuration for corporate structuring and launching upcoming workflows.", "travel": "🟢 **Good:** Energizing transit windows.", "health": "🟢 **Excellent:** Excellent vitality indices.", "legal": "🟢 **Favorable:** Auspicious for managing governmental licensing or certificates."}
    }
    return matrix.get(day_name, matrix["Sunday"])

def get_hora_vibe(hora_planet):
    vibes = {
        "Jupiter": "🌟 **Auspicious Hour (Supreme):** Perfect for high-value financial actions, long-term investments, meeting mentors, and major decisions.",
        "Mercury": "🧠 **Intellectual Hour (Highly Productive):** Prime for signing contracts, sending key updates, coding, and analytical reviews.",
        "Venus": "🎨 **Creative Hour (Smooth):** Great for visual design, client relationship management, and personal comfort items.",
        "Moon": "🌊 **Intuitive Hour (Fluid):** Ideal for team alignment, conceptual brainstorming, and liquid capital shifts.",
        "Sun": "👑 **Authority Hour (Powerful):** Top configuration for leadership execution and connecting with executive decision-makers.",
        "Mars": "⚡ **Aggressive Hour (Volatile):** Best for auditing bugs and immediate execution. **Avoid** taking new liabilities or initiating sensitive arguments.",
        "Saturn": "⏳ **Delay Hour (Restrictive):** Focus purely on server maintenance, data archiving, and systemic admin processing. **Avoid** project kickoffs."
    }
    return vibes.get(hora_planet, "")

def calculate_hora_sequence(day_name):
    order = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    day_lords = {"Sunday": "Sun", "Monday": "Moon", "Tuesday": "Mars", "Wednesday": "Mercury", "Thursday": "Jupiter", "Friday": "Venus", "Saturday": "Saturn"}
    start_index = order.index(day_lords[day_name])
    return [(f"{(6 + i) % 24:02d}:00 - {(7 + i) % 24:02d}:00", order[(start_index + i) % 7]) for i in range(24)]

# Mobile UI Configuration
st.set_page_config(page_title="Cosmic Guide", page_icon="🌙", layout="centered")

st.markdown("<h1 style='font-size: 26px; font-weight: bold; margin-bottom: 0px;'>🔱 My Daily Cosmic Guide</h1>", unsafe_allow_html=True)
st.caption(f"Lagna: Pisces | Birth Star: {MY_PROFILE['birth_nakshatra']} | Rashi: Gemini")

# Interactive State Engine for Date Selection
if "selected_date" not in st.session_state:
    st.session_state.selected_date = datetime.date.today()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Yesterday", use_container_width=True):
        st.session_state.selected_date = datetime.date.today() - datetime.timedelta(days=1)
with col2:
    if st.button("☀️ Today", use_container_width=True):
        st.session_state.selected_date = datetime.date.today()
with col3:
    if st.button("➡️ Tomorrow", use_container_width=True):
        st.session_state.selected_date = datetime.date.today() + datetime.timedelta(days=1)

calendar_date = st.date_input("Or look up an alternative date:", value=st.session_state.selected_date)
if calendar_date != st.session_state.selected_date:
    st.session_state.selected_date = calendar_date

target_date = st.session_state.selected_date
day_name = target_date.strftime("%A")

theme = PLANET_THEMES[day_name]
style_info = DAILY_STYLE_LOOKUP[day_name]
current_star, tarabala = get_live_nakshatra_and_tarabala(target_date)
rahu_start, rahu_end = get_dubai_rahu_kaal(day_name, target_date)

# Render: Day Influencer Card
st.markdown(f"""
<div style="background-color: {theme['bg']}; border-left: 5px solid {theme['color']}; padding: 15px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);">
    <span style="font-size: 24px; float: right;">{theme['emoji']}</span>
    <h3 style="margin: 0; color: {theme['color']}; font-size: 15px; font-weight: bold; letter-spacing: 0.5px;">DAY INFLUENCER: {theme['planet'].upper()}</h3>
    <p style="margin: 5px 0 0 0; color: #ffffff; font-size: 13px; font-style: italic; opacity: 0.9;">{theme['vibe']}</p>
</div>
""", unsafe_allow_html=True)

# Render: Live Star Strength Card (Tarabala)
st.markdown(f"""
<div style="background-color: #0b1511; border-left: 5px solid #00FF7F; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);">
    <span style="font-size: 18px; float: right;">✨</span>
    <h3 style="margin: 0; color: #00FF7F; font-size: 14px; font-weight: bold;">STAR TIMING: {current_star.upper()} ({tarabala['status']})</h3>
    <p style="margin: 3px 0 0 0; color: #ffffff; font-size: 13px; font-weight: bold;">{tarabala['name']}</p>
    <p style="margin: 3px 0 0 0; color: #cccccc; font-size: 12px; opacity: 0.85;">{tarabala['vibe']}</p>
</div>
""", unsafe_allow_html=True)

# Render: Rahu Kaal Banner
st.error(f"🛑 **Critical Restriction Window (Dubai):** Avoid executing high-stakes business deals, wire transfers, or asset commitments today during **Rahu Kaal: {rahu_start} - {rahu_end}**.")

# Render: Decision Matrix
st.markdown(f"<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>✨ Decision Matrix for {day_name}</h2>", unsafe_allow_html=True)
decisions = get_detailed_decision_matrix(day_name)

# RESTORED: Clean, highly visual dropdown blocks for appearance metrics
with st.expander("🎨 Styling & Clothing Color", expanded=False):
    st.info(f"**Recommended Colors for {day_name}:**\n\n{style_info['color']}")

with st.expander("💇‍♂️ Personal Care & Grooming", expanded=False):
    st.warning(f"**Grooming Directives:**\n\n{style_info['grooming']}")

with st.expander("💰 Wealth & Investments", expanded=False): st.write(decisions["wealth"])
with st.expander("💼 Business & Career", expanded=False): st.write(decisions["business"])
with st.expander("✈️ Travel & Relocation", expanded=False): st.write(decisions["travel"])
with st.expander("🏥 Health & Medical", expanded=False): st.write(decisions["health"])
with st.expander("⚖️ Property & Legal", expanded=False): st.write(decisions["legal"])

st.write("---")

# Render: Hora Dropdown
st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 10px; margin-bottom: 5px;'>⏰ Hourly Time Planner (Hora)</h2>", unsafe_allow_html=True)
st.caption("Plan your specific execution windows throughout the day:")

hora_list = calculate_hora_sequence(day_name)
local_now = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
default_slot_index = (local_now.hour - 6) % 24

dropdown_options = [f"{slot[0]} (Ruled by {slot[1]})" for slot in hora_list]
selected_slot = st.selectbox("Choose a time block to inspect:", options=dropdown_options, index=default_slot_index)

chosen_planet = selected_slot.split("Ruled by ")[1].replace(")", "")
st.info(get_hora_vibe(chosen_planet))

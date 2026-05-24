import streamlit as st
import datetime

# Permanent custom birth chart coordinates
MY_PROFILE = {
    "ascendant_lagna": "Pisces",
    "birth_nakshatra": "Ardra",
    "moon_sign": "Gemini",
    "benefic_planets": ["Jupiter", "Mars", "Moon"],
    "malefic_planets": ["Saturn", "Venus"]
}

# 1. Day-level rules engine
def get_detailed_decision_matrix(day_name):
    if day_name == "Monday":
        return {
            "wealth": "🟢 **Good:** Excellent for micro-investments, creative budgeting, or routing funds to liquid assets. Avoid high-risk speculative trading.",
            "business": "🟢 **Favorable:** Great day for team building, creative brainstorming, and client communications. Rely heavily on your intuition today.",
            "travel": "🟢 **Safe:** Short-distance travel or commuting yields peaceful outcomes. Ideal for domestic planning.",
            "health": "🟡 **Neutral:** Pay attention to hydration, diet, and mental rest. Good for beginning light wellness routines.",
            "legal": "❌ **Avoid:** Do not engage in aggressive legal battles or sign long-term adversarial settlements today."
        }
    elif day_name == "Tuesday":
        return {
            "wealth": "❌ **Strict Restriction:** Do not sign major loan papers or clear high-value liabilities unless absolutely mandatory. Do not lend cash.",
            "business": "🟢 **High Power:** Excellent for technical execution, audits, and resolving lingering internal operational backlogs.",
            "travel": "🟡 **Caution:** Avoid driving fast or initiating long, stressful journeys. Keep local travel structured.",
            "health": "🟢 **Excellent:** High vital energy. Perfect day for high-intensity physical training or starting medical recoveries.",
            "legal": "🟢 **Favorable:** Highly auspicious for filing cases, facing competition, or confronting complex contractual disputes."
        }
    elif day_name == "Wednesday":
        return {
            "wealth": "🟢 **Auspicious:** Top alignment for opening trading accounts, executing short-term investments, or negotiating payment terms.",
            "business": "🟢 **Excellent:** Maximum alignment for marketing campaigns, signing commercial vendor contracts, and launching digital assets.",
            "travel": "🟢 **Highly Favorable:** Excellent day for business-related travel, logistics coordination, or moving inventory.",
            "health": "🟢 **Good:** Great day for neurological wellness, yoga, breathing exercises, and dietary adjustments.",
            "legal": "🟢 **Favorable:** Ideal for document verification, licensing applications, and finalizing partnership mediation."
        }
    elif day_name == "Thursday":
        return {
            "wealth": "🟢 **Supreme Alignment:** The absolute best day for long-term wealth building, setting up systematic investment plans (SIPs), or managing mutual funds/ETFs.",
            "business": "🟢 **Supreme Alignment:** Perfect for high-level strategic planning, launching new business units, meeting mentors, and major corporate expansions.",
            "travel": "🟢 **Favorable:** Highly auspicious for long-distance travel, especially international or educational journeys.",
            "health": "🟢 **Good:** Excellent for liver health, systemic treatments, and incorporating traditional alternative therapies.",
            "legal": "🟢 **Excellent:** Supreme alignment for justice, clean compliance filings, and arbitration where you hold the moral ground."
        }
    elif day_name == "Friday":
        return {
            "wealth": "🟡 **Neutral:** Safe for routine spending or buying lifestyle items. Avoid routing massive capital into heavy industrial stocks today.",
            "business": "🟢 **Favorable:** Excellent day for creative design, UI/UX upgrades, media creation, hospitality, and public relations events.",
            "travel": "🟢 **Safe:** Excellent for luxury travel or personal vacations. Smooth, comfortable transit windows.",
            "health": "🟡 **Neutral:** Avoid overindulgence in sugary foods or heavy diets. Focus on relaxation and premium spa therapies.",
            "legal": "🟡 **Neutral:** Safe for routine corporate filings; defer major high-stakes litigations if possible."
        }
    elif day_name == "Saturday":
        return {
            "wealth": "🟡 **Caution:** Avoid quick-return, speculative bets. Highly favorable for purchasing long-term hard assets like land, steel, or warehouse machinery.",
            "business": "🟢 **Productive:** Dedicate today strictly to deep structural reorganization, database cleanup, maintenance, and warehouse logistics.",
            "travel": "❌ **Avoid:** Postpone non-essential long journeys. Saturn transits can create unexpected logistical delays.",
            "health": "🟡 **Caution:** Watch out for joint pain, bone health, or chronic fatigue. Excellent day for physical rest.",
            "legal": "🟡 **Neutral:** Slow progress. Good for reviewing fine-print clauses, but poor for seeking fast, immediate legal judgments."
        }
    elif day_name == "Sunday":
        return {
            "wealth": "🟢 **Favorable:** Excellent for tax planning, reviewing government bonds, or running high-level financial audits on your assets.",
            "business": "🟢 **High Alignment:** Perfect for setting executive goals, asserting leadership, and organizing your personal management schedule for the upcoming week.",
            "travel": "🟢 **Good:** Highly energizing travel, especially if traveling to meet authorities or heading out into sunny, open spaces.",
            "health": "🟢 **Excellent:** Heart, bone, and vision vitality are boosted. Great day for outdoor physical movement.",
            "legal": "🟢 **Favorable:** Strong alignment for dealing with governmental approvals, regulatory bodies, and compliance certificates."
        }

# 2. Hour-level (Hora) engine
def get_hora_vibe(hora_planet):
    if hora_planet == "Jupiter":
        return "🌟 **Auspicious Hour (Supreme):** Perfect for high-value financial transactions, long-term investments, meeting mentors, legal clarity, and major decisions."
    elif hora_planet == "Mercury":
        return "🧠 **Intellectual Hour (Highly Productive):** Excellent for signing contracts, sending important emails, marketing campaigns, coding, and analytical reviews."
    elif hora_planet == "Venus":
        return "🎨 **Creative Hour (Smooth):** Great for design work, client relationship building, purchasing luxury assets, and personal grooming/spa treatments."
    elif hora_planet == "Moon":
        return "🌊 **Intuitive Hour (Fluid):** Good for public relations, team meetings, creative conceptual planning, and liquid asset movements. Avoid high-risk bets."
    elif hora_planet == "Sun":
        return "👑 **Authority Hour (Powerful):** Top alignment for leadership execution, connecting with high-level executives or government officials, and setting goals."
    elif hora_planet == "Mars":
        return "⚡ **Aggressive Hour (Volatile):** Good for intense workouts, auditing errors, and swift execution. **Avoid** taking new loans, starting arguments, or signing peaceful deals."
    elif hora_planet == "Saturn":
        return "⏳ **Delay Hour (Restrictive):** Best used for routine maintenance, deep organizing, data cleaning, and heavy administrative work. **Avoid** launching new projects."

def calculate_hora_sequence(day_name):
    order = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    day_lords = {
        "Sunday": "Sun", "Monday": "Moon", "Tuesday": "Mars", 
        "Wednesday": "Mercury", "Thursday": "Jupiter", "Friday": "Venus", "Saturday": "Saturn"
    }
    
    start_planet = day_lords[day_name]
    start_index = order.index(start_planet)
    
    sequence = []
    for i in range(24):
        planet = order[(start_index + i) % 7]
        hour_num = (6 + i) % 24
        time_label = f"{hour_num:02d}:00 - {(hour_num + 1) % 24:02d}:00"
        sequence.append((time_label, planet))
    return sequence

# Mobile UI Layout Setup
st.set_page_config(page_title="Cosmic Guide", page_icon="🌙", layout="centered")

st.markdown("<h1 style='font-size: 26px; font-weight: bold; margin-bottom: 0px;'>🔱 My Daily Cosmic Guide</h1>", unsafe_allow_html=True)
st.caption(f"Lagna: {MY_PROFILE['ascendant_lagna']} | Nakshatra: {MY_PROFILE['birth_nakshatra']} | Rashi: {MY_PROFILE['moon_sign']}")

target_date = st.date_input("Select Date", datetime.date.today())
day_name = target_date.strftime("%A")

# Fix: Only this specific subheading line font size is reduced to 18px to ensure it fits perfectly in 1 line
st.markdown(f"<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>✨ Decision Matrix for {day_name}</h2>", unsafe_allow_html=True)
decisions = get_detailed_decision_matrix(day_name)

with st.expander("💰 Wealth & Investments", expanded=False):
    st.write(decisions["wealth"])
with st.expander("💼 Business & Career", expanded=False):
    st.write(decisions["business"])
with st.expander("✈️ Travel & Relocation", expanded=False):
    st.write(decisions["travel"])
with st.expander("🏥 Health & Medical", expanded=False):
    st.write(decisions["health"])
with st.expander("⚖️ Property & Legal", expanded=False):
    st.write(decisions["legal"])

st.write("---")

st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 10px; margin-bottom: 5px;'>⏰ Hourly Time Planner (Hora)</h2>", unsafe_allow_html=True)
st.caption("Plan your specific execution windows throughout the day:")

hora_list = calculate_hora_sequence(day_name)

# Dynamic local time calculation (UTC + 4 hours for Dubai local context)
local_now = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
current_hour = local_now.hour

default_slot_index = (current_hour - 6) % 24
dropdown_options = [f"{slot[0]} (Ruled by {slot[1]})" for slot in hora_list]

selected_slot = st.selectbox(
    "Choose a time block to inspect:",
    options=dropdown_options,
    index=default_slot_index
)

chosen_planet = selected_slot.split("Ruled by ")[1].replace(")", "")
st.info(get_hora_vibe(chosen_planet))

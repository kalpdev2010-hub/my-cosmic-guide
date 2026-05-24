import streamlit as st
import datetime

# Your permanent custom birth chart coordinates
MY_PROFILE = {
    "ascendant_lagna": "Pisces",
    "birth_nakshatra": "Ardra",
    "moon_sign": "Gemini",
    "benefic_planets": ["Jupiter", "Mars", "Moon"],
    "malefic_planets": ["Saturn", "Venus"]
}

def get_detailed_decision_matrix(day_name):
    # Advanced astrological decision rule-set customized for Pisces Lagna
    matrix = {}
    
    if day_name == "Monday":
        matrix = {
            "wealth": "🟢 **Good:** Excellent for micro-investments, creative budgeting, or routing funds to liquid assets. Avoid high-risk speculative trading.",
            "business": "🟢 **Favorable:** Great day for team building, creative brainstorming, and client communications. Rely heavily on your intuition today.",
            "travel": "🟢 **Safe:** short-distance travel or commuting yields peaceful outcomes. Ideal for domestic planning.",
            "health": "🟡 **Neutral:** Pay attention to hydration, diet, and mental rest. Good for beginning light wellness routines.",
            "legal": "❌ **Avoid:** Do not engage in aggressive legal battles or sign long-term adversarial settlements today."
        }
    elif day_name == "Tuesday":
        matrix = {
            "wealth": "❌ **Strict Restriction:** Do not sign major loan papers or clear high-value liabilities unless absolutely mandatory. Do not lend cash.",
            "business": "🟢 **High Power:** Excellent for technical execution, engineering tasks, audits, and resolving lingering internal operational backlogs.",
            "travel": "🟡 **Caution:** Avoid driving fast or initiating long, stressful journeys. Keep local travel structured.",
            "health": "🟢 **Excellent:** High vital energy. Perfect day for high-intensity physical training, surgeries, or starting aggressive medical recoveries.",
            "legal": "🟢 **Favorable:** Highly auspicious for filing cases, facing competition, or confronting complex contractual disputes."
        }
    elif day_name == "Wednesday":
        matrix = {
            "wealth": "🟢 **Auspicious:** Top alignment for opening trading accounts, executing short-term investments, or negotiating payment terms.",
            "business": "🟢 **Excellent:** Maximum alignment for marketing campaigns, signing commercial vendor contracts, and launching digital assets.",
            "travel": "🟢 **Highly Favorable:** Excellent day for business-related travel, logistics coordination, or moving inventory.",
            "health": "🟢 **Good:** Great day for neurological wellness, yoga, breathing exercises, and dietary adjustments.",
            "legal": "🟢 **Favorable:** Ideal for document verification, licensing applications, and finalizing partnership mediation."
        }
    elif day_name == "Thursday":
        matrix = {
            "wealth": "🟢 **Supreme Alignment:** The absolute best day for long-term wealth building, setting up systematic investment plans (SIPs), or managing mutual funds/ETFs.",
            "business": "🟢 **Supreme Alignment:** Perfect for high-level strategic planning, launching new business units, meeting mentors, and major corporate expansions.",
            "travel": "🟢 **Favorable:** Highly auspicious for long-distance travel, especially international or educational journeys.",
            "health": "🟢 **Good:** Excellent for liver health, systemic treatments, and incorporating traditional alternative therapies.",
            "legal": "🟢 **Excellent:** Supreme alignment for justice, clean compliance filings, and arbitration where you hold the moral ground."
        }
    elif day_name == "Friday":
        matrix = {
            "wealth": "🟡 **Neutral:** Safe for routine spending or buying lifestyle items. Avoid routing massive capital into heavy industrial stocks today.",
            "business": "🟢 **Favorable:** Excellent day for creative design, UI/UX upgrades, media creation, hospitality, and public relations events.",
            "travel": "🟢 **Safe:** Excellent for luxury travel or personal vacations. Smooth, comfortable transit windows.",
            "health": "🟡 **Neutral:** Avoid overindulgence in sugary foods or heavy diets. Focus on relaxation and premium spa therapies.",
            "legal": "🟡 **Neutral:** Safe for routine corporate filings; defer major high-stakes litigations if possible."
        }
    elif day_name == "Saturday":
        matrix = {
            "wealth": "🟡 **Caution:** Avoid quick-return, speculative bets. Highly favorable for purchasing long-term hard assets like land, steel, or warehouse machinery.",
            "business": "🟢 **Productive:** Dedicate today strictly to deep structural reorganization, database cleanup, maintenance, and warehouse logistics.",
            "travel": "❌ **Avoid:** Postpone non-essential long journeys. Saturn transits can create unexpected logistical delays or vehicle breakdowns.",
            "health": "🟡 **Caution:** Watch out for joint pain, bone health, or chronic fatigue. Excellent day for physical rest and structural therapy.",
            "legal": "🟡 **Neutral:** Slow progress. Good for reviewing fine-print clauses, but poor for seeking fast, immediate legal judgments."
        }
    elif day_name == "Sunday":
        matrix = {
            "wealth": "🟢 **Favorable:** Excellent for tax planning, reviewing government bonds, or running high-level financial audits on your assets.",
            "business": "🟢 **High Alignment:** Perfect for setting executive goals, asserting leadership, and organizing your personal management schedule for the upcoming week.",
            "travel": "🟢 **Good:** Highly energizing travel, especially if traveling to meet authorities or heading out into sunny, open spaces.",
            "health": "🟢 **Excellent:** Heart, bone, and vision vitality are boosted. Great day for outdoor physical movement and vitamin D absorption.",
            "legal": "🟢 **Favorable:** Strong alignment for dealing with governmental approvals, regulatory bodies, and compliance certificates."
        }
        
    return matrix

# Mobile UI Layout Setup
st.set_page_config(page_title="Cosmic Guide", page_icon="🌙", layout="centered")

st.markdown("<h1 style='font-size: 26px; font-weight: bold; margin-bottom: 0px;'>🔱 My Daily Cosmic Guide</h1>", unsafe_allow_html=True)
st.caption(f"Lagna: {MY_PROFILE['ascendant_lagna']} | Nakshatra: {MY_PROFILE['birth_nakshatra']} | Rashi: {MY_PROFILE['moon_sign']}")

target_date = st.date_input("Select Date", datetime.date.today())
day_name = target_date.strftime("%A")

decisions = get_detailed_decision_matrix(day_name)

st.subheader(f"✨ Decision Matrix for {day_name}")
st.write("---")

# Expandable/Scannable Category Blocks for easy decision making
with st.expander("💰 Wealth & Investments", expanded=True):
    st.write(decisions["wealth"])

with st.expander("💼 Business & Career", expanded=True):
    st.write(decisions["business"])

with st.expander("✈️ Travel & Relocation", expanded=True):
    st.write(decisions["travel"])

with st.expander("🏥 Health & Medical", expanded=True):
    st.write(decisions["health"])

with st.expander("⚖️ Property & Legal", expanded=True):
    st.write(decisions["legal"])

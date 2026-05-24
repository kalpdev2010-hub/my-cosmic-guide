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
    1: {"name": "Janma Tara (Volatile)", "status": "❌ Avoid", "vibe": "Focus on routine care; avoid major physical operations or high-stakes personal initiations."},
    2: {"name": "Sampat Tara (Prosperous)", "status": "🟢 Exceptional", "vibe": "Elite alignment for wealth generation, asset purchases, and financial growth."},
    3: {"name": "Vipat Tara (High Risk)", "status": "❌ Critical Alert", "vibe": "High risk of sudden operational setbacks. Postpone signing important personal contracts."},
    4: {"name": "Kshema Tara (Protected)", "status": "🟢 Highly Secure", "vibe": "Safe, shielded window. Excellent for logistical planning and personal travel execution."},
    5: {"name": "Pratyak Tara (Obstacles)", "status": "❌ Minor Delays", "vibe": "Expect unexpected administrative friction. Double-check fine print details."},
    6: {"name": "Sadhana Tara (Success)", "status": "🟢 Elite Success", "vibe": "Outstanding frequency for achieving workplace targets and personal goals."},
    7: {"name": "Naidhana Tara (Terminal)", "status": "❌ Deep Restriction", "vibe": "Strict personal boundary control needed. Postpone high-stakes commitments."},
    8: {"name": "Mitra Tara (Harmonious)", "status": "🟢 Very Favorable", "vibe": "Highly supportive for professional discussions, relationship upgrades, and collaboration."},
    9: {"name": "Param Mitra Tara (Supreme)", "status": "👑 Maximum Alignment", "vibe": "Flawless astronomical window for securing lifetime professional alliances."}
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
    "Monday": {"color": "White, Silver, or Cream", "grooming": "✅ Safe for hair & nail cutting.", "task": "Routed excess personal funds toward liquid capital holdings."},
    "Tuesday": {"color": "Bright Red or Coral", "grooming": "❌ Avoid cutting hair or nails today (Mars energy).", "task": "Held firm boundaries against taking on new personal liabilities or debts."},
    "Wednesday": {"color": "Green or Pastel Shades", "grooming": "✅ Excellent day for grooming and personal care.", "task": "Audited active workplace task lists, schedules, or personal asset accounts."},
    "Thursday": {"color": "Golden Yellow or Saffron", "grooming": "⚠️ Avoid major haircuts to preserve Jupiter energy.", "task": "Verified allocation targets for compounding long-term assets (SIPs/ETFs)."},
    "Friday": {"color": "Clean White or Off-White", "grooming": "✅ Perfect for aesthetic grooming and spa routines.", "task": "Reviewed personal workplace performance metrics or professional targets."},
    "Saturday": {"color": "Black, Dark Blue, or Charcoal", "grooming": "❌ Strictly avoid hair and nail cutting today.", "task": "Dedicated execution strictly to structural organizing, desk cleanup, or personal administration."},
    "Sunday": {"color": "Orange, Ruby Red, or Gold", "grooming": "Neutral day. Keep grooming minimal.", "task": "Completed an audit on personal savings and configured the upcoming weekly goals."}
}

MACRO_DATA = {
    "Weekly": {
        "job": {"good": "Strong communication surge early in the week; excellent for workplace discussions, scheduling, and presenting ideas.", "bad": "Friction during routine data management mid-week. Keep task logs clear and organized."},
        "finance": {"good": "Liquid capital flow is stable; good for handling immediate personal expenses or routine bills.", "bad": "Avoid impulsive retail spending or fast financial changes on Thursday afternoon."},
        "health": {"good": "High mental clarity and focus profiles for demanding workplace responsibilities.", "bad": "Minor sleep inconsistencies. Reduce late-night mobile screen usage."},
        "relationship": {"good": "Supportive configurations for immediate professional collaboration and workplace harmony.", "bad": "Miscommunications possible under professional pressure. Verify work instructions clearly."}
    },
    "Monthly": {
        "job": {"good": "Excellent phase for optimizing your daily workflow, showcasing job performance, and tracking productivity.", "bad": "Expect short-term administrative delays from external office systems or processing queues."},
        "finance": {"good": "Strong returns on systemic personal investments (SIPs/ETFs) and structured savings fields.", "bad": "Check auto-renewals on streaming accounts or hidden digital subscription leaks."},
        "health": {"good": "Ideal month to establish solid nutritional habits and cardiovascular exercise discipline.", "bad": "High mental workload can induce eye strain or posture fatigue. Take routine desk breaks."},
        "relationship": {"good": "Great for professional networking, office rapport, and visibility within your company.", "bad": "Keep workspace discussions objective and separate from personal feelings."}
    },
    "Quarterly": {
        "job": {"good": "Major professional capabilities. Excellent window for taking on workplace leadership roles or managing large projects.", "bad": "High task volume at your job requires sharp time-management and strict scheduling protocols."},
        "finance": {"good": "Opportunities to structure long-term personal assets or rebalance older investments.", "bad": "Avoid over-leveraging on unnecessary fresh personal loans or financial liabilities."},
        "health": {"good": "Vibrant physical recovery phases and strength gains under a structured wellness routine.", "bad": "Watch out for seasonal shifts causing minor digestive slowing or joint stiffness."},
        "relationship": {"good": "Alignments favor deep, long-range planning with primary trusted partners.", "bad": "Ensure shared financial or family responsibilities are explicitly discussed."}
    },
    "6 Months": {
        "job": {"good": "Transit support favors massive professional growth, expanding your career authority, and mastering workplace skills.", "bad": "Hidden stress from older, pending work assignments. Resolve administrative backlogs early."},
        "finance": {"good": "Substantial foundational savings growth. Excellent for structural financial planning.", "bad": "Rahu/Ketu transits require total caution regarding ambiguous financial schemes or non-verified funds."},
        "health": {"good": "High nervous system resilience and stamina recovery windows.", "bad": "Do not skip regular health checkpoints or stress auditing."},
        "relationship": {"good": "Excellent period to solidify your inner circle and eliminate distracting, draining associations.", "bad": "Opaque communication can create minor misunderstandings if not cleared up immediately."}
    },
    "Yearly": {
        "job": {"good": "Foundational transit window for establishing career stability, workplace authority, and professional respect.", "bad": "Saturn in your house of expenditure demands meticulous attention to your personal living overhead costs."},
        "finance": {"good": "Major accumulation pathways open through disciplined, compounding asset vehicles.", "bad": "Strictly ban high-volatility financial exposure to preserve your core wealth blocks."},
        "health": {"good": "Strong physical alignment when backed by long-term wellness frameworks.", "bad": "Prone to burnout from working long hours. Enforce strict, non-negotiable downtime boundaries."},
        "relationship": {"good": "Major stabilizing energy for lifelong personal and family bonds.", "bad": "Avoid complex personal financial loans where boundaries and repayments are not documented."}
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

# Dynamic Oracle Parsing Engine (Upgraded with Targeted Strategic Directives)
def evaluate_cosmic_oracle(question, day_name, tarabala):
    q = question.lower()
    is_good_tara = "❌" not in tarabala["status"]
    
    # 1. Targeted Segment: Money Lending & Debts (Mars Conflict Core)
    if any(w in q for w in ["lend", "lending", "borrow", "debt", "loan", "give money", "creditor"]):
        if day_name == "Tuesday":
            return "❌ **Oracle Directive: ABSOLUTELY DENIED.** Today is Tuesday, ruled directly by Mars. Classical Vedic principles heavily state that lending capital or initiating financial credits on a Tuesday traps the money in friction and delays. Do not distribute cash tokens today under any circumstance to preserve asset peace."
        elif day_name == "Saturday" or not is_good_tara:
            return "⏳ **Oracle Directive: ADVISE DELAY.** The background star matrix indicates restrictive or volatile patterns. Lending capital right now creates an asymmetric risk of baseline communication blocks. Hold your funds and table the discussion for a supportive Jupiter/Mercury day window."
        else:
            return "🟢 **Oracle Directive: APPROVED.** Frequencies are stable for managed transactions. Ensure the arrangement terms are documented clearly in writing, and execute outside of the local Dubai Rahu Kaal hour framework."

    # 2. Targeted Segment: Impulse Control, Habits & Compulsions (Rahu Illusion Shield)
    elif any(w in q for w in ["porn", "addiction", "habit", "urge", "relapse", "temptation", "impulse"]):
        if day_name in ["Tuesday", "Saturday"] or not is_good_tara:
            return "⚡ **Oracle Emergency Shield: ACTIVE.** Understand that the mental urge you are experiencing right now is an amplified cosmic shadow projection driven by Rahu friction. It is a temporary chemical illusion, not reality. **Actionable Step:** Shut down your mobile display immediately. Step into an open room or take a brisk walk for 15 minutes. Let this specific planetary frequency wave pass over your system without engaging it. Your core resilience is higher than the current transit pulse."
        else:
            return "🌱 **Oracle Support Directive:** Frequencies favor discipline and system cleansing today. Use this stable baseline window to redirect your focus into physical tasks, tracking compounding accounts, or organizing office logs. A short, focused wellness adjustment or breathing routine right now will completely stabilize your mental energy."

    # 3. Targeted Segment: Work Pressure & Stress Relief (Saturn Core)
    elif any(w in q for w in ["pressure", "stress", "workload", "deadline", "heavy", "tired", "burnout", "boss"]):
        return "⏳ **Oracle De-escalation Directive:** Saturn is currently transiting your 1st house (body), which amplifies physical sensations of workplace pressure and exhaustion. Realize that this heavy mental load is an environmental transit frequency, not a permanent limitation. **Actionable Step:** Do not execute defining decisions or send reactive updates right now. Break your workload into smaller segments. Dedicate the next upcoming Jupiter or Venus Hora block purely to silent, focused execution, and enforce an ironclad boundary around your evening rest."

    # 4. Targeted Segment: Personal Expenses & Outflows
    elif any(w in q for w in ["expense", "buy", "purchase", "spend", "cost", "bill", "pc", "laptop", "phone"]):
        if is_good_tara and day_name in ["Wednesday", "Thursday", "Friday"]:
            return "🟢 **Oracle Verdict: APPROVED.** Your current star frequency matches the active day lines beautifully. Asset processing, hardware optimization, or essential lifestyle allocations carry stable grounding. Execute your checkout during an active Mercury or Jupiter Hora block for seamless operational alignment."
        else:
            return "⏳ **Oracle Verdict: CHOOSE DEFENSIVE DELAY.** The current background current presents a restrictive environment for technical or capital outflows. Processing a physical purchase under this sky pattern can elevate risks of technical faults or transaction friction. Table the transaction for 24-48 hours."

    # 5. Targeted Segment: Food & Dietary Choices
    elif any(w in q for w in ["food", "diet", "meal", "eating", "fasting", "dinner", "lunch"]):
        if day_name in ["Tuesday", "Saturday"]:
            return "⚠️ **Oracle Wellness Check:** Ambient cosmic energy is dense today. Avoid heavy, oily, or highly processed meals which can trigger slow digestion and posture fatigue. Opt for light, clean vegetarian fuel to shield your physical body from Saturn's transit pressure."
        else:
            return "🟢 **Oracle Wellness Check:** Good configuration to nurture your physical system. Excellent window for hydration planning, consuming whole grains, and maintaining structural nutrition consistency."

    # Universal Fallback
    else:
        if is_good_tara:
            return f"✨ **Oracle Verdict: GENERALLY APPROVED.** Your active birth star timing is currently protected and supportive ({tarabala['name']}). Proceed with mindful attention to daily boundaries."
        else:
            return f"⏳ **Oracle Verdict: CHOOSE DEFENSIVE DELAY.** Your active star profile is transiting a restrictive phase ({tarabala['name']}). Classic Vedic planning recommends avoiding defining personal commitments for the next 24 hours."

def get_advanced_predictions(day_name, status_str):
    if "Exceptional" in status_str or "Supreme" in status_str or "Success" in status_str:
        return {
            "career": "🟢 **High Momentum:** Saturn transiting 10th from your Moon rewards workplace precision and discipline. Exalted Jupiter triggers clean professional clarity. Execute complex assignments, optimize your task schedules, or tackle critical workplace duties during peak hours.",
            "finance": "🟢 **Compounding Peak:** Excellent alignment for tracking personal Systematic Investment Plans (SIPs) or long-term fund positioning. A supportive window to audit personal savings or route income safely.",
            "health": "🟢 **Vital Recovery:** Jupiter casts its protective 9th aspect back onto your body (1st house). Immune vectors are boosted. High physical endurance window; execute demanding daily workflows confidently."
        }
    elif "Avoid" in status_str or "Alert" in status_str or "Restriction" in status_str:
        return {
            "career": "❌ **Consolidation Required:** Ambient friction could cause minor communication delays or administrative bottlenecks in daily office routines. Dedicate energy strictly to resolving pending task backlogs or organizing your personal schedule.",
            "finance": "❌ **Defensive Posture:** Keep core personal capital reserves insulated. Postpone heavy initial investments into unverified luxury items or taking on fresh personal financial obligations today.",
            "health": "⚠️ **Energy Drain Warning:** Saturn hovering in your 1st house can trigger physical fatigue or digital eye strain under high pressure. Set mandatory desk breaks and enforce firm boundaries around sleep."
        }
    else:
        return {
            "career": "🟡 **Linear Progression:** Stable parameters for processing standard job tasks, coordinating with professional colleagues, and reviewing daily outputs. Focus is well-aligned for steady, reliable execution.",
            "finance": "🟡 **Stable Balance:** Safe configuration for micro-budget adjustments or routine banking transfers. Maintain your default compounding strategies; avoid high-risk financial speculation.",
            "health": "🟡 **Grounded Vitality:** Standard physical and nervous system stability. Keep posture aligned during long desk sessions and maintain your standard hydration index."
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
        "Monday": {"wealth": "🟢 **Good:** Micro-investments or routing funds to liquid assets. Avoid risky speculative trading.", "business": "🟢 **Favorable:** Great for office teamwork, professional coordination, and clear workplace communication.", "travel": "🟢 **Safe:** Peaceful short-distance transits or commutes.", "health": "🟡 **Neutral:** Prioritize hydration and rest.", "legal": "❌ **Avoid:** Do not execute adversarial personal legal agreements today."},
        "Tuesday": {"wealth": "❌ **Restriction:** Avoid signing major personal loan frameworks or lending capital.", "business": "🟢 **High Power:** Perfect for organizing schedules, handling detailed reports, and executing pending job tasks.", "travel": "🟡 **Caution:** Keep transits brief and highly structured.", "health": "🟢 **Excellent:** High energy window. Ideal for starting workout variations or physical adjustments.", "legal": "🟢 **Favorable:** Strong configuration for filing updates and managing documentation."},
        "Wednesday": {"wealth": "🟢 **Auspicious:** Excellent for personal asset adjustments and reviewing account configurations.", "business": "🟢 **Excellent:** Maximum professional alignment for completing key assignments, sending important updates, and organizing tasks.", "travel": "🟢 **Highly Favorable:** Top alignment for professional logistics and work-related transits.", "health": "🟢 **Good:** Great day for neurological wellness, yoga, breathing exercises, and dietary adjustments.", "legal": "🟢 **Favorable:** Ideal for document registration filings and contract reviews."},
        "Thursday": {"wealth": "🟢 **Supreme Alignment:** Premier window for mutual fund review, long-term asset positioning, and setting strategic personal investments.", "business": "🟢 **Supreme Alignment:** Perfect for high-level career planning, aligning with professional mentors, and focusing on job growth.", "travel": "🟢 **Favorable:** Supports executive or career-related transit.", "health": "🟢 **Good:** Highly favorable for beginning systematic dietary regimens.", "legal": "🟢 **Excellent:** Exceptional protection for regulatory compliance reviews."},
        "Friday": {"wealth": "🟡 **Neutral:** Safe for regular budgeting; avoid allocating massive capital to high-risk stocks.", "business": "🟢 **Favorable:** Exceptional for front-facing collaboration, presentation reviews, and design tasks at your job.", "travel": "🟢 **Safe:** Smooth, stress-free travel profiles.", "health": "🟡 **Neutral:** Rest up and avoid heavy, dense meals.", "legal": "🟡 **Neutral:** Safe for standard document processing."},
        "Saturday": {"wealth": "🟡 **Caution:** Avoid volatile trades. Favorable for purchasing durable hard assets or necessary equipment.", "business": "🟢 **Productive:** Lock down backend documentation, personal schedule organization, and clearing administrative logs.", "travel": "❌ **Avoid:** Postpone long personal journeys to bypass unexpected delays.", "health": "🟡 **Caution:** Watch joint strain. Excellent for deep rest cycles.", "legal": "🟡 **Neutral:** Slow movement; use strictly to review structural fine-print clauses."},
        "Sunday": {"wealth": "🟢 **Favorable:** Perfect window for personal asset audits and long-term asset balancing.", "business": "🟢 **High Alignment:** Elite configuration for outlining upcoming workplace goals and structuring your personal task list.", "travel": "🟢 **Good:** Permanent, energetic transit windows.", "health": "🟢 **Excellent:** Excellent vitality indices.", "legal": "🟢 **Favorable:** Auspicious for managing personal licensing or certificates."}
    }
    return matrix.get(day_name, matrix["Sunday"])

def get_hora_vibe(hora_planet):
    vibes = {"Jupiter": "🌟 **Auspicious Hour (Supreme):** Perfect for high-value financial actions, long-term investments, meeting mentors, and major decisions.", "Mercury": "🧠 **Intellectual Hour (Highly Productive):** Prime for organizing schedules, sending key updates, coding, and analytical reviews.", "Venus": "🎨 **Creative Hour (Smooth):** Great for visual layout, professional communication, and personal comfort items.", "Moon": "🌊 **Intuitive Hour (Fluid):** Ideal for team coordination, conceptual brainstorming, and managing personal cash flows.", "Sun": "👑 **Authority Hour (Powerful):** Top configuration for leadership execution and connecting with executive decision-makers.", "Mars": "⚡ **Aggressive Hour (Volatile):** Best for clearing pending backlogs and immediate execution. **Avoid** taking new liabilities or initiating sensitive arguments.", "Saturn": "⏳ **Delay Hour (Restrictive):** Focus purely on routine filing, sorting archives, and systemic admin processing. **Avoid** project kickoffs."}
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
    
    preds = get_advanced_predictions(day_name, tarabala["status"])

    st.markdown(f'<div style="background-color: {theme["bg"]}; border-left: 5px solid {theme["color"]}; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);"><span style="font-size: 24px; float: right;">{theme["emoji"]}</span><h3 style="margin: 0; color: {theme["color"]}; font-size: 15px; font-weight: bold; letter-spacing: 0.5px;">DAY INFLUENCER: {theme["planet"].upper()}</h3><p style="margin: 5px 0 0 0; color: #ffffff; font-size: 13px; font-style: italic; opacity: 0.9;">{theme["vibe"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background-color: #0b1511; border-left: 5px solid #00FF7F; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);"><span style="font-size: 18px; float: right;">✨</span><h3 style="margin: 0; color: #00FF7F; font-size: 14px; font-weight: bold;">STAR TIMING: {current_star.upper()} ({tarabala["status"]})</h3><p style="margin: 3px 0 0 0; color: #ffffff; font-size: 13px; font-weight: bold;">{tarabala["name"]}</p><p style="margin: 3px 0 0 0; color: #cccccc; font-size: 12px; opacity: 0.85;">{tarabala["vibe"]}</p></div>', unsafe_allow_html=True)
    
    # Cosmic Decision Oracle Module
    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>🔮 Cosmic Decision Oracle</h2>", unsafe_allow_html=True)
    user_q = st.text_input("Ask a question regarding your day:", placeholder="e.g., Should I lend money today? / Urge help", key="oracle_query_input")
    
    if user_q:
        oracle_verdict = evaluate_cosmic_oracle(user_q, day_name, tarabala)
        st.markdown(f"""
        <div style="background-color: #171b26; border-radius: 8px; padding: 14px; border-left: 4px solid #9A7BFF; margin-bottom: 15px; box-shadow: 0px 2px 8px rgba(0,0,0,0.2);">
            <p style="margin: 0; font-size: 13px; color: #ffffff; line-height: 1.5;">{oracle_verdict}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>🔮 Gochar Forecast (Predictions)</h2>", unsafe_allow_html=True)
    with st.expander("💼 Job & Career Prediction", expanded=True): st.write(preds["career"])
    with st.expander("💰 Personal Finance Prediction", expanded=False): st.write(preds["finance"])
    with st.expander("🏥 Personal Health Prediction", expanded=False): st.write(preds["health"])
        
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
    with st.expander("💼 Job & Career Focus", expanded=False): st.write(decisions["business"])
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

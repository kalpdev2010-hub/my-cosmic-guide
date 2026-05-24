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
    1: {"name": "Janma Tara (Volatile)", "status": "❌ Avoid", "vibe": "Focus on routine care; avoid major physical changes or high-stakes personal initiations."},
    2: {"name": "Sampat Tara (Prosperous)", "status": "🟢 Exceptional", "vibe": "Elite alignment for personal wealth generation, asset purchases, and financial growth."},
    3: {"name": "Vipat Tara (High Risk)", "status": "❌ Critical Alert", "vibe": "High risk of sudden personal setbacks. Postpone signing important private commitments."},
    4: {"name": "Kshema Tara (Protected)", "status": "🟢 Highly Secure", "vibe": "Safe, shielded window. Excellent for lifestyle logistics and personal travel execution."},
    5: {"name": "Pratyak Tara (Obstacles)", "status": "❌ Minor Delays", "vibe": "Expect unexpected administrative or personal friction. Double-check fine print details."},
    6: {"name": "Sadhana Tara (Success)", "status": "🟢 Elite Success", "vibe": "Outstanding frequency for achieving self-mastery, personal targets, and development goals."},
    7: {"name": "Naidhana Tara (Terminal)", "status": "❌ Deep Restriction", "vibe": "Strict personal boundary control needed. Postpone high-stakes private changes."},
    8: {"name": "Mitra Tara (Harmonious)", "status": "🟢 Very Favorable", "vibe": "Highly supportive for family bonding, relationship upgrades, and mutual understanding."},
    9: {"name": "Param Mitra Tara (Supreme)", "status": "👑 Maximum Alignment", "vibe": "Flawless astronomical window for securing lifetime personal alliances and deep family peace."}
}

PLANET_THEMES = {
    "Sunday": {"planet": "Sun", "emoji": "☀️", "color": "#FF8C00", "bg": "#2b1a00", "vibe": "Pure Vitality & Inner Leadership Aura Active"},
    "Monday": {"planet": "Moon", "emoji": "🌙", "color": "#A9A9A9", "bg": "#131822", "vibe": "Fluid Intuition & Emotional Clarity Active"},
    "Tuesday": {"planet": "Mars", "emoji": "💥", "color": "#FF4500", "bg": "#2b0b00", "vibe": "High-Drive Execution & Mindful Self-Discipline Active"},
    "Wednesday": {"planet": "Mercury", "emoji": "🌿", "color": "#00FF7F", "bg": "#00240f", "vibe": "Sharp Communication & Analytical Edge Active"},
    "Thursday": {"planet": "Jupiter", "emoji": "👑", "color": "#FFD700", "bg": "#2b2500", "vibe": "Supreme Wisdom & Spiritual Consciousness Expansion Active"},
    "Friday": {"planet": "Venus", "emoji": "💎", "color": "#FF69B4", "bg": "#2b001a", "vibe": "Creative Masterclass & Personal Life Harmony Active"},
    "Saturday": {"planet": "Saturn", "emoji": "🪐", "color": "#4682B4", "bg": "#0d1b2a", "vibe": "Deep Focus, Structure & Discipline Active"}
}

DAILY_STYLE_LOOKUP = {
    "Monday": {"color": "White, Silver, or Cream", "grooming": "✅ Safe for hair & nail cutting.", "task": "Routed excess personal funds toward liquid capital holdings."},
    "Tuesday": {"color": "Bright Red or Coral", "grooming": "❌ Avoid cutting hair or nails today (Mars energy).", "task": "Held firm boundaries against taking on new personal liabilities or debts."},
    "Wednesday": {"color": "Green or Pastel Shades", "grooming": "✅ Excellent day for grooming and personal care.", "task": "Audited active personal routine checklists, schedules, or savings fields."},
    "Thursday": {"color": "Golden Yellow or Saffron", "grooming": "⚠️ Avoid major haircuts to preserve Jupiter energy.", "task": "Verified allocation targets for compounding long-term assets (SIPs/ETFs)."},
    "Friday": {"color": "Clean White or Off-White", "grooming": "✅ Perfect for aesthetic grooming and spa routines.", "task": "Reviewed personal self-improvement targets or habit trackers."},
    "Saturday": {"color": "Black, Dark Blue, or Charcoal", "grooming": "❌ Strictly avoid hair and nail cutting today.", "task": "Dedicated execution strictly to structural organizing, home cleanup, or personal administration."},
    "Sunday": {"color": "Orange, Ruby Red, or Gold", "grooming": "Neutral day. Keep grooming minimal.", "task": "Completed an audit on personal savings and configured the upcoming weekly goals."}
}

MACRO_DATA = {
    "Weekly": {
        "job": {"good": "Strong communication surge early in the week; excellent for organizing personal diaries, study planning, and creative hobbies.", "bad": "Friction during routine domestic document management mid-week. Keep personal tasks clear and organized."},
        "finance": {"good": "Liquid capital flow is stable; good for handling immediate personal expenses or routine bills.", "bad": "Avoid impulsive retail spending or sudden financial choices on Thursday afternoon."},
        "health": {"good": "High mental clarity and focus profiles for demanding personal responsibilities, reading, and software studies.", "bad": "Minor sleep inconsistencies. Reduce late-night mobile screen usage."},
        "relationship": {"good": "Supportive configurations for family connections, spending time with your children, and domestic harmony.", "bad": "Miscommunications possible under daily life stress. Maintain a calm tone with loved ones."}
    },
    "Monthly": {
        "job": {"good": "Excellent phase for optimizing your daily lifestyle routine, showcasing personal habit discipline, and tracking productivity.", "bad": "Expect short-term processing delays from external public or personal utility administration queues."},
        "finance": {"good": "Strong returns on systemic personal investments (SIPs/ETFs) and structured savings fields.", "bad": "Check auto-renewals on streaming accounts or hidden digital subscription leaks."},
        "health": {"good": "Ideal month to establish solid nutritional habits and cardiovascular exercise discipline.", "bad": "High mental load can induce eye strain or posture fatigue. Take routine reading breaks."},
        "relationship": {"good": "Great for community connections, personal rapport, and positive presence within your social circle.", "bad": "Keep personal discussions objective and separate from temporary emotional fluctuations."}
    },
    "Quarterly": {
        "job": {"good": "Major personal expansion capabilities. Excellent window for taking on family leadership responsibilities or mastering long-term technical skills.", "bad": "High volume of personal chores requires sharp time-management and strict daily scheduling protocols."},
        "finance": {"good": "Opportunities to structure long-term personal assets or rebalance older investments.", "bad": "Avoid over-leveraging on unnecessary fresh personal loans or financial liabilities."},
        "health": {"good": "Vibrant physical recovery phases and strength gains under a structured wellness routine.", "bad": "Watch out for seasonal weather shifts causing minor digestive slowing or joint stiffness."},
        "relationship": {"good": "Alignments favor deep, long-range life planning with primary trusted family members.", "bad": "Ensure shared financial or household responsibilities are explicitly and calmly aligned."}
    },
    "6 Months": {
        "job": {"good": "Transit support favors massive personal growth, expanding your self-discipline, and mastering deep life skills.", "bad": "Hidden stress from older, pending household tasks. Resolve personal administrative backlogs early."},
        "finance": {"good": "Substantial foundational savings growth. Excellent for structural financial planning.", "bad": "Rahu/Ketu transits require total caution regarding ambiguous financial schemes or unverified funds."},
        "health": {"good": "High nervous system resilience and stamina recovery windows.", "bad": "Do not skip regular physical health checkups or personal stress auditing."},
        "relationship": {"good": "Excellent period to solidify your close circle and eliminate distracting, draining associations.", "bad": "Opaque communication can create minor misunderstandings if not cleared up immediately."}
    },
    "Yearly": {
        "job": {"good": "Foundational transit window for establishing personal life stability, lifestyle authority, and tracking individual achievements.", "bad": "Saturn in your house of expenditure demands meticulous attention to your personal living overhead costs."},
        "finance": {"good": "Major accumulation pathways open through disciplined, compounding asset vehicles.", "bad": "Strictly ban high-volatility financial exposure to preserve your core wealth blocks."},
        "health": {"good": "Strong physical alignment when backed by long-term wellness frameworks.", "bad": "Prone to burnout from over-exertion. Enforce strict, non-negotiable downtime boundaries."},
        "relationship": {"good": "Major stabilizing energy for lifelong personal and family bonds.", "bad": "Avoid complex personal financial arrangements where boundaries and expectations are not documented."}
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

def evaluate_cosmic_oracle(question, day_name, tarabala):
    q = question.lower()
    is_good_tara = "❌" not in tarabala["status"]
    
    if any(w in q for w in ["lend", "lending", "borrow", "debt", "loan", "give money", "creditor"]):
        if day_name == "Tuesday":
            return "❌ **Oracle Directive: ABSOLUTELY DENIED.** Today is Tuesday, ruled directly by Mars. Financial credits on a Tuesday trap the money in friction. Do not distribute cash tokens today."
        elif day_name == "Saturday" or not is_good_tara:
            return "⏳ **Oracle Directive: ADVISE DELAY.** The background star matrix indicates restrictive patterns. Hold your funds for a supportive Jupiter/Mercury day window."
        else:
            return "🟢 **Oracle Directive: APPROVED.** Frequencies are stable. Ensure arrangement terms are documented cleanly, and execute outside of Rahu Kaal."

    elif any(w in q for w in ["porn", "addiction", "habit", "urge", "relapse", "temptation", "impulse"]):
        if day_name in ["Tuesday", "Saturday"] or not is_good_tara:
            return "⚡ **Oracle Emergency Shield: ACTIVE.** This mental urge is an amplified cosmic shadow projection driven by Rahu friction. It is a temporary illusion. **Actionable Step:** Shut down your mobile display immediately. Step into an open room or take a walk for 15 minutes. Let this specific wave pass."
        else:
            return "🌱 **Oracle Support Directive:** Frequencies favor discipline today. Redirect your focus into physical tasks, tracking compounding accounts, or organizing logs. A short breathing routine right now will completely stabilize your mental energy."

    elif any(w in q for w in ["pressure", "stress", "workload", "deadline", "heavy", "tired", "burnout", "boss"]):
        return "⏳ **Oracle De-escalation Directive:** Saturn is transiting your 1st house (body), which amplifies physical sensations of pressure. Realize that this heavy mental load is a temporary environmental transit frequency. Break your personal task list into smaller segments and protect your evening rest."

    elif any(w in q for w in ["expense", "buy", "purchase", "spend", "cost", "bill", "pc", "laptop", "phone"]):
        if is_good_tara and day_name in ["Wednesday", "Thursday", "Friday"]:
            return "🟢 **Oracle Verdict: APPROVED.** Your current star frequency matches the active day lines beautifully. Execute your checkout during an active Mercury or Jupiter Hora block."
        else:
            return "⏳ **Oracle Verdict: CHOOSE DEFENSIVE DELAY.** The current background current presents a restrictive environment for technical or capital outflows. Table the transaction for 24-48 hours."

    elif any(w in q for w in ["food", "diet", "meal", "eating", "fasting", "dinner", "lunch"]):
        if day_name in ["Tuesday", "Saturday"]:
            return "⚠️ **Oracle Wellness Check:** Ambient cosmic energy is dense today. Avoid heavy, oily, or highly processed meals. Opt for light, clean vegetarian fuel to shield your physical body."
        else:
            return "🟢 **Oracle Wellness Check:** Good configuration to nurture your physical system. Excellent window for hydration planning and whole grains."
    else:
        if is_good_tara:
            return f"✨ **Oracle Verdict: GENERALLY APPROVED.** Your active birth star timing is currently protected and supportive ({tarabala['name']})."
        else:
            return f"⏳ **Oracle Verdict: CHOOSE DEFENSIVE DELAY.** Your active star profile is transiting a restrictive phase ({tarabala['name']})."

def get_advanced_predictions(day_name, status_str):
    if "Exceptional" in status_str or "Supreme" in status_str or "Success" in status_str:
        return {
            "career": "🟢 **High Momentum:** Saturn transiting your sign rewards personal precision and step-by-step consistency. Exalted Jupiter triggers clean life clarity. Execute complex personal tasks or focus entirely on software and personal studies.",
            "finance": "🟢 **Compounding Peak:** Excellent alignment for tracking personal Systematic Investment Plans (SIPs) or long-term fund positioning. A supportive window to audit personal savings safely.",
            "health": "🟢 **Vital Recovery:** Jupiter casts its protective 9th aspect back onto your body (1st house). Immune vectors are boosted. High physical endurance window; execute demanding daily fitness or lifestyle routines confidently."
        }
    elif "Avoid" in status_str or "Alert" in status_str or "Restriction" in status_str:
        return {
            "career": "❌ **Consolidation Required:** Ambient friction could cause minor execution delays or mental restlessness in daily personal routines. Dedicate energy strictly to resolving pending personal task backlogs.",
            "finance": "❌ **Defensive Posture:** Keep core personal capital reserves insulated. Postpone heavy initial investments into unverified luxury items today.",
            "health": "⚠️ **Energy Drain Warning:** Saturn hovering in your 1st house can trigger physical fatigue under high pressure. Set mandatory reading breaks and enforce firm boundaries around sleep."
        }
    else:
        return {
            "career": "🟡 **Steady Progress:** Stable baseline for completing routine life chores, organizing your private schedule, and reflecting on personal habits.",
            "finance": "🟡 **Stable Balance:** Safe configuration for micro-budget adjustments or routine banking transfers. Maintain your default compounding strategies.",
            "health": "🟡 **Grounded Vitality:** Standard physical and nervous system stability. Keep posture aligned during long sitting sessions."
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
        "Monday": {"wealth": "🟢 **Good:** Micro-investments or routing funds to liquid assets. Avoid risky speculative trading.", "business": "🟢 **Favorable:** Great for setting personal schedules, household coordination, and clear communication with family.", "travel": "🟢 **Safe:** Peaceful short-distance transits or commutes.", "health": "🟡 **Neutral:** Prioritize hydration and rest.", "legal": "❌ **Avoid:** Do not execute adversarial personal legal agreements today."},
        "Tuesday": {"wealth": "❌ **Restriction:** Avoid signing major personal loan frameworks or lending capital.", "business": "🟢 **High Power:** Perfect for organizing personal diaries, sorting domestic logs, and executing pending daily chores.", "travel": "🟡 **Caution:** Keep transits brief and highly structured.", "health": "🟢 **Excellent:** High energy window. Ideal for starting workout variations or physical adjustments.", "legal": "🟢 **Favorable:** Strong configuration for filing updates and managing personal documentation."},
        "Wednesday": {"wealth": "🟢 **Auspicious:** Excellent for personal asset adjustments and reviewing account configurations.", "business": "🟢 **Excellent:** Maximum alignment for completing study assignments, sorting digital files, and organizing personal responsibilities.", "travel": "🟢 **Highly Favorable:** Top alignment for logistical routines and travel planning.", "health": "🟢 **Good:** Great day for neurological wellness, yoga, breathing exercises, and dietary adjustments.", "legal": "🟢 **Favorable:** Ideal for document registration filings and personal contract reviews."},
        "Thursday": {"wealth": "🟢 **Supreme Alignment:** Premier window for mutual fund review, long-term asset positioning, and setting strategic personal investments.", "business": "🟢 **Supreme Alignment:** Perfect for high-level lifestyle planning, aligning with personal development, and focusing on long-term self-growth.", "travel": "🟢 **Favorable:** Supports long-distance travel planning or transits.", "health": "🟢 **Good:** Highly favorable for beginning systematic dietary regimens.", "legal": "🟢 **Excellent:** Exceptional protection for regulatory compliance reviews."},
        "Friday": {"wealth": "🟡 **Neutral:** Safe for regular budgeting; avoid allocating massive capital to high-risk stocks.", "business": "🟢 **Favorable:** Exceptional for front-facing collaboration, presentation reviews, and creative design hobbies.", "travel": "🟢 **Safe:** Smooth, stress-free travel profiles.", "health": "🟡 **Neutral:** Rest up and avoid heavy, dense meals.", "legal": "🟡 **Neutral:** Safe for standard document processing."},
        "Saturday": {"wealth": "🟡 **Caution:** Avoid volatile trades. Favorable for purchasing durable hard assets or necessary equipment.", "business": "🟢 **Productive:** Lock down domestic documentation, personal schedule organization, and clearing home administration logs.", "travel": "❌ **Avoid:** Postpone long personal journeys to bypass unexpected delays.", "health": "🟡 **Caution:** Watch joint strain. Excellent for deep rest cycles.", "legal": "🟡 **Neutral:** Slow movement; use strictly to review structural fine-print clauses."},
        "Sunday": {"wealth": "🟢 **Favorable:** Perfect window for personal asset audits and long-term asset balancing.", "business": "🟢 **High Alignment:** Elite configuration for outlining upcoming lifestyle goals and structuring your personal task list.", "travel": "🟢 **Good:** Permanent, energetic transit windows.", "health": "🟢 **Excellent:** Excellent vitality indices.", "legal": "🟢 **Favorable:** Auspicious for managing personal licensing or certificates."}
    }
    return matrix.get(day_name, matrix["Sunday"])

def get_hora_vibe(hora_planet):
    vibes = {
        "Jupiter": "🌟 **Auspicious Hour (Supreme):** Excellent for tracking personal asset charts, routing long-term fund segments (SIPs/ETFs), studying, or engaging in rewarding self-improvement reading.",
        "Mercury": "🧠 **Intellectual Hour (Highly Productive):** Prime window for learning Python/AI modules, drafting personal logs, organizing digital family archives, and refining your daily schedules.",
        "Venus": "🎨 **Creative Hour (Smooth):** Great for self-care, clothing styling choices, personal grooming routines, listening to music, and creating comfort within your living space.",
        "Moon": "🌊 **Intuitive Hour (Fluid):** Supported window for connecting with your children, adjusting family budget metrics, food tracking, and listening to your inner mental cues.",
        "Sun": "👑 **Authority Hour (Powerful):** Peak time to anchor personal vitality, build self-confidence, enforce strict boundary goals in your personal life, and sort out your lifestyle path.",
        "Mars": "⚡ **Aggressive Hour (Volatile):** Best for high-energy physical execution—intense workouts, handling heavy household chores, or aggressively shutting down compulsive habit or urge loops.",
        "Saturn": "⏳ **Delay Hour (Restrictive):** Dedicate this energy strictly to sorting household clutter, listing recent personal expenses, organizing files, or forcing a deep, restorative relaxation period. Avoid starting complex personal projects."
    }
    return vibes.get(hora_planet, "")

def calculate_hora_sequence(day_name):
    order = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
    day_lords = {"Sunday": "Sun", "Monday": "Moon", "Tuesday": "Mars", "Wednesday": "Mercury", "Thursday": "Jupiter", "Friday": "Venus", "Saturday": "Saturn"}
    start_index = order.index(day_lords[day_name])
    return [(f"{(6 + i) % 24:02d}:00 - {(7 + i) % 24:02d}:00", order[(start_index + i) % 7]) for i in range(24)]
    # Mobile UI Layout Configuration
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
    
    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>🔮 Cosmic Decision Oracle</h2>", unsafe_allow_html=True)
    user_q = st.text_input("Ask a question regarding your day:", placeholder="e.g., Should I lend money today? / Urge help", key="oracle_query_input")
    
    if user_q:
        oracle_verdict = evaluate_cosmic_oracle(user_q, day_name, tarabala)
        st.markdown(f"""<div style="background-color: #171b26; border-radius: 8px; padding: 14px; border-left: 4px solid #9A7BFF; margin-bottom: 15px; box-shadow: 0px 2px 8px rgba(0,0,0,0.2);"><p style="margin: 0; font-size: 13px; color: #ffffff; line-height: 1.5;">{oracle_verdict}</p></div>""", unsafe_allow_html=True)

    st.markdown("<h2 style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>🔮 Gochar Forecast (Predictions)</h2>", unsafe_allow_html=True)
    with st.expander("🧘‍♂️ Inner Growth & Mindset Prediction", expanded=True): st.write(preds["career"])
    with st.expander("💰 Personal Finance Prediction", expanded=False): st.write(preds["finance"])
    with st.expander("🏥 Personal Health Prediction", expanded=False): st.write(preds["health"])
        
    st.error(f"🛑 **Critical Restriction Window (Dubai):** Avoid executing high-stakes personal financial decisions, private contracts, or heavy lifestyle commitments today during **Rahu Kaal: {rahu_start} - {rahu_end}**.")

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
    with st.expander("🧘‍♂️ Inner Growth & Routine", expanded=False): st.write(decisions["business"])
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
        {"name": "👤 Personal Routine & Tasks", "key": "job"},
        {"name": "💰 Finance & Wealth", "key": "finance"},
        {"name": "🏥 Health & Wellness", "key": "health"},
        {"name": "🤝 Relationships & Alliances", "key": "relationship"}
    ]
    
    for s in sectors:
        st.markdown(f"<h3 style='font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;'>{s['name']}</h3>", unsafe_allow_html=True)
        st.markdown(f"""<div style="background-color: #111622; padding: 12px; border-radius: 8px; box-shadow: 0px 2px 6px rgba(0,0,0,0.2);"><p style="margin: 0px 0px 6px 0px; font-size: 13px; color: #00FF7F;">🟢 <b>Favorable (Good):</b> {data[s['key']]['good']}</p><p style="margin: 0; font-size: 13px; color: #FF4500;">❌ <b>Caution (Bad):</b> {data[s['key']]['bad']}</p></div>""", unsafe_allow_html=True)
        

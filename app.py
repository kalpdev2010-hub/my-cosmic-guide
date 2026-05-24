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

def get_daily_advice(day_name):
    # Core customized rules engine for your profile
    if day_name == "Monday":
        return {"color": "White, Silver, or Cream", "grooming": "✅ Safe for hair & nail cutting.", "finance": "Good for routine expenses; avoid risky lending.", "avoid": "Arguments and emotional confrontations."}
    elif day_name == "Tuesday":
        return {"color": "Bright Red or Coral", "grooming": "❌ Avoid cutting hair or nails today (Mars energy).", "finance": "Clear old debts; strictly avoid taking out new loans.", "avoid": "Signing major long-term agreements."}
    elif day_name == "Wednesday":
        return {"color": "Green or Pastel Shades", "grooming": "✅ Excellent day for grooming and personal care.", "finance": "Highly auspicious for investments and asset tracking.", "avoid": "Isolation or delaying important communications."}
    elif day_name == "Thursday":
        return {"color": "Golden Yellow or Saffron", "grooming": "⚠️ Avoid major haircuts to preserve Jupiter energy.", "finance": "Top alignment for long-term investments (SIPs/ETFs).", "avoid": "Disrespecting mentors or being overly cynical."}
    elif day_name == "Friday":
        return {"color": "Clean White or Off-White", "grooming": "✅ Perfect for aesthetic grooming and spa routines.", "finance": "Great for routine wealth auditing; avoid overspending.", "avoid": "Neglecting your core disciplines."}
    elif day_name == "Saturday":
        return {"color": "Black, Dark Blue, or Charcoal", "grooming": "❌ Strictly avoid hair and nail cutting today.", "finance": "Focus on stable long-term assets; avoid speculative trades.", "avoid": "Starting celebratory events or unexpected travel."}
    elif day_name == "Sunday":
        return {"color": "Orange, Ruby Red, or Gold", "grooming": "Neutral day. Keep grooming minimal.", "finance": "Excellent for reviewing financial targets or auditing wealth.", "avoid": "Oversleeping or low-energy environments."}

# Streamlit Mobile UI Configuration
st.set_page_config(page_title="Cosmic Guide", page_icon="🌙", layout="centered")

st.title("🔱 My Daily Cosmic Guide")
st.caption(f"Lagna: {MY_PROFILE['ascendant_lagna']} | Nakshatra: {MY_PROFILE['birth_nakshatra']} | Rashi: {MY_PROFILE['moon_sign']}")

# Interactive Date Picker (Defaults to Today)
target_date = st.date_input("Select Date", datetime.date.today())
day_name = target_date.strftime("%A")

day_advice = get_daily_advice(day_name)

st.subheader(f"📅 Blueprint for {day_name}")
st.write("---")

# Clean, scannable display boxes
st.info(f"🎨 **Clothing Color:**\n\n{day_advice['color']}")
st.success(f"📈 **Money & Loans:**\n\n{day_advice['finance']}")
st.warning(f"💇‍♂️ **Grooming (Hair/Nails):**\n\n{day_advice['grooming']}")
st.error(f"🛑 **What to Avoid:**\n\n{day_advice['avoid']}")

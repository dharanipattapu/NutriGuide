import streamlit as st
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, time
from streamlit_autorefresh import st_autorefresh

REMINDER_FILE = "user_reminders.yaml"

# ────────────────────────────────
# Load/save reminder data
# ────────────────────────────────
def load_reminders(username):
    try:
        with open(REMINDER_FILE, "r") as file:
            data = yaml.load(file, Loader=SafeLoader) or {}
            return data.get(username, {"daily": [], "once": []})
    except FileNotFoundError:
        return {"daily": [], "once": []}

def save_reminders(username, reminders):
    try:
        with open(REMINDER_FILE, "r") as file:
            data = yaml.load(file, Loader=SafeLoader) or {}
    except FileNotFoundError:
        data = {}
    data[username] = reminders
    with open(REMINDER_FILE, "w") as file:
        yaml.dump(data, file)

def time_to_str(t):
    return t.strftime("%H:%M")

def str_to_time(s):
    return datetime.strptime(s, "%H:%M").time()

# ────────────────────────────────
# Main reminder UI
# ────────────────────────────────
def reminder_page(username):
    st.title("⏰ Reminders")

    # Auto-refresh every 60 seconds
    st_autorefresh(interval=60000, key="auto_refresh")

    if "reminders" not in st.session_state:
        st.session_state.reminders = load_reminders(username)

    # Form to set new reminder
    reminder_type = st.selectbox("Set Reminder Type", ["Once", "Daily"])
    message = st.text_input("Reminder Message")
    reminder_time = st.time_input("Reminder Time", value=time(8, 0))

    if st.button("Set Reminder"):
        reminder = {
            "message": message,
            "time": time_to_str(reminder_time),
        }

        if reminder_type == "Daily":
            st.session_state.reminders["daily"].append(reminder)
            save_reminders(username, st.session_state.reminders)
            st.success("✅ Daily reminder saved!")
        else:
            st.session_state.reminders["once"].append(reminder)
            st.success("✅ One-time reminder set! Will not persist after showing.")

    # Show notifications if due
    now = datetime.now().time()
    triggered_once = []
    still_pending_once = []

    # Show daily reminders
    for r in st.session_state.reminders["daily"]:
        r_time = str_to_time(r["time"])
        if now.hour == r_time.hour and now.minute == r_time.minute:
            st.toast(f"📅 Daily Reminder: {r['message']}")

    # Handle one-time reminders
    for r in st.session_state.reminders["once"]:
        r_time = str_to_time(r["time"])
        if now.hour == r_time.hour and now.minute == r_time.minute:
            st.toast(f"📌 One-Time Reminder: {r['message']}")
        else:
            still_pending_once.append(r)

    # Clear expired one-time reminders
    st.session_state.reminders["once"] = still_pending_once
    save_reminders(username, st.session_state.reminders)

    # View all current reminders
    st.subheader("🗂 Saved Reminders")

    if st.session_state.reminders["daily"]:
        st.markdown("**📅 Daily Reminders:**")
        for r in st.session_state.reminders["daily"]:
            st.markdown(f"⏰ {r['time']} - {r['message']}")
    else:
        st.info("No daily reminders yet.")

    if st.session_state.reminders["once"]:
        st.markdown("**📌 One-Time Reminders (Waiting):**")
        for r in st.session_state.reminders["once"]:
            st.markdown(f"⏰ {r['time']} - {r['message']}")

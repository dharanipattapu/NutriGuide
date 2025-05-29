import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from auth import load_authenticator
from diet_logic import diet_page
from chatbot import chatbot_page
from reminder_page import reminder_page
from todo import todo_page
from calorie_estimator import calorie_estimator_page


# ───────────────────────────────────────────────────────────────
# UI CONFIG & STYLING
# ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="NutriGuide", layout="wide")

st.markdown(f"""
    <style>
    /* Background image and full height */
    html, body, .stApp {{
        background-image: url("https://i.pinimg.com/736x/ac/a6/2a/aca62ac050ce6983687064a732c3c356.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    /* Hide Streamlit's top nav, header, main menu & footer completely with no space */
    #MainMenu, header, footer {{
        visibility: hidden;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: -1;
    }}

    /* Remove extra space from header area */
    .css-18e3th9 {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}

    button[title="View app"], .stActionButton {{
        display: none !important;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(6px);
        border-right: 2px solid rgba(255, 255, 255, 0.2);
    }}

    /* Main content container */
    .main-container {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 1.5rem;
        max-width: 900px;
        margin: auto;
        box-shadow: 0 0 30px rgba(0,0,0,0.4);
    }}

    /* Hover style for sidebar radio */
    .css-1aumxhk:hover {{
        background-color: rgba(140, 185, 100, 0.2);
        border-radius: 10px;
    }}

    /* Inputs & Button styling */
    input, textarea, .stTextInput > div > div > input {{
        border-radius: 10px !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: black !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(8px);
    }}

    input::placeholder, textarea::placeholder {{
        color: black !important;
    }}

    input:focus, textarea:focus {{
        outline: none !important;
        border: 1.5px solid #8cb964 !important;
        background-color: rgba(255, 255, 255, 0.25) !important;
    }}

    button {{
        background-color: #8cb964 !important;
        color: white !important;
        border-radius: 8px !important;
        box-shadow: 0 0 10px #8cb964;
        border: none !important;
        padding: 0.5rem 1.2rem;
        cursor: pointer;
    }}

    button:hover {{
        background-color: #6d994e !important;
        box-shadow: 0 0 15px #b0ff7a;
        transition: 0.3s ease-in-out;
    }}

    /* Glowing text */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stTextInput label {{
        color: white !important;
        text-shadow: 0 0 6px rgba(0, 0, 0, 0.5);
    }}
    </style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────
# Registration Logic
# ───────────────────────────────────────────────────────────────
def save_user(username, name, email, password):
    with open("users.yaml", "r") as file:
        config = yaml.load(file, Loader=SafeLoader)

    if username in config["credentials"]["usernames"]:
        st.error("Username already exists.")
        return

    hashed_password = stauth.Hasher([password]).generate()[0]
    config["credentials"]["usernames"][username] = {
        "name": name,
        "email": email,
        "password": hashed_password
    }

    with open("users.yaml", "w") as file:
        yaml.dump(config, file, default_flow_style=False)

# ───────────────────────────────────────────────────────────────
# Initial State Setup
# ───────────────────────────────────────────────────────────────
if "register" not in st.session_state:
    st.session_state["register"] = False

# ───────────────────────────────────────────────────────────────
# Main UI Layout
# ───────────────────────────────────────────────────────────────
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with Logo and Title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.markdown("## NutriGuide")
    st.markdown("Welcome to your personal diet and wellness assistant.")

st.markdown("---")

# ───────────────────────────────────────────────────────────────
# Registration and Login Logic
# ───────────────────────────────────────────────────────────────
if st.session_state["register"]:
    st.markdown("### Create Your Account")
    username = st.text_input("Choose a Username")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif not username or not name or not email:
            st.error("Please fill out all fields.")
        else:
            save_user(username, name, email, password)
            st.success("Registration successful! Please login.")
            st.session_state["register"] = False

    if st.button("Already have an account? Login"):
        st.session_state["register"] = False

else:
    authenticator, config = load_authenticator()
    name, auth_status, username = authenticator.login(
        fields={"Form name": "Login"},
        location="main"
    )

    if auth_status:
        authenticator.logout("Logout", location="sidebar")
        st.sidebar.success(f"Welcome, {name}!")

        menu = st.sidebar.radio("Go to", [
            "🏠 Dashboard",
            "🍽 Diet Plan",
            "🤖 AI Chatbot",
            "⏰ Reminders",
            "📝 To-Do List",
            "📷 Calorie from Image"
        ])

        if menu == "🏠 Dashboard":
            st.title("Welcome to NutriGuide!")
            st.markdown("Your personalized wellness assistant — eat better, live healthier.")
        elif menu == "🍽 Diet Plan":
            diet_page(username)
        elif menu == "🤖 AI Chatbot":
            chatbot_page()
        elif menu == "⏰ Reminders":
            reminder_page(username)
        elif menu == "📝 To-Do List":
            todo_page(username)
        elif menu == "📷 Calorie from Image":
            calorie_estimator_page()


    elif auth_status is False:
        st.error("Incorrect username or password.")
        if st.button("New user? Register here"):
            st.session_state["register"] = True

    elif auth_status is None:
        st.markdown("### Login")
        if st.button("New user? Register here"):
            st.session_state["register"] = True

st.markdown('</div>', unsafe_allow_html=True)

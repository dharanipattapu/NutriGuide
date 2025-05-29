import streamlit as st
from groq import Groq
import yaml
from yaml.loader import SafeLoader

# Load your Groq API key here (or use dotenv for security)
API_KEY = "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"
client = Groq(api_key=API_KEY)

MEAL_PLAN_FILE = "user_meal_plans.yaml"

# Load saved meal plan for a user
def load_meal_plan(username):
    try:
        with open(MEAL_PLAN_FILE, "r") as file:
            data = yaml.load(file, Loader=SafeLoader) or {}
            return data.get(username, "")
    except FileNotFoundError:
        return ""

# Save generated meal plan
def save_meal_plan(username, meal_plan):
    try:
        with open(MEAL_PLAN_FILE, "r") as file:
            data = yaml.load(file, Loader=SafeLoader) or {}
    except FileNotFoundError:
        data = {}

    data[username] = meal_plan
    with open(MEAL_PLAN_FILE, "w") as file:
        yaml.dump(data, file)

# Generate meal plan using Groq API
def generate_meal_plan(age, weight, height, gender, restrictions):
    prompt = (
        f"Create a daily nutrition meal plan for:\n"
        f"- Age: {age} years\n"
        f"- Weight: {weight} kg\n"
        f"- Height: {height} cm\n"
        f"- Gender: {gender}\n"
        f"- Dietary restrictions: {', '.join(restrictions) if restrictions else 'None'}\n\n"
        "Instructions:\n"
        "- Start with: 'Here is your personalized nutrition plan:'\n"
        "- Include breakfast, lunch, dinner, and 2 snacks\n"
        "- For each meal, list dish names, ingredients, calories, and cost in INR\n"
        "- Ensure meals match the user's dietary restrictions\n"
        "- Keep it realistic and affordable in Indian context"
    )

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=1500,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit diet plan UI
def diet_page(username):
    st.title("🍽 Personalized Nutrition Plan")

    st.markdown("Enter your personal details to get a daily customized meal plan.")

    age = st.number_input("Age", min_value=10, max_value=100)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    restrictions = st.multiselect(
        "Dietary Restrictions",
        ["Vegetarian", "Vegan", "Gluten-Free", "Low Carb", "High Protein", "Lactose-Free", "Diabetic Friendly"]
    )

    if st.button("Generate Nutrition Plan"):
        with st.spinner("Generating your personalized plan..."):
            meal_plan = generate_meal_plan(age, weight, height, gender, restrictions)
            st.session_state.generated_meal = meal_plan
            save_meal_plan(username, meal_plan)
            st.success("✅ Nutrition plan saved to your profile!")

    # Display saved plan
    existing_plan = load_meal_plan(username)
    if existing_plan:
        st.subheader("🗂 Your Saved Nutrition Plan:")
        st.markdown(existing_plan)

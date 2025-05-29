# NutriGuide
A personalized nutrition and wellness tracker with AI-based diet plans, food image upload for calorie analysis, reminders, and chatbot support.
# 🥗 NutriGuide – Your AI-Powered Nutrition Companion

NutriGuide is a Streamlit-based wellness and nutrition tracker that helps users generate personalized meal plans, estimate calories from food images, set reminders, and get advice through an integrated AI chatbot. Designed for simplicity and usability, NutriGuide is your all-in-one health assistant.

---

## 🌟 Key Features

- **🔐 User Login System**  
  Register/Login using email or mobile number (no OTP)  
  Data saved in JSON/YAML format

- **📊 Personalized Diet Plans**  
  Custom meal plans based on user profile (age, weight, gender, height)  
  Stored per user in `user_profiles/`

- **🖼️ Food Upload & Calorie Estimation**  
  Upload images of meals  
  Estimate calorie count using AI in `calorie_estimator.py`

- **🤖 AI Chatbot Support**  
  Ask food- and nutrition-related questions  
  Powered by OpenAI (see `chatbot.py`)

- **⏰ Reminders & To-Do Tasks**  
  Set and manage reminders (`reminder_page.py`, `todo.py`)  
  Data stored in `user_reminders.yaml` and `user_tasks.yaml`

- **🎨 Wellness-Themed UI**  
  Designed with a cream and olive green color palette  
  Includes logo, assets, and polished layout

---

## 🗂️ Project Folder Structure
STREAMLIT_NUTRI_APP/
├── .streamlit/ # Streamlit config and customizations
├── assets/ # Images, icons, styles
├── user_profiles/ # Individual user data
├── venv/ # Virtual environment
├── pycache/ # Python cache
├── app.py # Main entry point for the Streamlit app
├── auth.py # Authentication logic
├── calorie_estimator.py # Image upload & calorie estimation
├── chatbot.py # AI chatbot integration
├── config.yaml # App configuration
├── diet_logic.py # Personalized diet plan generation
├── reminder_page.py # Reminder feature UI
├── todo.py # Task/to-do management
├── logo.png # App branding
├── user_meal_plans.yaml # Stores generated diet plans
├── user_reminders.yaml # Stores reminders per user
├── user_tasks.yaml # Stores task/to-do data
├── users.yaml # Registered users data
├── users.json # Alternative user storage
├── .env # Environment variables (API keys, etc.)
├── README.md # Project documentation
└── requirements.txt # Python dependencies

2. Set up Virtual Environment
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Add .env File
   OPENAI_API_KEY=your_openai_key

5. Run the App
streamlit run app.py

🔐 Environment Variables
Make sure to set up a .env file with the following:
OPENAI_API_KEY=your_key_here

🤝 Contributing
Contributions are welcome! Feel free to fork this repository and open a pull request.

🙌 Acknowledgements
Streamlit for frontend

OpenAI for chatbot support

Canva-style theme inspiration
![Uploading 1.png…]()

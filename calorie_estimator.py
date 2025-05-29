import streamlit as st
import requests
from PIL import Image
import io
import base64

# Your API Key
API_KEY = "AIzaSyDoQnDTyz8sSpLoHnS85uBBdKFBln_KdK4"
MODEL = "gemini-1.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

# Convert image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Query Gemini API
def query_gemini(base64_img):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": (
                        "You're a nutritionist AI. Analyze this food image and list each visible food item with approximate calories. "
                        "Example:\n- Food: Rice\n- Calories: ~200 kcal\n\nBe concise."
                    )},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_img
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise Exception(response.json())

# Streamlit page
def calorie_estimator_page():
    st.title("📷 Calorie Estimator")
    st.markdown("Upload a food image. We'll estimate the calories using Gemini 1.5 Flash AI.")

    uploaded_image = st.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Estimate Calories"):
            with st.spinner("Analyzing image with Gemini..."):
                try:
                    base64_img = image_to_base64(image)
                    result = query_gemini(base64_img)
                    st.success("🍽 Calorie Estimate:")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

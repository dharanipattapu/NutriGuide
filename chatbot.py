import streamlit as st
from groq import Groq

# Load your API key (replace or load from .env)
API_KEY = "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"
client = Groq(api_key=API_KEY)

def chatbot_page():
    st.title("🤖 NutriGuide Chatbot")
    st.markdown("Ask me anything about food, fitness, nutrition, or wellness!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("💬 You:", key="user_input")

    if st.button("Send") and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            try:
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",  # Free, powerful model
                    messages=st.session_state.chat_history,
                    temperature=0.7,
                    max_tokens=500
                )
                response = completion.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            except Exception as e:
                response = f"❌ Error: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Display full conversation
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['content']}")

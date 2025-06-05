from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
import streamlit as st

# Load Google API key from Streamlit secrets or fallback to local env
os.environ["GOOGLE_API_KEY"] = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Streamlit UI config
st.set_page_config(page_title="Bhagavad Gita Chatbot", layout="centered")
st.title("🕉️ Bhagavad Gita Wisdom Chatbot")
st.markdown("""
Ask anything about the Bhagavad Gita – its teachings, verses, interpretations, or philosophy.
Choose your preferred style of response.
""")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Style options
style = st.selectbox("Choose Explanation Style:", [
    "Simple & Spiritual",
    "Detailed with Sanskrit References",
    "Philosophical & Reflective",
    "Action-Oriented Advice"
])

# User input
user_question = st.text_area("🧘‍♂️ What would you like to ask Krishna?", "What does Krishna say about duty?")

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["question", "style"],
    template="""
You are a wise and spiritually enlightened teacher who deeply understands the Bhagavad Gita.

User's question: "{question}"

Respond in the following style: {style}.

Ensure your explanation is rooted in the teachings of the Bhagavad Gita. Include relevant verse references if appropriate.
Avoid deviating from the core message of the Gita.
"""
)

# Handle question
if st.button("🕉️ Ask Krishna") and user_question.strip():
    final_prompt = prompt_template.format(question=user_question, style=style)
    response = model.invoke(final_prompt)
    st.session_state.chat_history.append((user_question, response.content))

# Show chat history
if st.session_state.chat_history:
    st.subheader("📜 Chat History")
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"_A{i}:_ {a}")
        st.markdown("---")

# Clear chat history
if st.button("🗑️ DELETE HISTORY"):
    st.session_state.chat_history = []
    st.success("Chat history deleted.")

st.markdown("🙏 Jai Shri Krishna 🙏")

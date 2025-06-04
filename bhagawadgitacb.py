from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize the Gemini model
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

# Streamlit UI setup
st.set_page_config(page_title="Bhagavad Gita Chatbot", layout="centered")
st.title("🕉️ Bhagavad Gita Wisdom Chatbot")
st.markdown("""
Ask anything about the Bhagavad Gita – its teachings, verses, interpretations, or philosophy.
Choose your preferred style of response.
""")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Style and tone options
style = st.selectbox("Choose Explanation Style:", [
    "Simple & Spiritual",
    "Detailed with Sanskrit References",
    "Philosophical & Reflective",
    "Action-Oriented Advice",
])

# User input
user_question = st.text_area("🧘‍♂️ What would you like to ask Krishna?", "What does Krishna say about duty?")

# Prompt Template
from langchain_core.prompts import PromptTemplate

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

# Generate response
if st.button("🕉️ Ask Krishna") and user_question.strip():
    final_prompt = prompt_template.format(question=user_question, style=style)
    response = model.invoke(final_prompt)

    # Append to chat history
    st.session_state.chat_history.append((user_question, response.content))

# Display chat history
if st.session_state.chat_history:
    st.subheader("📜 Chat History")
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"_A{i}:_ {a}")
        st.markdown("---")

# Button to delete chat history
if st.button("🗑️ DELETE HISTORY"):
    st.session_state.chat_history = []
    st.success("Chat history deleted.")

st.markdown("🙏 Jai Shri Krishna 🙏")

import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

# LangSmith setup for tracing
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Groq AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Chatbot with Groq")
st.markdown("Lightning-fast chatbot powered by Groq + LangChain ⚡")

# Give each browser session a unique ID so LangSmith can track threads separately
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Keep the full conversation in session state so it survives reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Give accurate, concise, and user-friendly answers."),
    ("user", "Question: {question}")
])

# Cache the model so it doesn't reload on every Streamlit rerun
@st.cache_resource
def load_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="openai/gpt-oss-120b",
        temperature=0.3
    )

llm = load_llm()
chain = prompt | llm | StrOutputParser()

# Render existing chat history before showing the input box
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            response = chain.invoke(
                {"question": user_input},
                config={"configurable": {"session_id": st.session_state.session_id}}
            )
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")
st.caption("⚡ Powered by Groq + LangChain + Streamlit + LangSmith")
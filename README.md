# ⚡ GroqChat — Lightning-Fast AI Chatbot

> A conversational AI chatbot built with Groq's ultra-fast inference, LangChain pipelines, and a clean Streamlit UI — with full observability via LangSmith.

---

## 💡 Suggested Project Names

| Name | Why it fits |
|---|---|
| **GroqChat** | Simple, direct — Groq + Chat |
| **SwiftMind** | Emphasizes the speed of Groq inference |
| **NeuralDesk** | General AI assistant feel |
| **AskGroq** | Tells you exactly what it does |
| **VelocityAI** | Highlights Groq's speed advantage |

---

## 🚀 What This Project Does

GroqChat is a simple but production-aware AI chatbot. You type a question, it answers instantly. Under the hood it uses Groq's inference API (one of the fastest LLM providers available) routed through a LangChain pipeline, displayed in a Streamlit web UI, and traced end-to-end via LangSmith.

It's a great starting point for anyone learning LangChain or building more complex apps like RAG pipelines, document Q&A, or AI agents — the `requirements.txt` already includes tools for all of that (ChromaDB, FAISS, HuggingFace embeddings, PDFs, Wikipedia, and more).

---

## 🧠 How It Works

### The Big Picture

```
User types a question
        ↓
Streamlit captures input
        ↓
LangChain formats it into a prompt
        ↓
Groq API runs inference (very fast)
        ↓
Response parsed and displayed in chat UI
        ↓
LangSmith logs the full trace
```

### Step-by-Step Breakdown

**1. Environment & API Keys**

The app loads all secrets from a `.env` file using `python-dotenv`. Four environment variables are set:
- `GROQ_API_KEY` — authenticates with Groq
- `LANGCHAIN_API_KEY` — enables LangSmith tracing
- `LANGCHAIN_PROJECT` — groups traces under a named project
- `LANGCHAIN_TRACING_V2` — turns on the tracing pipeline

**2. Session Management**

Every time a new browser tab opens the app, Streamlit creates a fresh session. The app assigns that session a random UUID so LangSmith can track each user's conversation separately — even when multiple people use the app at the same time.

```python
st.session_state.session_id = str(uuid.uuid4())
# e.g. "3f2a1c-9d84-..." — unique per browser tab
```

**3. Chat History**

Conversation history is stored in `st.session_state.messages` as a list of `{"role": ..., "content": ...}` dicts. Since Streamlit reruns the entire script on every interaction, storing state this way is what makes the chat history persist across messages.

**4. The LangChain Pipeline**

```python
chain = prompt | llm | StrOutputParser()
```

Three components chained together using LangChain's pipe (`|`) operator:

- **`ChatPromptTemplate`** — wraps the user's question in a structured format with a system instruction and a user message
- **`ChatGroq`** — sends the formatted prompt to Groq's API and gets a response; cached with `@st.cache_resource` so the model client isn't recreated on every rerun
- **`StrOutputParser`** — strips LangChain metadata and returns a plain Python string

**5. Rendering the Chat**

Before showing the input box, the app loops through `st.session_state.messages` and renders each one using `st.chat_message()`. This is what makes previous messages visible when Streamlit reruns after each new input.

**6. LangSmith Tracing**

Every `chain.invoke()` call passes a `session_id` in the config. LangSmith uses this to group all messages from the same browser tab into one traceable thread — useful for debugging, latency monitoring, and reviewing conversation quality.

---

## 📦 Requirements Explained

| Package | Used for |
|---|---|
| `langchain`, `langchain-core` | Core pipeline and prompt tools |
| `langchain-groq` | Groq LLM integration |
| `streamlit` | Web UI |
| `python-dotenv` | Loading `.env` secrets |

---

## 🗂️ Project Structure

```
groqchat/
├── app.py              # Main chatbot application
├── .env                # API keys (never commit this)
├── requirements.txt    # All dependencies
└── README.md
```

---

## ⚙️ Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/your-username/groqchat.git
cd groqchat
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create your `.env` file**
```env
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=GroqChat
```

Get your Groq key at [console.groq.com](https://console.groq.com) and LangSmith key at [smith.langchain.com](https://smith.langchain.com).

**5. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser and start chatting.

---

## 🔭 What You Can Build Next

Since your dependencies already include vector stores, embeddings, and document loaders, natural next steps are:

- **RAG Chatbot** — let users upload PDFs and chat with them using FAISS or ChromaDB
- **Wikipedia/Arxiv Research Bot** — answer questions grounded in real sources
- **LangServe API** — expose your chain as a REST endpoint using FastAPI + LangServe
- **Multi-turn memory** — add `ConversationBufferMemory` to make the bot remember context across turns

---

## 📄 License

MIT — free to use, modify, and build on.

---

## 🙌 Built With

- [Groq](https://groq.com) — fastest LLM inference available
- [LangChain](https://langchain.com) — composable AI pipelines
- [Streamlit](https://streamlit.io) — instant Python web UIs
- [LangSmith](https://smith.langchain.com) — observability and tracing

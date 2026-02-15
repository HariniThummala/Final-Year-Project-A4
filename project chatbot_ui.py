import streamlit as st
import requests
from datetime import datetime
import random

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="Placement Guidance Bot",
    page_icon="🎓",
    layout="centered"
)

quotes = [
    "🚀 Dream big. Start small. Act now.",
    "💡 Skills pay bills!",
    "🔥 Every expert was once a beginner.",
    "📚 Learn today. Lead tomorrow.",
    "✨ Your placement journey starts here!"
]

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

.main-title {
    background: linear-gradient(90deg,#6a11cb,#2575fc);
    color:white;
    padding:15px;
    border-radius:12px;
    text-align:center;
}

.chat-container {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background: linear-gradient(135deg,#dcf8c6,#b2f7b2);
    padding: 12px;
    border-radius: 18px;
    margin-bottom: 10px;
    text-align: right;
}

.bot-msg {
    background: linear-gradient(135deg,#f1f0f0,#ffffff);
    padding: 12px;
    border-radius: 18px;
    margin-bottom: 10px;
    text-align: left;
}

.timestamp {
    font-size: 10px;
    color: gray;
}

.quick-btn {
    background:#2575fc;
    color:white;
    padding:6px 10px;
    border-radius:10px;
    margin-right:6px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("🎓 Placement Bot")
    st.success(random.choice(quotes))
    st.divider()

    st.markdown("### 🚀 Quick Actions")
    if st.button("📄 Resume Tips"):
        st.session_state.chat.append({
            "role":"user",
            "text":"resume tips",
            "time":datetime.now().strftime("%H:%M")
        })
        st.rerun()

    if st.button("🎤 Interview Prep"):
        st.session_state.chat.append({
            "role":"user",
            "text":"interview preparation",
            "time":datetime.now().strftime("%H:%M")
        })
        st.rerun()

    if st.button("💻 Tech Skills"):
        st.session_state.chat.append({
            "role":"user",
            "text":"python topics",
            "time":datetime.now().strftime("%H:%M")
        })
        st.rerun()

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.chat = []
        st.rerun()

# ---------------- MAIN HEADER ---------------- #
st.markdown('<div class="main-title"><h2>🎓 Placement Guidance Chatbot</h2><p>Your AI mentor for placements</p></div>', unsafe_allow_html=True)

st.caption("Ask about placements, skills, resumes & interviews — let’s crack your dream job 💼")

# ---------------- SESSION STATE ---------------- #
if "chat" not in st.session_state:
    st.session_state.chat = []

# Welcome message
if len(st.session_state.chat) == 0:
    st.session_state.chat.append({
        "role":"assistant",
        "text":"👋 Hi! I’m your Placement Buddy 🤖\n\nAsk me about:\n💻 Skills\n📄 Resume\n🎤 Interviews\n🏢 Companies\n\nLet’s grow together 🚀",
        "time":datetime.now().strftime("%H:%M")
    })

# ---------------- DISPLAY CHAT ---------------- #
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for c in st.session_state.chat:
    time = c["time"]

    if c["role"] == "user":
        st.markdown(f"""
        <div class="user-msg">
            🙋 <b>You</b><br>
            {c["text"]}
            <div class="timestamp">{time}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="bot-msg">
            🤖 <b>Placement Buddy</b><br>
            {c["text"]}
            <div class="timestamp">{time}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INPUT BOX ---------------- #
msg = st.chat_input("Type your career question here... 🚀")

# ---------------- HANDLE MESSAGE ---------------- #
if msg:
    now = datetime.now().strftime("%H:%M")

    st.session_state.chat.append({
        "role": "user",
        "text": msg,
        "time": now
    })

    with st.spinner("🤖 Thinking... preparing something awesome..."):
        try:
            r = requests.post(
                "http://127.0.0.1:5000/ask",
                json={"question": msg},
                timeout=30
            )
            reply = r.json().get("answer", "No response from backend.")

        except:
            reply = "⚠ Backend not running."

    st.session_state.chat.append({
        "role": "assistant",
        "text": reply + "\n\n✨ Keep learning. You’re doing great!",
        "time": datetime.now().strftime("%H:%M")
    })

    st.rerun()

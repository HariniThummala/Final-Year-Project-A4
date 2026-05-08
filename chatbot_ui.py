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

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.chats[st.session_state.current_chat] = []

# ---------------- SIDEBAR ---------------- #
with st.sidebar:

    st.title("💬 Chat History")
    st.success(random.choice(quotes))

    # New Chat
    if st.button("➕ New Chat"):
        new_chat = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.current_chat = new_chat
        st.session_state.chats[new_chat] = []
        st.rerun()

    st.divider()

    # Chat history
    for chat_name in st.session_state.chats.keys():
        if st.button(chat_name):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()

    st.markdown("### 🚀 Quick Career Help")

    if st.button("📄 Resume Tips"):
        st.session_state.quick_action = "resume"

    if st.button("🎤 Interview Prep"):
        st.session_state.quick_action = "interview"

    if st.button("💻 Tech Skills"):
        st.session_state.quick_action = "skills"

# ---------------- MAIN HEADER ---------------- #
st.markdown(
    '<div class="main-title"><h2>🎓 Placement Guidance Chatbot</h2><p>Your AI mentor for placements</p></div>',
    unsafe_allow_html=True
)

st.caption("Ask about placements, skills, resumes & interviews — let’s crack your dream job 💼")

chat = st.session_state.chats[st.session_state.current_chat]
# ---------------- QUICK ACTION RESPONSES ---------------- #

if "quick_action" in st.session_state:

    action = st.session_state.quick_action
    now = datetime.now().strftime("%H:%M")

    if action == "resume":
        reply = """📄 Resume Tips for Placements

• Keep it 1 page for freshers
• Highlight projects & internships
• Use action words like Built, Developed, Designed
• Add GitHub & LinkedIn links
• Mention technical skills clearly

⭐ Bonus Tip: Recruiters scan resumes in 6–8 seconds
"""

    elif action == "interview":
        reply = """🎤 Interview Preparation Guide

1️⃣ Prepare DSA basics
2️⃣ Practice mock interviews
3️⃣ Revise projects thoroughly
4️⃣ Learn HR questions

Common HR Questions:
• Tell me about yourself
• Why should we hire you?
• What are your strengths?

⭐ Confidence matters as much as knowledge
"""

    elif action == "skills":
        reply = """💻 Top Tech Skills for Placements

Programming
• Python
• Java
• C++

Core Skills
• Data Structures & Algorithms
• OOP concepts
• DBMS
• Operating Systems

Extra Advantage
• Web Development
• Machine Learning
• Cloud Basics

⭐ Build real projects to stand out
"""

    chat.append({
        "role": "assistant",
        "text": reply,
        "time": now
    })

    del st.session_state.quick_action
    st.rerun()

# ---------------- WELCOME MESSAGE ---------------- #
if len(chat) == 0:
    chat.append({
        "role":"assistant",
        "text":"👋 Hi! I’m your Placement Buddy 🤖\n\nAsk me about:\n💻 Skills\n📄 Resume\n🎤 Interviews\n🏢 Companies\n\nLet’s grow together 🚀",
        "time":datetime.now().strftime("%H:%M")
    })

# ---------------- DISPLAY CHAT ---------------- #
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for c in chat:
    time = c["time"]

    if c["role"] == "user":
        st.markdown(f"""
        <div class="user-msg">
            🙋 <b>You</b><br>
            {c["text"].replace("\n","<br>")}
            <div class="timestamp">{time}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="bot-msg">
            🤖 <b>Placement Buddy</b><br>
            {c["text"].replace("\n","<br>")}
            <div class="timestamp">{time}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INPUT BOX ---------------- #
msg = st.chat_input("Type your career question here... 🚀")

# ---------------- HANDLE MESSAGE ---------------- #
if msg:

    now = datetime.now().strftime("%H:%M")

    chat.append({
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

            if r.status_code == 200:
                data = r.json()
                reply = data.get("answer", "No response from backend.")
            else:
                reply = f"⚠ Server error: {r.status_code}"

        except Exception as e:
            reply = f"⚠ Connection error: {str(e)}"

    chat.append({
        "role": "assistant",
        "text": reply + "\n\n✨ Keep learning. You’re doing great!",
        "time": datetime.now().strftime("%H:%M")
    })

    st.rerun()
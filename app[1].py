import os
import streamlit as st
from huggingface_hub import InferenceClient

# ---------------------------------------------------------
# Khurram's AI — Pakistani school tutor (Classes 1–10)
# Add HF_TOKEN in Streamlit Secrets for hosted AI responses.
# ---------------------------------------------------------

st.set_page_config(
    page_title="Khurram's AI | Pakistani School Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 85% 3%, rgba(94, 91, 255, .14), transparent 28%),
      radial-gradient(circle at 20% 0%, rgba(24, 177, 255, .10), transparent 24%),
      #080d19;
    color: #eef3ff;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a2e 0%, #0b1220 100%);
    border-right: 1px solid rgba(142, 164, 210, .17);
}
[data-testid="stSidebar"] * { color: #e9efff; }
.hero {
    padding: 28px 30px;
    border: 1px solid rgba(125, 151, 255, .28);
    border-radius: 24px;
    background: linear-gradient(120deg, rgba(24, 42, 79, .95), rgba(23, 20, 58, .92));
    box-shadow: 0 18px 60px rgba(0,0,0,.22);
    margin-bottom: 22px;
}
.hero h1 { font-size: clamp(2rem, 4vw, 3.2rem); margin: 0; letter-spacing: -1.5px; }
.hero p { color: #b9c8e8; font-size: 1.05rem; margin: 10px 0 0; }
.gradient { background: linear-gradient(90deg,#69d5ff,#a99bff); -webkit-background-clip:text; background-clip:text; color:transparent; }
.pill {
    display:inline-block; margin: 18px 7px 0 0; padding: 7px 12px;
    border-radius: 999px; border: 1px solid rgba(140,164,255,.3);
    background: rgba(95,119,255,.12); color: #dce6ff; font-size: .82rem;
}
.panel {
    border: 1px solid rgba(133, 156, 206, .19);
    border-radius: 18px; padding: 18px 20px;
    background: rgba(16, 25, 44, .72); margin-bottom: 14px;
}
.small-muted { color: #9eaccb; font-size: .9rem; }
div[data-testid="stChatMessage"] {
    background: rgba(17, 27, 48, .78);
    border: 1px solid rgba(130, 154, 209, .15);
    border-radius: 16px; padding: 14px;
}
.stButton button {
    border-radius: 12px; border: 1px solid rgba(133,158,255,.32);
    background: linear-gradient(100deg,#2463eb,#7255ed); color: white;
    font-weight: 600; min-height: 42px;
}
.stButton button:hover { border-color: #a7c5ff; color: white; }
div[data-testid="stChatInput"] textarea { background: #101a2d; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

SUBJECTS = [
    "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
    "English", "Urdu", "Islamiat", "Pakistan Studies", "General Science",
    "Social Studies", "Other",
]
BOARDS = ["Punjab Board (PCTB)", "Sindh Board (STBB)", "Federal Board (FBISE)",
          "Khyber Pakhtunkhwa Board", "Balochistan Board", "Not sure / Other"]

with st.sidebar:
    st.markdown("## 🎓 Khurram's **AI**")
    st.caption("Your personal Pakistani syllabus tutor")
    st.divider()
    page = st.radio("NAVIGATION", ["Study chat", "How to use", "About"], label_visibility="visible")
    st.divider()
    st.markdown("### 📚 Your study setup")
    grade = st.selectbox("Class", [f"Class {i}" for i in range(1, 11)], index=8)
    subject = st.selectbox("Subject", SUBJECTS, index=0)
    board = st.selectbox("Education board", BOARDS, index=0)
    language = st.selectbox("Answer language", ["English", "Urdu", "Roman Urdu", "English + Urdu"], index=0)
    detail = st.select_slider("Explanation detail", options=["Quick", "Standard", "Very detailed"], value="Very detailed")
    st.divider()
    st.markdown('<p class="small-muted">Built for Pakistani students · Classes 1–10 · Extra focus on 9 & 10</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if page == "Study chat":
    st.markdown("""
    <div class="hero">
      <h1>Learn smarter with <span class="gradient">Khurram's AI</span></h1>
      <p>Your AI study partner for Classes 1–10, with extra focus on Matric (9 &amp; 10).</p>
      <span class="pill">📘 Pakistani syllabus focused</span>
      <span class="pill">🧮 Step-by-step maths</span>
      <span class="pill">✨ Detailed explanations</span>
      <span class="pill">🇵🇰 Made for Pakistan</span>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.65, 1], gap="large")
    with left:
        st.markdown("### 💬 Ask Khurram")
        st.caption(f"{grade} · {subject} · {board} · {language}")
        if not st.session_state.messages:
            st.markdown("""
            <div class="panel">
              <h4>👋 Assalam-o-Alaikum! I'm Khurram's AI.</h4>
              Tell me what you're studying. I'll explain it in clear, student-friendly steps.
              <p class="small-muted">Try asking a question below to begin.</p>
            </div>
            """, unsafe_allow_html=True)

        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🎓" if message["role"] == "assistant" else "🧑‍🎓"):
                st.markdown(message["content"])

        prompt = st.chat_input("Ask a question, solve a maths problem, or explain a chapter…")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(prompt)

            token = None
            try:
                token = st.secrets.get("HF_TOKEN", None)
            except Exception:
                token = None
            token = token or os.getenv("HF_TOKEN")

            model = None
            try:
                model = st.secrets.get("HF_MODEL", None)
            except Exception:
                model = None
            model = model or os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")

            system_prompt = f"""You are Khurram's AI, a careful and encouraging Pakistani school tutor.
Teach a student studying {grade}, subject {subject}, board {board}.
Answer language: {language}. Explanation detail: {detail}.
Use the relevant Pakistani school curriculum and textbook-style terminology where you can.
Do not claim to have checked the latest official syllabus or a specific textbook unless its contents are supplied.
If the board or textbook edition matters, say so briefly and ask for the chapter/page or a photo/text excerpt.
For mathematics: show every step, write the formula, substitute values, explain each operation,
and clearly mark the final answer. Verify arithmetic and do not skip steps.
For science: explain concepts, define key terms, show formulas/units and examples when useful.
For exam preparation: include a short exam-style answer when appropriate.
Use age-appropriate language, headings and examples. If unsure, be transparent rather than inventing facts.
"""

            with st.chat_message("assistant", avatar="🎓"):
                if not token:
                    answer = (
                        "The website interface is ready, but the AI connection is not configured yet.\n\n"
                        "**To activate answers:** create a Hugging Face access token, then add it as "
                        "`HF_TOKEN` in your Streamlit app's Secrets. You can also set `HF_MODEL` to a "
                        "model available through your Hugging Face Inference Providers account.\n\n"
                        "For security, do not paste your token into this chat or hard-code it in `app.py`."
                    )
                    st.info(answer)
                else:
                    try:
                        client = InferenceClient(model=model, token=token)
                        with st.spinner("Khurram is preparing your explanation…"):
                            response = client.chat_completion(
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    *[
                                        {"role": m["role"], "content": m["content"]}
                                        for m in st.session_state.messages[-10:]
                                    ],
                                ],
                                max_tokens=1400,
                                temperature=0.35,
                            )
                        answer = response.choices[0].message.content or "I couldn't generate an answer. Please try again."
                        st.markdown(answer)
                    except Exception as exc:
                        answer = (
                            "I couldn't connect to the selected Hugging Face model right now. "
                            "The model may be unavailable through your account, its provider may be busy, "
                            "or the token/model setting may need checking.\n\n"
                            f"**Technical detail:** `{type(exc).__name__}: {str(exc)[:500]}`\n\n"
                            "Check your `HF_TOKEN` and `HF_MODEL` settings, then try again."
                        )
                        st.error(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})

        if st.session_state.messages:
            if st.button("🗑️ Clear conversation"):
                st.session_state.messages = []
                st.rerun()

    with right:
        st.markdown("### ✨ Your study dashboard")
        st.markdown("""
        <div class="panel">
          <h4>🎯 Built around your class</h4>
          <p class="small-muted">Choose your class, subject and board in the sidebar to tailor each answer.</p>
        </div>
        <div class="panel">
          <h4>🧮 Maths, without skipped steps</h4>
          <p class="small-muted">Ask for the formula, working, reasoning, and final answer in textbook-style format.</p>
        </div>
        <div class="panel">
          <h4>📝 Exam preparation</h4>
          <p class="small-muted">Request short questions, long questions, definitions, MCQs, revision notes and practice tests.</p>
        </div>
        <div class="panel">
          <h4>📖 Textbook accuracy</h4>
          <p class="small-muted">For exact exercise answers, share the board, chapter and question text. This starter version does not yet contain all official textbooks.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("#### Quick prompts")
        examples = [
            "Solve a Class 10 algebra question step by step.",
            "Explain Newton's laws with examples.",
            "Make 10 exam-style MCQs from this chapter.",
            "Explain this topic in simple Urdu.",
        ]
        for example in examples:
            if st.button(example, key=f"quick_{example}", use_container_width=True):
                st.session_state.pending_prompt = example
                st.rerun()
        if "pending_prompt" in st.session_state:
            st.info("Quick prompt selected. Copy it into the chat box to send it.")

elif page == "How to use":
    st.markdown('<div class="hero"><h1>How to use <span class="gradient">Khurram\'s AI</span></h1><p>Get better answers by sharing clear questions and textbook context.</p></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="panel">
    <h3>1. Choose your class and board</h3>
    Select the class, subject, education board and answer language from the sidebar.
    </div>
    <div class="panel">
    <h3>2. Ask one clear question</h3>
    Include the chapter, exercise number and complete question when possible.
    </div>
    <div class="panel">
    <h3>3. Check the answer</h3>
    AI can make mistakes. For exam-critical answers, compare with your current textbook or teacher's guidance.
    </div>
    <div class="panel">
    <h3>4. Exact syllabus support</h3>
    This starter website does not automatically include every current Pakistani textbook. A later version can add legally obtained, board-specific textbook files and retrieval search.
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown('<div class="hero"><h1>About <span class="gradient">Khurram\'s AI</span></h1><p>A learning assistant concept designed for Pakistani school students.</p></div>', unsafe_allow_html=True)
    st.markdown("""
    Khurram's AI is a Streamlit-based tutoring website prototype for Classes 1–10, prioritising Classes 9 and 10.

    **What is included**
    - Responsive Streamlit layout
    - Class, subject, board and language selectors
    - Chat history during the current session
    - Hugging Face Inference API integration
    - Mathematics-focused step-by-step instructions

    **What still needs to be added for a production-quality syllabus tutor**
    - Board-verified and up-to-date textbooks
    - Retrieval-Augmented Generation (RAG) for textbook citations
    - More robust maths verification and testing
    - Usage limits, monitoring and privacy policy
    - A Hugging Face token stored securely in deployment secrets

    This app is an educational aid, not an official service of any Pakistani education board.
    """)

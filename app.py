# app.py
import streamlit as st
from FSM import EduFSM

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RuangSobat",
    page_icon="🧠",
    layout="centered"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

* { box-sizing: border-box; }
.stApp {
    background: #0d0d0d;
}
.stApp > header,
#MainMenu,
footer,
[data-testid="stToolbar"],
[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
}
.block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem 6rem !important;
    margin: 0 auto;
}

/* ── Header ── */
.rs-header {
    text-align: center;
    padding: 1.5rem 0 1.75rem;
    font-family: 'JetBrains Mono', monospace;
}
.rs-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #e8e8e8;
    letter-spacing: -0.02em;
    margin-bottom: 0.3rem;
}
.rs-title .accent { color: #10B981; }
.rs-sub {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3a3a3a;
    font-weight: 400;
}

/* ── Terminal window title bar ── */
.term-window {
    background: linear-gradient(160deg, #111111 0%, #161616 60%, #1a1a1a 100%);
    border: 0.5px solid #2a2a2a;
    border-radius: 10px 10px 0 0;
    overflow: hidden;
    margin-bottom: 0;
}
.term-titlebar {
    background: #1c1c1c;
    border-bottom: 0.5px solid #252525;
    padding: 8px 14px;
    display: flex;
    align-items: center;
    gap: 7px;
}
.term-dot { width: 11px; height: 11px; border-radius: 50%; }
.term-dot.red    { background: #FF5F57; }
.term-dot.yellow { background: #FFBD2E; }
.term-dot.green  { background: #28C840; }
.term-titlebar-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #444;
    margin-left: 6px;
    letter-spacing: 0.05em;
}

/* ── Strip default chat chrome ── */
div[data-testid="chatAvatarIcon-assistant"],
div[data-testid="chatAvatarIcon-user"] { display: none !important; }
div[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}
div[data-testid="stChatMessage"] > div { gap: 0 !important; }

/* ── Terminal message lines ── */
.term-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.65;
    padding: 5px 18px;
    white-space: pre-wrap;
    word-break: break-word;
}
.term-line.user {
    color: #c8c8c8;
    border-left: 2px solid #222;
}
.term-line.bot {
    color: #b0efcc;
    border-left: 2px solid #10B981;
    background: rgba(16, 185, 129, 0.03);
}
.term-prompt-user { color: #60a5fa; font-weight: 700; }
.term-prompt-bot  { color: #10B981; font-weight: 700; }
.term-dollar      { color: #444; }

/* inner markdown resets */
.term-line p      { margin: 0; display: inline; }
.term-line br     { display: block; content: ""; margin-top: 2px; }
.term-line code {
    background: #1a1a1a;
    border: 0.5px solid #2a2a2a;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #a3e4c8;
}
.term-line strong { color: #e8e8e8; font-weight: 700; }
.term-line em     { color: #777; font-style: italic; }

/* ── Chat input ── */
[data-testid="stChatInputContainer"] {
    background: linear-gradient(160deg, #111111 0%, #161616 100%) !important;
    border: 0.5px solid #2a2a2a !important;
    border-radius: 0 0 10px 10px !important;
    border-top: 0.5px solid #1e1e1e !important;
    padding: 2px 6px !important;
    margin-top: 0 !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #c8c8c8 !important;
    background: transparent !important;
    caret-color: #10B981 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #2e2e2e !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stChatInput"] button {
    background: transparent !important;
    color: #10B981 !important;
    border: none !important;
}
[data-testid="stChatInput"] button:hover { color: #34d399 !important; }

/* ── Floating right panel ── */
.float-panel {
    position: fixed;
    top: 80px;
    right: 24px;
    width: 200px;
    background: linear-gradient(160deg, #0f0f0f 0%, #151515 100%);
    border: 0.5px solid #222;
    border-radius: 10px;
    font-family: 'JetBrains Mono', monospace;
    z-index: 999;
    overflow: visible;
}
.float-panel-header {
    background: #1a1a1a;
    border-bottom: 0.5px solid #222;
    padding: 7px 11px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 10px 10px 0 0;
}
.float-panel-title {
    color: #3a3a3a;
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.float-panel-body { padding: 10px 11px 11px; }

.fp-section-label {
    color: #303030;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 5px;
    margin-top: 9px;
}
.fp-section-label:first-child { margin-top: 0; }

.fp-state-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 5px;
}
.fp-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; opacity: 0.8; }
.fp-choosing { background: #0a1525; color: #60a5fa; border: 0.5px solid #152040; }
.fp-idle     { background: #1a1100; color: #fbbf24; border: 0.5px solid #2a1c00; }
.fp-quiz     { background: #180808; color: #f87171; border: 0.5px solid #281010; }
.fp-eval     { background: #06150d; color: #34d399; border: 0.5px solid #0d2818; }

.fp-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    color: #333;
    border-bottom: 0.5px solid #181818;
    font-size: 0.65rem;
}
.fp-row:last-child { border-bottom: none; }
.fp-val {
    color: #777;
    background: #0a0a0a;
    padding: 1px 6px;
    border-radius: 3px;
    border: 0.5px solid #1e1e1e;
    max-width: 105px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 0.65rem;
}

/* ── Gear dropdown ── */
.fp-gear-wrap { position: relative; display: inline-block; }
.fp-gear-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #303030;
    font-size: 0.9rem;
    padding: 0 3px;
    line-height: 1;
}
.fp-gear-btn:hover { color: #555; }
.fp-dropdown {
    display: none;
    position: absolute;
    right: 0;
    top: calc(100% + 5px);
    background: #141414;
    border: 0.5px solid #252525;
    border-radius: 8px;
    min-width: 168px;
    z-index: 1001;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    overflow: hidden;
}
.fp-gear-wrap:hover .fp-dropdown,
.fp-gear-wrap:focus-within .fp-dropdown { display: block; }
.fp-dropdown-item {
    padding: 8px 13px;
    color: #555;
    font-size: 0.67rem;
    cursor: pointer;
    border-bottom: 0.5px solid #1c1c1c;
    white-space: nowrap;
    letter-spacing: 0.02em;
}
.fp-dropdown-item:last-child { border-bottom: none; }
.fp-dropdown-item:hover { background: #1c1c1c; color: #999; }
.fp-dropdown-item.danger { color: #c0392b; }
.fp-dropdown-item.danger:hover { background: #180808; color: #f87171; }
.fp-dd-divider { border-bottom: 0.5px solid #1e1e1e; margin: 2px 0; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE INIT ─────────────────────────────────────────────────────────
if "bot" not in st.session_state:
    st.session_state.bot = EduFSM()
    st.session_state.bot.step()
    st.session_state.messages = [{
        "role": "assistant",
        "content": st.session_state.bot.get_response()
    }]

# ── RESET HANDLER via query param ─────────────────────────────────────────────
if st.query_params.get("action") == "reset":
    st.session_state.bot.step("reset")
    st.session_state.messages = [{
        "role": "assistant",
        "content": st.session_state.bot.get_response()
    }]
    st.query_params.clear()
    st.rerun()

# ── FLOATING PANEL ─────────────────────────────────────────────────────────────
current_state = st.session_state.bot.state.name
subjek_aktif  = st.session_state.bot.current_subject or "—"
idx_soal      = st.session_state.bot.current_question_idx + 1
skor          = st.session_state.bot.score

state_map = {
    "IDLE":       ("fp-idle",     "State.IDLE"),
    "CHOOSING":   ("fp-choosing", "State.CHOOSING"),
    "QUIZ":       ("fp-quiz",     "State.QUIZ"),
    "EVALUATION": ("fp-eval",     "State.EVALUATION"),
}
badge_cls, badge_lbl = state_map.get(current_state, ("fp-idle", f"State.{current_state}"))

st.markdown(f"""
<div class="float-panel">
    <div class="float-panel-header">
        <span class="float-panel-title">rsb::monitor</span>
        <div class="fp-gear-wrap" tabindex="0">
            <button class="fp-gear-btn" aria-label="Options">⚙</button>
            <div class="fp-dropdown">
                <div class="fp-dropdown-item"
                     onclick="document.querySelector('[data-testid=stChatInput] textarea').value='menu'; document.querySelector('[data-testid=stChatInput] textarea').dispatchEvent(new Event('input',{{bubbles:true}}))">
                    📋 &nbsp;Lihat Menu Topik
                </div>
                <div class="fp-dropdown-item"
                     onclick="document.querySelector('[data-testid=stChatInput] textarea').value='help'; document.querySelector('[data-testid=stChatInput] textarea').dispatchEvent(new Event('input',{{bubbles:true}}))">
                    🆘 &nbsp;Panduan
                </div>
                <div class="fp-dd-divider"></div>
                <div class="fp-dropdown-item danger"
                     onclick="window.location.href='?action=reset'">
                    🔄 &nbsp;Reset Otomata
                </div>
            </div>
        </div>
    </div>
    <div class="float-panel-body">
        <div class="fp-section-label">fsm state</div>
        <div class="fp-state-badge {badge_cls}">
            <span class="fp-dot"></span>{badge_lbl}
        </div>
        <div class="fp-section-label">data log</div>
        <div class="fp-row"><span>subjek</span><span class="fp-val">{subjek_aktif}</span></div>
        <div class="fp-row"><span>soal ke-</span><span class="fp-val">{idx_soal}</span></div>
        <div class="fp-row"><span>skor</span><span class="fp-val">{skor}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rs-header">
    <div class="rs-title">🧠 <span class="accent">Ruang</span>Sobat</div>
    <div class="rs-sub">fsm chatbot &nbsp;·&nbsp; python &nbsp;·&nbsp; no api</div>
</div>
""", unsafe_allow_html=True)

# ── TERMINAL TITLEBAR ──────────────────────────────────────────────────────────
st.markdown("""
<div class="term-window">
    <div class="term-titlebar">
        <span class="term-dot red"></span>
        <span class="term-dot yellow"></span>
        <span class="term-dot green"></span>
        <span class="term-titlebar-label">ruangsobat@rsb: ~/fsm-chat</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── RENDER MESSAGES ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(
                f'<div class="term-line user">'
                f'<span class="term-prompt-user">you@user</span>'
                f'<span class="term-dollar">:~$ </span>'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        with st.chat_message("assistant"):
            st.markdown(
                f'<div class="term-line bot">'
                f'<span class="term-prompt-bot">ruangsobat@rsb</span>'
                f'<span class="term-dollar">:~$ </span>'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True
            )

# ── INPUT ──────────────────────────────────────────────────────────────────────
if user_input := st.chat_input("you@user:~$ ..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(
            f'<div class="term-line user">'
            f'<span class="term-prompt-user">you@user</span>'
            f'<span class="term-dollar">:~$ </span>'
            f'{user_input}'
            f'</div>',
            unsafe_allow_html=True
        )

    st.session_state.bot.step(user_input)
    bot_response = st.session_state.bot.get_response()

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(
            f'<div class="term-line bot">'
            f'<span class="term-prompt-bot">ruangsobat@rsb</span>'
            f'<span class="term-dollar">:~$ </span>'
            f'{bot_response}'
            f'</div>',
            unsafe_allow_html=True
        )

    if "Rampung." in bot_response or "Rapor Hasil" in bot_response:
        st.balloons()

    st.rerun()

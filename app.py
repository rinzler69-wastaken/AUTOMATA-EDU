# app.py
import streamlit as st
from FSM import EduFSM

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="RuangSobat - Platform FSM", 
    page_icon="🧠", 
    layout="centered"
)

# 2. EMBED CSS PEMANIS TAMPILAN
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Judul Utama Berkilaunya */
    .super-title {
        background: linear-gradient(45deg, #1E3A8A, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 0px;
        padding-top: 10px;
    }
    
    .super-sub {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        font-weight: 500;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Balon Obrolan RuangSobat */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #ffffff;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        border-left: 6px solid #10B981;
        padding: 18px;
        margin-bottom: 12px;
        animation: fadeIn 0.4s ease-in-out;
    }
    
    /* Balon Obrolan Siswa */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #E0F2FE;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.06);
        border-right: 6px solid #3B82F6;
        padding: 18px;
        margin-bottom: 12px;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(6px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# 3. TAMPILAN HEADER UTAMA
st.markdown('<div class="super-title">🧠 RuangSobat</div>', unsafe_allow_html=True)
st.markdown('<div class="super-sub">Teman Belajar & Diskusi Interaktif Berbasis Finite State Machine</div>', unsafe_allow_html=True)

# 4. INISIALISASI SESSION STATE
if "bot" not in st.session_state:
    st.session_state.bot = EduFSM()
    st.session_state.bot.step()  
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Halo! 👋 Selamat datang di **RuangSobat**. Di sini kita bisa seru-seruan belajar bareng sekaligus uji kemampuan lewat kuis interaktif. Ketik **'menu'** ya buat lihat topik apa aja yang bisa kita bedah!"
    }]

# 5. SIDEBAR MONITORING DASHBOARD
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8945/8945259.png", width=90)
    st.markdown("### 🛠️ Engine Control Center")
    st.caption("Monitoring status translasi bahasa & perpindahan state otomata secara realtime.")
    st.markdown("---")
    
    # Deteksi Warna State secara Dinamis
    current_state = st.session_state.bot.state.name
    st.markdown("**Status State Saat Ini:**")
    if current_state == "IDLE":
        st.warning(f"🟠 State.{current_state}")
    elif current_state == "CHOOSING":
        st.info(f"🔵 State.{current_state}")
    elif current_state == "QUIZ":
        st.error(f"🔴 State.{current_state}")
    else:
        st.success(f"🟢 State.{current_state}")
        
    st.markdown("---")
    st.markdown("**Data Log Tracker:**")
    
    subjek_aktif = st.session_state.bot.current_subject
    st.markdown(f"📖 Subjek Aktif: `{subjek_aktif if subjek_aktif else 'Belum Memilih'}`")
    st.markdown(f"❓ Index Soal: `Ke-{st.session_state.bot.current_question_idx + 1}`")
    st.markdown(f"🎯 Skor Benar: `{st.session_state.bot.score}`")
    
    st.markdown("---")
    if st.button("🔄 Paksa Reset Otomata (Reset)", use_container_width=True):
        st.session_state.bot.step("reset")
        st.session_state.messages = [{"role": "assistant", "content": st.session_state.bot.get_response()}]
        st.toast("Sistem automata berhasil dikembalikan ke State.IDLE!", icon="🔄")
        st.rerun()

# 6. RENDER DAFTAR PERCAKAPAN DI LAYAR WEB
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. PROSES INPUT CHAT SISWA
if user_input := st.chat_input("Tulis pesanmu di sini... (misal: 'menu', 'belajar sains', atau jawab soal)"):
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.bot.step(user_input)
    bot_response = st.session_state.bot.get_response()
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
        
    # Efek khusus: Balon terbang jika kuis selesai!
    if "Rampung." in bot_response or "Rapor Hasil" in bot_response:
        st.balloons()
        
    st.rerun()
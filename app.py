import streamlit as st
import random
import json
import os
from FSM import EduFSM
from engine import EduEngine

# ==========================================
# 1. KONFIGURASI HALAMAN & LAYOUT
# ==========================================
st.set_page_config(
    page_title="Dunia Belajar Sobat Cilik 🎓", 
    page_icon="🎮", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# ==========================================
# 2. PERSISTENCE LAYER (JSON SAVE/LOAD)
# ==========================================
PROGRESS_FILE = "progress_data.json"

DEFAULT_PROGRESS = {
    "bintang_skor": 0,
    "completed_games": [],
    "completed_readings": [],
    "claimed_chests": [],
    "petualang_name": "Petualang Cilik",
    "petualang_avatar": "🦁 Leo Lion",
    "streak": 1,
    "selected_matkul": "Berhitung Seru",
    "active_quiz_questions": [],
    "active_quiz_idx": 0,
    "active_quiz_score": 0,
    "active_quiz_answered": False,
    "active_quiz_feedback": "",
    "active_quiz_history": [],
    "active_quiz_completed": False
}

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                # Ensure all default keys are present
                for k, v in DEFAULT_PROGRESS.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            return DEFAULT_PROGRESS.copy()
    return DEFAULT_PROGRESS.copy()

def save_progress():
    if "progress_loaded" in st.session_state:
        data = {
            "bintang_skor": st.session_state.bintang_skor,
            "completed_games": st.session_state.completed_games,
            "completed_readings": st.session_state.completed_readings,
            "claimed_chests": st.session_state.claimed_chests,
            "petualang_name": st.session_state.petualang_name,
            "petualang_avatar": st.session_state.petualang_avatar,
            "streak": st.session_state.streak,
            "selected_matkul": st.session_state.selected_matkul,
            "active_quiz_questions": st.session_state.active_quiz_questions,
            "active_quiz_idx": st.session_state.active_quiz_idx,
            "active_quiz_score": st.session_state.active_quiz_score,
            "active_quiz_answered": st.session_state.active_quiz_answered,
            "active_quiz_feedback": st.session_state.active_quiz_feedback,
            "active_quiz_history": st.session_state.active_quiz_history,
            "active_quiz_completed": st.session_state.active_quiz_completed
        }
        try:
            with open(PROGRESS_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

# Monkeypatch st.rerun to auto-save on every rerun
_original_rerun = st.rerun
def custom_rerun():
    save_progress()
    _original_rerun()
st.rerun = custom_rerun

# Load progress into session state
if "progress_loaded" not in st.session_state:
    progress = load_progress()
    for k, v in progress.items():
        st.session_state[k] = v
    st.session_state.progress_loaded = True

if "edu_engine" not in st.session_state:
    st.session_state.edu_engine = EduEngine()

# Map dari cartridge game di app.py ke subject di engine.py (diselaraskan)
CARTRIDGE_TO_ENGINE = {
    "Berhitung Seru": "matematika",
    "Penjelajah Dunia (IPA)": "biologi",
    "Bahasa & Cerita": "bahasa indonesia",
    "Kreatif Digital": "teknologi informasi",
    "Penjelajah Bumi (Geografi)": "geografi",
    "Petualangan Fisika": "fisika",
    "Lab Kimia Cilik": "kimia",
    "Detektif Sejarah (IPS)": "sejarah",
    "English Adventure": "bahasa inggris"
}

def select_cartridge(name):
    st.session_state.selected_matkul = name
    engine_subj = CARTRIDGE_TO_ENGINE.get(name, "matematika")
    all_q = st.session_state.edu_engine.course_data[engine_subj]["kuis"]
    # Ambil 10 soal acak dari 20 soal yang tersedia
    st.session_state.active_quiz_questions = random.sample(all_q, min(len(all_q), 10))
    st.session_state.active_quiz_idx = 0
    st.session_state.active_quiz_score = 0
    st.session_state.active_quiz_answered = False
    st.session_state.active_quiz_feedback = ""
    st.session_state.active_quiz_history = []
    st.session_state.active_quiz_completed = False

def request_switch_cartridge(name, target_page="Petualangan"):
    if st.session_state.get("selected_matkul") == name:
        st.session_state.halaman_aktif = target_page
        return
    st.session_state.confirm_switch_cartridge = name
    st.session_state.confirm_switch_target_page = target_page

# Inisialisasi state game lainnya
if "halaman_aktif" not in st.session_state:
    st.session_state.halaman_aktif = "Beranda"

if "sub_tab_beranda" not in st.session_state:
    st.session_state.sub_tab_beranda = "Dasbor"

if "sub_tab_petualangan" not in st.session_state:
    st.session_state.sub_tab_petualangan = "Cartridges"

if "selected_matkul" not in st.session_state:
    st.session_state.selected_matkul = "Berhitung Seru"
elif st.session_state.selected_matkul is not None and st.session_state.selected_matkul not in CARTRIDGE_TO_ENGINE:
    st.session_state.selected_matkul = "Berhitung Seru"

if "active_quiz_questions" not in st.session_state or st.session_state.active_quiz_questions is None:
    if st.session_state.selected_matkul is not None:
        select_cartridge(st.session_state.selected_matkul)
    else:
        st.session_state.active_quiz_questions = []

if "buka_chat_piko" not in st.session_state:
    st.session_state.buka_chat_piko = False

# FSM instance — persistent across reruns, reset only when user triggers it
if "piko_fsm" not in st.session_state:
    fsm = EduFSM()
    fsm.step("")          # boot FSM ke state CHOOSING, hasilkan greeting
    st.session_state.piko_fsm = fsm
    st.session_state.riwayat_chat = [
        {"role": "assistant", "content": fsm.get_response()}
    ]

if "riwayat_chat" not in st.session_state:
    st.session_state.riwayat_chat = []

# ==========================================
# 3. DATA MATKUL & GAME
# ==========================================
matkul_data = {
    "Berhitung Seru": {
        "emoji": "🧮", 
        "desc": "Belajar tambah-tambahan, perkalian kilat, dan tebak angka ajaib lewat game seru!",
        "materi": (
            "• **Penjumlahan Ajaib:** Yuk bantu Milo si kelinci menghitung wortelnya! $2 + 3 = 5$ wortel manis! 🥕\n\n"
            "• **Tebak Bangun Datar:** Bentuk pizza itu lingkaran, kalau atap rumah itu segitiga, dan buku tulis itu persegi panjang! 🍕🏠📖\n\n"
            "• **Perkalian Kilat Jari:** Perkalian angka 9 itu ajaib lho! Coba lipat jari keempatmu dari kiri, taraaa! $4 \\times 9 = 36$! 🖐️✨\n\n"
            "• **Mengenal Jam & Waktu:** Jarum pendek menunjukkan jam, jarum panjang menunjukkan menit. 🎒⏰"
        )
    },
    "Penjelajah Dunia (IPA)": {
        "emoji": "🦁", 
        "desc": "Mengenal hewan purba, sistem tata surya, dan rahasia tumbuhan ajaib di sekitar kita.",
        "materi": (
            "• **Dunia Hewan:** Herbivora (Sapi 🐄), Karnivora (Singa 🦁), dan Omnivora (Ayam 🐓)!\n\n"
            "• **Sistem Tata Surya:** Bumi kita adalah planet ketiga yang berputar mengelilingi Matahari. Planet bercincin indah namanya Saturnus! 🌍🪐☀️\n\n"
            "• **Bagian Tumbuhan:** Akar mencari air, batang menopang, daun memasak makanan (fotosintesis), dan bunga menjadi buah! 🌳🍎\n\n"
            "• **Wujud Benda:** Ada benda padat (es batu 🧊), cair (air susu 🥛), dan gas (balon 🎈)."
        )
    },
    "Bahasa & Cerita": {
        "emoji": "📚", 
        "desc": "Membaca dongeng petualangan nusantara, menyusun kalimat sakti, dan kuis kosakata.",
        "materi": (
            "• **Membaca Dongeng:** Kisah Kancil yang cerdik mengelabui Buaya yang sedang kelaparan di sungai. 🐊\n\n"
            "• **Tiga Kata Sakti:** Selalu gunakan kata 'Tolong', 'Maaf', 'Terima Kerja', dan 'Terima Kasih'! 🌟\n\n"
            "• **Struktur Kalimat (SPOK):** Contoh: Budi (S) membaca (P) buku (O) di kelas (K). 📝\n\n"
            "• **Puisi Anak Indah:** Belajar membaca puisi dengan ekspresi penuh penjiwaan. 🌅"
        )
    },
    "Kreatif Digital": {
        "emoji": "🎨", 
        "desc": "Belajar menggambar pixel di komputer, logika blok warna, dan teknologi masa depan.",
        "materi": (
            "• **Mewarnai Pixel:** Gambar digital di komputer terbentuk dari kotak-kotak kecil bernama pixel. 👾\n\n"
            "• **Logika Robot:** Perintah arah berturut-turut (Maju -> Belok Kanan) agar robot berjalan lancar. 🤖\n\n"
            "• **Internet Sehat:** Internet adalah jendela dunia, gunakan didampingi orang tua! 💻👨‍👩‍👧\n\n"
            "• **Bikin Animasi Sederhana:** Menggabungkan gambar agar terlihat bergerak hidup! 🎬"
        )
    },
    "Penjelajah Bumi (Geografi)": {
        "emoji": "🌍",
        "desc": "Petualangan seru menjelajahi lapisan bumi, siklus air, dan peta benua raksasa!",
        "materi": (
            "• **Lapisan Bumi:** Kerak bumi paling luar tempat kita tinggal, di bawahnya ada mantel dan inti bumi. 🌍\n\n"
            "• **Siklus Air:** Penguapan (evaporasi), pembentukan awan (kondensasi), dan hujan turun (presipitasi). 🌧️\n\n"
            "• **Benua & Samudra:** Benua Asia adalah yang terbesar, dan Samudra Pasifik adalah yang terluas! 🗺️"
        )
    },
    "Petualangan Fisika": {
        "emoji": "⚡",
        "desc": "Belajar gaya gerak, energi potensial, hukum gravitasi, dan listrik dengan cara seru!",
        "materi": (
            "• **Gaya & Gerak:** Dorongan atau tarikan yang mengubah gerakan benda. $F = ma$! ⚡\n\n"
            "• **Energi Potensial:** Energi karena posisi ketinggian benda. $Ep = mgh$! 🍎\n\n"
            "• **Hukum Ohm:** Hubungan tegangan (V), arus (I), dan hambatan (R): $V = IR$. 🔌"
        )
    },
    "Lab Kimia Cilik": {
        "emoji": "🧪",
        "desc": "Temukan rahasia atom molekul, reaksi warna-warni, dan keajaiban asam-basa!",
        "materi": (
            "• **Bagian Atom:** Proton bermuatan positif (+), elektron bermuatan negatif (-), neutron netral. ⚛️\n\n"
            "• **Asam & Basa:** Asam memiliki pH kurang dari 7 (seperti jeruk 🍋), basa memiliki pH lebih dari 7 (seperti sabun 🧼).\n\n"
            "• **Reaksi Kimia:** Menggabungkan dua zat menjadi zat baru, contohnya hidrogen + oksigen menjadi air ($H_2O$)! 💧"
        )
    },
    "Detektif Sejarah (IPS)": {
        "emoji": "📜",
        "desc": "Membaca peta peristiwa bersejarah pahlawan bangsa, proklamasi kemerdekaan, dan budaya nusantara.",
        "materi": (
            "• **Proklamasi RI:** Dibacakan oleh Bung Karno pada 17 Agustus 1945 didampingi Bung Hatta. 🇮🇩\n\n"
            "• **Sumpah Pemuda:** Ikrar satu nusa, bangsa, dan bahasa pada 28 Oktober 1928. 🗺️\n\n"
            "• **Kerajaan Nusantara:** Patih Gajah Mada dari Majapahit bersumpah Palapa untuk menyatukan nusantara!"
        )
    },
    "English Adventure": {
        "emoji": "🇬🇧",
        "desc": "Belajar bahasa Inggris seru: kosakata (vocabulary), tata bahasa (grammar), percakapan sehari-hari, dan tenses dasar.",
        "materi": (
            "• **Greetings:** Hello, Good Morning, How are you?, Goodbye. 👋\n\n"
            "• **Simple Present Tense:** Menyatakan fakta atau kebiasaan. Rumus: $S + V_1(s/es)$. *Example: She eats an apple.* 🍎\n\n"
            "• **Vocabulary - Colors:** Red (merah), Blue (biru), Green (hijau), Yellow (kuning), White (putih). 🎨\n\n"
            "• **Prepositions:** In (di dalam), On (di atas permukaan), Under (di bawah), Beside (di samping). 📦"
        )
    }
}

ACHIEVEMENTS = [
    {
        "id": "first_star",
        "title": "Bintang Pertama",
        "emoji": "⭐",
        "desc": "Dapatkan 10 bintang pertama dalam petualanganmu!",
        "req": lambda stars, completed: stars >= 10
    },
    {
        "id": "math_wizard",
        "title": "Pakar Berhitung",
        "emoji": "🧮",
        "desc": "Selesaikan petualangan Berhitung Seru.",
        "req": lambda stars, completed: "Berhitung Seru" in completed
    },
    {
        "id": "nature_explorer",
        "title": "Penjelajah Alam",
        "emoji": "🦁",
        "desc": "Selesaikan kuis Penjelajah Dunia (IPA).",
        "req": lambda stars, completed: "Penjelajah Dunia (IPA)" in completed
    },
    {
        "id": "polyglot",
        "title": "Sahabat Bahasa",
        "emoji": "📚",
        "desc": "Selesaikan petualangan Bahasa & Cerita.",
        "req": lambda stars, completed: "Bahasa & Cerita" in completed
    },
    {
        "id": "digital_creator",
        "title": "Kreator Digital",
        "emoji": "🎨",
        "desc": "Selesaikan kuis Kreatif Digital.",
        "req": lambda stars, completed: "Kreatif Digital" in completed
    },
    {
        "id": "geo_wizard",
        "title": "Penjelajah Bumi",
        "emoji": "🌍",
        "desc": "Selesaikan kuis Penjelajah Bumi (Geografi).",
        "req": lambda stars, completed: "Penjelajah Bumi (Geografi)" in completed
    },
    {
        "id": "phys_wizard",
        "title": "Pakar Fisika",
        "emoji": "⚡",
        "desc": "Selesaikan kuis Petualangan Fisika.",
        "req": lambda stars, completed: "Petualangan Fisika" in completed
    },
    {
        "id": "chem_wizard",
        "title": "Pakar Kimia",
        "emoji": "🧪",
        "desc": "Selesaikan kuis Lab Kimia Cilik.",
        "req": lambda stars, completed: "Lab Kimia Cilik" in completed
    },
    {
        "id": "history_detective",
        "title": "Detektif Sejarah",
        "emoji": "🗺️",
        "desc": "Selesaikan kuis Detektif Sejarah (IPS).",
        "req": lambda stars, completed: "Detektif Sejarah (IPS)" in completed
    },
    {
        "id": "english_wizard",
        "title": "Master Bahasa Inggris",
        "emoji": "🇬🇧",
        "desc": "Selesaikan kuis English Adventure.",
        "req": lambda stars, completed: "English Adventure" in completed
    },
    {
        "id": "halfway_there",
        "title": "Kolektor Bintang",
        "emoji": "💎",
        "desc": "Kumpulkan total 50 bintang prestasi.",
        "req": lambda stars, completed: stars >= 50
    },
    {
        "id": "grandmaster",
        "title": "Legenda Akademi",
        "emoji": "👑",
        "desc": "Selesaikan seluruh 9 petualangan kuis!",
        "req": lambda stars, completed: len(completed) >= 9
    }
]

# LEVEL CALCULATION
def get_player_level(stars):
    level = (stars // 20) + 1
    xp_current = stars % 20
    xp_needed = 20
    progress = int((xp_current / xp_needed) * 100)
    
    if level == 1:
        title = "Petualang Pemula 🎒"
    elif level == 2:
        title = "Penjelajah Cerdas 🗺️"
    elif level == 3:
        title = "Ksatria Bintang ⭐"
    elif level == 4:
        title = "Juara Kelas Cilik 🏆"
    else:
        title = "Master Sobat Cilik 👑"
        
    return level, xp_current, xp_needed, progress, title

def get_unlocked_badges():
    unlocked = []
    completed = st.session_state.completed_games
    stars = st.session_state.bintang_skor
    for badge in ACHIEVEMENTS:
        if badge["req"](stars, completed):
            unlocked.append(badge["id"])
    return unlocked

# Bot requirements
konteks_materi_web = ""
for nama_mapel, isi in matkul_data.items():
    konteks_materi_web += f"\n- Mapel {nama_mapel}: {isi['desc']} Konten dasar: {isi['materi']}"

# ==========================================
# 4. CUSTOM DESIGN SYSTEM (CSS) OVERRIDES
# ==========================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@400;600;700;800&display=swap');

        [data-testid="stHeader"] { display: none; }
        
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Nunito', 'Poppins', sans-serif;
            background-color: #FAF8F0; 
            color: #2C3E50;
        }

        .stAppViewBlockContainer {
            padding-top: 2rem !important;
            padding-bottom: 6rem !important;
        }
        
        .stMarkdown {
            font-family: 'Nunito', sans-serif;
            color: #2C3E50;
        }

        /* Console Logo / Dock Header */
        .console-logo {
            font-family: 'Nunito', sans-serif;
            font-weight: 950;
            font-size: 24px;
            color: #FF8A00;
            text-shadow: 2px 2px 0px #2C3E50;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }

        /* Tactical Active navigation dock button selection */
        div[data-testid="stHorizontalBlock"]:has(.console-logo) .stButton > button {
            background: #FFFFFF !important; 
            color: #2C3E50 !important;
            font-weight: 800 !important; 
            font-size: 14px !important;
            border: 3px solid #2C3E50 !important;
            box-shadow: 0 4px 0px #2C3E50 !important;
            transition: all 0.1s ease !important;
            border-radius: 16px !important;
            padding: 8px 12px !important;
            text-transform: uppercase;
        }
        
        div[data-testid="stHorizontalBlock"]:has(.console-logo) .stButton > button:hover { 
            background-color: #FFFDF5 !important;
            transform: translateY(2px) !important;
            box-shadow: 0 2px 0px #2C3E50 !important;
        }

        /* Cartridge style Game Cards */
        .cartridge-card {
            background: white; 
            padding: 24px; 
            border-radius: 28px; 
            box-shadow: 0 10px 0px #2C3E50;
            text-align: center; 
            margin-bottom: 16px;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 4px solid #2C3E50;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        .cartridge-card.completed {
            border-color: #10C95B;
            box-shadow: 0 10px 0px #0EB351;
        }

        .cartridge-badge {
            background: #10C95B;
            color: white;
            border: 2px solid #2C3E50;
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 800;
            position: absolute;
            top: 12px;
            right: 12px;
        }

        .cartridge-emoji {
            font-size: 52px;
            margin: 12px 0;
            animation: float 3s ease-in-out infinite;
        }

        /* Mascot Speech Bubble */
        .mascot-speech-bubble {
            background: #FFFFFF;
            border: 4px solid #2C3E50;
            border-radius: 24px;
            padding: 20px 24px;
            position: relative;
            box-shadow: 0 8px 0px #2C3E50;
            margin-bottom: 24px;
        }

        .mascot-speech-bubble::after {
            content: '';
            position: absolute;
            left: 30px;
            bottom: -16px;
            border-width: 16px 16px 0;
            border-style: solid;
            border-color: #FFFFFF transparent;
            display: block;
            width: 0;
        }

        .mascot-speech-bubble::before {
            content: '';
            position: absolute;
            left: 28px;
            bottom: -21px;
            border-width: 17px 17px 0;
            border-style: solid;
            border-color: #2C3E50 transparent;
            display: block;
            width: 0;
        }

        /* Handheld console layout bezel styling */
        .game-screen-bezel-header {
            background: #FAF8F0;
            border: 4px solid #2C3E50;
            border-bottom: none;
            border-radius: 24px 24px 0 0;
            padding: 14px 24px;
            color: #2C3E50;
        }

        div.st-key-console_screen_container {
            background: #FAF8F0 !important;
            border: 4px solid #2C3E50 !important;
            border-top: none !important;
            border-radius: 0 0 24px 24px !important;
            padding: 24px 24px 12px 24px !important;
            box-shadow: 0 8px 0px #2C3E50 !important;
        }

        div.st-key-console_screen_container div[data-testid="column"],
        div.st-key-console_screen_container div[data-testid="stColumn"] {
            background: #FFFFFF !important;
            border: 3px solid #2C3E50 !important;
            border-radius: 20px !important;
            padding: 20px !important;
        }

        /* Keyframes */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0px); }
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-6px); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* Custom buttons styling */
        .stButton>button {
            background: #10C95B !important; 
            color: white !important;
            border-radius: 18px !important; 
            border: 3px solid #2C3E50 !important;
            font-weight: 800 !important; 
            font-size: 15px !important;
            box-shadow: 0 6px 0px #2C3E50 !important; 
            transition: all 0.1s ease !important; 
            padding: 10px 24px !important;
        }
        
        .stButton>button:hover { 
            transform: translateY(2px) !important; 
            box-shadow: 0 4px 0px #2C3E50 !important; 
            background: #0EB351 !important;
        }

        .stButton>button:active {
            transform: translateY(4px) !important;
            box-shadow: 0 1px 0px #2C3E50 !important;
        }

        .btn-orange button {
            background: #FF8A00 !important;
        }
        .btn-orange button:hover {
            background: #E67A00 !important;
        }
        
        .btn-red button {
            background: #FF4747 !important;
        }
        .btn-red button:hover {
            background: #D03B3B !important;
        }

        /* Custom chat bubble design */
        [data-testid="stChatMessage"]:nth-child(even) {
            background-color: #FFF5E6 !important; 
            border-radius: 20px 20px 4px 20px !important;
            border: 3px solid #2C3E50 !important;
            padding: 16px !important; 
            color: #2C3E50 !important; 
            box-shadow: 0 4px 0px #2C3E50 !important;
            margin-bottom: 12px;
        }
        
        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #E8F9F0 !important; 
            border-radius: 20px 20px 20px 4px !important;
            border: 3px solid #2C3E50 !important;
            padding: 16px !important; 
            color: #2C3E50 !important; 
            box-shadow: 0 4px 0px #2C3E50 !important;
            margin-bottom: 12px;
        }

        /* Floating Chatbot Button Container */
        div.st-key-piko_floating_avatar {
            position: fixed !important; 
            bottom: 32px !important; 
            right: 32px !important; 
            z-index: 99999 !important;
            width: 80px !important;
            height: 80px !important;
        }

        div.st-key-piko_floating_avatar button {
            background: #FF8A00 !important;
            color: white !important;
            border-radius: 50% !important;
            width: 80px !important;
            height: 80px !important;
            border: 4px solid #2C3E50 !important;
            box-shadow: 0 6px 0px #2C3E50 !important;
            font-size: 24px !important;
            font-weight: 900 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            line-height: 1 !important;
            padding: 0 !important;
            transition: all 0.1s ease !important;
        }

        div.st-key-piko_floating_avatar button:hover {
            transform: translateY(2px) !important;
            box-shadow: 0 4px 0px #2C3E50 !important;
        }

        div.st-key-piko_floating_avatar button:active {
            transform: translateY(4px) !important;
            box-shadow: 0 1px 0px #2C3E50 !important;
        }

        /* Floating Chatbot Window Container */
        div.st-key-chatbot_window {
            position: fixed !important;
            bottom: 130px !important;
            right: 32px !important;
            width: 380px !important;
            max-width: 90vw !important;
            height: 520px !important;
            max-height: 70vh !important;
            background: #FAF8F0 !important;
            border: 4px solid #2C3E50 !important;
            border-radius: 24px !important;
            box-shadow: 0 12px 0px #2C3E50 !important;
            z-index: 99998 !important;
            padding: 20px !important;
            display: flex !important;
            flex-direction: column !important;
            overflow: hidden !important;
        }

        /* Inner Scroll Area for Message History */
        div.st-key-chat_messages_scroll {
            flex-grow: 1 !important;
            overflow-y: auto !important;
            padding-right: 8px !important;
            margin-bottom: 12px !important;
            max-height: 320px !important;
        }

        /* Custom expander customisations */
        div[data-testid="stExpander"] {
            border: 3px solid #2C3E50 !important;
            border-radius: 20px !important;
            background: #FFFFFF !important;
            box-shadow: 0 6px 0px #2C3E50 !important;
            margin-bottom: 16px !important;
        }

        /* ==========================================
           RESPONSIVE MEDIA QUERIES
           ========================================== */
        @media (max-width: 768px) {
            /* Make console layout flex-wrap and horizontal even on mobile */
            div[data-testid="stHorizontalBlock"]:has(.console-logo) {
                flex-direction: row !important;
                flex-wrap: wrap !important;
                justify-content: center !important;
                gap: 8px !important;
            }
            
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="stColumn"] {
                width: calc(33.33% - 12px) !important;
                min-width: 90px !important;
                flex: unset !important;
            }

            /* Make the logo column take full width on mobile so buttons wrap below it */
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="column"]:first-child,
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="stColumn"]:first-child {
                width: 100% !important;
                text-align: center !important;
                justify-content: center !important;
                margin-bottom: 12px !important;
            }

            /* Responsive Bezel Screen Container */
            div.st-key-console_screen_container {
                padding: 16px 12px !important;
            }
            
            div.st-key-console_screen_container div[data-testid="column"],
            div.st-key-console_screen_container div[data-testid="stColumn"] {
                padding: 16px !important;
                margin-bottom: 16px !important;
                width: 100% !important;
                flex: none !important;
            }
 
            /* Responsive Home Metrics Grid (2x2 on Mobile/Tablet) */
            div[data-testid="stHorizontalBlock"]:has(.metric-card) {
                flex-direction: row !important;
                flex-wrap: wrap !important;
                gap: 12px !important;
            }
            div[data-testid="stHorizontalBlock"]:has(.metric-card) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(.metric-card) > div[data-testid="stColumn"] {
                width: calc(50% - 12px) !important;
                flex: none !important;
                min-width: 120px !important;
            }
 
            /* Responsive Cartridge Cards Grid (Stack vertically on mobile/tablet) */
            div[data-testid="stHorizontalBlock"]:has(.cartridge-card) {
                flex-direction: row !important;
                flex-wrap: wrap !important;
                gap: 12px !important;
            }
            div[data-testid="stHorizontalBlock"]:has(.cartridge-card) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(.cartridge-card) > div[data-testid="stColumn"] {
                width: 100% !important;
                flex: none !important;
                margin-bottom: 16px !important;
            }
 
            /* Responsive Badge Cards Grid (2-column wrap) */
            div[data-testid="stHorizontalBlock"]:has(div[style*="height: 230px"]) {
                flex-direction: row !important;
                flex-wrap: wrap !important;
                gap: 12px !important;
            }
            div[data-testid="stHorizontalBlock"]:has(div[style*="height: 230px"]) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(div[style*="height: 230px"]) > div[data-testid="stColumn"] {
                width: calc(50% - 12px) !important;
                flex: none !important;
                min-width: 120px !important;
            }
 
            /* Responsive Chest Cards Grid (Stack vertically on mobile/tablet) */
            div[data-testid="stHorizontalBlock"]:has(.chest-card) {
                flex-direction: row !important;
                flex-wrap: wrap !important;
                gap: 12px !important;
            }
            div[data-testid="stHorizontalBlock"]:has(.chest-card) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(.chest-card) > div[data-testid="stColumn"] {
                width: 100% !important;
                flex: none !important;
                margin-bottom: 12px !important;
            }
        }
 
        @media (max-width: 480px) {
            /* Full width stack on small screens */
            div[data-testid="stHorizontalBlock"]:has(.cartridge-card) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(.cartridge-card) > div[data-testid="stColumn"] {
                width: 100% !important;
                flex: none !important;
            }
            div[data-testid="stHorizontalBlock"]:has(.metric-card) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(.metric-card) > div[data-testid="stColumn"] {
                width: 100% !important;
                flex: none !important;
            }
            div[data-testid="stHorizontalBlock"]:has(div[style*="height: 230px"]) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(div[style*="height: 230px"]) > div[data-testid="stColumn"] {
                width: 100% !important;
                flex: none !important;
            }
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="column"],
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="stColumn"] {
                width: calc(50% - 8px) !important;
                flex: none !important;
            }
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="column"]:first-child,
            div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="stColumn"]:first-child {
                width: 100% !important;
                flex: none !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4b. SIDEBAR: PANEL BELAJAR (dari FSM)
# ==========================================
with st.sidebar:
    st.markdown("## 📘 Panel Belajar")
    st.markdown("---")

    fsm_instance: EduFSM = st.session_state.get("piko_fsm")
    if fsm_instance and fsm_instance.last_formula:
        st.markdown(fsm_instance.last_formula)
    else:
        st.info(
            "Panel ini akan otomatis terisi ketika kamu meminta materi ke **RuangSobat** "
            "di chat (klik ikon avatar di pojok kanan bawah).\n\n"
            "Contoh: ketik *'belajar fisika'* atau *'materi kimia'*."
        )

    st.markdown("---")
    if fsm_instance:
        st.caption(f"🤖 Status chat: **{fsm_instance.state.name}**")
        if fsm_instance.current_subject:
            st.caption(f"📖 Topik aktif: **{fsm_instance.current_subject.capitalize()}**")

# ==========================================
# 5. RENDER TOP NAV BAR (TACTICAL DOCK)
# ==========================================
nav_cols = st.columns([3.5, 1.7, 1.7, 1.7, 1.7, 1.7])

with nav_cols[0]:
    st.markdown('<div class="console-logo">🎮 SOBAT CILIK</div>', unsafe_allow_html=True)

with nav_cols[1]:
    if st.button("🏠 BERANDA", key="nav_beranda", use_container_width=True):
        st.session_state.halaman_aktif = "Beranda"
        st.rerun()

with nav_cols[2]:
    if st.button("🎮 MAIN", key="nav_game", use_container_width=True):
        st.session_state.halaman_aktif = "Petualangan"
        st.rerun()

with nav_cols[3]:
    if st.button("📚 BACA", key="nav_baca", use_container_width=True):
        st.session_state.halaman_aktif = "Ensiklopedia"
        st.rerun()

with nav_cols[4]:
    if st.button("🏆 LENCANA", key="nav_lencana", use_container_width=True):
        st.session_state.halaman_aktif = "Prestasi"
        st.rerun()

with nav_cols[5]:
    if st.button("👤 PROFIL", key="nav_profil", use_container_width=True):
        st.session_state.halaman_aktif = "Profil"
        st.rerun()

# Dynamic CSS for active tab highlight
active_tab_map = {
    "Beranda": 2,       # nav_cols[1]
    "Petualangan": 3,   # nav_cols[2]
    "Ensiklopedia": 4,  # nav_cols[3]
    "Prestasi": 5,      # nav_cols[4]
    "Profil": 6         # nav_cols[5]
}
active_idx = active_tab_map.get(st.session_state.halaman_aktif, 2)

st.markdown(f"""
<style>
div[data-testid="stHorizontalBlock"]:has(.console-logo) > div[data-testid="column"]:nth-child({active_idx}) .stButton > button {{
    background: #FF8A00 !important;
    color: white !important;
    box-shadow: 0 2px 0px #2C3E50 !important;
    transform: translateY(2px) !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. HALAMAN FILTER LOGIC & CONFIRMATION MODAL
# ==========================================

# Global switch cartridge confirmation modal
if st.session_state.get("confirm_switch_cartridge"):
    target_name = st.session_state.confirm_switch_cartridge
    target_page = st.session_state.get("confirm_switch_target_page", "Petualangan")
    
    st.markdown(f"""
        <div style="background: #FFF9E6; border: 4px solid #FF8A00; border-radius: 24px; padding: 32px; box-shadow: 0 8px 0px #2C3E50; margin: 40px auto; max-width: 600px; text-align: center;">
            <div style="font-size: 64px; margin-bottom: 16px;">⚠️</div>
            <h3 style="color: #2C3E50; font-weight: 950; margin-bottom: 12px; font-size: 24px;">Yakin mau ganti Cartridge?</h3>
            <p style="font-size: 16px; font-weight: 700; color: #7F8C8D; line-height: 1.5; margin-bottom: 24px;">
                Semua progres kuis aktifmu pada cartridge saat ini akan hilang loh.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        if st.button("❌ Batal", key="global_cancel_switch_cart", use_container_width=True):
            st.session_state.confirm_switch_cartridge = None
            st.rerun()
    with col_c2:
        if st.button("✅ Ya, Ganti!", key="global_execute_switch_cart", use_container_width=True):
            select_cartridge(target_name)
            st.session_state.confirm_switch_cartridge = None
            st.session_state.halaman_aktif = target_page
            # Auto-switch to active console tab so they see it immediately!
            st.session_state.sub_tab_petualangan = "Active Console"
            st.rerun()
    st.stop()

# --- HALAMAN 1: BERANDA (HOME / LAUNCHER) ---
# --- HALAMAN 1: BERANDA (HOME / LAUNCHER) ---
if st.session_state.halaman_aktif == "Beranda":
    # Sub-navigation bar at the top of Beranda page
    st.markdown("""
        <style>
        div.st-key-sub_tab_container button {
            font-size: 16px !important;
            font-weight: 900 !important;
            padding: 10px 20px !important;
            border-radius: 16px !important;
            border: 3px solid #2C3E50 !important;
            transition: all 0.2s ease-in-out !important;
        }
        div.st-key-sub_tab_container button[kind="primary"] {
            background: #FF8A00 !important;
            color: white !important;
            box-shadow: 0 4px 0px #2C3E50 !important;
        }
        div.st-key-sub_tab_container button[kind="secondary"] {
            background: #FAF8F0 !important;
            color: #2C3E50 !important;
            box-shadow: 0 4px 0px #2C3E50 !important;
        }
        div.st-key-sub_tab_container button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 0px #2C3E50 !important;
        }
        div.st-key-sub_tab_container button:active {
            transform: translateY(2px) !important;
            box-shadow: 0 2px 0px #2C3E50 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    sub_tab_beranda = st.session_state.get("sub_tab_beranda", "Dasbor")
    avatar_emoji = st.session_state.petualang_avatar.split()[0]
    avatar_name = st.session_state.petualang_avatar.split()[1]

    with st.container(key="sub_tab_container"):
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            if st.button("📊 DASBOR UTAMA", key="btn_sub_dasbor", use_container_width=True, type="primary" if sub_tab_beranda == "Dasbor" else "secondary"):
                st.session_state.sub_tab_beranda = "Dasbor"
                st.rerun()
        with sub_c2:
            if st.button(f"💬 RUANG CHAT {avatar_emoji}", key="btn_sub_chat", use_container_width=True, type="primary" if sub_tab_beranda == "Chat" else "secondary"):
                st.session_state.sub_tab_beranda = "Chat"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if sub_tab_beranda == "Dasbor":
        # A. Mascot Welcome Speech Bubble
        col_mascot, col_bubble = st.columns([1, 5])
        
        with col_mascot:
            st.markdown(f"""
                <div style="text-align: center; margin-top: 10px;">
                    <div style="font-size: 76px; animation: float 3s ease-in-out infinite;">{avatar_emoji}</div>
                    <div style="font-weight: 900; font-size: 14px; background: #2C3E50; color: white; border-radius: 10px; padding: 2px 8px; border: 2px solid #2C3E50; display: inline-block;">
                        {avatar_name}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_bubble:
            level, xp_curr, xp_need, progress_lvl, title = get_player_level(st.session_state.bintang_skor)
            special_title = title
            if "chest_100" in st.session_state.claimed_chests:
                special_title = "Ksatria Cahaya Sobat Cilik 🌟"
            elif "chest_20" in st.session_state.claimed_chests:
                special_title = "Teman Milo 🐰"
                
            st.markdown(f"""
                <div class="mascot-speech-bubble">
                    <h3 style="margin: 0 0 6px 0; color: #FF8A00; font-weight: 900;">Selamat Datang Kembali, {st.session_state.petualang_name}! 👋</h3>
                    <p style="margin: 0; font-size: 16px; font-weight: 700; color: #2C3E50; line-height: 1.5;">
                        Aku <b>{avatar_name}</b>, siap menemanimu bertualang hari ini! Saat ini kamu memegang gelar <b>{special_title}</b>. 
                        Kamu sudah mengumpulkan total <b>{st.session_state.bintang_skor}</b> Bintang! Yuk, taklukkan tantangan di bawah! 🚀
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

        # B. Progress Dashboard Metrics Cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
                <div class="metric-card" style="background: #FFEAA7; border: 4px solid #2C3E50; border-radius: 24px; padding: 20px; text-align: center; box-shadow: 0 6px 0px #2C3E50;">
                    <div style="font-size: 40px;">⭐</div>
                    <div style="font-size: 12px; font-weight: 900; color: #7F8C8D; text-transform: uppercase; letter-spacing: 0.5px;">Kantong Bintang</div>
                    <div style="font-size: 22px; font-weight: 950; color: #2C3E50; margin-top: 5px;">{st.session_state.bintang_skor} Bintang</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
                <div class="metric-card" style="background: #A8E6CF; border: 4px solid #2C3E50; border-radius: 24px; padding: 20px; text-align: center; box-shadow: 0 6px 0px #2C3E50;">
                    <div style="font-size: 40px;">🎮</div>
                    <div style="font-size: 12px; font-weight: 900; color: #7F8C8D; text-transform: uppercase; letter-spacing: 0.5px;">Game Diselesaikan</div>
                    <div style="font-size: 22px; font-weight: 950; color: #2C3E50; margin-top: 5px;">{len(st.session_state.completed_games)} / 9 Game</div>
                </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
                <div class="metric-card" style="background: #FFD3B6; border: 4px solid #2C3E50; border-radius: 24px; padding: 20px; text-align: center; box-shadow: 0 6px 0px #2C3E50;">
                    <div style="font-size: 40px;">🔥</div>
                    <div style="font-size: 12px; font-weight: 900; color: #7F8C8D; text-transform: uppercase; letter-spacing: 0.5px;">Streak Belajar</div>
                    <div style="font-size: 22px; font-weight: 950; color: #2C3E50; margin-top: 5px;">{st.session_state.streak} Hari</div>
                </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
                <div class="metric-card" style="background: #DED2F9; border: 4px solid #2C3E50; border-radius: 24px; padding: 20px; text-align: center; box-shadow: 0 6px 0px #2C3E50;">
                    <div style="font-size: 40px;">🏆</div>
                    <div style="font-size: 12px; font-weight: 900; color: #7F8C8D; text-transform: uppercase; letter-spacing: 0.5px;">Koleksi Lencana</div>
                    <div style="font-size: 22px; font-weight: 950; color: #2C3E50; margin-top: 5px;">{len(get_unlocked_badges())} Lencana</div>
                </div>
            """, unsafe_allow_html=True)

        # C. Leveling Progress Bar Panel
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background: #FFFFFF; border: 4px solid #2C3E50; border-radius: 24px; padding: 20px; box-shadow: 0 6px 0px #2C3E50; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-weight: 950; font-size: 18px; color: #2C3E50;">📈 Tingkat Kemajuan: Level {level} ({title})</span>
                    <span style="font-weight: 800; font-size: 14px; color: #7F8C8D;">{xp_curr} / {xp_need} Bintang untuk Level Berikutnya</span>
                </div>
                <div style="background: #E0E0E0; border-radius: 12px; height: 24px; padding: 3px; border: 3px solid #2C3E50; width: 100%; box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);">
                    <div style="background: linear-gradient(90deg, #10C95B, #2ECC71); height: 100%; border-radius: 8px; width: {progress_lvl}%; transition: width 0.5s ease-in-out;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # D. Main Launcher Action Button
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-orange' style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("🚀 MULAI PETUALANGAN BARU 🚀", key="main_action_play", use_container_width=True):
            if st.session_state.selected_matkul is not None:
                select_cartridge(st.session_state.selected_matkul)
                st.session_state.sub_tab_petualangan = "Active Console"
            else:
                st.session_state.sub_tab_petualangan = "Cartridges"
            st.session_state.halaman_aktif = "Petualangan"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # E. Featured Cartridge Recommendations
        st.markdown("<h3 style='color: #2C3E50; font-weight: 900; margin-top: 40px; margin-bottom: 20px;'>🎮 PETUALANGAN REKOMENDASI</h3>", unsafe_allow_html=True)
        
        if "rekomendasi_list" not in st.session_state:
            all_matkuls = list(matkul_data.keys())
            uncompleted = [m for m in all_matkuls if m not in st.session_state.completed_games]
            if not uncompleted:
                recs = random.sample(all_matkuls, 3) if len(all_matkuls) >= 3 else all_matkuls
            else:
                recs = random.sample(uncompleted, min(len(uncompleted), 3))
                if len(recs) < 3:
                    others = [m for m in all_matkuls if m not in recs]
                    recs += random.sample(others, min(len(others), 3 - len(recs)))
            st.session_state.rekomendasi_list = recs
        else:
            recs = st.session_state.rekomendasi_list

        col_recs = st.columns(3)
        for idx, name in enumerate(recs):
            info = matkul_data[name]
            is_done = name in st.session_state.completed_games
            with col_recs[idx]:
                st.markdown(f"""
                    <div class="cartridge-card {'completed' if is_done else ''}">
                        { '<div class="cartridge-badge">SELESAI ✅</div>' if is_done else '<div class="cartridge-badge" style="background: #FF8A00;">MAIN ⭐</div>' }
                        <div class="cartridge-emoji">{info['emoji']}</div>
                        <h4 style="font-weight: 900; margin: 8px 0; color: #2C3E50;">{name}</h4>
                        <p style="font-size: 13px; color: #7F8C8D; min-height: 48px; line-height: 1.4;">{info['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Mulai Main {info['emoji']}", key=f"rec_btn_{name}", use_container_width=True):
                    request_switch_cartridge(name, "Petualangan")
                    st.rerun()

    elif sub_tab_beranda == "Chat":
        st.markdown(f"<h2 style='color: #2C3E50; font-weight: 950; margin-bottom: 24px;'>💬 Ruang Chat Teman AI Pintar ({avatar_name})</h2>", unsafe_allow_html=True)
        
        chat_col1, chat_col2 = st.columns([1, 2], gap="large")
        
        with chat_col1:
            st.markdown(f"""
                <div style="background: #FAF8F0; border: 4px solid #2C3E50; border-radius: 24px; padding: 24px; box-shadow: 0 8px 0px #2C3E50; text-align: center;">
                    <div style="font-size: 96px; animation: float 3s ease-in-out infinite;">{avatar_emoji}</div>
                    <h3 style="color: #FF8A00; font-weight: 950; margin: 12px 0 4px 0;">{avatar_name}</h3>
                    <p style="color: #7F8C8D; font-weight: 700; font-size: 14px; margin-bottom: 16px;">Teman Belajar AI Pintarmu! ⚡</p>
                    <div style="background: #E8F9F0; border: 3px solid #2C3E50; border-radius: 12px; padding: 12px; font-weight: 800; color: #2C3E50; text-align: left; font-size: 14px;">
                        🤖 <b>Status Chat:</b> {st.session_state.piko_fsm.state.name}<br>
                        📖 <b>Topik Aktif:</b> {st.session_state.piko_fsm.current_subject or 'Belum memilih'}<br>
                        🎯 <b>Skor Kuis:</b> {st.session_state.piko_fsm.score} Poin
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🧹 Bersihkan Riwayat Chat", key="clear_full_chat", use_container_width=True):
                new_fsm = EduFSM()
                new_fsm.step("")
                st.session_state.piko_fsm = new_fsm
                st.session_state.riwayat_chat = [
                    {"role": "assistant", "content": new_fsm.get_response()}
                ]
                st.rerun()
                
        with chat_col2:
            chat_box = st.container(height=450)
            with chat_box:
                for msg in st.session_state.riwayat_chat:
                    with st.chat_message(msg["role"]):
                        st.write(msg["content"])
                
                if st.session_state.get("show_redirect_to_console"):
                    st.markdown("<div style='text-align: center; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
                    if st.button("🎮 Buka Konsol Aktif Sekarang!", key="redirect_to_active_console", use_container_width=True):
                        st.session_state.halaman_aktif = "Petualangan"
                        st.session_state.sub_tab_petualangan = "Active Console"
                        st.session_state.show_redirect_to_console = False
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                        
            # Chat input form
            with st.form(key="chat_full_input_form", clear_on_submit=True):
                tanya_anak = st.text_input("Tanya sesuatu ke teman belajarmu di sini...", key="chat_full_query_input", placeholder=f"Tanya {avatar_name} di sini...", label_visibility="collapsed")
                submit_btn = st.form_submit_button("Tanyakan 🚀", use_container_width=True)
                
                if submit_btn and tanya_anak:
                    st.session_state.show_redirect_to_console = False
                    st.session_state.riwayat_chat.append({"role": "user", "content": tanya_anak})
                    fsm: EduFSM = st.session_state.piko_fsm
                    fsm.step(tanya_anak)
                    jawaban_piko = fsm.get_response()
                    st.session_state.riwayat_chat.append({"role": "assistant", "content": jawaban_piko})
                    st.rerun()

# --- HALAMAN 2: PETUALANGAN (ADVENTURE ARENA) ---
elif st.session_state.halaman_aktif == "Petualangan":
    # Sub-tab navigation bar
    st.markdown("""
        <style>
        div.st-key-sub_tab_container_petualangan button {
            font-size: 16px !important;
            font-weight: 900 !important;
            padding: 10px 20px !important;
            border-radius: 16px !important;
            border: 3px solid #2C3E50 !important;
            transition: all 0.2s ease-in-out !important;
        }
        div.st-key-sub_tab_container_petualangan button[kind="primary"] {
            background: #FF8A00 !important;
            color: white !important;
            box-shadow: 0 4px 0px #2C3E50 !important;
        }
        div.st-key-sub_tab_container_petualangan button[kind="secondary"] {
            background: #FAF8F0 !important;
            color: #2C3E50 !important;
            box-shadow: 0 4px 0px #2C3E50 !important;
        }
        div.st-key-sub_tab_container_petualangan button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 0px #2C3E50 !important;
        }
        div.st-key-sub_tab_container_petualangan button:active {
            transform: translateY(2px) !important;
            box-shadow: 0 2px 0px #2C3E50 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    sub_tab_petualangan = st.session_state.get("sub_tab_petualangan", "Cartridges")

    with st.container(key="sub_tab_container_petualangan"):
        sub_p1, sub_p2, sub_p3 = st.columns([1.2, 1.2, 0.8])
        with sub_p1:
            if st.button("🎮 DAFTAR CARTRIDGE", key="btn_sub_cartridges", use_container_width=True, type="primary" if sub_tab_petualangan == "Cartridges" else "secondary"):
                st.session_state.sub_tab_petualangan = "Cartridges"
                st.rerun()
        with sub_p2:
            if st.button("📟 KONSOL AKTIF", key="btn_sub_console", use_container_width=True, type="primary" if sub_tab_petualangan == "Active Console" else "secondary"):
                st.session_state.sub_tab_petualangan = "Active Console"
                st.rerun()
        with sub_p3:
            st.markdown(f"""
                <div style="background: #FF8A00; border: 3px solid #2C3E50; color: white; border-radius: 16px; font-weight: 900; text-align: center; font-size: 16px; box-shadow: 0 4px 0px #2C3E50; height: 48px; display: flex; align-items: center; justify-content: center;">
                    ⭐ {st.session_state.bintang_skor} Bintang
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    selected = st.session_state.selected_matkul
    game_now = matkul_data[selected] if selected is not None else None

    if sub_tab_petualangan == "Cartridges":
        if selected is not None:
            col_status_cart, col_abort_cart = st.columns([3, 1])
            with col_status_cart:
                st.markdown(f"""
                    <div style="background: #E8F9F0; border: 3px solid #2C3E50; border-radius: 16px; padding: 10px 20px; font-weight: 900; color: #2C3E50; height: 48px; display: flex; align-items: center;">
                        📟 Cartridge Aktif: {selected} {game_now['emoji']}
                    </div>
                """, unsafe_allow_html=True)
            with col_abort_cart:
                if st.button("🔌 Cabut Cartridge", key="abort_cartridge_list", use_container_width=True, type="secondary"):
                    st.session_state.selected_matkul = None
                    st.session_state.active_quiz_questions = []
                    st.session_state.active_quiz_idx = 0
                    st.session_state.active_quiz_score = 0
                    st.session_state.active_quiz_completed = False
                    st.session_state.active_quiz_history = []
                    st.session_state.active_quiz_answered = False
                    st.session_state.active_quiz_feedback = ""
                    st.rerun()
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center; color: #2C3E50; font-weight: 950; margin-bottom: 12px;'>🎮 Pilih Cartridge Petualangan</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #7F8C8D; font-weight: 700; font-size: 18px; margin-bottom: 40px;'>Pilih salah satu cartridge untuk dipasang ke dalam konsol layar aktif!</p>", unsafe_allow_html=True)

        cols = st.columns(4)
        for idx, (name, info) in enumerate(matkul_data.items()):
            is_done = name in st.session_state.completed_games
            is_selected = name == st.session_state.selected_matkul
            
            # Selected border highlight style
            card_border_override = "border: 5px solid #FF8A00; box-shadow: 0 12px 0px #2C3E50; transform: translateY(-5px);" if is_selected else ""
            badge_text = "TAMAT ✅" if is_done else "BARU ⭐"
            badge_bg = "#10C95B" if is_done else "#FF8A00"
            
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class="cartridge-card {'completed' if is_done else ''}" style="{card_border_override}">
                        <div class="cartridge-badge" style="background: {badge_bg};">{badge_text}</div>
                        <div class="cartridge-emoji">{info['emoji']}</div>
                        <h4 style="font-weight: 900; margin: 8px 0; color: #2C3E50; font-size: 16px;">{name}</h4>
                        <p style="font-size: 13px; color: #7F8C8D; min-height: 48px; line-height: 1.4;">{info['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                btn_txt = "Cartridge Dipasang ➔" if is_selected else f"Pasang Cartridge {info['emoji']}"
                if st.button(btn_txt, key=f"sel_cart_{idx}", use_container_width=True, disabled=is_selected):
                    request_switch_cartridge(name, "Petualangan")
                    st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)

    elif sub_tab_petualangan == "Active Console":
        if selected is None:
            st.markdown("""
                <div style="text-align: center; padding: 60px 20px; background: #FAF8F0; border: 4px dashed #2C3E50; border-radius: 24px; box-shadow: 0 8px 0px #2C3E50; margin-top: 20px;">
                    <div style="font-size: 80px; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">📟</div>
                    <h3 style="color: #2C3E50; font-weight: 950; font-size: 24px;">BELUM ADA CARTRIDGE AKTIF</h3>
                    <p style="color: #7F8C8D; font-weight: 700; font-size: 16px; margin-bottom: 24px;">Silakan pilih salah satu cartridge dari tab <b>DAFTAR CARTRIDGE</b> untuk dimasukkan ke dalam konsol aktif!</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎮 Buka Daftar Cartridge Sekarang", key="go_to_cartridges_list", use_container_width=True, type="primary"):
                st.session_state.sub_tab_petualangan = "Cartridges"
                st.rerun()
        else:
            header_col1, header_col2 = st.columns([3, 1])
            with header_col1:
                st.markdown(f"""
                    <div style='text-align: left; margin-bottom: 24px;'>
                        <h2 style='color: #2C3E50; font-weight: 950; margin:0;'>🎮 LAYAR KONSOL AKTIF</h2>
                        <div style='background: #2C3E50; color: white; display: inline-block; padding: 4px 16px; border-radius: 12px; font-weight: 800; font-size: 14px; margin-top: 8px;'>
                            SEMENTARA BERMAIN: {selected.upper()} {game_now['emoji']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with header_col2:
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                if st.button("🔌 Cabut Cartridge", key="abort_active_cartridge", use_container_width=True, type="secondary"):
                    st.session_state.selected_matkul = None
                    st.session_state.active_quiz_questions = []
                    st.session_state.active_quiz_idx = 0
                    st.session_state.active_quiz_score = 0
                    st.session_state.active_quiz_completed = False
                    st.session_state.active_quiz_history = []
                    st.session_state.active_quiz_answered = False
                    st.session_state.active_quiz_feedback = ""
                    st.rerun()

            # Bezel Header HTML
            st.markdown(f"""
                <div class="game-screen-bezel-header">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="color: #FF8A00; font-weight: 900; font-size: 14px; display: flex; align-items: center; gap: 6px; letter-spacing: 0.5px;">
                            <span style="display: inline-block; width: 10px; height: 10px; background: #FF8A00; border-radius: 50%; animation: pulse 1.5s infinite;"></span>
                            LIVE MODE: PLAYING {selected.upper()}
                        </div>
                        <div style="color: #10C95B; font-weight: 800; font-size: 14px; letter-spacing: 0.5px;">BATTERY: 100% 🔋</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.container(key="console_screen_container"):
                st.markdown('<div class="console-screen-content"></div>', unsafe_allow_html=True)
                
                belajar_col1, belajar_col2 = st.columns([1, 1], gap="large")
                
                with belajar_col1:
                    st.markdown("<div style='background-color:#E8F9F0; padding:12px 18px; border-left: 6px solid #10C95B; border-radius:12px; margin-bottom:16px;'><h5 style='margin:0; color:#0EB351; font-weight: 800; font-size: 15px;'>📜 PETA PETUNJUK (Materi)</h5></div>", unsafe_allow_html=True)
                    st.info(game_now["materi"])

                with belajar_col2:
                    st.markdown("<div style='background-color:#FFF5E6; padding:12px 18px; border-left: 6px solid #FF8A00; border-radius:12px; margin-bottom:16px;'><h5 style='margin:0; color:#E67A00; font-weight: 800; font-size: 15px;'>🧩 TEKA-TEKI KUIS</h5></div>", unsafe_allow_html=True)
                    
                    # Pastikan state kuis aktif terinisialisasi
                    if "active_quiz_questions" not in st.session_state:
                        select_cartridge(selected)
                    
                    idx = st.session_state.active_quiz_idx
                    questions = st.session_state.active_quiz_questions
                    completed = st.session_state.active_quiz_completed
                    score = st.session_state.active_quiz_score
                    answered = st.session_state.active_quiz_answered
                
                    if completed:
                        st.markdown(f"""
                            <div style="background: #E8F9F0; border: 4px solid #10C95B; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 6px 0px #2C3E50;">
                                <h3 style="color: #0EB351; margin-bottom: 8px;">🎉 Kuis Selesai!</h3>
                                <p style="font-size: 16px; font-weight: 700; color: #2C3E50;">
                                    Kamu berhasil menyelesaikan kuis <b>{selected}</b>!
                                </p>
                                <div style="font-size: 32px; font-weight: 950; color: #FF8A00; margin: 12px 0;">
                                    Skor: {score} / 10 Benar
                                </div>
                                <p style="font-size: 14px; font-weight: 700; color: #7F8C8D;">
                                    Kamu mendapatkan <b>{score * 2} Bintang</b>! ⭐
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Main Lagi 🔄", key=f"restart_quiz_{selected}", use_container_width=True):
                            select_cartridge(selected)
                            st.rerun()
                    else:
                        q_now = questions[idx]
                        soal_text = q_now["soal"]
                        kunci_jawaban = q_now["kunci"]
                        
                        st.markdown(f"""
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <span style="font-weight: 900; color: #2C3E50;">Soal {idx + 1} dari 10</span>
                                <span style="background: #FF8A00; color: white; padding: 2px 10px; border-radius: 8px; font-size: 12px; font-weight: 800;">
                                    ⭐ {score} Benar
                                </span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Progress bar
                        progress_val = int((idx / 10) * 100)
                        st.markdown(f"""
                            <div style="background: #E0E0E0; border-radius: 6px; height: 12px; border: 2px solid #2C3E50; width: 100%; margin-bottom: 20px;">
                                <div style="background: #FF8A00; height: 100%; border-radius: 4px; width: {progress_val}%;"></div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Question bubble
                        st.markdown(f"""
                            <div style="background: #FAF8F0; border: 3px solid #2C3E50; border-radius: 16px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 0 #2C3E50;">
                                <span style="font-size: 12px; font-weight: 800; color: #7F8C8D; text-transform: uppercase;">Pertanyaan:</span>
                                <p style="font-size: 16px; font-weight: 900; color: #2C3E50; margin: 4px 0 0 0;">{soal_text}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # History Scrollable Box
                        if st.session_state.active_quiz_history:
                            st.markdown("<p style='font-size: 12px; font-weight: 800; color: #7F8C8D; margin-bottom: 4px;'>Riwayat Jawaban:</p>", unsafe_allow_html=True)
                            hist_box = st.container(height=180)
                            with hist_box:
                                for item in st.session_state.active_quiz_history:
                                    icon = "✅" if item["is_correct"] else "❌"
                                    color = "#E8F9F0" if item["is_correct"] else "#FFEBEE"
                                    border = "#10C95B" if item["is_correct"] else "#FF8A8A"
                                    st.markdown(f"""
                                        <div style="background: {color}; border-left: 5px solid {border}; padding: 8px; border-radius: 8px; margin-bottom: 8px; font-size: 13px;">
                                            <b>Tanya:</b> {item['soal']}<br>
                                            <b>Jawabmu:</b> <code style="font-size: 12px;">{item['user_ans']}</code> ({icon})<br>
                                            {"" if item['is_correct'] else f"<b>Kunci:</b> <code>{item['kunci']}</code>"}
                                        </div>
                                    """, unsafe_allow_html=True)
                        
                        # Input / Feedback Area
                        if not answered:
                            with st.form(key=f"quiz_input_form_{selected}", clear_on_submit=True):
                                ans_input = st.text_input("Tulis jawabanmu di sini...", placeholder="Ketik jawaban kamu...", label_visibility="collapsed", key=f"quiz_ans_field_{selected}")
                                submit_ans = st.form_submit_button("Kirim Jawaban 🚀", use_container_width=True)
                                
                                if submit_ans and ans_input:
                                    is_correct = ans_input.lower().strip() == kunci_jawaban.lower().strip()
                                    if is_correct:
                                        st.session_state.active_quiz_score += 1
                                        st.session_state.active_quiz_feedback = "🎯 **BENAR!** Hebat banget jawabanmu tepat! 🌟"
                                    else:
                                        st.session_state.active_quiz_feedback = f"❌ **JAWABAN KURANG TEPAT!** Kunci jawaban yang benar adalah: **{kunci_jawaban}**"
                                        
                                    st.session_state.active_quiz_history.append({
                                        "soal": soal_text,
                                        "user_ans": ans_input,
                                        "kunci": kunci_jawaban,
                                        "is_correct": is_correct
                                    })
                                    st.session_state.active_quiz_answered = True
                                    st.rerun()
                        else:
                            # Show feedback and Next button
                            if "BENAR" in st.session_state.active_quiz_feedback:
                                st.success(st.session_state.active_quiz_feedback)
                            else:
                                st.error(st.session_state.active_quiz_feedback)
                                
                            next_btn_text = "Lanjut ke Soal Berikutnya ➔" if idx < 9 else "Lihat Hasil Kuis 🏆"
                            if st.button(next_btn_text, key=f"quiz_next_btn_{selected}", use_container_width=True):
                                st.session_state.active_quiz_answered = False
                                st.session_state.active_quiz_feedback = ""
                                
                                if idx < 9:
                                    st.session_state.active_quiz_idx += 1
                                else:
                                    st.session_state.active_quiz_completed = True
                                    # Award stars!
                                    stars_earned = st.session_state.active_quiz_score * 2
                                    st.session_state.bintang_skor += stars_earned
                                    if selected not in st.session_state.completed_games:
                                        st.session_state.completed_games.append(selected)
                                st.rerun()

# --- HALAMAN 3: ENSIKLOPEDIA (LIBRARY MEMBACA) ---
elif st.session_state.halaman_aktif == "Ensiklopedia":
    st.markdown("<h2 style='text-align: center; color: #2C3E50; font-weight: 950; margin-bottom: 12px;'>📚 Ensiklopedia Catatan Pintar</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7F8C8D; font-weight: 700; font-size: 18px; margin-bottom: 40px;'>Pelajari ulang inti pembahasan di perpustakaan digital dan dapatkan bintang ekstra! 🌟</p>", unsafe_allow_html=True)
    
    for name, info in matkul_data.items():
        is_read = name in st.session_state.completed_readings
        header_text = f"{info['emoji']} Pembahasan Lengkap: {name} "
        status_badge = "✅ (Dibaca)" if is_read else "⭐ +5 Bintang"
        
        with st.container():
            with st.expander(f"{header_text} — {status_badge}", expanded=False):
                col_materi_kiri, col_materi_kanan = st.columns([2, 1])
                
                with col_materi_kiri:
                    st.markdown(f"<h4 style='color: #FF8A00; font-weight: 800; margin-bottom: 12px;'>📌 Inti Pelajaran</h4>", unsafe_allow_html=True)
                    st.info(info["materi"])
                    
                with col_materi_kanan:
                    st.markdown(f"<h4 style='color: #10C95B; font-weight: 800; margin-bottom: 12px;'>💡 Sekilas Info</h4>", unsafe_allow_html=True)
                    st.success(f"**Deskripsi:**\n\n{info['desc']}")
                    
                    if not is_read:
                        if st.button(f"Tandai Selesai Membaca (+5 ⭐)", key=f"read_{name}", use_container_width=True):
                            st.session_state.completed_readings.append(name)
                            st.session_state.bintang_skor += 5
                            st.rerun()
                    else:
                        st.markdown("""
                            <div style="background: #A8E6CF; border: 3px solid #2C3E50; border-radius: 12px; padding: 12px; text-align: center; font-weight: 900; color: #2C3E50; font-size: 14px; margin-bottom: 12px;">
                                Selesai Membaca! +5 ⭐
                            </div>
                        """, unsafe_allow_html=True)
                        
                    if st.button(f"Mainkan Game {info['emoji']}", key=f"rangkum_{name}", use_container_width=True):
                        st.session_state.selected_matkul = name
                        st.session_state.halaman_aktif = "Petualangan"
                        st.rerun()

# --- HALAMAN 4: PRESTASI (ACHIEVEMENT ALBUM) ---
elif st.session_state.halaman_aktif == "Prestasi":
    st.markdown("<h2 style='text-align: center; color: #2C3E50; font-weight: 950; margin-bottom: 12px;'>🏆 Ruang Prestasi & Lencana</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7F8C8D; font-weight: 700; font-size: 18px; margin-bottom: 40px;'>Kumpulkan lencana ajaib dan buka peti harta karun rahasiamu! 🎁⭐</p>", unsafe_allow_html=True)

    # 1. Chest milestones
    st.markdown("<h3 style='color: #2C3E50; font-weight: 900; margin-bottom: 20px;'>🎁 Peti Harta Karun Milestone</h3>", unsafe_allow_html=True)
    
    chest_milestones = [
        {
            "id": "chest_20",
            "stars": 20,
            "title": "Peti Rahasia Milo 🐰",
            "reward": "Gelar 'Teman Milo 🐰' + Bonus 10 Bintang!",
            "bonus_stars": 10
        },
        {
            "id": "chest_50",
            "stars": 50,
            "title": "Peti Naga Emas 🐉",
            "reward": "Mascot Avatar '🐉 Naga Emas' + Bonus 25 Bintang!",
            "bonus_stars": 25
        },
        {
            "id": "chest_100",
            "stars": 100,
            "title": "Peti Cahaya Legendaris 🌟",
            "reward": "Gelar 'Ksatria Cahaya Sobat Cilik 🌟' + Bonus 50 Bintang!",
            "bonus_stars": 50
        }
    ]
    
    col_chests = st.columns(3)
    for idx, chest in enumerate(chest_milestones):
        is_unlocked = st.session_state.bintang_skor >= chest["stars"]
        is_claimed = chest["id"] in st.session_state.claimed_chests
        
        with col_chests[idx]:
            if is_claimed:
                st.markdown(f"""
                    <div class="chest-card" style="background: #E2E8F0; border: 4px solid #7F8C8D; border-radius: 24px; padding: 24px; text-align: center; box-shadow: 0 6px 0px #7F8C8D;">
                        <div style="font-size: 52px;">🔓</div>
                        <h4 style="color: #7F8C8D; font-weight: 900; margin-top: 10px;">{chest['title']}</h4>
                        <p style="font-size: 13px; color: #7F8C8D; font-weight: 700; margin-top: 5px;">SUDAH DIKLAIM ✅</p>
                    </div>
                """, unsafe_allow_html=True)
            elif is_unlocked:
                st.markdown(f"""
                    <div class="chest-card" style="background: #FFFDF0; border: 4px solid #FF8A00; border-radius: 24px; padding: 24px; text-align: center; box-shadow: 0 8px 0px #FF8A00; animation: bounce 2s infinite;">
                        <div style="font-size: 52px;">🎁</div>
                        <h4 style="color: #E67A00; font-weight: 900; margin-top: 10px;">{chest['title']}</h4>
                        <p style="font-size: 13px; color: #2C3E50; font-weight: 800; margin-top: 5px;">BISA DIBUKA!</p>
                        <p style="font-size: 12px; color: #7F8C8D; font-weight: 600; margin-top: 4px;">{chest['reward']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Buka Peti! ➔", key=f"claim_{chest['id']}", use_container_width=True):
                    st.session_state.claimed_chests.append(chest["id"])
                    st.session_state.bintang_skor += chest["bonus_stars"]
                    st.balloons()
                    st.rerun()
            else:
                st.markdown(f"""
                    <div class="chest-card" style="background: #F1F5F9; border: 4px dashed #CBD5E1; border-radius: 24px; padding: 24px; text-align: center; opacity: 0.7;">
                        <div style="font-size: 52px; filter: grayscale(100%);">🔒</div>
                        <h4 style="color: #94A3B8; font-weight: 900; margin-top: 10px;">{chest['title']}</h4>
                        <p style="font-size: 12px; color: #94A3B8; font-weight: 700; margin-top: 5px;">Butuh {chest['stars']} Bintang (Kurang {chest['stars'] - st.session_state.bintang_skor})</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border: 2px solid #2C3E50; margin: 32px 0;'><br>", unsafe_allow_html=True)

    # 2. Collectible Badge Album
    st.markdown("<h3 style='color: #2C3E50; font-weight: 900; margin-bottom: 24px;'>🏆 ALBUM LENCANA PRESTASI</h3>", unsafe_allow_html=True)
    
    unlocked_badges = get_unlocked_badges()
    col_badges = st.columns(4)
    
    for idx, badge in enumerate(ACHIEVEMENTS):
        is_unlocked = badge["id"] in unlocked_badges
        bg_color = "#EBF8FF" if is_unlocked else "#F1F5F9"
        border_color = "#2B6CB0" if is_unlocked else "#94A3B8"
        shadow_color = "#2B6CB0" if is_unlocked else "#94A3B8"
        emoji_filter = "" if is_unlocked else "filter: grayscale(100%) opacity(0.5);"
        title_color = "#2C3E50" if is_unlocked else "#94A3B8"
        status_label = "TERBUKA! 🏆" if is_unlocked else "TERKUNCI 🔒"
        
        with col_badges[idx % 4]:
            st.markdown(f"""
                <div style="background: {bg_color}; border: 4px solid {border_color}; border-radius: 24px; padding: 20px; text-align: center; box-shadow: 0 6px 0px {shadow_color}; height: 230px; margin-bottom: 24px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative;">
                    <div style="font-size: 52px; margin-bottom: 8px; {emoji_filter}">{badge['emoji']}</div>
                    <h4 style="font-weight: 900; margin: 4px 0; color: {title_color}; font-size: 16px;">{badge['title']}</h4>
                    <p style="font-size: 12px; color: #7F8C8D; font-weight: 600; min-height: 36px; line-height: 1.3;">{badge['desc']}</p>
                    <div style="font-size: 11px; font-weight: 900; background: {border_color}; color: white; padding: 4px 10px; border-radius: 10px; display: inline-block; margin-top: 10px; border: 2px solid #2C3E50;">
                        {status_label}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- HALAMAN 5: PROFIL (SETTINGS & DATA SHEET) ---
elif st.session_state.halaman_aktif == "Profil":
    st.markdown("<h2 style='text-align: center; color: #2C3E50; font-weight: 950; margin-bottom: 24px;'>👤 Profil Petualang Cilik</h2>", unsafe_allow_html=True)

    dragon_unlocked = "chest_50" in st.session_state.claimed_chests
    avatar_options = ["🦁 Leo Lion", "🐰 Milo Rabbit", "🤖 Piko Robot", "🐧 Ping Penguin", "🦖 Dino Dino"]
    if dragon_unlocked:
        avatar_options.append("🐉 Naga Emas")
        
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("<div style='background-color:#E8F9F0; padding:12px 18px; border-left: 6px solid #10C95B; border-radius:12px; margin-bottom:20px;'><h5 style='margin:0; color:#0EB351; font-weight: 800; font-size: 16px;'>⚙️ Pengaturan Karakter</h5></div>", unsafe_allow_html=True)
        
        # Edit Name
        new_name = st.text_input("Ganti Nama Petualangmu:", value=st.session_state.petualang_name, max_chars=20)
        if new_name:
            st.session_state.petualang_name = new_name
            
        # Select Avatar Partner
        new_avatar = st.selectbox("Pilih Partner Petualanganmu:", avatar_options, index=avatar_options.index(st.session_state.petualang_avatar) if st.session_state.petualang_avatar in avatar_options else 0)
        if new_avatar:
            st.session_state.petualang_avatar = new_avatar
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Reset Chemical Button
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.session_state.get("show_reset_warning", False):
            st.warning("⚠️ **PERINGATAN KERAS:** Tindakan ini akan menghapus semua skor bintang, lencana, game yang diselesaikan, dan riwayat belajarmu selamanya! Tindakan ini tidak dapat dibatalkan.")
            st.write("Ketik **RESET** di bawah ini untuk mengonfirmasi:")
            confirm_text = st.text_input("Konfirmasi Teks:", key="reset_confirm_text")
            
            col_warn1, col_warn2 = st.columns(2)
            with col_warn1:
                if st.button("❌ Batal", key="cancel_reset", use_container_width=True):
                    st.session_state.show_reset_warning = False
                    st.rerun()
            with col_warn2:
                is_disabled = confirm_text != "RESET"
                if st.button("🔥 Ya, Hapus Semua Data!", key="execute_reset", use_container_width=True, disabled=is_disabled):
                    st.session_state.bintang_skor = 0
                    st.session_state.completed_games = []
                    st.session_state.completed_readings = []
                    st.session_state.claimed_chests = []
                    st.session_state.petualang_name = "Petualang Cilik"
                    st.session_state.petualang_avatar = "🦁 Leo Lion"
                    st.session_state.streak = 1
                    st.session_state.riwayat_chat = []
                    st.session_state.halaman_aktif = "Beranda"
                    st.session_state.show_reset_warning = False
                    st.session_state.selected_matkul = "Berhitung Seru"
                    st.session_state.active_quiz_questions = []
                    st.session_state.active_quiz_idx = 0
                    st.session_state.active_quiz_score = 0
                    st.session_state.active_quiz_answered = False
                    st.session_state.active_quiz_feedback = ""
                    st.session_state.active_quiz_history = []
                    st.session_state.active_quiz_completed = False
                    # Reset FSM
                    new_fsm = EduFSM()
                    new_fsm.step("")
                    st.session_state.piko_fsm = new_fsm
                    if "rekomendasi_list" in st.session_state:
                        del st.session_state.rekomendasi_list
                    save_progress()
                    st.success("Semua data kemajuanmu berhasil dihapus!")
                    st.rerun()
        else:
            if st.button("🚨 Reset Semua Progress", use_container_width=True):
                st.session_state.show_reset_warning = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='background-color:#FFF5E6; padding:12px 18px; border-left: 6px solid #FF8A00; border-radius:12px; margin-bottom:20px;'><h5 style='margin:0; color:#E67A00; font-weight: 800; font-size: 16px;'>📊 Kartu Status Petualang</h5></div>", unsafe_allow_html=True)
        
        level, xp_curr, xp_need, progress_lvl, title = get_player_level(st.session_state.bintang_skor)
        special_title = title
        if "chest_100" in st.session_state.claimed_chests:
            special_title = "Ksatria Cahaya Sobat Cilik 🌟"
        elif "chest_20" in st.session_state.claimed_chests:
            special_title = "Teman Milo 🐰"
            
        avatar_char = st.session_state.petualang_avatar.split()[0]
        
        st.markdown(f"""
            <div style="background: #FFFFFF; border: 4px solid #2C3E50; border-radius: 28px; padding: 24px; box-shadow: 0 8px 0px #2C3E50;">
                <div style="display: flex; align-items: center; gap: 24px; margin-bottom: 20px;">
                    <div style="font-size: 80px; animation: float 3s ease-in-out infinite;">{avatar_char}</div>
                    <div>
                        <h3 style="margin: 0; color: #2C3E50; font-weight: 950; font-size: 22px;">{st.session_state.petualang_name}</h3>
                        <div style="background: #FF8A00; color: white; padding: 4px 12px; border-radius: 10px; display: inline-block; font-size: 13px; font-weight: 900; border: 2.5px solid #2C3E50; margin-top: 6px; box-shadow: 0 2px 0px #2C3E50;">
                            {special_title}
                        </div>
                    </div>
                </div>
                <hr style="border: 1.5px solid #2C3E50; margin: 16px 0;">
                <div style="display: flex; flex-direction: column; gap: 12px; font-weight: 800; color: #2C3E50; font-size: 15px;">
                    <div>🎮 <b>Level Karakter:</b> Level {level}</div>
                    <div>⭐ <b>Total Bintang:</b> {st.session_state.bintang_skor} Bintang</div>
                    <div>🔥 <b>Streak Petualang:</b> {st.session_state.streak} Hari</div>
                    <div>📚 <b>Mapel Dibaca:</b> {len(st.session_state.completed_readings)} / 9 Selesai</div>
                    <div>🏆 <b>Kuis Ditaklukkan:</b> {len(st.session_state.completed_games)} / 9 Tamat</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


# Auto-save at the end of execution to capture any updates not followed by rerun
save_progress()
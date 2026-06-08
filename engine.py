# engine.py
import re

class EduEngine:
    def __init__(self):
        # Database materi dan kuis dengan gaya bahasa santai
        self.course_data = {
            "matematika": {
                "desc": "Kupas tuntas logika Aljabar, matriks, dan persamaan linear bareng-bareng.",
                "emoji": "🧮",
                "materi": "📌 **Catatan Matematika:**\n1. **Aljabar Dasar:** Kalau ada persamaan $x + 5 = 12$, cara cari nilai $x$ tinggal kurangi aja kedua sisi dengan 5. Jadi, $x = 12 - 5$, ketemu deh hasilnya $x = 7$.\n2. **Persamaan Kuadrat:** Bentuk umumnya $ax^2 + bx + c = 0$. Contohnya nih, kalau $x^2 - 9 = 0$, berarti nilai $x$ bisa 3 atau -3.\n3. **Nilai Mutlak:** Nilai mutlak itu konsepnya selalu bikin angka jadi positif. Contoh: $|-5| = 5$.",
                "kuis": [
                    {"soal": "Kalau $2x = 10$, berapakah nilai $x$?", "kunci": "5"},
                    {"soal": "Berapakah hasil dari $3x + 2$ kalau nilai $x = 4$?", "kunci": "14"},
                    {"soal": "Misal $x^2 = 16$ dan $x$ itu bilangan positif, berapakah nilai $x$?", "kunci": "4"},
                    {"soal": "Berapakah nilai dari $|-12| + 3$?", "kunci": "15"},
                    {"soal": "Tentukan nilai $x$ dari persamaan $3x - 5 = 10$!", "kunci": "5"}
                ]
            },
            "sains": {
                "desc": "Bedah rahasia alam, biologi makhluk hidup, dan kimia di sekitar kita.",
                "emoji": "🌱",
                "materi": "📌 **Catatan Sains (IPA):**\n1. **Fotosintesis:** Proses tumbuhan hijau bikin makanannya sendiri pakai bantuan matahari. Di proses ini, mereka menyerap gas **Karbondioksida ($CO_2$)** dan air, terus menghasilkan **Oksigen ($O_2$)** yang kita hirup sehari-hari.\n2. **Tata Surya:** Matahari itu pusatnya. Planet yang posisinya paling dekat sama matahari namanya Merkurius, nah kalau yang dijuluki planet merah itu Mars.\n3. **Zat Hijau Daun:** Daun bisa berwarna hijau karena punya pigmen alami bernama klorofil. Tugasnya buat menangkap cahaya matahari.",
                "kuis": [
                    {"soal": "Gas apa yang dilepaskan tumbuhan waktu proses fotosintesis?", "kunci": "oksigen"},
                    {"soal": "Zat pada daun yang bertugas menangkap cahaya matahari namanya apa?", "kunci": "klorofil"},
                    {"soal": "Planet mana nih yang sering dijuluki sebagai 'Planet Merah'?", "kunci": "mars"},
                    {"soal": "Apa nama benda langit yang jadi pusat tata surya kita?", "kunci": "matahari"},
                    {"soal": "Air kan punya rumus kimia $H_2O$. Nah, huruf O itu singkatan dari unsur apa?", "kunci": "oksigen"}
                ]
            }
        }
        
        # Pola kunci regex otomatis membaca dari dictionary keys
        course_keys = "|".join(self.course_data.keys())
        self.re_course = rf"\b({course_keys})\b"

    def parse_subject(self, text):
        text = text.lower().strip()
        match = re.search(self.re_course, text)
        if match:
            return match.group(1)
        return None

    def detect_intent(self, text):
        text = text.lower().strip()
        
        if re.search(r"\b(reset|ulang|mulai baru|keluar)\b", text):
            return "RESET_SYSTEM"
        if re.search(r"\b(menu|daftar|pelajaran|list|subjek|belajar apa)\b", text):
            return "ASK_MENU"
        if re.search(r"\b(materi|baca|belajar|teori)\b", text):
            return "LEARN_MATERIAL"
        if re.search(r"\b(kuis|tes|ujian|soal|latihan)\b", text):
            return "START_QUIZ"
        if re.search(r"\b(ya|yes|oke|mulai|siap|betul)\b", text):
            return "YES"
        if re.search(r"\b(tidak|enggak|no|batal|belum)\b", text):
            return "NO"
            
        return "UNKNOWN"
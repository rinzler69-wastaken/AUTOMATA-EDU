# FSM.py
from enum import Enum, auto
from engine import EduEngine

class State(Enum):
    IDLE = auto()
    CHOOSING = auto()
    QUIZ = auto()
    EVALUATION = auto()

class EduFSM:
    def __init__(self):
        self.nlp = EduEngine()
        self.state = State.IDLE
        self.current_subject = None
        self.current_question_idx = 0
        self.score = 0
        self.response = ""

    def get_response(self):
        return self.response

    def get_menu_text(self):
        teks_menu = "📚 **Pilihan Topik yang Bisa Kita Bahas:**\n\n"
        for key, data in self.nlp.course_data.items():
            teks_menu += f"- {data['emoji']} **{key.capitalize()}**: *{data['desc']}*\n"
        teks_menu += "\nYuk, ketik topik yang mau kamu pelajari (misal: *'mau belajar matematika'* atau *'baca materi sains'*)."
        return teks_menu

    def step(self, user_input=""):
        intent = self.nlp.detect_intent(user_input)
        
        # Fitur Interupsi Global: Kapan pun user ketik 'reset', sistem kembali ke awal
        if intent == "RESET_SYSTEM" and self.state != State.IDLE:
            self.state = State.IDLE
            self.current_subject = None
            self.current_question_idx = 0
            self.score = 0

        # ============================================================
        # STATE LOGIC: IDLE
        # ============================================================
        if self.state == State.IDLE:
            self.response = "Sistem di-refresh! Halo, aku **RuangSobat**. Mau bahas materi apa hari ini? Ketik **'menu'** buat lihat daftarnya ya."
            self.state = State.CHOOSING
            return

        # ============================================================
        # STATE LOGIC: CHOOSING
        # ============================================================
        elif self.state == State.CHOOSING:
            # Bersihkan tracker kuis lama jika user meminta aktivitas baru
            if intent in ["ASK_MENU", "LEARN_MATERIAL", "START_QUIZ"] or self.nlp.parse_subject(user_input):
                self.current_question_idx = 0
                self.score = 0

            detected_subject = self.nlp.parse_subject(user_input)
            if detected_subject:
                self.current_subject = detected_subject

            if intent == "ASK_MENU":
                self.response = self.get_menu_text()
            elif self.current_subject and (intent == "LEARN_MATERIAL" or detected_subject):
                materi_teks = self.nlp.course_data[self.current_subject]["materi"]
                self.response = f"📚 **Catatan Seru: {self.current_subject.capitalize()}**\n\n{materi_teks}\n\n🏆 Biar makin nempel di otak, cobain latihan soalnya yuk! Ketik **'mulai kuis'** kalau kamu udah siap."
            elif intent == "START_QUIZ":
                if self.current_subject:
                    self.state = State.QUIZ
                    self.current_question_idx = 0
                    self.score = 0
                    soal_pertama = self.nlp.course_data[self.current_subject]["kuis"][0]["soal"]
                    self.response = f"🚀 **Kuis {self.current_subject.capitalize()} Dimulai!**\n\n**Soal 1:** {soal_pertama}\n\n*Langsung ketik jawabanmu di bawah ya!*"
                else:
                    self.response = "Pilih dulu mata pelajarannya maba/sis, baru kita bisa kuis. Ketik **'menu'** dulu gih."
            else:
                self.response = "Aku agak kurang paham maksudmu nih. Coba ketik **'menu'** aja buat lihat opsi pelajaran yang ada."

        # ============================================================
        # STATE LOGIC: QUIZ
        # ============================================================
        elif self.state == State.QUIZ:
            subjek = self.current_subject
            daftar_soal = self.nlp.course_data[subjek]["kuis"]
            idx = self.current_question_idx
            
            kunci_jawaban = daftar_soal[idx]["kunci"]
            
            # Koreksi pintar: hapus spasi tak sengaja dan samakan ke huruf kecil
            if user_input.lower().strip() == kunci_jawaban.lower():
                self.score += 1
                feedback = "✅ **Hebat! Jawabanmu BENAR!**"
            else:
                feedback = f"❌ **Kurang tepat!** Jawaban yang benar itu: **{kunci_jawaban}**"
            
            self.current_question_idx += 1
            idx_baru = self.current_question_idx
            
            if idx_baru < len(daftar_soal):
                soal_berikutnya = daftar_soal[idx_baru]["soal"]
                self.response = f"{feedback}\n\n---\n\n**Soal {idx_baru + 1}:** {soal_berikutnya}"
            else:
                # Jika soal habis, lompat langsung ke state evaluasi nilai
                self.state = State.EVALUATION
                self.step(user_input)

        # ============================================================
        # STATE LOGIC: EVALUATION
        # ============================================================
        elif self.state == State.EVALUATION:
            subjek = self.current_subject
            total_soal = len(self.nlp.course_data[subjek]["kuis"])
            nilai_akhir = int((self.score / total_soal) * 100)
            
            self.response = f"🎉 **Selesai! Kuis {subjek.capitalize()} Udah Rampung.**\n\n📊 **Rapor Hasil Latihanmu:**\n- Jawaban Benar: {self.score} dari {total_soal} soal.\n- Skor Akhir Kamu: **{nilai_akhir} / 100**\n\nMantap banget udah mau belajar bareng RuangSobat hari ini! Kalau masih penasaran sama topik lain, tinggal ketik **'menu'** lagi ya."
            
            # Kembalikan state ke CHOOSING tanpa menghapus data tracker agar visual di sidebar bertahan sementara
            self.state = State.CHOOSING
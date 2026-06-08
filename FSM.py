# FSM.py
from enum import Enum, auto
from engine import EduEngine

class State(Enum):
    IDLE       = auto()
    CHOOSING   = auto()
    QUIZ       = auto()
    EVALUATION = auto()

class EduFSM:
    def __init__(self):
        self.nlp                 = EduEngine()
        self.state               = State.IDLE
        self.current_subject     = None
        self.current_question_idx = 0
        self.score               = 0
        self.response            = ""

    def get_response(self):
        return self.response

    def get_menu_text(self):
        lines = "📚 **Daftar Topik yang Bisa Kita Bahas:**\n\n"
        for key, data in self.nlp.course_data.items():
            lines += f"- {data['emoji']} **{key.capitalize()}** — *{data['desc']}*\n"
        lines += (
            "\n💡 Cara pakai:\n"
            "- Ketik nama topik untuk **baca materi** (contoh: *'belajar fisika'*, *'materi kimia'*)\n"
            "- Tambah kata kuis untuk **langsung latihan** (contoh: *'kuis biologi'*, *'soal geografi'*)\n"
            "- Ketik **'reset'** kapan saja untuk kembali ke awal."
        )
        return lines

    def _help_text(self):
        return (
            "🆘 **Butuh bantuan? Tenang, ini panduannya:**\n\n"
            "- Ketik **'menu'** → lihat semua topik yang tersedia\n"
            "- Ketik **'belajar [topik]'** → baca materi (contoh: *belajar kimia*)\n"
            "- Ketik **'kuis [topik]'** → langsung ke soal (contoh: *kuis sejarah*)\n"
            "- Ketik **'reset'** → mulai ulang dari awal\n\n"
            "Topik tersedia: " + ", ".join(
                f"{v['emoji']} {k.capitalize()}" for k, v in self.nlp.course_data.items()
            )
        )

    def step(self, user_input=""):
        intent           = self.nlp.detect_intent(user_input)
        detected_subject = self.nlp.parse_subject(user_input)

        # ── Global interrupts (work from any state) ────────────────────────
        if intent == "RESET_SYSTEM" and self.state != State.IDLE:
            self.state                = State.IDLE
            self.current_subject      = None
            self.current_question_idx = 0
            self.score                = 0

        if intent == "HELP":
            self.response = self._help_text()
            return

        # ==================================================================
        # IDLE → boot into CHOOSING immediately
        # ==================================================================
        if self.state == State.IDLE:
            self.response = (
                "Sistem di-refresh! Halo, aku **RuangSobat** 👋\n\n"
                "Mau bahas materi apa hari ini? Ketik **'menu'** buat lihat semua topik yang ada."
            )
            self.state = State.CHOOSING
            return

        # ==================================================================
        # CHOOSING
        # ==================================================================
        elif self.state == State.CHOOSING:
            # Reset quiz tracker whenever a new activity starts
            if intent in ("ASK_MENU", "LEARN_MATERIAL", "START_QUIZ") or detected_subject:
                self.current_question_idx = 0
                self.score                = 0

            if detected_subject:
                self.current_subject = detected_subject

            if intent == "ASK_MENU":
                self.response = self.get_menu_text()

            elif self.current_subject and intent == "START_QUIZ":
                self.state                = State.QUIZ
                self.current_question_idx = 0
                self.score                = 0
                first_q = self.nlp.course_data[self.current_subject]["kuis"][0]["soal"]
                total   = len(self.nlp.course_data[self.current_subject]["kuis"])
                self.response = (
                    f"🚀 **Kuis {self.current_subject.capitalize()} Dimulai!** ({total} soal)\n\n"
                    f"**Soal 1 dari {total}:** {first_q}\n\n"
                    "*Langsung ketik jawabanmu ya!*"
                )

            elif self.current_subject and intent in ("LEARN_MATERIAL", "YES") or (detected_subject and intent not in ("START_QUIZ",)):
                if self.current_subject:
                    data   = self.nlp.course_data[self.current_subject]
                    total  = len(data["kuis"])
                    self.response = (
                        f"{data['emoji']} **Materi: {self.current_subject.capitalize()}**\n\n"
                        f"{data['materi']}\n\n"
                        f"---\n🏆 Ada **{total} soal latihan** buat topik ini. "
                        f"Ketik **'kuis {self.current_subject}'** kalau udah siap diuji!"
                    )

            elif intent == "START_QUIZ" and not self.current_subject:
                self.response = (
                    "📌 Pilih dulu topiknya baru bisa kuis!\n"
                    "Ketik **'menu'** untuk lihat semua topik yang tersedia."
                )

            elif intent == "UNKNOWN":
                # Try closest-match suggestions
                suggestions = self.nlp.suggest_closest(user_input)
                if suggestions:
                    suggestion_list = ", ".join(
                        f"**{s.capitalize()}**" for s in suggestions
                    )
                    self.response = (
                        f"🤔 Maksudmu salah satu dari ini: {suggestion_list}?\n\n"
                        "Ketik nama topiknya lebih lengkap, atau ketik **'menu'** untuk lihat semua pilihan."
                    )
                else:
                    self.response = (
                        "😅 Aku kurang nangkep nih. Coba salah satu:\n"
                        "- Ketik **'menu'** untuk lihat topik\n"
                        "- Ketik **'help'** untuk panduan lengkap"
                    )

            else:
                self.response = (
                    "Hmm, kurang jelas nih. Ketik **'menu'** untuk lihat topik, "
                    "atau **'help'** untuk panduan."
                )

        # ==================================================================
        # QUIZ
        # ==================================================================
        elif self.state == State.QUIZ:
            soal_list = self.nlp.course_data[self.current_subject]["kuis"]
            idx       = self.current_question_idx
            total     = len(soal_list)
            kunci     = soal_list[idx]["kunci"]

            if user_input.lower().strip() == kunci.lower():
                self.score += 1
                feedback = "✅ **Benar!** Mantap!"
            else:
                feedback = f"❌ **Kurang tepat.** Jawaban yang benar: **{kunci}**"

            self.current_question_idx += 1
            idx_baru = self.current_question_idx

            if idx_baru < total:
                soal_next = soal_list[idx_baru]["soal"]
                self.response = (
                    f"{feedback}\n\n---\n\n"
                    f"**Soal {idx_baru + 1} dari {total}:** {soal_next}"
                )
            else:
                # All questions done → jump to EVALUATION
                self.state = State.EVALUATION
                self.step(user_input)

        # ==================================================================
        # EVALUATION
        # ==================================================================
        elif self.state == State.EVALUATION:
            total      = len(self.nlp.course_data[self.current_subject]["kuis"])
            nilai      = int((self.score / total) * 100)
            salah      = total - self.score

            if nilai == 100:
                predikat = "🏆 Sempurna! Luar biasa banget!"
            elif nilai >= 80:
                predikat = "🥇 Bagus sekali! Tinggal poles dikit lagi."
            elif nilai >= 60:
                predikat = "🥈 Lumayan! Coba ulangi materinya buat perkuat pemahaman."
            else:
                predikat = "🥉 Masih perlu banyak latihan nih. Jangan nyerah!"

            self.response = (
                f"🎉 **Kuis {self.current_subject.capitalize()} Selesai!**\n\n"
                f"📊 **Hasil Latihanmu:**\n"
                f"- ✅ Benar: **{self.score}** dari {total} soal\n"
                f"- ❌ Salah: **{salah}** soal\n"
                f"- 🎯 Skor: **{nilai} / 100**\n\n"
                f"{predikat}\n\n"
                f"Mau lanjut? Ketik **'menu'** untuk topik lain, "
                f"atau **'kuis {self.current_subject}'** untuk ngulang topik ini."
            )
            self.state = State.CHOOSING
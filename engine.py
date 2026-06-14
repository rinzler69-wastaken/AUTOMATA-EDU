# engine.py
import re

class EduEngine:
    def __init__(self):
        self.course_data = {

            # ================================================================
            # MATEMATIKA
            # ================================================================
            "matematika": {
                "desc": "Aljabar, geometri, statistika, peluang, dan logika matematika.",
                "emoji": "🧮",
                "aliases": ["math", "mtk", "maths", "matik", "matematika", "mate"],
                "materi": (
                    "📌 **Catatan Matematika:**\n"
                    "1. **Aljabar:** $x + 5 = 12$ → $x = 7$. Operasi di kedua sisi harus sama.\n"
                    "2. **Persamaan Kuadrat:** $ax^2+bx+c=0$, selesaikan dengan rumus ABC atau faktorisasi.\n"
                    "3. **Nilai Mutlak:** $|-8| = 8$, selalu positif.\n"
                    "4. **FPB & KPK:** FPB = faktor persekutuan terbesar, KPK = kelipatan persekutuan terkecil.\n"
                    "5. **Peluang:** $P(A) = \\frac{\\text{kejadian yang diinginkan}}{\\text{total kejadian}}$, nilainya 0–1.\n"
                    "6. **Statistika:** Mean = rata-rata, Median = nilai tengah, Modus = nilai terbanyak.\n"
                    "7. **Teorema Pythagoras:** $a^2 + b^2 = c^2$ untuk segitiga siku-siku.\n"
                    "8. **Deret Aritmetika:** $S_n = \\frac{n}{2}(a + U_n)$, beda antar suku konstan."
                ),
                "kuis": [
                    {"soal": "Kalau $2x = 10$, berapa nilai $x$?", "kunci": "5"},
                    {"soal": "Hasil dari $3x + 2$ jika $x = 4$?", "kunci": "14"},
                    {"soal": "$x^2 = 16$, $x$ positif. Berapa $x$?", "kunci": "4"},
                    {"soal": "Berapa nilai $|-12| + 3$?", "kunci": "15"},
                    {"soal": "Nilai $x$ dari $3x - 5 = 10$?", "kunci": "5"},
                    {"soal": "FPB dari 12 dan 18 adalah?", "kunci": "6"},
                    {"soal": "KPK dari 4 dan 6 adalah?", "kunci": "12"},
                    {"soal": "Luas segitiga dengan alas 8 dan tinggi 5?", "kunci": "20"},
                    {"soal": "Sisi miring segitiga siku-siku dengan kaki 3 dan 4?", "kunci": "5"},
                    {"soal": "Rata-rata dari 6, 8, 10, 12, 14?", "kunci": "10"},
                    {"soal": "Peluang muncul angka genap saat lempar dadu 1–6?", "kunci": "1/2"},
                    {"soal": "Suku ke-10 deret aritmetika 2, 5, 8, ... ?", "kunci": "29"},
                    {"soal": "Hasil dari $5^2 - 3^2$?", "kunci": "16"},
                    {"soal": "Berapa $\\sqrt{144}$?", "kunci": "12"},
                    {"soal": "Jika $y = 2x + 1$ dan $x = 3$, berapa $y$?", "kunci": "7"},
                    {"soal": "Luas lingkaran dengan jari-jari 7? (gunakan π=22/7)", "kunci": "154"},
                    {"soal": "Volume kubus dengan sisi 4 cm?", "kunci": "64"},
                    {"soal": "Median dari data: 3, 7, 9, 11, 15?", "kunci": "9"},
                    {"soal": "Modus dari data: 2, 3, 3, 5, 7, 3, 9?", "kunci": "3"},
                    {"soal": "Hasil $\\frac{3}{4} + \\frac{1}{4}$?", "kunci": "1"},
                ],
            },

            # ================================================================
            # FISIKA
            # ================================================================
            "fisika": {
                "desc": "Mekanika, termodinamika, gelombang, listrik, dan optika.",
                "emoji": "⚡",
                "aliases": ["fisik", "physics", "fis", "fisika"],
                "materi": (
                    "📌 **Catatan Fisika:**\n"
                    "1. **Hukum Newton I:** Benda diam tetap diam / bergerak lurus beraturan jika resultan gaya = 0.\n"
                    "2. **Hukum Newton II:** $F = ma$. Gaya = massa × percepatan.\n"
                    "3. **Hukum Newton III:** Setiap aksi ada reaksi yang sama besar, berlawanan arah.\n"
                    "4. **GLB & GLBB:** GLB: kecepatan konstan. GLBB: percepatan konstan, $v = v_0 + at$.\n"
                    "5. **Energi:** Energi kinetik $Ek = \\frac{1}{2}mv^2$, potensial $Ep = mgh$.\n"
                    "6. **Usaha:** $W = F \\cdot d \\cdot \\cos\\theta$.\n"
                    "7. **Hukum Ohm:** $V = IR$. Tegangan = Arus × Hambatan.\n"
                    "8. **Gelombang:** $v = \\lambda f$. Kecepatan = panjang gelombang × frekuensi.\n"
                    "9. **Tekanan:** $P = \\frac{F}{A}$. Semakin kecil luas, tekanan makin besar.\n"
                    "10. **Suhu & Kalor:** $Q = mc\\Delta T$. Kalor = massa × kalor jenis × perubahan suhu."
                ),
                "kuis": [
                    {"soal": "Rumus Hukum Newton II adalah?", "kunci": "F=ma"},
                    {"soal": "Satuan gaya dalam SI?", "kunci": "newton"},
                    {"soal": "Benda bermassa 5 kg, percepatan 3 m/s². Gaya yang bekerja?", "kunci": "15"},
                    {"soal": "Ek dari benda 2 kg berkecepatan 4 m/s? (dalam Joule)", "kunci": "16"},
                    {"soal": "Rumus kecepatan gelombang?", "kunci": "v=lambdaf"},
                    {"soal": "Hukum Ohm menyatakan $V = ...$?", "kunci": "IR"},
                    {"soal": "Tegangan 12V, hambatan 4 ohm. Arusnya?", "kunci": "3"},
                    {"soal": "Satuan tekanan dalam SI?", "kunci": "pascal"},
                    {"soal": "Energi potensial benda 2 kg di ketinggian 5 m (g=10)?", "kunci": "100"},
                    {"soal": "GLB singkatan dari?", "kunci": "gerak lurus beraturan"},
                    {"soal": "Rumus usaha adalah?", "kunci": "W=Fd"},
                    {"soal": "Frekuensi 50 Hz artinya berapa getaran per detik?", "kunci": "50"},
                    {"soal": "Suhu 0°C sama dengan berberapa Kelvin?", "kunci": "273"},
                    {"soal": "Hukum Newton III berbicara tentang apa?", "kunci": "aksi reaksi"},
                    {"soal": "Tekanan di kedalaman laut bertambah karena?", "kunci": "berat air"},
                    {"soal": "Benda jatuh bebas mengalami percepatan berapa? (g=10 m/s²)", "kunci": "10"},
                    {"soal": "Rumus kalor adalah $Q = mc...$?", "kunci": "deltaT"},
                    {"soal": "Cermin cekung bersifat?", "kunci": "konvergen"},
                    {"soal": "Bunyi tidak bisa merambat melalui?", "kunci": "vakum"},
                    {"soal": "Alat ukur kuat arus listrik disebut?", "kunci": "amperemeter"},
                ],
            },

            # ================================================================
            # KIMIA
            # ================================================================
            "kimia": {
                "desc": "Atom, ikatan kimia, reaksi, asam-basa, dan tabel periodik.",
                "emoji": "🧪",
                "aliases": ["chem", "chemistry", "kimia", "kem"],
                "materi": (
                    "📌 **Catatan Kimia:**\n"
                    "1. **Atom:** Terdiri dari proton (+), neutron (netral), dan elektron (−). Proton+neutron = inti.\n"
                    "2. **Tabel Periodik:** Unsur diurutkan berdasarkan nomor atom. Periode = baris, Golongan = kolom.\n"
                    "3. **Ikatan Kimia:** Ionik (logam+nonlogam), kovalen (nonlogam+nonlogam), logam.\n"
                    "4. **Reaksi Kimia:** Reaktan → Produk. Hukum kekekalan massa: massa reaktan = massa produk.\n"
                    "5. **Asam-Basa:** pH < 7 = asam, pH = 7 = netral, pH > 7 = basa.\n"
                    "6. **Mol:** $n = \\frac{\\text{massa}}{M_r}$. Satu mol = $6,02 \\times 10^{23}$ partikel (Avogadro).\n"
                    "7. **Larutan:** Pelarut + zat terlarut. Air adalah pelarut universal.\n"
                    "8. **Oksidasi-Reduksi:** Oksidasi = lepas elektron, reduksi = terima elektron."
                ),
                "kuis": [
                    {"soal": "Partikel bermuatan positif dalam atom disebut?", "kunci": "proton"},
                    {"soal": "Partikel yang mengelilingi inti atom?", "kunci": "elektron"},
                    {"soal": "pH larutan asam lebih kecil dari berapa?", "kunci": "7"},
                    {"soal": "Lambang unsur emas (Gold)?", "kunci": "Au"},
                    {"soal": "Lambang unsur natrium?", "kunci": "Na"},
                    {"soal": "Rumus kimia air?", "kunci": "H2O"},
                    {"soal": "Rumus kimia garam dapur?", "kunci": "NaCl"},
                    {"soal": "Bilangan Avogadro = $6,02 \\times 10^{...}$?", "kunci": "23"},
                    {"soal": "Reaksi yang melepaskan panas disebut reaksi?", "kunci": "eksoterm"},
                    {"soal": "Ikatan antara dua atom nonlogam disebut ikatan?", "kunci": "kovalen"},
                    {"soal": "Unsur dengan nomor atom 1 adalah?", "kunci": "hidrogen"},
                    {"soal": "Unsur dengan nomor atom 8 adalah?", "kunci": "oksigen"},
                    {"soal": "Basa kuat contohnya adalah?", "kunci": "NaOH"},
                    {"soal": "Rumus kimia karbon dioksida?", "kunci": "CO2"},
                    {"soal": "Oksidasi berarti atom?", "kunci": "melepas elektron"},
                    {"soal": "Jumlah proton = jumlah elektron menentukan sifat?", "kunci": "netral"},
                    {"soal": "Golongan VIII A berisi gas-gas?", "kunci": "mulia"},
                    {"soal": "Massa atom relatif ($M_r$) $H_2O$?", "kunci": "18"},
                    {"soal": "Larutan buffer berguna untuk?", "kunci": "menjaga pH"},
                    {"soal": "Reaksi pembakaran sempurna menghasilkan $CO_2$ dan?", "kunci": "H2O"},
                ],
            },

            # ================================================================
            # BIOLOGI
            # ================================================================
            "biologi": {
                "desc": "Sel, genetika, ekosistem, evolusi, dan sistem organ tubuh.",
                "emoji": "🌿",
                "aliases": ["bio", "biology", "biologi", "biolog"],
                "materi": (
                    "📌 **Catatan Biologi:**\n"
                    "1. **Sel:** Unit terkecil kehidupan. Prokariotik (tanpa inti) vs eukariotik (punya inti).\n"
                    "2. **Fotosintesis:** $6CO_2 + 6H_2O + cahaya → C_6H_{12}O_6 + 6O_2$. Terjadi di kloroplas.\n"
                    "3. **Respirasi Sel:** $C_6H_{12}O_6 + 6O_2 → 6CO_2 + 6H_2O + energi (ATP)$.\n"
                    "4. **DNA & RNA:** DNA = cetak biru genetik, double helix. RNA = pembawa pesan protein.\n"
                    "5. **Hukum Mendel:** Pewarisan sifat. Dominan vs resesif.\n"
                    "6. **Ekosistem:** Produsen → Konsumen → Dekomposer. Rantai makanan.\n"
                    "7. **Sistem Organ:** Pencernaan, peredaran darah, pernapasan, ekskresi, saraf.\n"
                    "8. **Evolusi:** Darwin: seleksi alam. Organisme paling adaptif bertahan."
                ),
                "kuis": [
                    {"soal": "Organel tempat fotosintesis terjadi?", "kunci": "kloroplas"},
                    {"soal": "Organel penghasil energi ATP disebut?", "kunci": "mitokondria"},
                    {"soal": "Basa nitrogen DNA berpasangan: Adenin dengan?", "kunci": "timin"},
                    {"soal": "Sel tanpa membran inti disebut sel?", "kunci": "prokariotik"},
                    {"soal": "Gas yang diserap tumbuhan untuk fotosintesis?", "kunci": "karbondioksida"},
                    {"soal": "Hewan pemakan tumbuhan disebut?", "kunci": "herbivora"},
                    {"soal": "Proses pembelahan sel menjadi 2 sel identik disebut?", "kunci": "mitosis"},
                    {"soal": "Organ yang menyaring darah di tubuh manusia?", "kunci": "ginjal"},
                    {"soal": "Teori evolusi dikemukakan oleh?", "kunci": "darwin"},
                    {"soal": "Golongan darah manusia ditentukan oleh?", "kunci": "antigen"},
                    {"soal": "Jaringan pengangkut air pada tumbuhan?", "kunci": "xilem"},
                    {"soal": "Vitamin C juga dikenal sebagai?", "kunci": "asam askorbat"},
                    {"soal": "Bagian otak yang mengatur keseimbangan?", "kunci": "serebelum"},
                    {"soal": "Hormon pengatur kadar gula darah?", "kunci": "insulin"},
                    {"soal": "Proses perubahan larva jadi kupu-kupu disebut?", "kunci": "metamorfosis"},
                    {"soal": "Organisme pengurai dalam ekosistem disebut?", "kunci": "dekomposer"},
                    {"soal": "DNA berbentuk?", "kunci": "double helix"},
                    {"soal": "Sel darah putih berfungsi untuk?", "kunci": "imunitas"},
                    {"soal": "Proses penyerapan air oleh akar tumbuhan?", "kunci": "osmosis"},
                    {"soal": "Ilmu yang mempelajari makhluk hidup?", "kunci": "biologi"},
                ],
            },

            # ================================================================
            # SEJARAH
            # ================================================================
            "sejarah": {
                "desc": "Peristiwa bersejarah Indonesia dan dunia dari masa ke masa.",
                "emoji": "📜",
                "aliases": ["history", "sejarah", "seja", "histori", "hist"],
                "materi": (
                    "📌 **Catatan Sejarah:**\n"
                    "1. **Proklamasi RI:** 17 Agustus 1945, dibacakan Soekarno–Hatta di Jl. Pegangsaan Timur 56, Jakarta.\n"
                    "2. **Sumpah Pemuda:** 28 Oktober 1928, ikrar satu bangsa, satu bahasa, satu tanah air.\n"
                    "3. **Perang Dunia II:** 1939–1945. Dimenangkan Sekutu. Bom atom dijatuhkan di Hiroshima (6 Agustus) dan Nagasaki (9 Agustus 1945).\n"
                    "4. **Reformasi 1998:** Soeharto mundur 21 Mei 1998 setelah 32 tahun berkuasa.\n"
                    "5. **Kerajaan Majapahit:** Kerajaan Hindu-Buddha terbesar di Nusantara. Patih Gajah Mada bersumpah Palapa.\n"
                    "6. **VOC:** Kongsi dagang Belanda di Indonesia, berdiri 1602, bubar 1799.\n"
                    "7. **Perang Dunia I:** 1914–1918. Dipicu pembunuhan Franz Ferdinand.\n"
                    "8. **Revolusi Perancis:** 1789. Semboyan Liberté, Égalité, Fraternité."
                ),
                "kuis": [
                    {"soal": "Proklamasi kemerdekaan Indonesia dibacakan tanggal?", "kunci": "17 agustus 1945"},
                    {"soal": "Siapa yang membacakan teks proklamasi?", "kunci": "soekarno"},
                    {"soal": "Sumpah Pemuda terjadi pada tanggal?", "kunci": "28 oktober 1928"},
                    {"soal": "Perang Dunia II berakhir pada tahun?", "kunci": "1945"},
                    {"soal": "Soeharto mundur pada tahun?", "kunci": "1998"},
                    {"soal": "VOC adalah kongsi dagang milik negara?", "kunci": "belanda"},
                    {"soal": "Patih Majapahit yang bersumpah Palapa?", "kunci": "gajah mada"},
                    {"soal": "Perang Dunia I dipicu oleh pembunuhan siapa?", "kunci": "franz ferdinand"},
                    {"soal": "Kota yang dibom atom pertama kali dalam PD II?", "kunci": "hiroshima"},
                    {"soal": "Revolusi Perancis terjadi pada tahun?", "kunci": "1789"},
                    {"soal": "Presiden pertama Indonesia?", "kunci": "soekarno"},
                    {"soal": "Wakil presiden pertama Indonesia?", "kunci": "hatta"},
                    {"soal": "Kerajaan Islam pertama di Indonesia?", "kunci": "samudera pasai"},
                    {"soal": "Tahun berdirinya VOC?", "kunci": "1602"},
                    {"soal": "Peristiwa G30S/PKI terjadi pada tahun?", "kunci": "1965"},
                    {"soal": "Boedi Oetomo didirikan pada tahun?", "kunci": "1908"},
                    {"soal": "Negara yang menjajah Indonesia selama 350 tahun?", "kunci": "belanda"},
                    {"soal": "Jepang menyerah tanpa syarat kepada siapa?", "kunci": "sekutu"},
                    {"soal": "Konferensi Meja Bundar menghasilkan pengakuan kedaulatan RI oleh?", "kunci": "belanda"},
                    {"soal": "Nama asli Ki Hajar Dewantara?", "kunci": "soewardi suryaningrat"},
                ],
            },

            # ================================================================
            # GEOGRAFI
            # ================================================================
            "geografi": {
                "desc": "Bumi, atmosfer, hidrosfer, litosfer, dan geografi manusia.",
                "emoji": "🌍",
                "aliases": ["geo", "geografi", "geography", "geog"],
                "materi": (
                    "📌 **Catatan Geografi:**\n"
                    "1. **Lapisan Bumi:** Kerak (crust) → Mantel → Inti luar (cair) → Inti dalam (padat).\n"
                    "2. **Lempeng Tektonik:** Bumi terdiri dari lempeng-lempeng yang bergerak. Menyebabkan gempa & gunung api.\n"
                    "3. **Atmosfer:** Troposfer → Stratosfer → Mesosfer → Termosfer → Eksosfer.\n"
                    "4. **Siklus Air:** Evaporasi → Kondensasi → Presipitasi → Run-off → kembali ke laut.\n"
                    "5. **Iklim & Cuaca:** Iklim = jangka panjang. Cuaca = jangka pendek. Tropis, subtropis, sedang, kutub.\n"
                    "6. **Erosi:** Pengikisan tanah oleh air, angin, atau es. Menyebabkan sedimentasi.\n"
                    "7. **Peta:** Simbol, skala, legenda, orientasi. Skala besar = detail lebih banyak.\n"
                    "8. **Penduduk:** Sensus, kepadatan penduduk, urbanisasi, migrasi."
                ),
                "kuis": [
                    {"soal": "Lapisan atmosfer paling bawah dekat permukaan bumi?", "kunci": "troposfer"},
                    {"soal": "Proses penguapan air disebut?", "kunci": "evaporasi"},
                    {"soal": "Lapisan bumi paling luar disebut?", "kunci": "kerak"},
                    {"soal": "Titik di permukaan bumi tepat di atas pusat gempa disebut?", "kunci": "episentrum"},
                    {"soal": "Benua terbesar di dunia?", "kunci": "asia"},
                    {"soal": "Samudra terluas di dunia?", "kunci": "pasifik"},
                    {"soal": "Proses pembentukan awan dari uap air disebut?", "kunci": "kondensasi"},
                    {"soal": "Garis khayal yang membagi bumi jadi utara dan selatan?", "kunci": "khatulistiwa"},
                    {"soal": "Peta topografi menggambarkan?", "kunci": "ketinggian"},
                    {"soal": "Gunung berapi aktif di Indonesia yang terkenal?", "kunci": "merapi"},
                    {"soal": "Angin yang bertiup dari darat ke laut terjadi pada?", "kunci": "malam"},
                    {"soal": "Perpindahan penduduk dari desa ke kota disebut?", "kunci": "urbanisasi"},
                    {"soal": "Indonesia berada di antara dua samudra, yaitu Hindia dan?", "kunci": "pasifik"},
                    {"soal": "Lapisan ozon berada di lapisan atmosfer?", "kunci": "stratosfer"},
                    {"soal": "Batas lempeng yang saling mendekat disebut?", "kunci": "konvergen"},
                    {"soal": "Iklim di Indonesia secara umum adalah iklim?", "kunci": "tropis"},
                    {"soal": "Proses hujan turun ke bumi disebut?", "kunci": "presipitasi"},
                    {"soal": "Negara dengan jumlah penduduk terbanyak di dunia?", "kunci": "india"},
                    {"soal": "Danau terdalam di dunia?", "kunci": "baikal"},
                    {"soal": "Sungai terpanjang di dunia?", "kunci": "nil"},
                ],
            },

            # ================================================================
            # BAHASA INDONESIA
            # ================================================================
            "bahasa indonesia": {
                "desc": "EYD, teks, sastra, struktur kalimat, dan majas bahasa Indonesia.",
                "emoji": "📝",
                "aliases": ["bahasa", "b.indo", "bindo", "indo", "bahasa indonesia", "b indo"],
                "materi": (
                    "📌 **Catatan Bahasa Indonesia:**\n"
                    "1. **EYD/PUEBI:** Pedoman ejaan resmi. Huruf kapital awal kalimat, nama orang, nama tempat.\n"
                    "2. **Jenis Kata:** Kata benda (nomina), kata kerja (verba), kata sifat (adjektiva), kata keterangan (adverbia).\n"
                    "3. **Kalimat Efektif:** Jelas, logis, hemat kata, tidak ambigu.\n"
                    "4. **Teks Narasi:** Menceritakan urutan peristiwa. Ada orientasi, komplikasi, resolusi.\n"
                    "5. **Teks Deskripsi:** Menggambarkan objek secara detail dengan panca indera.\n"
                    "6. **Majas:** Metafora (perbandingan langsung), simile (menggunakan 'seperti/bagai'), personifikasi (sifat manusia ke benda).\n"
                    "7. **Paragraf:** Kalimat utama + kalimat penjelas. Deduktif (utama di awal), induktif (utama di akhir).\n"
                    "8. **Sastra:** Puisi (bait, rima, irama), cerpen (singkat), novel (panjang)."
                ),
                "kuis": [
                    {"soal": "Kata yang menyatakan nama orang, tempat, atau benda disebut kata?", "kunci": "nomina"},
                    {"soal": "Majas yang membandingkan dua hal tanpa kata 'seperti' disebut?", "kunci": "metafora"},
                    {"soal": "Majas yang memberikan sifat manusia kepada benda mati disebut?", "kunci": "personifikasi"},
                    {"soal": "Paragraf yang kalimat utamanya ada di awal disebut paragraf?", "kunci": "deduktif"},
                    {"soal": "Teks yang menceritakan urutan kejadian disebut teks?", "kunci": "narasi"},
                    {"soal": "Singkatan EYD kepanjangannya adalah?", "kunci": "ejaan yang disempurnakan"},
                    {"soal": "Kata kerja dalam bahasa Indonesia disebut?", "kunci": "verba"},
                    {"soal": "Rima pada puisi yang berselang disebut rima?", "kunci": "silang"},
                    {"soal": "Kalimat yang memiliki satu subjek dan satu predikat disebut kalimat?", "kunci": "tunggal"},
                    {"soal": "Bagian awal cerpen yang memperkenalkan tokoh disebut?", "kunci": "orientasi"},
                    {"soal": "Antonim dari kata 'besar' adalah?", "kunci": "kecil"},
                    {"soal": "Sinonim dari kata 'bagus' adalah?", "kunci": "indah"},
                    {"soal": "Kalimat tanya diakhiri dengan tanda baca?", "kunci": "tanya"},
                    {"soal": "Teks yang bertujuan memengaruhi pembaca disebut teks?", "kunci": "persuasi"},
                    {"soal": "Imbuhan yang diletakkan di awal kata disebut?", "kunci": "prefiks"},
                    {"soal": "Imbuhan yang diletakkan di akhir kata disebut?", "kunci": "sufiks"},
                    {"soal": "Teks yang menggambarkan objek secara detail disebut teks?", "kunci": "deskripsi"},
                    {"soal": "Peribahasa 'ada udang di balik batu' artinya?", "kunci": "ada maksud tersembunyi"},
                    {"soal": "Kata 'berlari' terdiri dari kata dasar dan imbuhan apa?", "kunci": "ber-"},
                    {"soal": "Jenis paragraf yang kalimat utamanya di akhir disebut?", "kunci": "induktif"},
                ],
            },

            # ================================================================
            # TEKNOLOGI INFORMASI
            # ================================================================
            "teknologi informasi": {
                "desc": "Perangkat keras, lunak, jaringan, algoritma, dan literasi digital.",
                "emoji": "💻",
                "aliases": ["ti", "tik", "komputer", "it", "informatika", "computer", "teknologi", "tekinfo"],
                "materi": (
                    "📌 **Catatan Teknologi Informasi:**\n"
                    "1. **Hardware:** CPU (otak komputer), RAM (memori sementara), Storage (HDD/SSD), GPU.\n"
                    "2. **Software:** OS (Windows, Linux, macOS), aplikasi, driver, firmware.\n"
                    "3. **Jaringan:** LAN (lokal), WAN (luas), Internet. Protokol TCP/IP. IP Address.\n"
                    "4. **Algoritma:** Langkah-langkah logis untuk memecahkan masalah. Dasar pemrograman.\n"
                    "5. **Binary:** Komputer pakai sistem biner (0 dan 1). 1 byte = 8 bit.\n"
                    "6. **Database:** Kumpulan data terstruktur. SQL untuk query. Tabel, baris, kolom.\n"
                    "7. **Keamanan:** Enkripsi, password kuat, antivirus, phishing, malware.\n"
                    "8. **Internet:** WWW, HTTP/HTTPS, browser, search engine, email."
                ),
                "kuis": [
                    {"soal": "CPU singkatan dari?", "kunci": "central processing unit"},
                    {"soal": "1 byte terdiri dari berapa bit?", "kunci": "8"},
                    {"soal": "Sistem bilangan yang digunakan komputer (0 dan 1)?", "kunci": "biner"},
                    {"soal": "RAM singkatan dari?", "kunci": "random access memory"},
                    {"soal": "OS yang dikembangkan oleh open-source komunitas?", "kunci": "linux"},
                    {"soal": "Jaringan komputer dalam satu gedung disebut?", "kunci": "LAN"},
                    {"soal": "Protokol utama internet?", "kunci": "TCP/IP"},
                    {"soal": "HTML singkatan dari?", "kunci": "hypertext markup language"},
                    {"soal": "Perangkat keras untuk menampilkan gambar ke layar?", "kunci": "GPU"},
                    {"soal": "File yang merusak sistem komputer disebut?", "kunci": "malware"},
                    {"soal": "1 kilobyte = berapa byte?", "kunci": "1024"},
                    {"soal": "Basis data relasional menggunakan bahasa query?", "kunci": "SQL"},
                    {"soal": "HTTPS lebih aman dari HTTP karena menggunakan?", "kunci": "enkripsi"},
                    {"soal": "Google, Bing, DuckDuckGo adalah contoh?", "kunci": "search engine"},
                    {"soal": "Perangkat untuk menghubungkan jaringan berbeda disebut?", "kunci": "router"},
                    {"soal": "Proses mengubah data agar tidak terbaca orang lain?", "kunci": "enkripsi"},
                    {"soal": "Penipuan online yang mencuri data akun disebut?", "kunci": "phishing"},
                    {"soal": "Software yang mengatur semua resource komputer?", "kunci": "operating system"},
                    {"soal": "Kode unik yang mengidentifikasi perangkat di jaringan?", "kunci": "IP address"},
                    {"soal": "Penyimpanan data di server jarak jauh lewat internet disebut?", "kunci": "cloud"},
                ],
            },

            # ================================================================
            # BAHASA INGGRIS
            # ================================================================
            "bahasa inggris": {
                "desc": "Belajar bahasa Inggris seru: kosakata (vocabulary), tata bahasa (grammar), percakapan sehari-hari, dan tenses dasar.",
                "emoji": "🇬🇧",
                "aliases": ["english", "inggris", "eng", "english adventure", "bahasa inggris"],
                "materi": (
                    "📌 **Catatan English Adventure:**\n"
                    "1. **Greetings:** Hello, Good Morning, How are you?, Goodbye.\n"
                    "2. **Pronouns:** I (saya), You (kamu), They (mereka), We (kita), He (dia laki-laki), She (dia perempuan), It (benda/hewan).\n"
                    "3. **To Be:** Present (am, is, are), Past (was, were). *Example: I am a student.*\n"
                    "4. **Simple Present Tense:** Menyatakan fakta atau kebiasaan. Rumus: $S + V_1(s/es)$. *Example: She eats an apple.*\n"
                    "5. **Simple Past Tense:** Menyatakan kejadian masa lalu. Rumus: $S + V_2$. *Example: We played soccer yesterday.*\n"
                    "6. **Vocabulary - Animals:** Cat (kucing), Dog (anjing), Bird (burung), Elephant (gajah), Fish (ikan).\n"
                    "7. **Vocabulary - Colors:** Red (merah), Blue (biru), Green (hijau), Yellow (kuning), White (putih).\n"
                    "8. **Question Words (5W1H):** Who (siapa), What (apa), Where (di mana), When (kapan), Why (kenapa), How (bagaimana).\n"
                    "9. **Singular & Plural:** Book (satu buku) → Books (banyak buku). Tambahkan -s atau -es.\n"
                    "10. **Prepositions:** In (di dalam), On (di atas permukaan), Under (di bawah), Beside (di samping)."
                ),
                "kuis": [
                    {"soal": "Apa bahasa Inggris dari 'Kucing'?", "kunci": "cat"},
                    {"soal": "Translate to English: 'Saya adalah seorang siswa'.", "kunci": "I am a student"},
                    {"soal": "Translate to English: 'Apel merah'.", "kunci": "red apple"},
                    {"soal": "What is the plural form of 'Book'?", "kunci": "books"},
                    {"soal": "Complete: She ___ (go/goes) to school every day.", "kunci": "goes"},
                    {"soal": "Past tense dari kata kerja 'play' adalah?", "kunci": "played"},
                    {"soal": "Apa bahasa Inggris dari warna 'Kuning'?", "kunci": "yellow"},
                    {"soal": "Complete: They ___ (am/is/are) playing football.", "kunci": "are"},
                    {"soal": "Apa bahasa Inggris dari 'Di bawah meja'?", "kunci": "under the table"},
                    {"soal": "Kata tanya untuk menanyakan tempat?", "kunci": "where"},
                    {"soal": "Apa lawan kata dari 'Big' (besar)?", "kunci": "small"},
                    {"soal": "Bahasa Inggris dari angka 'Sebelas'?", "kunci": "eleven"},
                    {"soal": "Complete: We ___ (was/were) happy yesterday.", "kunci": "were"},
                    {"soal": "Apa arti dari kata kerja 'Run'?", "kunci": "lari"},
                    {"soal": "Apa bahasa Inggris dari 'Burung'?", "kunci": "bird"},
                    {"soal": "Complete: An ___ (a/an) apple a day keeps the doctor away.", "kunci": "an"},
                    {"soal": "Apa bahasa Inggris dari 'Selamat pagi'?", "kunci": "good morning"},
                    {"soal": "Lawan kata dari 'Hot' (panas)?", "kunci": "cold"},
                    {"soal": "Bahasa Inggris dari 'Keluarga'?", "kunci": "family"},
                    {"soal": "Complete: He has a ___ (dog/dogs) named Blacky.", "kunci": "dog"},
                ],
            },

        }

        # ── Build alias → canonical key map ────────────────────────────────
        self.alias_map = {}
        for canonical, data in self.course_data.items():
            for alias in data.get("aliases", []):
                self.alias_map[alias.lower()] = canonical
            self.alias_map[canonical.lower()] = canonical

        # ── Dynamic regex: all aliases + canonical keys ─────────────────────
        all_terms = sorted(self.alias_map.keys(), key=len, reverse=True)  # longest first
        escaped   = [re.escape(t) for t in all_terms]
        self.re_course = re.compile(r"(?<!\w)(" + "|".join(escaped) + r")(?!\w)", re.IGNORECASE)

    # ── Subject parser ───────────────────────────────────────────────────────
    def parse_subject(self, text):
        text = text.lower().strip()
        match = self.re_course.search(text)
        if match:
            return self.alias_map.get(match.group(1).lower())
        return None

    # ── Closest-match fallback ────────────────────────────────────────────────
    def suggest_closest(self, text):
        """Return a list of subjects whose names/aliases partially appear in text."""
        text = text.lower()
        suggestions = []
        for alias, canonical in self.alias_map.items():
            if len(alias) >= 3 and alias in text:
                if canonical not in suggestions:
                    suggestions.append(canonical)
        return suggestions

    # ── Intent detector ──────────────────────────────────────────────────────
    def detect_intent(self, text):
        t = text.lower().strip()

        # Normalize common typos / gaul forms
        t = re.sub(r"\bngga[kh]?\b|\bkaga\b|\bnggak\b|\benggak\b", "tidak", t)
        t = re.sub(r"\bokee?\b|\boke\b|\bsip\b|\bgas\b|\bgass\b|\byuk\b", "ya", t)
        t = re.sub(r"\blatian\b", "latihan", t)
        t = re.sub(r"\bpelajaran\b|\bmapel\b", "subjek", t)
        t = re.sub(r"\baku\b|\baku\b", "aku", t)
        t = re.sub(r"\bberhitung seru\b", "matematika", t)
        t = re.sub(r"\bpenjelajah dunia\b|\bpenjelajah dunia ipa\b|\bbiologi\b", "biologi", t)
        t = re.sub(r"\bbahasa & cerita\b|\bbahasa indonesia\b|\bbahasa indonesia sma\b", "bahasa indonesia", t)
        t = re.sub(r"\bkreatif digital\b|\bteknologi informasi\b|\bTI\b|\bTIK\b", "teknologi informasi", t)
        t = re.sub(r"\bpenjelajah bumi\b|\bgeografi\b", "geografi", t)
        t = re.sub(r"\bpetualangan fisika\b|\bfisika\b", "fisika", t)
        t = re.sub(r"\blab kimia cilik\b|\bkimia\b", "kimia", t)
        t = re.sub(r"\bdetektif sejarah\b|\bsejarah\b|\bIPS\b", "sejarah", t)
        t = re.sub(r"\benglish adventure\b|\bbahasa inggris\b", "bahasa inggris", t)

        if re.search(r"\b(reset|ulang|mulai baru|keluar|restart|from scratch|awal lagi)\b", t):
            return "RESET_SYSTEM"

        if re.search(
            r"(menu|menunya|menu nya|daftar|list|pilihan|opsi|fitur|"
            r"subjek|mapel|mata pelajaran|pelajaran|materi|topik|"
            r"belajar apa|belajar apa aja|belajar apa saja|"
            r"ada apa aja|ada apa saja|ada apa|"
            r"apa aja|apa saja|apa yg ada|apa yang ada|"
            r"bisa apa aja|bisa apa saja|"
            r"bisa belajar apa|"
            r"materinya apa|materi apa aja|materi apa saja|"
            r"topiknya apa|topik apa aja|topik apa saja|"
            r"pelajaran apa aja|pelajaran apa saja|"
            r"mapelnya apa|mapel apa aja|"
            r"ada menu ga|ada menu gak|ada menu kah|"
            r"ada menunya|ada menu nya|"
            r"menu dong|lihat menu|show menu|"
            r"kasih menu|tampilkan menu|"
            r"ada mapelnya apa|ada mapelnya apa aja|ada mapel apa|ada mapel apa aja|"
            r"ada subjek apa aja|ada subjek apa aja|"
            r"ada pelajaran apa aja|ada pelajaran apa aja|"
            r"ada materi apa aja|ada materi apa aja|"
            r"ada topik apa aja|ada topik apa aja|"
            r"lihat menu bro|lihat menu breh|spill dong menu nya|apa aja menunya|"
            r"liat menu|lihat daftar|"
            r"pilihannya apa|opsinya apa|"
            r"mau belajar apa|"
            r"tersedia apa aja|"
            r"yang bisa dipelajari apa aja|"
            r"yang tersedia apa aja|"
            r"ada pelajaran apa aja|"
            r"ada materi apa aja|"
            r"ada topik apa aja|"
            r"materi yang tersedia|"
            r"fiturnya apa aja|"
            r"isinya apa aja|"
            r"ada apa disini|"
            r"disini bisa apa aja|"
            r"aku bisa ngapain aja|"
            r"ngapain aja disini|"
            r"mulai dari mana|"
            r"harus belajar apa|"
            r"rekomendasi materi|"
            r"rekomendasi topik)",
            t
        ):
            return "ASK_MENU"

        if re.search(
            r"(materi|baca|belajar|teori|penjelasan|jelasin|jelaskan|"
            r"rangkuman|rangkum|ringkasan|catatan|notes|"
            r"pelajari|paham|memahami|ngerti|mengerti|"
            r"info|informasi|wawasan|pengetahuan|"
            r"ajari|ajarin|ajarkan|teach|"
            r"bahas|bahasin|pembahasan|"
            r"kupas|kupasin|ulas|ulasan|"
            r"apa itu|apaan itu|"
            r"ceritain|ceritakan|"
            r"kasih materi|"
            r"kasih penjelasan|"
            r"mau belajar|"
            r"ingin belajar|"
            r"pengen belajar|"
            r"mau ngerti|"
            r"ingin ngerti|"
            r"pengen ngerti|"
            r"tolong jelaskan|"
            r"bantu jelaskan|"
            r"bantu pahami|"
            r"pengertian|"
            r"definisi|"
            r"konsep|"
            r"dasar dasar|"
            r"dasarnya|"
            r"fundamental)",
            t
        ):
            return "LEARN_MATERIAL"

        if re.search(
            r"(kuis|quiz|tes|test|ujian|"
            r"soal|latihan soal|"
            r"uji kemampuan|"
            r"tryout|try out|"
            r"mau kuis|"
            r"mulai kuis|"
            r"mulai quiz|"
            r"mulai tes|"
            r"mulai ujian|"
            r"kasih soal|"
            r"beri soal|"
            r"berikan soal|"
            r"punya soal|"
            r"ada soal|"
            r"latihan dong|"
            r"latihan yuk|"
            r"mau latihan|"
            r"ingin latihan|"
            r"pengen latihan|"
            r"uji saya|"
            r"tes saya|"
            r"kuis dong|"
            r"quiz dong|"
            r"ayo kuis|"
            r"ayo quiz|"
            r"langsung soal|"
            r"langsung kuis)",
            t
        ):
            return "START_QUIZ"


        if re.search(
            r"\b(ya|yes|oke|ok|sip|siap|betul|benar|"
            r"gaskeun|gaspol|gasin|gass|bolehlah|boleh|"
            r"iyoi|ha a|ho oh|yoii|yoi|ha yoi|yoi ah|ha a yoi|"
            r"boleh|oke|bolehlah|boleeeeh|"
            r"lanjut|next|boleh|mau|deal|setuju|"
            r"gas+|gass+|gaspol+|gas pol+|"
            r"gaskan|gasin|gaskeun|"
            r"heeh|he eh|ho oh|ho o)\b",
            t
        ):
            return "YES"

        if re.search(r"\b(tidak|no|batal|belum|gak|nope|skip|cancel|rak|moh|gah|ogah|ogeh|nanti|lain kali|lain waktu|keluar|keluar dari kuis|keluar dari materi|keluar dari pembelajaran|mau keluar|ingin keluar|pengen keluar|keluar aja|selesai|stop|udah cukup|udahlah|udahan|cukup ah)\b", t):
            return "NO"

        if re.search(r"\b(bantuan|help|bingung|bingungy|bantuin dong|bantuin ya|hah gimana|piye|piye iki|gimana ini|piye to|tolong piye|piye iki carane|tolong gimana|tolong gimana ya|tolong gimana carane|piye carane|piye to carane|piye toh|piye toh iki|piye toh iki carane|piye toh carane|piye toh carane iki|piye toh carane iki piye|huh|apa|gimana|cara|how|tolong)\b", t):
            return "HELP"

        return "UNKNOWN"
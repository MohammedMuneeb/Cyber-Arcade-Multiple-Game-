"""
=============================================================================

                      GENERAL KNOWLEDGE QUIZ - MODERN GUI
=============================================================================
A sleek, dark-themed interactive General Knowledge quiz built with Tkinter.
Features:
- 50+ questions across Science, History, Geography, Sports, Movies, Music
- Timed rounds with animated progress bar
- Lifelines: 50/50, Time Freeze (+15s), Skip
- Streak multiplier & combo scoring
- Instant feedback with detailed explanations
- Final results summary with category breakdown
=============================================================================
"""

import tkinter as tk
from tkinter import ttk
import random
import time

# ---------------------------------------------------------------------------
# THEME
# ---------------------------------------------------------------------------
THEME = {
    "bg_dark":        "#0d1117", 
    "bg_card":        "#161b22", 
    "bg_card_alt":    "#21262d", 
    "border":         "#30363d", 
    "text_primary":   "#f0f6fc", 
    "text_secondary": "#8b949e", 
    "accent_cyan":    "#00d2ff",

    "accent_purple":  "#a371f7", 
    "accent_amber":   "#f0883e", 
    "accent_green":   "#3fb950", 
    "success":        "#2ea043", 
    "success_light":  "#3fb950", 
    "danger":         "#da3633", 
    "danger_light":   "#f85149", 
    "gold":           "#d29922", 
    "btn_opt_bg":     "#21262d", 

    "btn_opt_fg":     "#e6edf3", 
} 
# --------------------------------------------------------------------------- 
# QUESTION BANK  (60 questions across 6 categories) 
# --------------------------------------------------------------------------- 
QUESTIONS = [ 
    # ── SCIENCE & NATURE ───────────────────────────────────────────────── 
    {"id":1,"category":"Science","difficulty":"Easy",
     "question":"What is the chemical symbol for water?",
     "options":["H2O","HO2","H3O","O2H"],"answer":0,
     "explanation":"Water is made of 2 hydrogen atoms bonded to 1 oxygen atom, giving H₂O."},

    {"id":2,"category":"Science","difficulty":"Easy",
     "question":"What planet is known as the Red Planet?",
     "options":["Venus","Jupiter","Mars","Saturn"],"answer":2,
     "explanation":"Mars appears red due to iron oxide (rust) on its surface."},

    {"id":3,"category":"Science","difficulty":"Medium",
     "question":"What is the speed of light in a vacuum (approx)?",
     "options":["300,000 km/s","150,000 km/s","450,000 km/s","30,000 km/s"],"answer":0,
     "explanation":"Light travels at approximately 299,792 km/s in a vacuum."},

    {"id":4,"category":"Science","difficulty":"Medium",
     "question":"How many bones are in the adult human body?",
     "options":["206","198","215","230"],"answer":0,
     "explanation":"Adults have 206 bones; babies are born with around 270 and some fuse over time."},

    {"id":5,"category":"Science","difficulty":"Medium",
     "question":"Which gas do plants absorb from the atmosphere during photosynthesis?",
     "options":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],"answer":2,
     "explanation":"Plants absorb CO₂ and release O₂ during photosynthesis."},

    {"id":6,"category":"Science","difficulty":"Hard",
     "question":"What is the atomic number of Gold (Au)?",
     "options":["47","79","82","29"],"answer":1,
     "explanation":"Gold (Au) has atomic number 79 on the periodic table."},

    {"id":7,"category":"Science","difficulty":"Hard",
     "question":"What is the powerhouse of the cell?",
     "options":["Nucleus","Ribosome","Mitochondria","Golgi Apparatus"],"answer":2,
     "explanation":"Mitochondria generate ATP — the energy currency of the cell."},

    {"id":8,"category":"Science","difficulty":"Hard",
     "question":"Which element has the highest melting point?",
     "options":["Iron","Tungsten","Carbon","Platinum"],"answer":1,
     "explanation":"Tungsten (W) has the highest melting point of any element at 3,422 °C."},

    # ── HISTORY ───────────────────────────────────────────────────────────
    {"id":9,"category":"History","difficulty":"Easy",
     "question":"Who was the first President of the United States?",
     "options":["Abraham Lincoln","Thomas Jefferson","George Washington","John Adams"],"answer":2,
     "explanation":"George Washington served as the 1st US President from 1789–1797."},

    {"id":10,"category":"History","difficulty":"Easy",
     "question":"In which year did World War II end?",
     "options":["1943","1944","1945","1946"],"answer":2,
     "explanation":"WWII ended in 1945: V-E Day (May) and V-J Day (September)."},

    {"id":11,"category":"History","difficulty":"Medium",
     "question":"Which ancient wonder was located in Alexandria, Egypt?",
     "options":["Colossus of Rhodes","Lighthouse of Alexandria","Temple of Artemis","Statue of Zeus"],"answer":1,
     "explanation":"The Lighthouse of Alexandria (Pharos) was one of the Seven Wonders of the Ancient World."},

    {"id":12,"category":"History","difficulty":"Medium",
     "question":"Who painted the Mona Lisa?",
     "options":["Michelangelo","Raphael","Leonardo da Vinci","Caravaggio"],"answer":2,
     "explanation":"Leonardo da Vinci painted the Mona Lisa between 1503–1519."},

    {"id":13,"category":"History","difficulty":"Medium",
     "question":"The Berlin Wall fell in which year?",
     "options":["1987","1988","1989","1991"],"answer":2,
     "explanation":"The Berlin Wall fell on November 9, 1989, ending the division of East and West Berlin."},

    {"id":14,"category":"History","difficulty":"Hard",
     "question":"Which empire was ruled by Genghis Khan?",
     "options":["Ottoman","Mongol","Roman","Persian"],"answer":1,
     "explanation":"Genghis Khan founded the Mongol Empire, the largest contiguous land empire in history."},

    {"id":15,"category":"History","difficulty":"Hard",
     "question":"The Treaty of Versailles (1919) officially ended which war?",
     "options":["World War II","The Crimean War","World War I","The Boer War"],"answer":2,
     "explanation":"The Treaty of Versailles ended World War I and imposed harsh penalties on Germany."},

    # ── GEOGRAPHY ────────────────────────────────────────────────────────
    {"id":16,"category":"Geography","difficulty":"Easy",
     "question":"What is the largest continent by area?",
     "options":["Africa","North America","Europe","Asia"],"answer":3,
     "explanation":"Asia is the largest continent, covering about 44.6 million km²."},

    {"id":17,"category":"Geography","difficulty":"Easy",
     "question":"Which is the longest river in the world?",
     "options":["Amazon","Congo","Nile","Yangtze"],"answer":2,
     "explanation":"The Nile River stretches about 6,650 km through northeastern Africa."},

    {"id":18,"category":"Geography","difficulty":"Medium",
     "question":"What is the capital of Australia?",
     "options":["Sydney","Melbourne","Brisbane","Canberra"],"answer":3,
     "explanation":"Canberra is the capital of Australia, chosen as a compromise between Sydney and Melbourne."},

    {"id":19,"category":"Geography","difficulty":"Medium",
     "question":"Which country has the most natural lakes?",
     "options":["Russia","USA","Brazil","Canada"],"answer":3,
     "explanation":"Canada has over 60% of the world's natural lakes."},

    {"id":20,"category":"Geography","difficulty":"Medium",
     "question":"Mount Everest is located on the border of which two countries?",
     "options":["India & China","Nepal & China","Nepal & India","Bhutan & China"],"answer":1,
     "explanation":"Mount Everest sits on the Nepal–China (Tibet) border in the Himalayas."},

    {"id":21,"category":"Geography","difficulty":"Hard",
     "question":"What is the smallest country in the world by area?",
     "options":["Monaco","San Marino","Vatican City","Liechtenstein"],"answer":2,
     "explanation":"Vatican City covers just 0.44 km², making it the smallest sovereign state."},

    {"id":22,"category":"Geography","difficulty":"Hard",
     "question":"The Strait of Malacca separates which two landmasses?",
     "options":["Sumatra & Java","Borneo & Sumatra","Malay Peninsula & Sumatra","Malay Peninsula & Borneo"],"answer":2,
     "explanation":"The Strait of Malacca lies between the Malay Peninsula and the Indonesian island of Sumatra."},

    # ── SPORTS ───────────────────────────────────────────────────────────
    {"id":23,"category":"Sports","difficulty":"Easy",
     "question":"How many players are on a standard football (soccer) team on the field?",
     "options":["9","10","11","12"],"answer":2,
     "explanation":"Each soccer team fields 11 players including the goalkeeper."},

    {"id":24,"category":"Sports","difficulty":"Easy",
     "question":"In which sport would you perform a 'slam dunk'?",
     "options":["Volleyball","Tennis","Basketball","Handball"],"answer":2,
     "explanation":"A slam dunk is a basketball shot where the player jumps and forces the ball into the hoop."},

    {"id":25,"category":"Sports","difficulty":"Medium",
     "question":"Which country has won the most FIFA World Cup titles?",
     "options":["Germany","Argentina","Italy","Brazil"],"answer":3,
     "explanation":"Brazil has won the FIFA World Cup a record 5 times (1958, 62, 70, 94, 2002)."},

    {"id":26,"category":"Sports","difficulty":"Medium",
     "question":"How many Grand Slam tournaments are held in tennis each year?",
     "options":["2","3","4","5"],"answer":2,
     "explanation":"The four Grand Slams are Australian Open, French Open, Wimbledon, and US Open."},

    {"id":27,"category":"Sports","difficulty":"Medium",
     "question":"In Olympic swimming, how many metres is the standard long-course pool?",
     "options":["25m","50m","75m","100m"],"answer":1,
     "explanation":"Olympic pools are 50 metres long (long-course). Short-course pools are 25 m."},

    {"id":28,"category":"Sports","difficulty":"Hard",
     "question":"Who holds the world record for the 100m sprint (as of 2024)?",
     "options":["Yohan Blake","Justin Gatlin","Usain Bolt","Tyreek Hill"],"answer":2,
     "explanation":"Usain Bolt set the 100m world record of 9.58 seconds at the 2009 World Championships in Berlin."},

    {"id":29,"category":"Sports","difficulty":"Hard",
     "question":"Which country hosted the first modern Olympic Games in 1896?",
     "options":["France","UK","USA","Greece"],"answer":3,
     "explanation":"The first modern Olympics were held in Athens, Greece in 1896."},

    # ── MOVIES & TV ──────────────────────────────────────────────────────
    {"id":30,"category":"Entertainment","difficulty":"Easy",
     "question":"Who played Iron Man in the Marvel Cinematic Universe?",
     "options":["Chris Evans","Chris Hemsworth","Robert Downey Jr.","Mark Ruffalo"],"answer":2,
     "explanation":"Robert Downey Jr. portrayed Tony Stark / Iron Man across 10+ MCU films."},

    {"id":31,"category":"Entertainment","difficulty":"Easy",
     "question":"Which movie features the quote 'May the Force be with you'?",
     "options":["Star Trek","Star Wars","Interstellar","The Matrix"],"answer":1,
     "explanation":"'May the Force be with you' is the iconic phrase from the Star Wars franchise."},

    {"id":32,"category":"Entertainment","difficulty":"Medium",
     "question":"Which film won the Best Picture Oscar at the 2020 Academy Awards?",
     "options":["1917","Joker","Parasite","Once Upon a Time in Hollywood"],"answer":2,
     "explanation":"Parasite (Bong Joon-ho) made history as the first non-English-language film to win Best Picture."},

    {"id":33,"category":"Entertainment","difficulty":"Medium",
     "question":"In the TV show 'Breaking Bad', what subject does Walter White teach?",
     "options":["Biology","Chemistry","Physics","Mathematics"],"answer":1,
     "explanation":"Walter White is a high school chemistry teacher turned methamphetamine manufacturer."},

    {"id":34,"category":"Entertainment","difficulty":"Medium",
     "question":"Who directed the movie 'Inception' (2010)?",
     "options":["Steven Spielberg","James Cameron","Christopher Nolan","Ridley Scott"],"answer":2,
     "explanation":"Christopher Nolan wrote and directed Inception, released in 2010."},

    {"id":35,"category":"Entertainment","difficulty":"Hard",
     "question":"What is the highest-grossing film of all time (unadjusted for inflation)?",
     "options":["Avengers: Endgame","Titanic","Avatar","Star Wars: The Force Awakens"],"answer":2,
     "explanation":"Avatar (2009, re-released 2022) holds the all-time box office record at over $2.9 billion."},

    # ── MUSIC ────────────────────────────────────────────────────────────
    {"id":36,"category":"Music","difficulty":"Easy",
     "question":"Which band performed 'Bohemian Rhapsody'?",
     "options":["The Beatles","Led Zeppelin","Queen","The Rolling Stones"],"answer":2,
     "explanation":"Bohemian Rhapsody was written by Freddie Mercury and performed by Queen, released in 1975."},

    {"id":37,"category":"Music","difficulty":"Easy",
     "question":"How many strings does a standard guitar have?",
     "options":["4","5","6","7"],"answer":2,
     "explanation":"A standard guitar has 6 strings, tuned E-A-D-G-B-E from lowest to highest."},

    {"id":38,"category":"Music","difficulty":"Medium",
     "question":"Which artist released the album 'Thriller' (1982)?",
     "options":["Prince","Michael Jackson","David Bowie","Stevie Wonder"],"answer":1,
     "explanation":"Michael Jackson's Thriller is the best-selling album of all time with over 66 million copies sold."},

    {"id":39,"category":"Music","difficulty":"Medium",
     "question":"What nationality was the composer Ludwig van Beethoven?",
     "options":["Austrian","German","Italian","French"],"answer":1,
     "explanation":"Beethoven was born in Bonn, Germany in 1770 and later moved to Vienna."},

    {"id":40,"category":"Music","difficulty":"Hard",
     "question":"Which instrument does a pianist play?",
     "options":["Violin","Piano","Harp","Harpsichord"],"answer":1,
     "explanation":"A pianist plays the piano — a keyboard instrument with strings struck by hammers."},

    # ── GENERAL KNOWLEDGE ────────────────────────────────────────────────
    {"id":41,"category":"General","difficulty":"Easy",
     "question":"How many sides does a hexagon have?",
     "options":["5","6","7","8"],"answer":1,
     "explanation":"A hexagon has 6 sides. Hex- comes from the Greek word for six."},

    {"id":42,"category":"General","difficulty":"Easy",
     "question":"What colour is the sky on a clear day?",
     "options":["Green","Grey","Blue","Violet"],"answer":2,
     "explanation":"The sky appears blue because of Rayleigh scattering — short blue wavelengths scatter more."},

    {"id":43,"category":"General","difficulty":"Medium",
     "question":"What is the currency of Japan?",
     "options":["Yuan","Won","Rupee","Yen"],"answer":3,
     "explanation":"Japan's currency is the Japanese Yen (¥), introduced in 1871."},

    {"id":44,"category":"General","difficulty":"Medium",
     "question":"What does 'URL' stand for?",
     "options":["Uniform Resource Locator","Universal Reference Link","Unified Remote Library","Uniform Routing Label"],"answer":0,
     "explanation":"URL stands for Uniform Resource Locator — the web address you type in a browser."},

    {"id":45,"category":"General","difficulty":"Medium",
     "question":"How many time zones does Russia have?",
     "options":["9","10","11","12"],"answer":2,
     "explanation":"Russia spans 11 time zones, making it the country with the most time zones in the world."},

    {"id":46,"category":"General","difficulty":"Hard",
     "question":"What is the loudest animal on Earth?",
     "options":["Blue Whale","Howler Monkey","Sperm Whale","Lion"],"answer":2,
     "explanation":"The Sperm Whale produces clicks up to 230 dB — the loudest sound made by any animal."},

    {"id":47,"category":"General","difficulty":"Hard",
     "question":"What is the most spoken language in the world by native speakers?",
     "options":["English","Hindi","Spanish","Mandarin Chinese"],"answer":3,
     "explanation":"Mandarin Chinese has the most native speakers (~920 million). English leads in total speakers."},

    {"id":48,"category":"General","difficulty":"Hard",
     "question":"Which element is liquid at room temperature besides Mercury?",
     "options":["Bromine","Fluorine","Chlorine","Phosphorus"],"answer":0,
     "explanation":"Bromine is one of only two elements (along with Mercury) that are liquid at room temperature."},

    {"id":49,"category":"Science","difficulty":"Medium",
     "question":"What force keeps planets in orbit around the Sun?",
     "options":["Magnetism","Electrostatic force","Gravity","Nuclear force"],"answer":2,
     "explanation":"Gravity is the attractive force between masses that keeps planets in their orbital paths."},

    {"id":50,"category":"History","difficulty":"Medium",
     "question":"Who wrote 'Romeo and Juliet'?",
     "options":["Charles Dickens","Geoffrey Chaucer","William Shakespeare","John Milton"],"answer":2,
     "explanation":"Romeo and Juliet was written by William Shakespeare around 1594–1596."},
]


# ---------------------------------------------------------------------------
# CATEGORY COLORS
# ---------------------------------------------------------------------------
CATEGORY_COLORS = {
    "Science":       "#00e5ff",
    "History":       "#a371f7",
    "Geography":     "#3fb950",
    "Sports":        "#f0883e",
    "Entertainment": "#ff79c6",
    "Music":         "#ffb700",
    "General":       "#64748b",
}

DIFFICULTY_COLORS = {
    "Easy":   "#3fb950",
    "Medium": "#f0883e",
    "Hard":   "#f85149",
}


# ---------------------------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------------------------
class GeneralQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 General Knowledge Quiz")
        self.root.geometry("820x700")
        self.root.minsize(760, 620)
        self.root.config(bg=THEME["bg_dark"])

        # Game state
        self.all_questions = QUESTIONS.copy()
        random.shuffle(self.all_questions)
        self.questions = self.all_questions[:20]   # pick 20 random

        self.q_index = 0
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.correct_count = 0
        self.time_left = 30
        self.timer_running = False
        self.answered = False

        self.lifelines = {"fifty_fifty": True, "freeze": True, "skip": True}
        self.eliminated = []   # indices of 50/50 eliminated options

        self.answer_record = []  # {q, chosen, correct, got_right}

        self._timer_id = None
        self._bar_anim_id = None

        self._build_ui()
        self._load_question()

    # ── UI BUILD ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=THEME["bg_card"], pady=10)
        hdr.pack(fill="x")

        tk.Label(hdr, text="🌍  GENERAL KNOWLEDGE QUIZ",
                 font=("Helvetica", 18, "bold"),
                 bg=THEME["bg_card"], fg=THEME["accent_cyan"]).pack(side="left", padx=18)

        right = tk.Frame(hdr, bg=THEME["bg_card"])
        right.pack(side="right", padx=16)

        self.score_lbl = tk.Label(right, text="SCORE  0",
                                   font=("Helvetica", 13, "bold"),
                                   bg=THEME["bg_card"], fg=THEME["gold"])
        self.score_lbl.pack(side="left", padx=12)

        self.streak_lbl = tk.Label(right, text="🔥 0",
                                    font=("Helvetica", 12, "bold"),
                                    bg=THEME["bg_card"], fg=THEME["accent_amber"])
        self.streak_lbl.pack(side="left", padx=8)

        # Question progress bar
        pb_frame = tk.Frame(self.root, bg=THEME["bg_dark"])
        pb_frame.pack(fill="x", padx=20, pady=(8, 0))

        self.progress_var = tk.DoubleVar(value=0)
        self.prog_bar = ttk.Progressbar(pb_frame, variable=self.progress_var,
                                         maximum=len(self.questions), length=780)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("green.Horizontal.TProgressbar",
                         troughcolor=THEME["bg_card_alt"],
                         background=THEME["accent_cyan"], thickness=6)
        self.prog_bar.configure(style="green.Horizontal.TProgressbar")
        self.prog_bar.pack(fill="x")

        self.q_progress_lbl = tk.Label(self.root,
                                        text="Question 1 / 20",
                                        font=("Helvetica", 10),
                                        bg=THEME["bg_dark"],
                                        fg=THEME["text_secondary"])
        self.q_progress_lbl.pack(anchor="e", padx=22)

        # Timer bar
        timer_frm = tk.Frame(self.root, bg=THEME["bg_dark"])
        timer_frm.pack(fill="x", padx=20, pady=(4, 0))

        self.timer_lbl = tk.Label(timer_frm, text="⏱ 30s",
                                   font=("Helvetica", 11, "bold"),
                                   bg=THEME["bg_dark"], fg=THEME["accent_cyan"])
        self.timer_lbl.pack(side="left")

        self.timer_canvas = tk.Canvas(timer_frm, height=8,
                                       bg=THEME["bg_card_alt"],
                                       highlightthickness=0)
        self.timer_canvas.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.timer_bar_rect = None

        # Category & difficulty badges
        badge_frm = tk.Frame(self.root, bg=THEME["bg_dark"])
        badge_frm.pack(fill="x", padx=20, pady=(10, 4))

        self.cat_lbl = tk.Label(badge_frm, text="", font=("Helvetica", 10, "bold"),
                                  bg=THEME["bg_dark"], fg=THEME["accent_cyan"])
        self.cat_lbl.pack(side="left")

        self.diff_lbl = tk.Label(badge_frm, text="",
                                  font=("Helvetica", 10, "bold"),
                                  bg=THEME["bg_dark"], fg=THEME["accent_amber"])
        self.diff_lbl.pack(side="left", padx=14)

        # Question card
        qcard = tk.Frame(self.root, bg=THEME["bg_card"],
                          relief="flat", bd=0)
        qcard.pack(fill="x", padx=20, pady=(0, 10))

        self.q_text = tk.Label(qcard,
                                text="",
                                font=("Helvetica", 14, "bold"),
                                bg=THEME["bg_card"],
                                fg=THEME["text_primary"],
                                wraplength=740,
                                justify="left",
                                padx=20, pady=18)
        self.q_text.pack(fill="x")

        # Answer buttons
        self.btn_frame = tk.Frame(self.root, bg=THEME["bg_dark"])
        self.btn_frame.pack(fill="x", padx=20)

        self.opt_btns = []
        for i in range(4):
            btn = tk.Button(self.btn_frame,
                             text="",
                             font=("Helvetica", 12),
                             bg=THEME["btn_opt_bg"],
                             fg=THEME["btn_opt_fg"],
                             activebackground=THEME["bg_card_alt"],
                             relief="flat", bd=0,
                             wraplength=700,
                             justify="left",
                             padx=16, pady=14,
                             cursor="hand2",
                             command=lambda idx=i: self._choose(idx))
            btn.pack(fill="x", pady=5)
            self.opt_btns.append(btn)

        # Explanation label (hidden until answered)
        self.explain_lbl = tk.Label(self.root, text="",
                                     font=("Helvetica", 11, "italic"),
                                     bg=THEME["bg_dark"],
                                     fg=THEME["text_secondary"],
                                     wraplength=740,
                                     justify="left",
                                     padx=22, pady=6)
        self.explain_lbl.pack(fill="x")

        # Lifeline bar
        ll_frm = tk.Frame(self.root, bg=THEME["bg_dark"])
        ll_frm.pack(pady=(6, 4))

        self.btn_fifty = tk.Button(ll_frm, text="50/50",
                                    font=("Helvetica", 10, "bold"),
                                    bg=THEME["accent_purple"], fg="#fff",
                                    relief="flat", bd=0, padx=12, pady=6,
                                    cursor="hand2",
                                    command=self._lifeline_fifty)
        self.btn_fifty.pack(side="left", padx=6)

        self.btn_freeze = tk.Button(ll_frm, text="⏱ +15s",
                                     font=("Helvetica", 10, "bold"),
                                     bg=THEME["accent_cyan"], fg="#000",
                                     relief="flat", bd=0, padx=12, pady=6,
                                     cursor="hand2",
                                     command=self._lifeline_freeze)
        self.btn_freeze.pack(side="left", padx=6)

        self.btn_skip = tk.Button(ll_frm, text="⏭ Skip",
                                   font=("Helvetica", 10, "bold"),
                                   bg=THEME["accent_amber"], fg="#000",
                                   relief="flat", bd=0, padx=12, pady=6,
                                   cursor="hand2",
                                   command=self._lifeline_skip)
        self.btn_skip.pack(side="left", padx=6)

        # Next button (hidden until answered)
        self.next_btn = tk.Button(self.root,
                                   text="NEXT  ▶",
                                   font=("Helvetica", 12, "bold"),
                                   bg=THEME["accent_cyan"], fg="#000",
                                   relief="flat", bd=0,
                                   padx=26, pady=10,
                                   cursor="hand2",
                                   command=self._next_question)
        self.next_btn.pack(pady=8)
        self.next_btn.pack_forget()

    # ── QUESTION LOADING ──────────────────────────────────────────────────
    def _load_question(self):
        if self.q_index >= len(self.questions):
            self._show_results()
            return

        q = self.questions[self.q_index]
        self.answered = False
        self.eliminated = []
        self.time_left = 30
        self.explain_lbl.config(text="")
        self.next_btn.pack_forget()

        # Badges
        cat_color = CATEGORY_COLORS.get(q["category"], THEME["accent_cyan"])
        diff_color = DIFFICULTY_COLORS.get(q["difficulty"], THEME["accent_amber"])
        self.cat_lbl.config(text=f"📌 {q['category']}", fg=cat_color)
        self.diff_lbl.config(text=f"⚡ {q['difficulty']}", fg=diff_color)

        # Progress
        self.progress_var.set(self.q_index)
        self.q_progress_lbl.config(
            text=f"Question {self.q_index + 1} / {len(self.questions)}")

        # Question text
        self.q_text.config(text=q["question"])

        # Shuffle options
        indices = list(range(4))
        random.shuffle(indices)
        self._option_map = {}   # display_pos -> original_index
        for pos, orig in enumerate(indices):
            self._option_map[pos] = orig
            letter = "ABCD"[pos]
            self.opt_btns[pos].config(
                text=f"  {letter}.  {q['options'][orig]}",
                bg=THEME["btn_opt_bg"],
                fg=THEME["btn_opt_fg"],
                state="normal")

        self._start_timer()

    # ── TIMER ─────────────────────────────────────────────────────────────
    def _start_timer(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        self.timer_running = True
        self._tick()

    def _tick(self):
        if not self.timer_running:
            return
        self._draw_timer_bar()
        self.timer_lbl.config(
            text=f"⏱ {self.time_left}s",
            fg=THEME["danger_light"] if self.time_left <= 8 else THEME["accent_cyan"])

        if self.time_left <= 0:
            self.timer_running = False
            self._time_up()
            return

        self.time_left -= 1
        self._timer_id = self.root.after(1000, self._tick)

    def _draw_timer_bar(self):
        self.timer_canvas.update_idletasks()
        w = self.timer_canvas.winfo_width()
        h = 8
        self.timer_canvas.delete("all")
        ratio = self.time_left / 30
        fill_w = int(w * ratio)
        color = (THEME["success_light"] if ratio > 0.5
                 else THEME["accent_amber"] if ratio > 0.25
                 else THEME["danger_light"])
        self.timer_canvas.create_rectangle(0, 0, fill_w, h, fill=color, outline="")

    def _time_up(self):
        if self.answered:
            return
        self.answered = True
        q = self.questions[self.q_index]
        correct_orig = q["answer"]

        # Highlight correct answer green, rest red
        for pos in range(4):
            orig = self._option_map[pos]
            if orig == correct_orig:
                self.opt_btns[pos].config(bg=THEME["success"], fg="#fff")
            else:
                self.opt_btns[pos].config(bg=THEME["bg_card_alt"],
                                           fg=THEME["text_secondary"],
                                           state="disabled")

        self.streak = 0
        self.streak_lbl.config(text=f"🔥 {self.streak}")
        self.explain_lbl.config(
            text=f"⏰ Time's up!  {q['explanation']}",
            fg=THEME["danger_light"])

        self.answer_record.append({
            "q": q, "chosen": -1,
            "correct": correct_orig, "got_right": False
        })
        self.next_btn.pack(pady=8)

    # ── ANSWERING ─────────────────────────────────────────────────────────
    def _choose(self, display_pos):
        if self.answered or display_pos in self.eliminated:
            return
        self.answered = True
        self.timer_running = False

        q = self.questions[self.q_index]
        chosen_orig = self._option_map[display_pos]
        correct_orig = q["answer"]

        # Find display pos of correct answer
        correct_display = next(p for p, o in self._option_map.items()
                               if o == correct_orig)

        if chosen_orig == correct_orig:
            # Correct
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            pts = 100 + (self.streak - 1) * 30 + self.time_left * 2
            self.score += pts
            self.correct_count += 1
            self.opt_btns[display_pos].config(bg=THEME["success"], fg="#fff")
            self.explain_lbl.config(
                text=f"✅  +{pts} pts  |  {q['explanation']}",
                fg=THEME["success_light"])
        else:
            # Wrong
            self.streak = 0
            self.opt_btns[display_pos].config(bg=THEME["danger"], fg="#fff")
            self.opt_btns[correct_display].config(bg=THEME["success"], fg="#fff")
            self.explain_lbl.config(
                text=f"❌  Wrong!  {q['explanation']}",
                fg=THEME["danger_light"])

        # Disable all buttons
        for btn in self.opt_btns:
            btn.config(state="disabled")

        self.score_lbl.config(text=f"SCORE  {self.score}")
        self.streak_lbl.config(text=f"🔥 {self.streak}")

        self.answer_record.append({
            "q": q, "chosen": chosen_orig,
            "correct": correct_orig,
            "got_right": chosen_orig == correct_orig
        })
        self.next_btn.pack(pady=8)

    # ── NEXT ──────────────────────────────────────────────────────────────
    def _next_question(self):
        self.q_index += 1
        self._load_question()

    # ── LIFELINES ─────────────────────────────────────────────────────────
    def _lifeline_fifty(self):
        if not self.lifelines["fifty_fifty"] or self.answered:
            return
        self.lifelines["fifty_fifty"] = False
        self.btn_fifty.config(state="disabled",
                               bg=THEME["bg_card_alt"], fg=THEME["text_secondary"])

        q = self.questions[self.q_index]
        correct_orig = q["answer"]

        # Collect wrong display positions
        wrong_positions = [p for p, o in self._option_map.items()
                           if o != correct_orig and p not in self.eliminated]
        remove = random.sample(wrong_positions, min(2, len(wrong_positions)))

        for pos in remove:
            self.eliminated.append(pos)
            self.opt_btns[pos].config(
                text="", bg=THEME["bg_dark"], state="disabled")

    def _lifeline_freeze(self):
        if not self.lifelines["freeze"] or self.answered:
            return
        self.lifelines["freeze"] = False
        self.btn_freeze.config(state="disabled",
                                bg=THEME["bg_card_alt"], fg=THEME["text_secondary"])
        self.time_left = min(self.time_left + 15, 30)

    def _lifeline_skip(self):
        if not self.lifelines["skip"] or self.answered:
            return
        self.lifelines["skip"] = False
        self.btn_skip.config(state="disabled",
                              bg=THEME["bg_card_alt"], fg=THEME["text_secondary"])
        self.timer_running = False
        self.answer_record.append({
            "q": self.questions[self.q_index],
            "chosen": -2, "correct": self.questions[self.q_index]["answer"],
            "got_right": False
        })
        self.q_index += 1
        self._load_question()

    # ── RESULTS ───────────────────────────────────────────────────────────
    def _show_results(self):
        self.timer_running = False

        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.config(bg=THEME["bg_dark"])

        canvas = tk.Canvas(self.root, bg=THEME["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=THEME["bg_dark"])

        frame.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _scroll)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        pct = round(self.correct_count / len(self.questions) * 100)
        grade = ("🏆 EXCELLENT!" if pct >= 90 else
                 "🌟 GREAT!"     if pct >= 70 else
                 "👍 GOOD"       if pct >= 50 else
                 "📚 KEEP STUDYING")

        # Title
        tk.Label(frame, text=grade,
                 font=("Helvetica", 22, "bold"),
                 bg=THEME["bg_dark"], fg=THEME["accent_cyan"]).pack(pady=(28, 4))

        tk.Label(frame, text="Quiz Complete!",
                 font=("Helvetica", 14),
                 bg=THEME["bg_dark"], fg=THEME["text_secondary"]).pack()

        # Score box
        sbox = tk.Frame(frame, bg=THEME["bg_card"], padx=30, pady=20)
        sbox.pack(pady=18, padx=40, fill="x")

        stats = [
            ("Final Score",   str(self.score),                     THEME["gold"]),
            ("Correct",       f"{self.correct_count} / {len(self.questions)}", THEME["success_light"]),
            ("Accuracy",      f"{pct}%",                            THEME["accent_cyan"]),
            ("Best Streak",   f"🔥 {self.best_streak}",             THEME["accent_amber"]),
        ]
        for label, val, color in stats:
            row = tk.Frame(sbox, bg=THEME["bg_card"])
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label,
                     font=("Helvetica", 12),
                     bg=THEME["bg_card"], fg=THEME["text_secondary"],
                     width=16, anchor="w").pack(side="left")
            tk.Label(row, text=val,
                     font=("Helvetica", 13, "bold"),
                     bg=THEME["bg_card"], fg=color).pack(side="left")

        # Per-question review
        tk.Label(frame, text="─── Question Review ───",
                 font=("Helvetica", 12, "bold"),
                 bg=THEME["bg_dark"], fg=THEME["text_secondary"]).pack(pady=(10, 6))

        for i, rec in enumerate(self.answer_record):
            q = rec["q"]
            ok = rec["got_right"]
            icon = "✅" if ok else "❌"
            bg = THEME["bg_card"] if i % 2 == 0 else THEME["bg_card_alt"]

            rcard = tk.Frame(frame, bg=bg, padx=14, pady=8)
            rcard.pack(fill="x", padx=20, pady=2)

            tk.Label(rcard,
                     text=f"{icon}  Q{i+1}. {q['question']}",
                     font=("Helvetica", 11, "bold"),
                     bg=bg, fg=THEME["text_primary"],
                     wraplength=700, justify="left", anchor="w").pack(fill="x")

            answer_text = q["options"][q["answer"]]
            tk.Label(rcard,
                     text=f"     Correct: {answer_text}",
                     font=("Helvetica", 10),
                     bg=bg, fg=THEME["success_light"],
                     wraplength=700, justify="left", anchor="w").pack(fill="x")

        # Play again
        btn_row = tk.Frame(frame, bg=THEME["bg_dark"])
        btn_row.pack(pady=22)

        tk.Button(btn_row, text="🔄 Play Again",
                  font=("Helvetica", 12, "bold"),
                  bg=THEME["accent_cyan"], fg="#000",
                  relief="flat", bd=0, padx=22, pady=10,
                  cursor="hand2",
                  command=self._restart).pack(side="left", padx=8)

        tk.Button(btn_row, text="✖ Quit",
                  font=("Helvetica", 12, "bold"),
                  bg=THEME["bg_card_alt"], fg=THEME["text_primary"],
                  relief="flat", bd=0, padx=22, pady=10,
                  cursor="hand2",
                  command=self.root.destroy).pack(side="left", padx=8)

    def _restart(self):
        random.shuffle(self.all_questions)
        self.questions = self.all_questions[:20]
        self.q_index = 0
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.correct_count = 0
        self.lifelines = {"fifty_fifty": True, "freeze": True, "skip": True}
        self.answer_record = []

        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()
        self._load_question()


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GeneralQuizApp(root)
    root.mainloop()

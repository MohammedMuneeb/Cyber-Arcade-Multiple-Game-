import tkinter as tk 
from tkinter import messagebox 

import subprocess 
import sys 
import os 

# Import game classes from local modules 
try: 
    from tkttoe import TicTacToeGUI 
    from rockpaperscissor import RockPaperScissorsApp 
    from sudoko import SudokuGUI 

except ImportError as e : 
    messagebox.showerror("Import Error", f"Could not load game modules: {e }") 
class GameLauncherApp : 

    def __init__(self , root ): 
        self.root = root 
        self.root.title("Python Mini Games Arcade")
        self.root.geometry("680x740")
        self.root.minsize(640, 600)

        self.root.config(bg="#1e1e2f") 
        self.active_game_window = None 
        self.create_main_menu () 

    def create_main_menu (self ): 
        # Header Section
        header_frame = tk.Frame(self.root, bg="#1e1e2f")
        header_frame.pack(pady =(20, 10))  
        title_label = tk .Label ( 

            header_frame, 
            text="🎮 GAME ARCADE 🎮", 
            font=("Helvetica", 24, "bold"), 
            bg="#1e1e2f", 
            fg="#00d2ff" 
        ) 
        title_label.pack () 

        subtitle_label = tk.Label ( 
 
            header_frame, 
            text="Select a game to start playing", 
            font=("Helvetica", 13, "italic"),
            bg="#1e1e2f",
            fg="#a0a0c0"
        )
        subtitle_label.pack(pady=4)

        # Scrollable Games Container
        container = tk.Frame(self.root, bg="#1e1e2f")
        container.pack(fill="both", expand=True, padx=25, pady=(5, 10))

        canvas = tk.Canvas(container, bg="#1e1e2f", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2f")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mousewheel scroll binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Game Options Definition
        games = [
            {
                "title": "Tic-Tac-Toe",
                "emoji": "❌⭕",
                "tag": "Tkinter",
                "desc": "Play vs AI or 2-Player mode",
                "color": "#00d2ff",
                "launch": self.launch_tictactoe
            },
            {
                "title": "Rock Paper Scissors",
                "emoji": "✊✋✌️",
                "tag": "Tkinter",
                "desc": "Classic hand game vs Computer",
                "color": "#ff5555",
                "launch": self.launch_rps
            },
            {
                "title": "Sudoku Master",
                "emoji": "🧩",
                "tag": "Tkinter",
                "desc": "9x9 Grid with Easy, Medium, Hard",
                "color": "#2ecc71",
                "launch": self.launch_sudoku
            },
            {
                "title": "Crack The Code",
                "emoji": "🔐🔢",
                "tag": "Pygame",
                "desc": "Cyberpunk vault breaker digit-matching puzzle",
                "color": "#bd00ff",
                "launch": self.launch_crack_the_code
            },
            {
                "title": "Asteroids Odyssey",
                "emoji": "🚀☄️",
                "tag": "Pygame",
                "desc": "Classic space combat & asteroid blasting",
                "color": "#00e5ff",
                "launch": self.launch_asteroids
            },
            {
                "title": "Python Master Quiz",
                "emoji": "🧠🐍",
                "tag": "Tkinter",
                "desc": "Interactive trivia, lifelines & code challenges",
                "color": "#3fb950",
                "launch": self.launch_quiz
            },
            {
                "title": "Shooting Club",
                "emoji": "🎯🔫",
                "tag": "Pygame",
                "desc": "Tactical range with 4 weapons & 4 modes",
                "color": "#ffaa00",
                "launch": self.launch_shooting_club
            },
            {
                "title": "Tetris Classic",
                "emoji": "🧱🕹️",
                "tag": "Pygame",
                "desc": "Classic falling block puzzle arcade",
                "color": "#f1c40f",

                "launch": self.launch_tetris 
            }, 
            { 
                "title": "General Knowledge Quiz",
                "emoji": "🌍🧠",
                "tag": "Tkinter",
                "desc": "50+ questions: Science, History, Geography, Sports, Movies & Music",
                "color": "#00d2ff",
                "launch": self.launch_general_quiz

            } 
        ] 
        # Render Game Cards 
        for game in games: 
            card = tk.Frame(scrollable_frame, bg="#2d2d44", bd=2, relief="groove")
            card.pack(pady=7, fill="x", padx=6)

            # Left Info Frame
            info_frame = tk.Frame(card, bg="#2d2d44") 

            info_frame.pack(side="left", padx=15, pady=10) 
            title_row = tk.Frame(info_frame, bg="#2d2d44") 
            title_row.pack(anchor="w") 

            game_title = tk.Label ( 
                title_row, 
                text=f"{game['emoji']}  {game['title']}",
                font=("Helvetica", 13, "bold"),
                bg="#2d2d44",

                fg=game["color"] 
            ) 
            game_title.pack(side="left") 

            tag_badge = tk.Label(
                title_row,
                text=f" {game['tag']} ",
                font=("Helvetica", 8, "bold"),
                bg="#1e1e2f",
                fg="#a0a0c0",
                bd=1,

                relief="solid"
            )
            tag_badge.pack(side="left", padx =8 ) 
            game_desc = tk.Label( 
                info_frame , 
                text=game["desc"], 
                font=("Helvetica", 9),
                bg="#2d2d44",
                fg="#d0d0e0"

            ) 
            game_desc.pack(anchor="w", pady=(2, 0))

            # Right Launch Button
            play_btn = tk.Button(
                card,
                text="Play Now ▶",
                font=("Helvetica", 10, "bold"),
                bg=game["color"],
                fg="#000000" if game["color"] in ["#00d2ff", "#2ecc71", "#00e5ff", "#f1c40f", "#3fb950"] else "#ffffff",
                activebackground="#ffffff",
                activeforeground="#000000",
                width=11,
                bd=0,
                cursor="hand2",
                command=game["launch"]
            )
            play_btn.pack(side="right", padx=15, pady=10)

        # Footer
        footer_label = tk.Label(
            self.root,
            text="Built with Python, Tkinter & Pygame",
            font=("Helvetica", 9),
            bg="#1e1e2f",
            fg="#606080"
        )
        footer_label.pack(side="bottom", pady=10)

    def open_game_window(self, title, geometry):
        """Creates a dedicated Toplevel window for the chosen game."""
        game_win = tk.Toplevel(self.root)
        game_win.title(title)
        game_win.geometry(geometry)
        game_win.config(bg="#1e1e2f")
        game_win.resizable(False, False)
        # Bring new window to focus
        game_win.focus_force()
        return game_win

    def launch_tictactoe(self):
        win = self.open_game_window("Ultimate Tic-Tac-Toe", "480x600")
        TicTacToeGUI(win)

    def launch_rps(self):
        win = self.open_game_window("Ultimate Rock Paper Scissors", "600x550")
        RockPaperScissorsApp(win)

    def launch_sudoku(self):
        win = self.open_game_window("Advanced Sudoku Puzzle", "620x720")
        SudokuGUI(win)

    def launch_shooting_club(self):
        script = os.path.join(os.path.dirname(__file__), "shooting_club.py")
        subprocess.Popen([sys.executable, script])

    def launch_crack_the_code(self):
        script = os.path.join(os.path.dirname(__file__), "crack_the_code.py")
        subprocess.Popen([sys.executable, script])

    def launch_asteroids(self):
        script = os.path.join(os.path.dirname(__file__), "asteriod.py")
        subprocess.Popen([sys.executable, script])

    def launch_quiz(self):
        script = os.path.join(os.path.dirname(__file__), "python_quiz.py")
        subprocess.Popen([sys.executable, script])

    def launch_tetris(self):
        script = os.path.join(os.path.dirname(__file__), "tetris.py")
        subprocess.Popen([sys.executable, script])

    def launch_general_quiz(self):
        script = os.path.join(os.path.dirname(__file__), "general_quiz.py")
        subprocess.Popen([sys.executable, script])

if __name__ == "__main__": 
    root = tk.Tk() 
    app = GameLauncherApp(root)
    root.mainloop()
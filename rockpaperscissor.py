import tkinter as tk 
from tkinter import messagebox 

import random 
class RockPaperScissorsApp : 
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Rock Paper Scissors")
        self.root.geometry("600x550")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        # Game state variables
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0

        # Mapping choices to emoji representations
        self.choices = {
            "Rock": "✊",
            "Paper": "✋",
            "Scissors": "✌️"
        }

        self.create_widgets()

    def create_widgets(self):
        # Title Banner
        title_label = tk.Label(
            self.root, 
            text="ROCK • PAPER • SCISSORS", 
            font=("Helvetica", 20, "bold"), 
            bg="#1e1e2f", 
            fg="#00d2ff"
        )
        title_label.pack(pady=20)

        # Scoreboard Frame
        score_frame = tk.Frame(self.root, bg="#2d2d44", bd=2, relief="groove")
        score_frame.pack(pady=10, padx=20, fill="x")

        self.score_label = tk.Label(
            score_frame, 
            text="Score — You: 0 | Computer: 0 | Ties: 0", 
            font=("Helvetica", 12, "bold"), 
            bg="#2d2d44", 
            fg="#ffffff"
        )
        self.score_label.pack(pady=10)

        # Arena Display (User Choice vs Computer Choice)
        arena_frame = tk.Frame(self.root, bg="#1e1e2f")
        arena_frame.pack(pady=20)

        # Player Choice Display
        self.user_display = tk.Label(
            arena_frame, 
            text="👤\n---", 
            font=("Helvetica", 16), 
            bg="#2d2d44", 
            fg="#00d2ff",
            width=12, 
            height=5,
            relief="ridge"
        )
        self.user_display.grid(row=0, column=0, padx=20)

        vs_label = tk.Label(
            arena_frame, 
            text="VS", 
            font=("Helvetica", 16, "bold"), 
            bg="#1e1e2f", 
            fg="#ff5555"
        )
        vs_label.grid(row=0, column=1, padx=10)

        # Computer Choice Display
        self.comp_display = tk.Label(
            arena_frame, 
            text="💻\n---", 
            font=("Helvetica", 16), 
            bg="#2d2d44", 
            fg="#ff5555",
            width=12, 
            height=5,
            relief="ridge"
        )
        self.comp_display.grid(row=0, column=2, padx=20)

        # Result Announcement Label
        self.result_label = tk.Label(
            self.root, 
            text="Make your move below!", 
            font=("Helvetica", 14, "italic"), 
            bg="#1e1e2f", 
            fg="#f1f1f1"
        )
        self.result_label.pack(pady=10)

        # Action Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=15)

        # Create styled buttons for each choice 
        for choice, emoji in self.choices.items ():
            btn = tk .Button ( 
                btn_frame, 
                text=f"{emoji}\n{choice}", 
                font=("Helvetica", 12, "bold"),
                bg="#3a3a5e", 
                fg="#ffffff", 
                activebackground="#00d2ff",

                activeforeground="#000000", 
                width =10, 
                height =3, 
                command =lambda c=choice: self.play_round(c)
            ) 
            btn.pack(side="left", padx=10)

        # Reset Stats Button
        reset_btn = tk.Button ( 

            self .root , 
            text ="Reset Game Stats", 
            font =("Helvetica", 10), 
            bg ="#ff5555", 
            fg="#ffffff", 
            command=self.reset_game 
        ) 
        reset_btn.pack (pady =5 ) 
    def play_round (self, user_choice ): 

        computer_choice = random.choice(list(self.choices.keys())) 
        # Update visual indicators with emojis 
        self.user_display.config(text=f"You\n{self.choices[user_choice]}\n{user_choice }") 
        self.comp_display.config(text=f"Computer\n{self.choices[computer_choice]}\n{computer_choice }") 

        # Determine winner
        if user_choice == computer_choice:
            self.ties += 1
            result_text = "It's a Tie!"
            result_color = "#f1c40f" # Yellow
        elif (
            (user_choice == "Rock" and computer_choice == "Scissors") or
            (user_choice == "Paper" and computer_choice == "Rock") or
            (user_choice == "Scissors" and computer_choice == "Paper")
        ):
            self.user_score += 1
            result_text = f"You Win! {user_choice} beats {computer_choice}"
            result_color = "#2ecc71" # Green
        else:
            self.computer_score += 1
            result_text = f"Computer Wins! {computer_choice} beats {user_choice}"
            result_color = "#e74c3c" # Red

        # Update scoreboard labels
        self.score_label.config(
            text=f"Score — You: {self.user_score} | Computer: {self.computer_score} | Ties: {self.ties}"
        )
        self.result_label.config(text=result_text, fg=result_color)

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.score_label.config(
            text=f"Score — You: {self.user_score} | Computer: {self.computer_score} | Ties: {self.ties}"
        )
        self.user_display.config(text="👤\n---")
        self.comp_display.config(text="💻\n---")
        self.result_label.config(text="Scores reset. Make your move!", fg="#f1f1f1")

if __name__ == "__main__": 
    root = tk.Tk() 
    app = RockPaperScissorsApp(root)
    root.mainloop () 
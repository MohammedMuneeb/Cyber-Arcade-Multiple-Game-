import tkinter as tk 
from tkinter import messagebox 

import random 
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic-Tac-Toe")
        self.root.geometry("480x600")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        # Game mode: "PvP" (Player vs Player) or "AI" (Player vs Computer)
        self.game_mode = "AI"
        
        # Scores
        self.score_x = 0
        self.score_o = 0
        self.ties = 0

        # Board state and current turn ('X' always starts)
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="TIC • TAC • TOE",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e2f",
            fg="#00d2ff"
        )
        title_label.pack(pady=15)

        # Mode Selection Frame
        mode_frame = tk.Frame(self.root, bg="#1e1e2f")
        mode_frame.pack(pady=5)

        self.pvp_btn = tk.Button(
            mode_frame, text="2 Player", font=("Helvetica", 9, "bold"),
            bg="#3a3a5e", fg="#ffffff", width=10, command=lambda: self.set_mode("PvP")
        )
        self.pvp_btn.grid(row=0, column=0, padx=5)

        self.ai_btn = tk.Button(
            mode_frame, text="vs AI", font=("Helvetica", 9, "bold"),
            bg="#00d2ff", fg="#000000", width=10, command=lambda: self.set_mode("AI")
        )
        self.ai_btn.grid(row=0, column=1, padx=5)

        # Scoreboard Card
        score_frame = tk.Frame(self.root, bg="#2d2d44", bd=2, relief="groove")
        score_frame.pack(pady=10, padx=20, fill="x")

        self.score_label = tk.Label(
            score_frame,
            text="Score — X: 0 | O: 0 | Ties: 0",
            font=("Helvetica", 11, "bold"),
            bg="#2d2d44",
            fg="#ffffff"
        )
        self.score_label.pack(pady=8)

        # Status / Turn Indicator
        self.status_label = tk.Label(
            self.root,
            text="Player X's Turn",
            font=("Helvetica", 12, "italic"),
            bg="#1e1e2f",
            fg="#2ecc71"
        )
        self.status_label.pack(pady=5)

        grid_outer = tk.Frame(self.root, bg="#00d2ff", bd=3, relief="solid")
        grid_outer.pack(pady=15)

        self.grid_frame = tk.Frame(grid_outer, bg="#1e1e2f")
        self.grid_frame.pack()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    font=("Helvetica", 24, "bold"),
                    bg="#2d2d44",
                    fg="#ffffff",
                    activebackground="#3a3a5e",
                    activeforeground="#ffffff",
                    width=4,
                    height=2,
                    bd=0,
                    command=lambda row=r, col=c: self.on_cell_click(row, col)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[r][c] = btn

        # Action Buttons (Reset)
        action_frame = tk.Frame(self.root, bg="#1e1e2f")
        action_frame.pack(pady=10)

        reset_btn = tk.Button(
            action_frame,
            text="Reset Game",
            font=("Helvetica", 10, "bold"),
            bg="#ff5555",
            fg="#ffffff",
            width=12,
            command=self.reset_board
        )
        reset_btn.pack()

    def set_mode(self, mode):
        self.game_mode = mode
        if mode == "PvP":
            self.pvp_btn.config(bg="#00d2ff", fg="#000000")
            self.ai_btn.config(bg="#3a3a5e", fg="#ffffff")
        else:
            self.ai_btn.config(bg="#00d2ff", fg="#000000")
            self.pvp_btn.config(bg="#3a3a5e", fg="#ffffff")
        self.reset_board()

    def on_cell_click(self, r, c):
        if not self.game_active or self.board[r][c] != "":
            return

        # Player move
        self.make_move(r, c, self.current_player)

        if self.check_win(self.current_player):
            self.end_game(f"🎉 Player {self.current_player} Wins!")
            return
        elif self.is_board_full():
            self.end_game("🤝 It's a Tie!")
            return

        # Switch turn
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status()

        # If AI mode and it's O's turn, trigger computer move
        if self.game_mode == "AI" and self.current_player == "O" and self.game_active:
            self.root.after(400, self.ai_move)

    def make_move(self, r, c, player):
        self.board[r][c] = player
        color = "#00d2ff" if player == "X" else "#ff5555"
        self.buttons[r][c].config(text=player, fg=color)

    def ai_move(self):
        if not self.game_active:
            return

        # 1. Check if AI can win in the next move
        move = self.find_best_move("O")
        # 2. Block player if player is about to win
        if not move:
            move = self.find_best_move("X")
        # 3. Take center if available
        if not move and self.board[1][1] == "":
            move = (1, 1)
        # 4. Otherwise pick a random available spot
        if not move:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
            if empty_cells:
                move = random.choice(empty_cells)

        if move:
            r, c = move
            self.make_move(r, c, "O")
            if self.check_win("O"):
                self.end_game("🤖 AI Wins!")
                return
            elif self.is_board_full():
                self.end_game("🤝 It's a Tie!")
                return

            self.current_player = "X"
            self.update_status()

    def find_best_move(self, player):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = player
                    won = self.check_win(player)
                    self.board[r][c] = ""
                    if won:
                        return (r, c)
        return None

    def check_win(self, p):
        b = self.board
        # Rows & Columns
        for i in range(3):
            if b[i][0] == p and b[i][1] == p and b[i][2] == p:
                return True
            if b[0][i] == p and b[1][i] == p and b[2][i] == p:
                return True
        # Diagonals
        if b[0][0] == p and b[1][1] == p and b[2][2] == p:
            return True
        if b[0][2] == p and b[1][1] == p and b[2][0] == p:
            return True
        return False

    def is_board_full(self):
        return all(self.board[r][c] != "" for r in range(3) for c in range(3))

    def update_status(self):
        if self.current_player == "X":
            self.status_label.config(text="Player X's Turn", fg="#2ecc71")
        else:
            self.status_label.config(text="Player O's Turn (AI)" if self.game_mode == "AI" else "Player O's Turn", fg="#ff5555")

    def end_game(self, message):
        self.game_active = False
        if "X" in message:
            self.score_x += 1
        elif "O" in message or "AI" in message:
            self.score_o += 1
        else:
            self.ties += 1

        self.score_label.config(text=f"Score — X: {self.score_x} | O: {self.score_y if hasattr(self, 'score_y') else self.score_o} | Ties: {self.ties}")
        # Fix label text format
        self.score_label.config(text=f"Score — X: {self.score_x} | O: {self.score_o} | Ties: {self.ties}")
        self.status_label.config(text=message, fg="#f1c40f")
        messagebox.showinfo("Game Over", message)

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        self.update_status()
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", fg="#ffffff")

if __name__ == "__main__":
    root = tk.Tk () 
    app = TicTacToeGUI (root ) 
    root.mainloop () 
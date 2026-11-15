# import random 
# import os 

# class SudokuBoard : 
#     def __init__(self , size =9 ): 
#         """Initializes a 9x9 Sudoku board with empty cells."""
#         self.size = size
#         self.board = [[0 for _ in range(size)] for _ in range(size)]
#         self.solution = [[0 for _ in range(size)] for _ in range(size)]

#     def print_board(self, board_to_print):
#         """Renders the Sudoku grid cleanly with 3x3 block separators in the terminal."""
#         os.system('cls' if os.name == 'nt' else 'clear')
#         print("\n  =================================")
#         print("         PYTHON SUDOKU PUZZLE      ")
#         print("  =================================\n")
#         print("     1   2   3     4   5   6     7   8   9")
#         print("   +-----------+-----------+-----------+")
        
#         for i in range(self.size):
#             row_str = f" {i+1} |"
#             for j in range(self.size):
#                 val = board_to_print[i][j]
#                 cell = str(val) if val != 0 else "."
#                 row_str += f" {cell} "
#                 if (j + 1) % 3 == 0:
#                     row_str += "|"
#             print(row_str)
#             if (i + 1) % 3 == 0 and i < self.size - 1:
#                 print("   +-----------+-----------+-----------+")
#         print("   +-----------+-----------+-----------+\n")

#     def is_valid(self, board, row, col, num):
#         """Checks if placing 'num' at board[row][col] is valid according to Sudoku rules."""
#         # Check row
#         if num in board[row]:
#             return False

#         # Check column
#         if num in [board[r][col] for r in range(self.size)]:
#             return False

#         # Check 3x3 subgrid
#         start_row, start_col = 3 * (row // 3), 3 * (col // 3)
#         for r in range(start_row, start_row + 3):
#             for c in range(start_col, start_col + 3):
#                 if board[r][c] == num:
#                     return False

#         return True

#     def solve(self, board):
#         """Solves the Sudoku puzzle using backtracking recursion."""
#         for row in range(self.size):
#             for col in range(self.size):
#                 if board[row][col] == 0:
#                     numbers = list(range(1, 10))
#                     random.shuffle(numbers)  # Randomize for unique puzzle generation
#                     for num in numbers:
#                         if self.is_valid(board, row, col, num):
#                             board[row][col] = num
#                             if self.solve(board):
#                                 return True
#                             board[row][col] = 0
#                     return False
#         return True

#     def generate_puzzle(self, difficulty=35):
#         """Generates a complete solved board and removes numbers to create the puzzle."""
#         # Step 1: Fill the diagonal boxes first to seed randomness quickly
#         for i in range(0, self.size, 3):
#             nums = list(range(1, 10))
#             random.shuffle(nums)
#             for r in range(3):
#                 for c in range(3):
#                     self.solution[i + r][i + c] = nums.pop()

#         # Step 2: Solve the rest of the board to get a valid full solution
#         self.solve(self.solution)

#         # Step 3: Copy solution to current board
#         for r in range(self.size):
#             for c in range(self.size):
#                 self.board[r][c] = self.solution[r][c]

#         # Step 4: Remove numbers based on difficulty level (cells to clear)
#         cells_to_remove = 81 - difficulty
#         removed = 0
#         while removed < cells_to_remove:
#             row = random.randint(0, 8)
#             col = random.randint(0, 8)
#             if self.board[row][col] != 0:
#                 self.board[row][col] = 0
#                 removed += 1

# def play_sudoku():
#     """Main game execution loop handling user moves and win conditions."""
#     game = SudokuBoard()
    
#     print("Select Difficulty:")
#     print("1. Easy (45 clues)")
#     print("2. Medium (35 clues)")
#     print("3. Hard (25 clues)")
    
#     choice = input("Enter choice (1-3, default 2): ").strip()
#     clues = 35
#     if choice == '1':
#         clues = 45
#     elif choice == '3':
#         clues = 25

#     game.generate_puzzle(difficulty=clues)
    
#     # Keep track of original puzzle cells so the user cannot overwrite starting clues
#     original_board = [[game.board[r][c] for c in range(9)] for r in range(9)]

#     while True:
#         game.print_board(game.board)

#         # Check if the board is completely filled and correct
#         if game.board == game.solution:
#             print("🎉 CONGRATULATIONS! You successfully solved the Sudoku puzzle! 🎉\n")
#             break

#         print("Commands: Enter [Row] [Col] [Num] (e.g., '2 4 7') | Type 'solve' to reveal answer | Type 'quit' to exit")
#         user_input = input("Your move: ").strip().lower()

#         if user_input == 'quit':
#             print("Thanks for playing!")
#             break
        
#         if user_input == 'solve':
#             game.board = [row[:] for row in game.solution]
#             game.print_board(game.board)
#             print("Puzzle solved by AI solver!\n")
#             break

#         parts = user_input.split()
#         if len(parts) != 3 or not all(p.isdigit() for p in parts):
#             input("❌ Invalid input format! Please enter Row Col Num (1-9). Press Enter to continue...")
#             continue

#         row, col, num = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])

#         if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
#             input("❌ Numbers must be between 1 and 9! Press Enter to continue...")
#             continue

#         if original_board[row][col] != 0:
#             input("⚠️ You cannot change original puzzle clues! Press Enter to continue...")
#             continue

#         # Check validity before applying move
#         if game.is_valid(game.board, row, col, num):
#             game.board[row][col] = num
#         else:
#             input(f"❌ Invalid move! '{num}' violates Sudoku rules in row, column, or 3x3 box. Press Enter...")

# if __name__ == "__main__": 
#     play_sudoku () 
import tkinter as tk 
from tkinter import messagebox 

import random 
import time 
class SudokuGUI : 
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sudoku Puzzle")
        self.root.geometry("620x720")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        # Game State Variables
        self.size = 9
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        
        self.selected_row = None
        self.selected_col = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        
        self.timer_seconds = 0
        self.timer_running = False
        self.difficulty_name = "Medium"

        self.create_widgets()
        self.new_game("Medium")

    def create_widgets(self):
        # Top Title & Info Bar
        title_frame = tk.Frame(self.root, bg="#1e1e2f")
        title_frame.pack(pady=10)

        title_label = tk.Label(
            title_frame, 
            text="SUDOKU MASTER", 
            font=("Helvetica", 18, "bold"), 
            bg="#1e1e2f", 
            fg="#00d2ff"
        )
        title_label.pack()

        # Status & Controls Frame (Timer & Difficulty)
        control_frame = tk.Frame(self.root, bg="#2d2d44", bd=2, relief="groove")
        control_frame.pack(pady=5, padx=20, fill="x")

        self.diff_label = tk.Label(
            control_frame, 
            text="Difficulty: Medium", 
            font=("Helvetica", 10, "bold"), 
            bg="#2d2d44", 
            fg="#ffffff"
        )
        self.diff_label.pack(side="left", padx=15, pady=8)

        self.timer_label = tk.Label(
            control_frame, 
            text="Time: 00:00", 
            font=("Helvetica", 10, "bold"), 
            bg="#2d2d44", 
            fg="#2ecc71"
        )
        self.timer_label.pack(side="right", padx=15, pady=8)

        # Sudoku Grid Frame (with 3x3 block borders)
        grid_outer_frame = tk.Frame(self.root, bg="#00d2ff", bd=3, relief="solid")
        grid_outer_frame.pack(pady=10)

        self.grid_frame = tk.Frame(grid_outer_frame, bg="#1e1e2f")
        self.grid_frame.pack()

        for r in range(9):
            for c in range(9):
                # Calculate thicker borders for 3x3 subgrids
                padx_val = (3 if c % 3 == 0 and c != 0 else 1, 1)
                pady_val = (3 if r % 3 == 0 and r != 0 else 1, 1)

                cell_frame = tk.Frame(self.grid_frame, bg="#3a3a5e", width=50, height=50)
                cell_frame.grid(row=r, column=c, padx=padx_val, pady=pady_val)
                cell_frame.grid_propagate(False)

                btn = tk.Button(
                    cell_frame,
                    text="",
                    font=("Helvetica", 14, "bold"),
                    bg="#2d2d44",
                    fg="#ffffff",
                    activebackground="#00d2ff",
                    activeforeground="#000000",
                    bd=0,
                    command=lambda row=r, col=c: self.select_cell(row, col)
                )
                btn.pack(fill="both", expand=True)
                self.cells[r][c] = btn

        # Number Keypad Frame (1-9 and Erase)
        keypad_frame = tk.Frame(self.root, bg="#1e1e2f")
        keypad_frame.pack(pady=10)

        for i in range(1, 10):
            num_btn = tk.Button(
                keypad_frame,
                text=str(i),
                font=("Helvetica", 12, "bold"),
                bg="#3a3a5e",
                fg="#00d2ff",
                width=4,
                height=1,
                command=lambda val=i: self.input_number(val)
            )
            num_btn.grid(row=0, column=i-1, padx=3)

        erase_btn = tk.Button(
            keypad_frame,
            text="Erase",
            font=("Helvetica", 10, "bold"),
            bg="#e74c3c",
            fg="#ffffff",
            width=8,
            height=1,
            command=lambda: self.input_number(0)
        )
        erase_btn.grid(row=0, column=9, padx=5)

        # Action Buttons Frame (Difficulty selection & Solver)
        action_frame = tk.Frame(self.root, bg="#1e1e2f")
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Easy", bg="#3a3a5e", fg="#ffffff", width=8, command=lambda: self.new_game("Easy")).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Medium", bg="#3a3a5e", fg="#ffffff", width=8, command=lambda: self.new_game("Medium")).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Hard", bg="#3a3a5e", fg="#ffffff", width=8, command=lambda: self.new_game("Hard")).grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Solve", bg="#f1c40f", fg="#000000", width=8, command=self.solve_board_ui).grid(row=0, column=3, padx=5)
        tk.Button(action_frame, text="Reset", bg="#ff5555", fg="#ffffff", width=8, command=self.reset_game).grid(row=0, column=4, padx=5)

    def generate_puzzle(self, clues):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]

        # Fill diagonal 3x3 boxes
        for i in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for r in range(3):
                for c in range(3):
                    self.solution[i + r][i + c] = nums.pop()

        self._solve_backtrack(self.solution)

        for r in range(9):
            for c in range(9):
                self.board[r][c] = self.solution[r][c]

        # Remove cells to create puzzle difficulty
        removed = 0
        cells_to_remove = 81 - clues
        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1

    def _is_valid(self, b, row, col, num):
        if num in b[row]:
            return False
        if num in [b[r][col] for r in range(9)]:
            return False
        start_r, start_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                if b[r][c] == num:
                    return False
        return True

    def _solve_backtrack(self, b):
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self._is_valid(b, r, c, num):
                            b[r][c] = num
                            if self._solve_backtrack(b):
                                return True
                            b[r][c] = 0
                    return False
        return True

    def new_game(self, difficulty):
        self.difficulty_name = difficulty
        self.diff_label.config(text=f"Difficulty: {difficulty}")
        
        clues = 45 if difficulty == "Easy" else (35 if difficulty == "Medium" else 25)
        self.generate_puzzle(clues)
        
        self.original_board = [[self.board[r][c] for c in range(9)] for r in range(9)]
        self.selected_row = None
        self.selected_col = None
        
        self.timer_seconds = 0
        self.timer_running = True
        
        self.update_board_ui()
        self.update_timer()

    def update_board_ui(self):
        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                btn = self.cells[r][c]
                if val != 0:
                    btn.config(text=str(val))
                    if self.original_board[r][c] != 0:
                        btn.config(fg="#00d2ff", bg="#2d2d44") # Original Clue
                    else:
                        btn.config(fg="#ffffff", bg="#2d2d44") # User input
                else:
                    btn.config(text="", bg="#2d2d44")

        if self.selected_row is not None and self.selected_col is not None:
            self.cells[self.selected_row][self.selected_col].config(bg="#4a4a75")

    def select_cell(self, r, c):
        self.selected_row = r
        self.selected_col = c
        self.update_board_ui()

    def input_number(self, num):
        if self.selected_row is None or self.selected_col is None:
            return
        r, c = self.selected_row, self.selected_col
        
        if self.original_board[r][c] != 0:
            return # Cannot modify original clues

        if num == 0:
            self.board[r][c] = 0
        else:
            # Check rule validation immediately
            if self._is_valid(self.board, r, c, num):
                self.board[r][c] = num
            else:
                self.board[r][c] = num
                self.cells[r][c].config(fg="#e74c3c") # Highlight error visually

        self.update_board_ui()
        self.check_win_condition()

    def solve_board_ui(self):
        self.board = [row[:] for row in self.solution]
        self.timer_running = False
        self.update_board_ui()
        messagebox.showinfo("Solved", "The AI solver has solved the puzzle! ") 

    def reset_game(self):
        self.board = [[self.original_board[r][c] for c in range(9)] for r in range(9)]
        self.update_board_ui()

    def check_win_condition(self):
        if self.board == self.solution:
            self.timer_running = False
            messagebox.showinfo("Victory!", f"🎉 Congratulations! You solved the Sudoku puzzle in {self.timer_label.cget('text').split(' ')[1]}!")

    def update_timer(self):
        if self.timer_running:
            self.timer_seconds += 1
            mins, secs = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
            self.root.after(1000, self.update_timer)

if __name__ == "__main__": 
    root = tk.Tk () 
    app = SudokuGUI (root ) 
    root.mainloop () 
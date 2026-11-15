"""
=============================================================================

                      PYTHON MASTER QUIZ - MODERN GUI 
=============================================================================
A modern, dark-themed interactive desktop quiz application built with Tkinter.
Features:
- Categorized question bank (Beginner, Intermediate, Advanced, Gotchas)
- Timer with visual animated gradient progress bar
- Lifelines: 50/50, +15s Time Boost, and Skip
- Streak multiplier & score calculation
- Interactive code-snippet viewer with syntax-styled monospaced display

- Instant answer feedback with thorough explanations
- Comprehensive results summary & question-by-question review
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math

# ---------------------------------------------------------------------------
# COLOR PALETTE (Modern Sleek Dark Theme)
# ---------------------------------------------------------------------------
THEME = {
    "bg_dark": "#0d1117",
    "bg_card": "#161b22",
    "bg_card_alt": "#21262d",
    "border": "#30363d",
    "text_primary": "#f0f6fc",
    "text_secondary": "#8b949e",
    "text_muted": "#58a6ff",
    "accent_cyan": "#00d2ff",
    "accent_purple": "#a371f7",
    "accent_amber": "#f0883e",
    "success": "#2ea043",
    "success_light": "#3fb950",
    "danger": "#da3633",
    "danger_light": "#f85149",
    "code_bg": "#0b0e14",
    "code_border": "#212836",
    "code_fg": "#79c0ff",
    "btn_opt_bg": "#21262d",
    "btn_opt_hover": "#30363d",
    "btn_opt_fg": "#e6edf3",
    "gold": "#d29922"
}

# ---------------------------------------------------------------------------
# QUESTION BANK (Python Concepts & Gotchas)
# ---------------------------------------------------------------------------
QUESTIONS = [
    # --- BEGINNER ---
    {
        "id": 1,
        "difficulty": "Beginner",
        "category": "Data Types",
        "question": "What is the output of the following type check?",
        "code": "print(type(5 / 2))",
        "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"],
        "answer": 1,
        "explanation": "In Python 3, the standard division operator `/` always returns a `float`, even when dividing evenly (e.g. 4 / 2 returns 2.0). Floor division `//` returns an integer."
    },
    {
        "id": 2,
        "difficulty": "Beginner",
        "category": "Strings",
        "question": "What will be printed by this negative string slice?",
        "code": "s = 'Python'\nprint(s[::-1])",
        "options": ["'P'", "'n'", "'nohtyP'", "IndexError"],
        "answer": 2,
        "explanation": "The slice syntax `[start:stop:step]` with a step of `-1` reverses the string, giving 'nohtyP'."
    },
    {
        "id": 3,
        "difficulty": "Beginner",
        "category": "Collections",
        "question": "Which of the following built-in collection types is IMMUTABLE in Python?",
        "code": None,
        "options": ["list", "set", "dict", "tuple"],
        "answer": 3,
        "explanation": "Tuples (and frozensets) are immutable. Lists, sets, and dictionaries can have their contents modified after creation."
    },
    {
        "id": 4,
        "difficulty": "Beginner",
        "category": "Control Flow",
        "question": "What is the output of this range iteration?",
        "code": "print(list(range(2, 9, 3)))",
        "options": ["[2, 5, 8]", "[2, 5, 8, 9]", "[3, 6, 9]", "[2, 3, 4, 5, 6, 7, 8]"],
        "answer": 0,
        "explanation": "`range(start, stop, step)` starts at 2 and steps by 3 (2, 5, 8). The stop value 9 is exclusive, so 9 is omitted."
    },
    {
        "id": 5,
        "difficulty": "Beginner",
        "category": "Operators",
        "question": "What is the value of the expression below?",
        "code": "result = 2 ** 3 ** 2\nprint(result)",
        "options": ["64", "512", "72", "256"],
        "answer": 1,
        "explanation": "The exponentiation operator `**` in Python binds from right to left! So `2 ** 3 ** 2` is evaluated as `2 ** (3 ** 2) = 2 ** 9 = 512`."
    },
    {
        "id": 6,
        "difficulty": "Beginner",
        "category": "Functions",
        "question": "What does a Python function return if it has no return statement?",
        "code": "def greet(name):\n    print(f'Hello {name}')\n\nx = greet('Alice')\nprint(x)",
        "options": ["0", "False", "None", "'' (Empty String)"],
        "answer": 2,
        "explanation": "In Python, any function that ends without an explicit `return` statement implicitly returns `None`."
    },
    {
        "id": 7,
        "difficulty": "Beginner",
        "category": "Booleans",
        "question": "Which of these values evaluates to `True` in a boolean context (truthy)?",
        "code": None,
        "options": ["0", "[] (Empty List)", "' ' (Single space string)", "None"],
        "answer": 2,
        "explanation": "An empty string `''` is falsy, but a string containing whitespace `' '` has length 1 and is therefore truthy!"
    },

    # --- INTERMEDIATE ---
    {
        "id": 8,
        "difficulty": "Intermediate",
        "category": "Comprehensions",
        "question": "What does this list comprehension produce?",
        "code": "matrix = [[1, 2], [3, 4]]\nflat = [x for row in matrix for x in row]\nprint(flat)",
        "options": ["[[1, 2], [3, 4]]", "[1, 2, 3, 4]", "[[1, 3], [2, 4]]", "TypeError"],
        "answer": 1,
        "explanation": "Nested loops in list comprehensions maintain their standard order: outer loop `for row in matrix` first, then inner loop `for x in row`, producing a flattened list `[1, 2, 3, 4]`."
    },
    {
        "id": 9,
        "difficulty": "Intermediate",
        "category": "Dictionaries",
        "question": "What happens when accessing a missing key with `.get()`?",
        "code": "data = {'apple': 5, 'banana': 8}\nval = data.get('orange', 0)\nprint(val)",
        "options": ["KeyError", "None", "0", "False"],
        "answer": 2,
        "explanation": "`dict.get(key, default)` returns the provided default value (here `0`) when the key does not exist, preventing a `KeyError`."
    },
    {
        "id": 10,
        "difficulty": "Intermediate",
        "category": "Equality vs Identity",
        "question": "What is the output of the comparisons below?",
        "code": "a = [1, 2, 3]\nb = [1, 2, 3]\nprint(a == b, a is b)",
        "options": ["True True", "True False", "False True", "False False"],
        "answer": 1,
        "explanation": "`==` checks for value equality (both lists have identical items, so `True`). `is` checks for object identity / memory address (distinct list instances in memory, so `False`)."
    },
    {
        "id": 11,
        "difficulty": "Intermediate",
        "category": "Variable Arguments",
        "question": "What type does `*args` unpack into inside a function?",
        "code": "def func(*args):\n    return type(args)\n\nprint(func(1, 2, 3))",
        "options": ["<class 'list'>", "<class 'tuple'>", "<class 'set'>", "<class 'generator'>"],
        "answer": 1,
        "explanation": "Positional arguments gathered with `*args` are packed into an immutable `tuple`. Keyword arguments `**kwargs` are packed into a `dict`."
    },
    {
        "id": 12,
        "difficulty": "Intermediate",
        "category": "Exceptions",
        "question": "Which block is GUARANTEED to execute whether an exception occurred or not?",
        "code": "try:\n    risky_operation()\nexcept Exception:\n    handle_error()\nelse:\n    run_if_no_error()\n# ???",
        "options": ["except", "else", "finally", "catch"],
        "answer": 2,
        "explanation": "The `finally` block always executes on completion of the try-except suite, even if an exception was raised, caught, or an unhandled exception or return occurred."
    },
    {
        "id": 13,
        "difficulty": "Intermediate",
        "category": "Copy Semantics",
        "question": "What is printed after modifying the nested list in a shallow copy?",
        "code": "import copy\noriginal = [[1, 2], [3, 4]]\nclone = copy.copy(original)\nclone[0][0] = 99\nprint(original[0][0])",
        "options": ["1", "99", "IndexError", "None"],
        "answer": 1,
        "explanation": "A shallow copy (`copy.copy` or list slice `[:]`) duplicates the outer container, but child references are shared! To clone nested objects independently, use `copy.deepcopy()`."
    },
    {
        "id": 14,
        "difficulty": "Intermediate",
        "category": "Lambda & Builtins",
        "question": "What is the output of sorting this list of tuples by the second element?",
        "code": "items = [(1, 'c'), (2, 'a'), (3, 'b')]\nitems.sort(key=lambda x: x[1])\nprint([x[0] for x in items])",
        "options": ["[1, 2, 3]", "[2, 3, 1]", "[3, 2, 1]", "[(2, 'a'), (3, 'b'), (1, 'c')]"],
        "answer": 1,
        "explanation": "Sorting by `x[1]` orders by the letters: 'a' (item 2), 'b' (item 3), 'c' (item 1). The first elements are therefore `[2, 3, 1]`."
    },

    # --- ADVANCED & GOTCHAS ---
    {
        "id": 15,
        "difficulty": "Advanced",
        "category": "Python Gotcha",
        "question": "What is the classic output of this mutable default argument gotcha?",
        "code": "def append_to(val, lst=[]):\n    lst.append(val)\n    return lst\n\nprint(append_to(1))\nprint(append_to(2))",
        "options": ["[1] then [2]", "[1] then [1, 2]", "[1] then []", "TypeError"],
        "answer": 1,
        "explanation": "Default argument expressions in Python are evaluated ONCE when the function definition is executed, NOT at each call! So `lst` reuses the same list object across successive calls."
    },
    {
        "id": 16,
        "difficulty": "Advanced",
        "category": "Closures & Scoping",
        "question": "What will this list of lambda closures print?",
        "code": "funcs = [lambda: i for i in range(3)]\nprint([f() for f in funcs])",
        "options": ["[0, 1, 2]", "[2, 2, 2]", "[3, 3, 3]", "NameError"],
        "answer": 1,
        "explanation": "Late binding gotcha! Closures look up the variable `i` at call time. When the lambdas are executed, the loop has finished and `i == 2`, so each call returns 2. Fix using `lambda i=i: i`."
    },
    {
        "id": 17,
        "difficulty": "Advanced",
        "category": "Generators",
        "question": "What does a generator function return when invoked directly?",
        "code": "def gen():\n    yield 1\n    yield 2\n\nres = gen()\nprint(type(res))",
        "options": ["<class 'int'>", "<class 'list'>", "<class 'generator'>", "<class 'iterator'>"],
        "answer": 2,
        "explanation": "Calling a function containing the `yield` keyword does not run code up to yield immediately; it instantiates and returns a generator iterator object (`<class 'generator'>`)."
    },
    {
        "id": 18,
        "difficulty": "Advanced",
        "category": "Integer Caching",
        "question": "Why does Python produce this surprising result in CPython?",
        "code": "x = 256\ny = 256\nprint(x is y)\n\na = 257\nb = 257\n# (Evaluated in separate interactive lines)\nprint(a is b)",
        "options": [
            "True True (All identical ints share IDs)",
            "True False (CPython caches small integers -5 to 256)",
            "False False (`is` never compares integers)",
            "SyntaxError"
        ],
        "answer": 1,
        "explanation": "CPython pre-allocates an array of small integer objects in the range [-5, 256]. Any integer in this range reuses the singleton reference, so `256 is 256` is `True`, whereas numbers >= 257 may create separate objects."
    },
    {
        "id": 19,
        "difficulty": "Advanced",
        "category": "OOP & Dunder",
        "question": "What is the primary difference between `__str__` and `__repr__`?",
        "code": None,
        "options": [
            "`__str__` is for developers/debugging; `__repr__` is for end users.",
            "`__str__` is informal/human-readable; `__repr__` is unambiguous/formal representation.",
            "`__str__` is deprecated in Python 3.",
            "There is no difference; they are exact aliases."
        ],
        "answer": 1,
        "explanation": "`__repr__` is meant to be unambiguous and, if possible, valid Python code to recreate the object (used by developers & REPL). `__str__` is meant to be readable and pleasant for end users."
    },
    {
        "id": 20,
        "difficulty": "Advanced",
        "category": "Decorators",
        "question": "What does the `@functools.wraps` decorator do when writing custom decorators?",
        "code": "import functools\ndef my_decorator(f):\n    @functools.wraps(f)\n    def wrapper(*args, **kwargs):\n        return f(*args, **kwargs)\n    return wrapper",
        "options": [
            "It speeds up execution via Cython compiling.",
            "It preserves the original function's `__name__`, docstring, and metadata.",
            "It automatically retries the function on error.",
            "It prevents the function from accepting keyword arguments."
        ],
        "answer": 1,
        "explanation": "Without `@functools.wraps`, the decorated function would report `wrapper` as its `__name__` and lose its original docstring. `wraps` copies over metadata like name, module, and docs."
    },
    {
        "id": 21,
        "difficulty": "Advanced",
        "category": "Scope",
        "question": "What keyword is needed to modify a variable in an enclosing (non-global) function scope?",
        "code": "def outer():\n    count = 0\n    def inner():\n        # ??? count\n        count += 1\n    inner()",
        "options": ["global", "nonlocal", "outer", "super"],
        "answer": 1,
        "explanation": "`nonlocal` binds a variable to the nearest enclosing (outer) function scope that is not global, allowing in-place rebinding."
    },
    {
        "id": 22,
        "difficulty": "Advanced",
        "category": "List vs Tuple",
        "question": "What is the output of modifying a list nested inside an immutable tuple?",
        "code": "t = (1, [10, 20], 3)\nt[1].append(30)\nprint(t)",
        "options": [
            "TypeError: 'tuple' object does not support item assignment",
            "(1, [10, 20, 30], 3)",
            "(1, [10, 20], 3, 30)",
            "ValueError"
        ],
        "answer": 1,
        "explanation": "While the tuple itself cannot be rebound to different objects, the objects it contains can still be mutable! Mutating the list inside `t` succeeds and results in `(1, [10, 20, 30], 3)`."
    },
    {
        "id": 23,
        "difficulty": "Intermediate",
        "category": "Unpacking",
        "question": "What is the value of `middle` after extended iterable unpacking?",
        "code": "first, *middle, last = [1, 2, 3, 4, 5]\nprint(middle)",
        "options": ["[2, 3, 4]", "(2, 3, 4)", "[2, 3]", "ValueError"],
        "answer": 0,
        "explanation": "Extended unpacking with `*` captures all intermediate items into a new list, resulting in `[2, 3, 4]`."
    },
    {
        "id": 24,
        "difficulty": "Advanced",
        "category": "Python Gotcha",
        "question": "What is the unexpected output of this list multiplication?",
        "code": "grid = [[0] * 2] * 2\ngrid[0][0] = 7\nprint(grid)",
        "options": ["[[7, 0], [0, 0]]", "[[7, 0], [7, 0]]", "[[7, 7], [0, 0]]", "IndexError"],
        "answer": 1,
        "explanation": "Multiplying a list containing a mutable object (`[sublist] * 2`) does NOT create independent copies; both elements point to the EXACT same list in memory! To create a 2D grid safely, use a comprehension: `[[0]*2 for _ in range(2)]`."
    },
    {
        "id": 25,
        "difficulty": "Intermediate",
        "category": "OOP & Types",
        "question": "Why is `isinstance(obj, Class)` generally preferred over `type(obj) is Class`?",
        "code": None,
        "options": [
            "`isinstance` supports inheritance and subclasses; `type` checks only exact class.",
            "`isinstance` is faster because it compiles to C.",
            "`type()` is deprecated in Python 3.10+.",
            "`isinstance` works on primitive numbers only."
        ],
        "answer": 0,
        "explanation": "`isinstance(obj, Class)` returns `True` if `obj` is an instance of `Class` OR any subclass derived from it. `type(obj) is Class` fails for subclasses, violating polymorphism."
    },
    {
        "id": 26,
        "difficulty": "Beginner",
        "category": "Strings",
        "question": "What is the output of chaining these string methods?",
        "code": "text = '  python quiz  '\nprint(text.strip().title())",
        "options": ["'  Python Quiz  '", "'Python Quiz'", "'python quiz'", "'PYTHON QUIZ'"],
        "answer": 1,
        "explanation": "`.strip()` removes leading and trailing whitespace, and `.title()` capitalizes the first character of each word, resulting in `'Python Quiz'`."
    },
    {
        "id": 27,
        "difficulty": "Intermediate",
        "category": "Built-in Functions",
        "question": "What does `zip()` do when the input iterables have unequal lengths?",
        "code": "letters = ['a', 'b', 'c', 'd']\nnums = [1, 2]\nprint(list(zip(letters, nums)))",
        "options": [
            "[('a', 1), ('b', 2), ('c', None), ('d', None)]",
            "[('a', 1), ('b', 2)]",
            "ValueError: Length mismatch",
            "[('a', 1), ('b', 2), ('c', 1), ('d', 2)]"
        ],
        "answer": 1,
        "explanation": "By default, `zip()` stops pairing elements when the shortest input iterable is exhausted. To pad missing values with None or a sentinel, use `itertools.zip_longest()`."
    },
    {
        "id": 28,
        "difficulty": "Advanced",
        "category": "Context Managers",
        "question": "Which pair of dunder methods must a class implement to support the `with` statement?",
        "code": None,
        "options": [
            "`__open__` and `__close__`",
            "`__init__` and `__del__`",
            "`__enter__` and `__exit__`",
            "`__start__` and `__stop__`"
        ],
        "answer": 2,
        "explanation": "The Context Manager protocol requires `__enter__(self)` (executed when entering the `with` block) and `__exit__(self, exc_type, exc_val, exc_tb)` (executed on exiting the block, even during exceptions)."
    },
    {
        "id": 29,
        "difficulty": "Intermediate",
        "category": "Sets",
        "question": "What does the `^` operator perform on Python sets?",
        "code": "a = {1, 2, 3}\nb = {3, 4, 5}\nprint(a ^ b)",
        "options": ["{3}", "{1, 2, 4, 5}", "{1, 2, 3, 4, 5}", "TypeError"],
        "answer": 1,
        "explanation": "The `^` operator calculates the Symmetric Difference between two sets: items in either set `a` or set `b`, but NOT in both (i.e. excludes the intersection `{3}`)."
    },
    {
        "id": 30,
        "difficulty": "Intermediate",
        "category": "Syntax & Operators",
        "question": "What is the official name and function of the `:=` operator introduced in Python 3.8?",
        "code": "if (n := len([1, 2, 3])) > 2:\n    print(f'Length is {n}')",
        "options": [
            "Walrus Operator (Assignment Expression) - assigns values inside expressions.",
            "Type Pointer - creates a memory alias.",
            "Strict Equality Operator - checks value and type.",
            "Pipeline Operator - chains functions left to right."
        ],
        "answer": 0,
        "explanation": "The `:=` operator is officially called the Assignment Expression (colloquially the Walrus Operator). It allows you to assign a value to a variable within an expression, such as inside `if` conditions or `while` loops."
    }
]

# ---------------------------------------------------------------------------
# APPLICATION CLASS
# ---------------------------------------------------------------------------
class PythonQuizApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Master Quiz // Interactive Knowledge Arena")
        self.root.geometry("880x740")
        self.root.minsize(800, 680)
        self.root.configure(bg=THEME["bg_dark"])

        # Configure styles
        self._init_styles()

        # Quiz State
        self.all_questions = QUESTIONS
        self.quiz_queue = []
        self.current_q_idx = 0
        self.current_q = None
        self.score = 0
        self.streak = 0
        self.max_streak = 0
        self.selected_difficulty = "All"
        self.mode = "Standard"  # "Standard", "Timed Blitz", "Practice"
        
        # Timing
        self.time_limit = 20  # seconds per question
        self.time_left = 20
        self.timer_running = False
        self.timer_job = None
        self.question_start_time = 0
        self.total_time_taken = 0

        # Lifelines (Available per game)
        self.lifeline_5050_used = False
        self.lifeline_time_used = False
        self.lifeline_skip_used = False

        # History tracking for post-quiz review
        self.user_history = []  # list of dicts: {q, user_choice, is_correct, time_spent}

        # Containers
        self.main_container = tk.Frame(self.root, bg=THEME["bg_dark"])
        self.main_container.pack(fill="both", expand=True)

        # Show Home Screen initially
        self.show_home_screen()

    def _init_styles(self):
        """Set up standard fonts and ttk widget styles."""
        self.font_title = ("Segoe UI", 24, "bold")
        self.font_subtitle = ("Segoe UI", 12)
        self.font_header = ("Segoe UI", 15, "bold")
        self.font_body = ("Segoe UI", 12)
        self.font_bold = ("Segoe UI", 12, "bold")
        self.font_small = ("Segoe UI", 10)
        self.font_code = ("Consolas", 11)

    def clear_container(self):
        """Remove all widgets from main container."""
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False

        for widget in self.main_container.winfo_children():
            widget.destroy()

    # =========================================================================
    # HOME / MENU SCREEN
    # =========================================================================
    def show_home_screen(self):
        self.clear_container()

        # Center card
        card = tk.Frame(self.main_container, bg=THEME["bg_card"], bd=1, relief="solid",
                        highlightbackground=THEME["border"], highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=720, height=620)

        # Header Badge
        badge = tk.Label(
            card,
            text="⚡ PYTHON KNOWLEDGE ENGINE ⚡",
            font=("Segoe UI", 10, "bold"),
            fg=THEME["accent_cyan"],
            bg=THEME["bg_card_alt"],
            padx=14,
            pady=4
        )
        badge.pack(pady=(28, 10))

        # Title
        title = tk.Label(
            card,
            text="Python Master Quiz",
            font=self.font_title,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        title.pack()

        subtitle = tk.Label(
            card,
            text="Test your knowledge on Python syntax, data structures, OOP & subtle gotchas.",
            font=self.font_subtitle,
            fg=THEME["text_secondary"],
            bg=THEME["bg_card"]
        )
        subtitle.pack(pady=(4, 25))

        # Divider
        sep = tk.Frame(card, height=1, bg=THEME["border"])
        sep.pack(fill="x", padx=40, pady=5)

        # Settings Section
        opts_frame = tk.Frame(card, bg=THEME["bg_card"])
        opts_frame.pack(fill="x", padx=40, pady=15)

        # Difficulty Selector
        diff_label = tk.Label(
            opts_frame,
            text="Select Difficulty Tier:",
            font=self.font_bold,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        diff_label.grid(row=0, column=0, sticky="w", pady=10)

        self.diff_var = tk.StringVar(value="All")
        diff_btn_frame = tk.Frame(opts_frame, bg=THEME["bg_card"])
        diff_btn_frame.grid(row=0, column=1, sticky="e", pady=10)

        for diff in ["All", "Beginner", "Intermediate", "Advanced"]:
            rb = tk.Radiobutton(
                diff_btn_frame,
                text=diff,
                value=diff,
                variable=self.diff_var,
                font=self.font_body,
                fg=THEME["text_primary"],
                bg=THEME["bg_card"],
                selectcolor=THEME["bg_card_alt"],
                activebackground=THEME["bg_card"],
                activeforeground=THEME["accent_cyan"],
                indicatoron=0,
                padx=12,
                pady=5,
                bd=1,
                relief="solid",
                highlightbackground=THEME["border"]
            )
            rb.pack(side="left", padx=4)

        # Game Mode Selector
        mode_label = tk.Label(
            opts_frame,
            text="Game Challenge Mode:",
            font=self.font_bold,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        mode_label.grid(row=1, column=0, sticky="w", pady=15)

        self.mode_var = tk.StringVar(value="Standard")
        mode_btn_frame = tk.Frame(opts_frame, bg=THEME["bg_card"])
        mode_btn_frame.grid(row=1, column=1, sticky="e", pady=15)

        modes = [
            ("Standard", "10 Qs • 20s Timer • Lifelines"),
            ("Timed Blitz", "15s Fast Countdown"),
            ("Practice", "Untimed • Study Mode")
        ]

        for m_name, _ in modes:
            rb = tk.Radiobutton(
                mode_btn_frame,
                text=m_name,
                value=m_name,
                variable=self.mode_var,
                font=self.font_body,
                fg=THEME["text_primary"],
                bg=THEME["bg_card"],
                selectcolor=THEME["bg_card_alt"],
                activebackground=THEME["bg_card"],
                activeforeground=THEME["accent_cyan"],
                indicatoron=0,
                padx=10,
                pady=5,
                bd=1,
                relief="solid",
                highlightbackground=THEME["border"]
            )
            rb.pack(side="left", padx=4)

        # Features Overview Card
        features_frame = tk.Frame(card, bg=THEME["bg_card_alt"], bd=1, relief="solid",
                                  highlightbackground=THEME["border"], highlightthickness=1)
        features_frame.pack(fill="x", padx=40, pady=10)

        f_txt = (
            "🎯  Features: Code Snippets • Lifelines (50:50, Time Boost, Skip)\n"
            "🔥  Streak Multiplier: Maintain consecutive correct answers for bonus points!\n"
            "💡  In-Depth Explanations: Master Python internals with detailed reasoning"
        )
        f_lbl = tk.Label(
            features_frame,
            text=f_txt,
            font=self.font_small,
            fg=THEME["text_secondary"],
            bg=THEME["bg_card_alt"],
            justify="left",
            pady=10,
            padx=15
        )
        f_lbl.pack(anchor="w")

        # Start Button
        start_btn = tk.Button(
            card,
            text="START QUIZ CHALLENGE ➔",
            font=("Segoe UI", 13, "bold"),
            fg="#0d1117",
            bg=THEME["accent_cyan"],
            activebackground="#38d9ff",
            activeforeground="#0d1117",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            command=self.start_quiz
        )
        start_btn.pack(pady=24)

    # =========================================================================
    # QUIZ ENGINE & GAMEPLAY
    # =========================================================================
    def start_quiz(self):
        self.selected_difficulty = self.diff_var.get()
        self.mode = self.mode_var.get()

        # Filter questions based on difficulty
        if self.selected_difficulty == "All":
            pool = list(self.all_questions)
        else:
            pool = [q for q in self.all_questions if q["difficulty"] == self.selected_difficulty]

        if not pool:
            pool = list(self.all_questions)

        random.shuffle(pool)

        # Number of questions per quiz session
        num_questions = min(10, len(pool))
        self.quiz_queue = pool[:num_questions]
        self.current_q_idx = 0
        self.score = 0
        self.streak = 0
        self.max_streak = 0
        self.total_time_taken = 0
        self.user_history = []

        # Reset Lifelines
        self.lifeline_5050_used = False
        self.lifeline_time_used = False
        self.lifeline_skip_used = False

        if self.mode == "Timed Blitz":
            self.time_limit = 15
        else:
            self.time_limit = 20

        self.render_quiz_screen()
        self.load_question()

    def render_quiz_screen(self):
        """Build the quiz dashboard interface."""
        self.clear_container()

        # Top Bar: Progress, Score, Streak, Timer
        top_bar = tk.Frame(self.main_container, bg=THEME["bg_card"], height=64,
                           bd=1, relief="solid", highlightbackground=THEME["border"], highlightthickness=1)
        top_bar.pack(fill="x", padx=16, pady=(12, 8))

        # Left Top: Question Tracker
        self.lbl_progress = tk.Label(
            top_bar,
            text=f"Question 1 of {len(self.quiz_queue)}",
            font=self.font_header,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        self.lbl_progress.pack(side="left", padx=18, pady=10)

        self.lbl_tag = tk.Label(
            top_bar,
            text="Syntax",
            font=self.font_small,
            fg=THEME["accent_cyan"],
            bg=THEME["bg_card_alt"],
            padx=10,
            pady=3
        )
        self.lbl_tag.pack(side="left", padx=5)

        # Right Top: Score & Streak
        self.lbl_streak = tk.Label(
            top_bar,
            text="🔥 Streak: 0",
            font=self.font_bold,
            fg=THEME["accent_amber"],
            bg=THEME["bg_card"]
        )
        self.lbl_streak.pack(side="right", padx=(10, 20))

        self.lbl_score = tk.Label(
            top_bar,
            text="Score: 0",
            font=self.font_header,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        self.lbl_score.pack(side="right", padx=10)

        # Timer Bar (Only for timed modes)
        if self.mode != "Practice":
            timer_container = tk.Frame(self.main_container, bg=THEME["bg_dark"], height=30)
            timer_container.pack(fill="x", padx=16, pady=(0, 6))

            self.timer_canvas = tk.Canvas(timer_container, height=10, bg=THEME["bg_card_alt"],
                                          highlightthickness=0)
            self.timer_canvas.pack(fill="x", side="left", expand=True, padx=(0, 10))

            self.lbl_timer_text = tk.Label(
                timer_container,
                text=f"⏱ {self.time_limit}s",
                font=self.font_bold,
                fg=THEME["accent_cyan"],
                bg=THEME["bg_dark"],
                width=8,
                anchor="e"
            )
            self.lbl_timer_text.pack(side="right")
        else:
            self.timer_canvas = None
            self.lbl_timer_text = None

        # Lifelines Bar
        if self.mode != "Practice":
            lifeline_frame = tk.Frame(self.main_container, bg=THEME["bg_dark"])
            lifeline_frame.pack(fill="x", padx=16, pady=(0, 6))

            ll_title = tk.Label(lifeline_frame, text="Lifelines:", font=self.font_small,
                                fg=THEME["text_secondary"], bg=THEME["bg_dark"])
            ll_title.pack(side="left", padx=(5, 10))

            self.btn_5050 = tk.Button(
                lifeline_frame, text="⚡ 50/50", font=self.font_small,
                fg=THEME["text_primary"], bg=THEME["bg_card_alt"], bd=1, relief="solid",
                highlightbackground=THEME["border"], cursor="hand2", padx=8, pady=2,
                command=self.use_lifeline_5050
            )
            self.btn_5050.pack(side="left", padx=4)

            self.btn_time = tk.Button(
                lifeline_frame, text="⏱ +15s Time", font=self.font_small,
                fg=THEME["text_primary"], bg=THEME["bg_card_alt"], bd=1, relief="solid",
                highlightbackground=THEME["border"], cursor="hand2", padx=8, pady=2,
                command=self.use_lifeline_time
            )
            self.btn_time.pack(side="left", padx=4)

            self.btn_skip = tk.Button(
                lifeline_frame, text="⏭ Skip Question", font=self.font_small,
                fg=THEME["text_primary"], bg=THEME["bg_card_alt"], bd=1, relief="solid",
                highlightbackground=THEME["border"], cursor="hand2", padx=8, pady=2,
                command=self.use_lifeline_skip
            )
            self.btn_skip.pack(side="left", padx=4)

        # Question Content Card (Scrollable / Flexible)
        self.content_card = tk.Frame(self.main_container, bg=THEME["bg_card"],
                                     bd=1, relief="solid", highlightbackground=THEME["border"],
                                     highlightthickness=1)
        self.content_card.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        # Question Text
        self.lbl_question_text = tk.Label(
            self.content_card,
            text="",
            font=self.font_header,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"],
            wraplength=780,
            justify="left",
            anchor="w"
        )
        self.lbl_question_text.pack(fill="x", padx=20, pady=(16, 8))

        # Code Snippet Box (Hidden if question has no code)
        self.code_frame = tk.Frame(
            self.content_card,
            bg=THEME["code_bg"],
            bd=1,
            relief="solid",
            highlightbackground=THEME["code_border"],
            highlightthickness=1
        )
        self.lbl_code = tk.Label(
            self.code_frame,
            text="",
            font=self.font_code,
            fg=THEME["code_fg"],
            bg=THEME["code_bg"],
            justify="left",
            anchor="w",
            padx=14,
            pady=10
        )
        self.lbl_code.pack(fill="x", anchor="w")

        # Answer Options Container
        self.options_frame = tk.Frame(self.content_card, bg=THEME["bg_card"])
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.opt_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.options_frame,
                text="",
                font=self.font_body,
                fg=THEME["btn_opt_fg"],
                bg=THEME["btn_opt_bg"],
                activebackground=THEME["btn_opt_hover"],
                activeforeground=THEME["text_primary"],
                bd=1,
                relief="solid",
                highlightbackground=THEME["border"],
                cursor="hand2",
                anchor="w",
                padx=18,
                pady=10,
                command=lambda idx=i: self.handle_answer(idx)
            )
            # Hover bindings
            btn.bind("<Enter>", lambda e, b=btn: self._on_btn_hover(b))
            btn.bind("<Leave>", lambda e, b=btn: self._on_btn_leave(b))
            btn.pack(fill="x", pady=4)
            self.opt_buttons.append(btn)

        # Feedback & Explanation Frame (Appears after answering)
        self.feedback_frame = tk.Frame(self.content_card, bg=THEME["bg_card_alt"],
                                       bd=1, relief="solid", highlightbackground=THEME["border"])
        
        self.lbl_feedback_status = tk.Label(
            self.feedback_frame,
            text="",
            font=self.font_bold,
            fg=THEME["success_light"],
            bg=THEME["bg_card_alt"],
            anchor="w"
        )
        self.lbl_feedback_status.pack(fill="x", padx=16, pady=(8, 2))

        self.lbl_feedback_exp = tk.Label(
            self.feedback_frame,
            text="",
            font=self.font_small,
            fg=THEME["text_secondary"],
            bg=THEME["bg_card_alt"],
            wraplength=760,
            justify="left",
            anchor="w"
        )
        self.lbl_feedback_exp.pack(fill="x", padx=16, pady=(0, 8))

        # Next Question Action Button
        self.btn_next = tk.Button(
            self.main_container,
            text="NEXT QUESTION ➔",
            font=self.font_bold,
            fg="#0d1117",
            bg=THEME["accent_cyan"],
            activebackground="#38d9ff",
            activeforeground="#0d1117",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=10,
            command=self.advance_question
        )
        # Initially hidden until answered

    def _on_btn_hover(self, btn):
        if btn["state"] == "normal" and btn["bg"] == THEME["btn_opt_bg"]:
            btn["bg"] = THEME["btn_opt_hover"]

    def _on_btn_leave(self, btn):
        if btn["state"] == "normal" and btn["bg"] == THEME["btn_opt_hover"]:
            btn["bg"] = THEME["btn_opt_bg"]

    def load_question(self):
        """Render the current question onto the UI."""
        if self.current_q_idx >= len(self.quiz_queue):
            self.show_results_screen()
            return

        self.current_q = self.quiz_queue[self.current_q_idx]
        self.answered = False
        self.question_start_time = time.time()

        # Update Top Tracker
        self.lbl_progress.config(text=f"Question {self.current_q_idx + 1} of {len(self.quiz_queue)}")
        self.lbl_tag.config(text=f"{self.current_q['difficulty']} • {self.current_q['category']}")
        self.lbl_score.config(text=f"Score: {self.score}")
        self.lbl_streak.config(text=f"🔥 Streak: {self.streak}")

        # Update Question Text
        self.lbl_question_text.config(text=self.current_q["question"])

        # Update Code Snippet
        if self.current_q.get("code"):
            self.lbl_code.config(text=self.current_q["code"])
            self.code_frame.pack(fill="x", padx=20, pady=(0, 10))
        else:
            self.code_frame.pack_forget()

        # Update Options
        prefixes = ["A", "B", "C", "D"]
        for i, opt in enumerate(self.current_q["options"]):
            btn = self.opt_buttons[i]
            btn.config(
                text=f"  {prefixes[i]}.   {opt}",
                state="normal",
                bg=THEME["btn_opt_bg"],
                fg=THEME["btn_opt_fg"],
                relief="solid"
            )
            btn.pack(fill="x", pady=4)

        # Hide Feedback & Next Button
        self.feedback_frame.pack_forget()
        self.btn_next.pack_forget()

        # Reset & Start Timer
        if self.mode != "Practice":
            self.time_left = self.time_limit
            self.update_timer_display()
            self.start_timer()

    # =========================================================================
    # TIMER ENGINE
    # =========================================================================
    def start_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = True
        self.run_timer_tick()

    def run_timer_tick(self):
        if not self.timer_running:
            return

        self.update_timer_display()

        if self.time_left <= 0:
            self.timer_running = False
            self.handle_time_out()
            return

        self.time_left -= 0.1
        self.timer_job = self.root.after(100, self.run_timer_tick)

    def update_timer_display(self):
        if not self.timer_canvas:
            return

        fraction = max(0.0, self.time_left / self.time_limit)
        w = self.timer_canvas.winfo_width()
        if w < 10:
            w = 700

        self.timer_canvas.delete("all")

        # Color shift: cyan -> amber -> red
        if fraction > 0.5:
            bar_color = THEME["accent_cyan"]
        elif fraction > 0.25:
            bar_color = THEME["accent_amber"]
        else:
            bar_color = THEME["danger_light"]

        bar_width = int(w * fraction)
        self.timer_canvas.create_rectangle(0, 0, bar_width, 10, fill=bar_color, width=0)

        seconds_int = max(0, int(math.ceil(self.time_left)))
        self.lbl_timer_text.config(
            text=f"⏱ {seconds_int}s",
            fg=bar_color
        )

    def handle_time_out(self):
        """Called when clock reaches 0."""
        if self.answered:
            return
        self.handle_answer(-1, timed_out=True)

    # =========================================================================
    # LIFELINES
    # =========================================================================
    def use_lifeline_5050(self):
        if self.lifeline_5050_used or self.answered:
            return
        self.lifeline_5050_used = True
        self.btn_5050.config(state="disabled", fg=THEME["text_secondary"])

        # Pick 2 wrong answers to eliminate
        correct_idx = self.current_q["answer"]
        wrong_indices = [i for i in range(4) if i != correct_idx]
        random.shuffle(wrong_indices)
        to_eliminate = wrong_indices[:2]

        for idx in to_eliminate:
            self.opt_buttons[idx].config(state="disabled", bg=THEME["bg_card"],
                                         text="  --- [Eliminated 50:50] ---",
                                         fg=THEME["text_secondary"])

    def use_lifeline_time(self):
        if self.lifeline_time_used or self.answered or self.mode == "Practice":
            return
        self.lifeline_time_used = True
        self.btn_time.config(state="disabled", fg=THEME["text_secondary"])

        # Add 15s to timer
        self.time_left = min(self.time_limit + 15, self.time_left + 15)
        self.update_timer_display()

    def use_lifeline_skip(self):
        if self.lifeline_skip_used or self.answered:
            return
        self.lifeline_skip_used = True
        self.btn_skip.config(state="disabled", fg=THEME["text_secondary"])

        # Stop timer and move to next question without score penalty
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False

        self.current_q_idx += 1
        self.load_question()

    # =========================================================================
    # ANSWER EVALUATION
    # =========================================================================
    def handle_answer(self, selected_idx: int, timed_out: bool = False):
        if self.answered:
            return

        self.answered = True
        self.timer_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        time_spent = round(time.time() - self.question_start_time, 1)
        self.total_time_taken += time_spent

        correct_idx = self.current_q["answer"]
        is_correct = (selected_idx == correct_idx)

        # Disable all option buttons
        for btn in self.opt_buttons:
            btn.config(state="disabled")

        # Visual highlights on options
        if timed_out:
            # Highlight correct answer in soft green
            self.opt_buttons[correct_idx].config(bg=THEME["success"], fg="#ffffff")
            self.lbl_feedback_status.config(
                text="⏳ Time's Up! No answer was selected in time.",
                fg=THEME["danger_light"]
            )
            self.streak = 0
        elif is_correct:
            self.opt_buttons[selected_idx].config(bg=THEME["success"], fg="#ffffff")
            
            # Streak bonus calculation
            self.streak += 1
            if self.streak > self.max_streak:
                self.max_streak = self.streak

            # Base points: 100. Time bonus up to +50. Streak bonus: +20 * streak
            time_bonus = int(max(0, (self.time_limit - time_spent) * 2.5)) if self.mode != "Practice" else 0
            streak_bonus = (self.streak - 1) * 20
            points_awarded = 100 + time_bonus + streak_bonus
            self.score += points_awarded

            bonus_text = f" (+{time_bonus}s speed, +{streak_bonus} streak)" if (time_bonus or streak_bonus) else ""
            self.lbl_feedback_status.config(
                text=f"✓ Correct! +{points_awarded} pts{bonus_text}",
                fg=THEME["success_light"]
            )
        else:
            # Selected wrong
            self.opt_buttons[selected_idx].config(bg=THEME["danger"], fg="#ffffff")
            # Highlight the true correct answer
            self.opt_buttons[correct_idx].config(bg=THEME["success"], fg="#ffffff")
            self.streak = 0
            self.lbl_feedback_status.config(
                text="✗ Incorrect! Review the correct concept below:",
                fg=THEME["danger_light"]
            )

        # Save to history for review screen
        self.user_history.append({
            "q": self.current_q,
            "selected_idx": selected_idx,
            "correct_idx": correct_idx,
            "is_correct": is_correct,
            "timed_out": timed_out,
            "time_spent": time_spent
        })

        # Update Top Labels
        self.lbl_score.config(text=f"Score: {self.score}")
        self.lbl_streak.config(text=f"🔥 Streak: {self.streak}")

        # Show Explanation
        self.lbl_feedback_exp.config(text=f"💡 Explanation: {self.current_q['explanation']}")
        self.feedback_frame.pack(fill="x", padx=20, pady=(6, 10))

        # Show Next Question Button
        if self.current_q_idx + 1 >= len(self.quiz_queue):
            self.btn_next.config(text="VIEW FINAL RESULTS ➔")
        else:
            self.btn_next.config(text="NEXT QUESTION ➔")
        self.btn_next.pack(side="bottom", pady=12)

    def advance_question(self):
        """Move forward to next question or results."""
        self.current_q_idx += 1
        self.load_question()

    # =========================================================================
    # RESULTS & REVIEW SCREEN
    # =========================================================================
    def show_results_screen(self):
        self.clear_container()

        total_questions = len(self.quiz_queue)
        correct_count = sum(1 for item in self.user_history if item["is_correct"])
        accuracy = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0

        # Rank Evaluation
        if accuracy >= 90:
            rank_title = "Python Grandmaster 🏆"
            rank_color = THEME["gold"]
            rank_desc = "Outstanding mastery of syntax, edge cases, and internals!"
        elif accuracy >= 70:
            rank_title = "Senior Pythonista 🚀"
            rank_color = THEME["accent_cyan"]
            rank_desc = "Solid conceptual foundation and strong problem-solving skills."
        elif accuracy >= 50:
            rank_title = "Intermediate Coder ⚙️"
            rank_color = THEME["accent_purple"]
            rank_desc = "Good effort! Keep exploring Python gotchas and advanced patterns."
        else:
            rank_title = "Python Apprentice 🌱"
            rank_color = THEME["accent_amber"]
            rank_desc = "A great learning opportunity! Review the detailed explanations below."

        # Main wrapper with scrollbar
        canvas = tk.Canvas(self.main_container, bg=THEME["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=THEME["bg_dark"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        # Keep frame centered/stretched
        def _on_canvas_resize(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)
        
        # Mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Center Container
        center_box = tk.Frame(scroll_frame, bg=THEME["bg_dark"])
        center_box.pack(padx=20, pady=20, fill="x")

        # Scorecard Panel
        card = tk.Frame(center_box, bg=THEME["bg_card"], bd=1, relief="solid",
                        highlightbackground=THEME["border"], highlightthickness=1)
        card.pack(fill="x", pady=(0, 20))

        # Title & Rank
        lbl_completed = tk.Label(card, text="QUIZ COMPLETE", font=self.font_small,
                                 fg=THEME["text_secondary"], bg=THEME["bg_card"])
        lbl_completed.pack(pady=(20, 4))

        lbl_rank = tk.Label(card, text=rank_title, font=self.font_title,
                            fg=rank_color, bg=THEME["bg_card"])
        lbl_rank.pack()

        lbl_desc = tk.Label(card, text=rank_desc, font=self.font_subtitle,
                            fg=THEME["text_secondary"], bg=THEME["bg_card"])
        lbl_desc.pack(pady=(2, 16))

        # Metrics Grid (4 columns)
        stats_frame = tk.Frame(card, bg=THEME["bg_card_alt"], bd=1, relief="solid",
                               highlightbackground=THEME["border"], highlightthickness=1)
        stats_frame.pack(fill="x", padx=30, pady=(0, 20))

        metrics = [
            ("FINAL SCORE", f"{self.score}", THEME["accent_cyan"]),
            ("ACCURACY", f"{accuracy}%", THEME["success_light"] if accuracy >= 60 else THEME["accent_amber"]),
            ("CORRECT ANSWERS", f"{correct_count} / {total_questions}", THEME["text_primary"]),
            ("BEST STREAK", f"🔥 {self.max_streak}", THEME["accent_amber"])
        ]

        for i, (label, val, color) in enumerate(metrics):
            box = tk.Frame(stats_frame, bg=THEME["bg_card_alt"])
            box.pack(side="left", fill="both", expand=True, padx=10, pady=14)

            tk.Label(box, text=label, font=("Segoe UI", 9, "bold"),
                     fg=THEME["text_secondary"], bg=THEME["bg_card_alt"]).pack()
            tk.Label(box, text=val, font=("Segoe UI", 18, "bold"),
                     fg=color, bg=THEME["bg_card_alt"]).pack(pady=(4, 0))

        # Actions buttons
        btn_frame = tk.Frame(card, bg=THEME["bg_card"])
        btn_frame.pack(pady=(0, 20))

        btn_retry = tk.Button(
            btn_frame,
            text="🔄 Play Again",
            font=self.font_bold,
            fg="#0d1117",
            bg=THEME["accent_cyan"],
            activebackground="#38d9ff",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.start_quiz
        )
        btn_retry.pack(side="left", padx=10)

        btn_home = tk.Button(
            btn_frame,
            text="🏠 Main Menu",
            font=self.font_bold,
            fg=THEME["text_primary"],
            bg=THEME["bg_card_alt"],
            activebackground=THEME["border"],
            bd=1,
            relief="solid",
            highlightbackground=THEME["border"],
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.show_home_screen
        )
        btn_home.pack(side="left", padx=10)

        # Detailed Question-by-Question Review Section
        rev_header = tk.Label(center_box, text="📋 Question Breakdown & Explanations",
                              font=self.font_header, fg=THEME["text_primary"], bg=THEME["bg_dark"])
        rev_header.pack(anchor="w", pady=(10, 12))

        prefixes = ["A", "B", "C", "D"]
        for idx, item in enumerate(self.user_history, start=1):
            q_data = item["q"]
            is_ok = item["is_correct"]
            sel_idx = item["selected_idx"]
            cor_idx = item["correct_idx"]

            item_card = tk.Frame(center_box, bg=THEME["bg_card"], bd=1, relief="solid",
                                 highlightbackground=THEME["border"], highlightthickness=1)
            item_card.pack(fill="x", pady=6)

            # Item title row
            row1 = tk.Frame(item_card, bg=THEME["bg_card"])
            row1.pack(fill="x", padx=16, pady=(12, 4))

            status_txt = "✓ CORRECT" if is_ok else ("⏳ TIMED OUT" if item["timed_out"] else "✗ INCORRECT")
            status_color = THEME["success_light"] if is_ok else THEME["danger_light"]

            tk.Label(row1, text=f"Q{idx}. {q_data['question']}", font=self.font_bold,
                     fg=THEME["text_primary"], bg=THEME["bg_card"], wraplength=580, justify="left").pack(side="left")
            tk.Label(row1, text=status_txt, font=self.font_small,
                     fg=status_color, bg=THEME["bg_card_alt"], padx=8, pady=2).pack(side="right")

            # Code if exists
            if q_data.get("code"):
                c_box = tk.Label(item_card, text=q_data["code"], font=self.font_code,
                                 fg=THEME["code_fg"], bg=THEME["code_bg"], justify="left",
                                 anchor="w", padx=10, pady=6)
                c_box.pack(fill="x", padx=16, pady=4)

            # Answers comparison
            ans_row = tk.Frame(item_card, bg=THEME["bg_card"])
            ans_row.pack(fill="x", padx=16, pady=4)

            user_ans_str = q_data["options"][sel_idx] if sel_idx >= 0 else "None (Timed Out)"
            cor_ans_str = q_data["options"][cor_idx]

            tk.Label(ans_row, text=f"Your Answer: {user_ans_str}", font=self.font_small,
                     fg=THEME["text_secondary"] if is_ok else THEME["danger_light"], bg=THEME["bg_card"]).pack(anchor="w")
            
            if not is_ok:
                tk.Label(ans_row, text=f"Correct Answer: {cor_ans_str}", font=self.font_small,
                         fg=THEME["success_light"], bg=THEME["bg_card"]).pack(anchor="w")

            # Explanation
            exp_lbl = tk.Label(item_card, text=f"💡 {q_data['explanation']}", font=self.font_small,
                               fg=THEME["text_secondary"], bg=THEME["bg_card"],
                               wraplength=760, justify="left", anchor="w")
            exp_lbl.pack(fill="x", padx=16, pady=(2, 12))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    app = PythonQuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

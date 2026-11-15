import { sounds } from '../audio.js';

export const QUIZ_QUESTIONS = [
  {
    id: 1,
    difficulty: "Beginner",
    category: "Data Types",
    question: "What is the output of the following expression in Python 3?",
    code: "type(1 / 1)",
    options: ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"],
    answer: 1,
    explanation: "In Python 3, the standard division operator `/` always produces a float, even when dividing integers evenly (1 / 1 == 1.0)."
  },
  {
    id: 2,
    difficulty: "Beginner",
    category: "Lists & Mutability",
    question: "What is the value of `b` after these operations?",
    code: "a = [1, 2, 3]\nb = a\na.append(4)\nprint(b)",
    options: ["[1, 2, 3]", "[1, 2, 3, 4]", "None", "Error"],
    answer: 1,
    explanation: "Variables in Python store references to objects. `b = a` points `b` to the same list object in memory, so mutating `a` also affects `b`."
  },
  {
    id: 3,
    difficulty: "Intermediate",
    category: "Scoping & Closures",
    question: "What does calling `funcs[0]()` return?",
    code: "funcs = [lambda: i for i in range(3)]\nprint(funcs[0]())",
    options: ["0", "1", "2", "IndexError"],
    answer: 2,
    explanation: "Python closures bind variables by reference (late binding), not value. By the time `funcs[0]()` is called, the loop has completed and `i` equals 2."
  },
  {
    id: 4,
    difficulty: "Gotchas",
    category: "Default Arguments",
    question: "What will the following code output?",
    code: "def add_item(val, items=[]):\n    items.append(val)\n    return items\n\nadd_item(1)\nprint(add_item(2))",
    options: ["[2]", "[1, 2]", "[[1], [2]]", "TypeError"],
    answer: 1,
    explanation: "Default parameter values in Python are evaluated ONCE when the function definition is executed, not at each call. The same list persists across calls."
  },
  {
    id: 5,
    difficulty: "Intermediate",
    category: "Dictionaries",
    question: "What does this dictionary comprehension produce?",
    code: "keys = ['a', 'b', 'c']\nd = {k: i * 2 for i, k in enumerate(keys)}\nprint(d['b'])",
    options: ["0", "1", "2", "KeyError"],
    answer: 2,
    explanation: "In `enumerate(keys)`, 'a' has index 0, 'b' has index 1, 'c' has index 2. So `d['b'] = 1 * 2 = 2`."
  },
  {
    id: 6,
    difficulty: "Advanced",
    category: "Generators & Memory",
    question: "What is the difference between a generator expression and a list comprehension?",
    code: "gen = (x**2 for x in range(1000000))\nlst = [x**2 for x in range(1000000)]",
    options: [
      "Generators are faster for random indexing.",
      "Generators yield items lazily on demand, using negligible O(1) memory.",
      "List comprehensions are evaluated in a background thread.",
      "There is no difference in memory or speed."
    ],
    answer: 1,
    explanation: "Generators compute items on-the-fly via iteration protocol (`yield`), consuming minimal memory regardless of sequence size."
  },
  {
    id: 7,
    difficulty: "Intermediate",
    category: "Syntax & Operators",
    question: "What is the official name and function of the `:=` operator introduced in Python 3.8?",
    code: "if (n := len([1, 2, 3])) > 2:\n    print(n)",
    options: [
      "Walrus Operator (Assignment Expression) - assigns values inside expressions.",
      "Type Pointer - creates a memory alias.",
      "Strict Equality Operator - checks value and type.",
      "Pipeline Operator - chains functions left to right."
    ],
    answer: 0,
    explanation: "The `:=` operator is officially called the Assignment Expression (colloquially the Walrus Operator). It assigns a value to a variable within an expression."
  },
  {
    id: 8,
    difficulty: "Gotchas",
    category: "String Interning",
    question: "What is the output of comparing string identities?",
    code: "s1 = 'hello'\ns2 = 'hello'\nprint(s1 is s2)",
    options: ["True", "False", "None", "TypeError"],
    answer: 0,
    explanation: "Python interns short immutable strings and string literals in memory, so `s1` and `s2` refer to the exact same object in memory (`s1 is s2` is True)."
  }
];

export class PythonQuizGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.questions = [...QUIZ_QUESTIONS].sort(() => Math.random() - 0.5);
    this.currentIndex = 0;
    this.score = 0;
    this.streak = 0;
    this.maxStreak = 0;

    this.timeLeft = 20;
    this.maxTime = 20;
    this.timerInterval = null;

    this.lifelines = {
      fiftyFifty: true,
      timeBoost: true,
      skip: true
    };

    this.hiddenOptions = [];
    this.answered = false;

    this.init();
  }

  init() {
    this.renderQuestion();
  }

  renderQuestion() {
    if (this.currentIndex >= this.questions.length) {
      this.endQuiz();
      return;
    }

    this.answered = false;
    this.hiddenOptions = [];
    this.timeLeft = this.maxTime;

    const q = this.questions[this.currentIndex];

    this.container.innerHTML = `
      <div class="quiz-container">
        <!-- Top Bar -->
        <div class="quiz-top-bar">
          <div>
            <span class="card-tag" style="background: rgba(0, 229, 255, 0.2); color: var(--neon-cyan); border-left: 3px solid var(--neon-cyan);">CODER ONLY</span>
            <span class="card-tag" style="margin-left: 6px;">${q.difficulty}</span>
            <span class="card-tag" style="background: rgba(255, 255, 255, 0.08); color: var(--text-secondary); margin-left: 6px;">
              ${q.category}
            </span>
          </div>
          <div style="font-family: var(--font-mono); font-weight: 800; color: var(--neon-amber);">
            SCORE: <span id="quiz-score">${this.score}</span> | STREAK: x${this.streak}
          </div>
        </div>

        <!-- Timer Bar -->
        <div class="timer-track">
          <div class="timer-fill" id="timer-bar" style="width: 100%;"></div>
        </div>

        <!-- Lifelines -->
        <div class="quiz-lifelines">
          <button class="lifeline-btn" id="ll-fifty" ${this.lifelines.fiftyFifty ? '' : 'disabled'}>
            ⚡ 50/50
          </button>
          <button class="lifeline-btn" id="ll-time" ${this.lifelines.timeBoost ? '' : 'disabled'}>
            ⏳ +15s Time
          </button>
          <button class="lifeline-btn" id="ll-skip" ${this.lifelines.skip ? '' : 'disabled'}>
            ⏭️ Skip
          </button>
        </div>

        <!-- Question Card -->
        <div class="quiz-card">
          <div style="font-size: 0.8rem; color: var(--text-muted);">
            QUESTION ${this.currentIndex + 1} OF ${this.questions.length}
          </div>
          <h3 class="quiz-question-text">${q.question}</h3>

          ${q.code ? `<pre class="quiz-code-box"><code>${q.code}</code></pre>` : ''}

          <!-- Options List -->
          <div class="quiz-options-list" id="options-list">
            ${q.options
              .map(
                (opt, idx) => `
              <button class="quiz-option-btn" data-opt-idx="${idx}">
                <span style="font-family: var(--font-mono); font-weight: 800; color: var(--neon-cyan);">
                  ${String.fromCharCode(65 + idx)}.
                </span>
                <span>${opt}</span>
              </button>
            `
              )
              .join('')}
          </div>
        </div>
      </div>
    `;

    this.attachEvents();
    this.startTimer();
  }

  attachEvents() {
    // Option clicks
    this.container.querySelectorAll('.quiz-option-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-opt-idx'), 10);
        this.selectAnswer(idx);
      });
    });

    // 50/50
    const llFifty = this.container.querySelector('#ll-fifty');
    if (llFifty && this.lifelines.fiftyFifty) {
      llFifty.addEventListener('click', () => {
        sounds.click();
        this.lifelines.fiftyFifty = false;
        llFifty.setAttribute('disabled', 'true');

        const q = this.questions[this.currentIndex];
        const wrongIndices = [0, 1, 2, 3].filter((i) => i !== q.answer);
        // Randomly hide 2 wrong
        wrongIndices.sort(() => Math.random() - 0.5);
        this.hiddenOptions = [wrongIndices[0], wrongIndices[1]];

        this.hiddenOptions.forEach((hIdx) => {
          const b = this.container.querySelector(`.quiz-option-btn[data-opt-idx="${hIdx}"]`);
          if (b) {
            b.style.opacity = '0.2';
            b.setAttribute('disabled', 'true');
          }
        });
      });
    }

    // Time Boost
    const llTime = this.container.querySelector('#ll-time');
    if (llTime && this.lifelines.timeBoost) {
      llTime.addEventListener('click', () => {
        sounds.click();
        this.lifelines.timeBoost = false;
        llTime.setAttribute('disabled', 'true');
        this.timeLeft += 15;
        this.updateTimerBar();
      });
    }

    // Skip
    const llSkip = this.container.querySelector('#ll-skip');
    if (llSkip && this.lifelines.skip) {
      llSkip.addEventListener('click', () => {
        sounds.click();
        this.lifelines.skip = false;
        llSkip.setAttribute('disabled', 'true');
        clearInterval(this.timerInterval);
        this.currentIndex++;
        this.renderQuestion();
      });
    }
  }

  startTimer() {
    clearInterval(this.timerInterval);
    this.timerInterval = setInterval(() => {
      this.timeLeft -= 0.1;
      this.updateTimerBar();

      if (this.timeLeft <= 0) {
        clearInterval(this.timerInterval);
        this.timeOut();
      }
    }, 100);
  }

  updateTimerBar() {
    const bar = this.container.querySelector('#timer-bar');
    if (bar) {
      const pct = Math.max(0, Math.min(100, (this.timeLeft / this.maxTime) * 100));
      bar.style.width = `${pct}%`;
      if (pct < 30) {
        bar.style.background = 'var(--neon-red)';
      } else if (pct < 60) {
        bar.style.background = 'var(--neon-amber)';
      } else {
        bar.style.background = 'linear-gradient(90deg, var(--neon-green), var(--neon-cyan))';
      }
    }
  }

  selectAnswer(selectedIdx) {
    if (this.answered) return;
    this.answered = true;
    clearInterval(this.timerInterval);

    const q = this.questions[this.currentIndex];
    const isCorrect = selectedIdx === q.answer;

    const selectedBtn = this.container.querySelector(`.quiz-option-btn[data-opt-idx="${selectedIdx}"]`);
    const correctBtn = this.container.querySelector(`.quiz-option-btn[data-opt-idx="${q.answer}"]`);

    if (isCorrect) {
      sounds.correct();
      if (selectedBtn) selectedBtn.classList.add('correct');
      this.streak++;
      if (this.streak > this.maxStreak) this.maxStreak = this.streak;
      const points = 100 + this.streak * 25 + Math.round(this.timeLeft * 5);
      this.score += points;
    } else {
      sounds.wrong();
      if (selectedBtn) selectedBtn.classList.add('wrong');
      if (correctBtn) correctBtn.classList.add('correct');
      this.streak = 0;
    }

    // Explanation card
    const expBox = document.createElement('div');
    expBox.style.cssText = `
      background: var(--bg-card-alt);
      border: 1px solid var(--border-glow);
      padding: 14px 18px;
      border-radius: var(--radius-md);
      margin-top: 14px;
      font-size: 0.9rem;
      line-height: 1.5;
      color: var(--text-primary);
    `;
    expBox.innerHTML = `
      <div style="font-weight: 800; color: ${isCorrect ? 'var(--neon-green)' : 'var(--neon-pink)'}; margin-bottom: 4px;">
        ${isCorrect ? '✓ CORRECT' : '✗ INCORRECT'}
      </div>
      <div>💡 ${q.explanation}</div>
      <button class="play-btn" style="margin-top: 12px; width: 100%;" id="quiz-btn-next">
        ${this.currentIndex < this.questions.length - 1 ? 'Next Question ▶' : 'Finish Quiz 🏆'}
      </button>
    `;
    this.container.querySelector('.quiz-card').appendChild(expBox);

    expBox.querySelector('#quiz-btn-next').addEventListener('click', () => {
      this.currentIndex++;
      this.renderQuestion();
    });
  }

  timeOut() {
    this.selectAnswer(-1);
  }

  endQuiz() {
    sounds.vaultUnlock();
    if (this.onScoreUpdate) {
      this.onScoreUpdate('python-quiz', this.score);
    }

    const overlay = document.createElement('div');
    overlay.className = 'overlay-modal';
    overlay.innerHTML = `
      <div class="modal-content">
        <div style="font-size: 3rem;">🎓🐍</div>
        <h3 class="modal-title" style="color: var(--neon-cyan);">QUIZ COMPLETED!</h3>
        <p style="color: var(--text-secondary);">You finished all Python challenges.</p>
        <div style="background: rgba(0,0,0,0.4); padding: 14px; border-radius: var(--radius-md);">
          <div style="font-size: 0.8rem; color: var(--text-muted);">FINAL SCORE</div>
          <div style="font-size: 2.2rem; font-weight: 900; color: var(--neon-amber);">${this.score} PTS</div>
          <div style="font-size: 0.85rem; color: var(--neon-green); font-weight: 700; margin-top: 4px;">
            Best Streak: x${this.maxStreak}
          </div>
        </div>
        <div style="display: flex; gap: 10px; margin-top: 8px;">
          <button class="nav-btn" style="flex: 1;" id="quiz-modal-hub">Arcade Hub</button>
          <button class="play-btn" style="flex: 1;" id="quiz-modal-replay">Retry Quiz</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#quiz-modal-hub').addEventListener('click', () => {
      overlay.remove();
      this.destroy();
      this.onExit();
    });

    overlay.querySelector('#quiz-modal-replay').addEventListener('click', () => {
      overlay.remove();
      this.score = 0;
      this.streak = 0;
      this.currentIndex = 0;
      this.questions.sort(() => Math.random() - 0.5);
      this.lifelines = { fiftyFifty: true, timeBoost: true, skip: true };
      this.renderQuestion();
    });
  }

  destroy() {
    clearInterval(this.timerInterval);
  }
}

import { sounds } from '../audio.js';
const GK_QUESTIONS = [

  // SCIENCE 
  { id: 1, category: "Science", difficulty: "Easy", question: "What is the chemical symbol for water?", options: ["H2O", "HO2", "H3O", "O2H"], answer: 0, explanation: "Water is 2 hydrogen atoms bonded to 1 oxygen atom — H₂O." },
  { id: 2, category: "Science", difficulty: "Easy", question: "Which planet is known as the Red Planet?", options: ["Venus", "Jupiter", "Mars", "Saturn"], answer: 2, explanation: "Mars looks red due to iron oxide (rust) on its surface." },
  { id: 3, category: "Science", difficulty: "Medium", question: "What is the approximate speed of light in a vacuum?", options: ["300,000 km/s", "150,000 km/s", "450,000 km/s", "30,000 km/s"], answer: 0, explanation: "Light travels at ≈299,792 km/s in a vacuum." },
  { id: 4, category: "Science", difficulty: "Medium", question: "How many bones are in the adult human body?", options: ["206", "198", "215", "230"], answer: 0, explanation: "Adults have 206 bones; babies start with ≈270 which fuse over time." },
  { id: 5, category: "Science", difficulty: "Medium", question: "Which gas do plants absorb during photosynthesis?", options: ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], answer: 2, explanation: "Plants absorb CO₂ and release O₂ during photosynthesis." },
  { id: 6, category: "Science", difficulty: "Hard", question: "What is the atomic number of Gold (Au)?", options: ["47", "79", "82", "29"], answer: 1, explanation: "Gold (Au) has atomic number 79 on the periodic table." },
  { id: 7, category: "Science", difficulty: "Easy", question: "What is the powerhouse of the cell?", options: ["Nucleus", "Ribosome", "Mitochondria", "Golgi Apparatus"], answer: 2, explanation: "Mitochondria generate ATP — the energy currency of the cell." },
  { id: 8, category: "Science", difficulty: "Hard", question: "Which element has the highest melting point?", options: ["Iron", "Tungsten", "Carbon", "Platinum"], answer: 1, explanation: "Tungsten (W) melts at 3,422 °C — the highest of any element." },
  { id: 9, category: "Science", difficulty: "Medium", question: "What force keeps planets in orbit around the Sun?", options: ["Magnetism", "Electrostatic force", "Gravity", "Nuclear force"], answer: 2, explanation: "Gravity is the attractive force between masses that keeps planets in orbit." },

  // HISTORY
  { id: 10, category: "History", difficulty: "Easy", question: "Who was the first President of the United States?", options: ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"], answer: 2, explanation: "George Washington served as the 1st US President from 1789–1797." },
  { id: 11, category: "History", difficulty: "Easy", question: "In which year did World War II end?", options: ["1943", "1944", "1945", "1946"], answer: 2, explanation: "WWII ended in 1945: V-E Day (May) and V-J Day (September)." },
  { id: 12, category: "History", difficulty: "Medium", question: "Which ancient wonder was located in Alexandria, Egypt?", options: ["Colossus of Rhodes", "Lighthouse of Alexandria", "Temple of Artemis", "Statue of Zeus"], answer: 1, explanation: "The Lighthouse of Alexandria was one of the Seven Ancient Wonders." },
  { id: 13, category: "History", difficulty: "Easy", question: "Who painted the Mona Lisa?", options: ["Michelangelo", "Raphael", "Leonardo da Vinci", "Caravaggio"], answer: 2, explanation: "Leonardo da Vinci painted the Mona Lisa between 1503–1519." },
  { id: 14, category: "History", difficulty: "Medium", question: "The Berlin Wall fell in which year?", options: ["1987", "1988", "1989", "1991"], answer: 2, explanation: "The Berlin Wall fell on November 9, 1989." },
  { id: 15, category: "History", difficulty: "Hard", question: "Which empire was ruled by Genghis Khan?", options: ["Ottoman", "Mongol", "Roman", "Persian"], answer: 1, explanation: "Genghis Khan founded the Mongol Empire — the largest contiguous land empire in history." },
  { id: 16, category: "History", difficulty: "Medium", question: "Who wrote Romeo and Juliet?", options: ["Charles Dickens", "Geoffrey Chaucer", "William Shakespeare", "John Milton"], answer: 2, explanation: "Shakespeare wrote Romeo and Juliet around 1594–1596." },

  // GEOGRAPHY
  { id: 17, category: "Geography", difficulty: "Easy", question: "What is the largest continent by area?", options: ["Africa", "North America", "Europe", "Asia"], answer: 3, explanation: "Asia is the largest continent covering about 44.6 million km²." },
  { id: 18, category: "Geography", difficulty: "Easy", question: "Which is the longest river in the world?", options: ["Amazon", "Congo", "Nile", "Yangtze"], answer: 2, explanation: "The Nile River stretches about 6,650 km through northeastern Africa." },
  { id: 19, category: "Geography", difficulty: "Medium", question: "What is the capital of Australia?", options: ["Sydney", "Melbourne", "Brisbane", "Canberra"], answer: 3, explanation: "Canberra is the capital, chosen as a compromise between Sydney and Melbourne." },
  { id: 20, category: "Geography", difficulty: "Medium", question: "Which country has the most natural lakes?", options: ["Russia", "USA", "Brazil", "Canada"], answer: 3, explanation: "Canada has over 60% of the world's natural lakes." },
  { id: 21, category: "Geography", difficulty: "Hard", question: "What is the smallest country in the world by area?", options: ["Monaco", "San Marino", "Vatican City", "Liechtenstein"], answer: 2, explanation: "Vatican City covers just 0.44 km², making it the smallest sovereign state." },
  { id: 22, category: "Geography", difficulty: "Medium", question: "Mount Everest borders which two countries?", options: ["India & China", "Nepal & China", "Nepal & India", "Bhutan & China"], answer: 1, explanation: "Mount Everest sits on the Nepal–China (Tibet) border in the Himalayas." },

  // SPORTS
  { id: 23, category: "Sports", difficulty: "Easy", question: "How many players are on a soccer team on the field?", options: ["9", "10", "11", "12"], answer: 2, explanation: "Each soccer team fields 11 players including the goalkeeper." },
  { id: 24, category: "Sports", difficulty: "Easy", question: "In which sport would you perform a 'slam dunk'?", options: ["Volleyball", "Tennis", "Basketball", "Handball"], answer: 2, explanation: "A slam dunk is a basketball shot where the player forces the ball into the hoop from above." },
  { id: 25, category: "Sports", difficulty: "Medium", question: "Which country has won the most FIFA World Cup titles?", options: ["Germany", "Argentina", "Italy", "Brazil"], answer: 3, explanation: "Brazil has won the FIFA World Cup a record 5 times." },
  { id: 26, category: "Sports", difficulty: "Medium", question: "How many Grand Slam tournaments are in tennis each year?", options: ["2", "3", "4", "5"], answer: 2, explanation: "The four Grand Slams: Australian Open, French Open, Wimbledon, US Open." },
  { id: 27, category: "Sports", difficulty: "Hard", question: "Who holds the world record for the 100m sprint?", options: ["Yohan Blake", "Justin Gatlin", "Usain Bolt", "Tyreek Hill"], answer: 2, explanation: "Usain Bolt set the 100m world record of 9.58s at the 2009 Berlin World Championships." },
  { id: 28, category: "Sports", difficulty: "Medium", question: "Which country hosted the first modern Olympic Games in 1896?", options: ["France", "UK", "USA", "Greece"], answer: 3, explanation: "The first modern Olympics were held in Athens, Greece in 1896." },

  // ENTERTAINMENT
  { id: 29, category: "Entertainment", difficulty: "Easy", question: "Who played Iron Man in the Marvel Cinematic Universe?", options: ["Chris Evans", "Chris Hemsworth", "Robert Downey Jr.", "Mark Ruffalo"], answer: 2, explanation: "Robert Downey Jr. portrayed Tony Stark / Iron Man across 10+ MCU films." },
  { id: 30, category: "Entertainment", difficulty: "Easy", question: "Which movie features 'May the Force be with you'?", options: ["Star Trek", "Star Wars", "Interstellar", "The Matrix"], answer: 1, explanation: "'May the Force be with you' is the iconic Star Wars phrase." },
  { id: 31, category: "Entertainment", difficulty: "Medium", question: "Which film won Best Picture at the 2020 Academy Awards?", options: ["1917", "Joker", "Parasite", "Once Upon a Time in Hollywood"], answer: 2, explanation: "Parasite by Bong Joon-ho was the first non-English film to win Best Picture." },
  { id: 32, category: "Entertainment", difficulty: "Medium", question: "In Breaking Bad, what subject does Walter White teach?", options: ["Biology", "Chemistry", "Physics", "Mathematics"], answer: 1, explanation: "Walter White is a high school chemistry teacher turned drug manufacturer." },
  { id: 33, category: "Entertainment", difficulty: "Hard", question: "What is the highest-grossing film of all time (unadjusted)?", options: ["Avengers: Endgame", "Titanic", "Avatar", "Star Wars: The Force Awakens"], answer: 2, explanation: "Avatar (2009, re-released 2022) holds the box office record at over $2.9 billion." },

  // MUSIC
  { id: 34, category: "Music", difficulty: "Easy", question: "Which band performed 'Bohemian Rhapsody'?", options: ["The Beatles", "Led Zeppelin", "Queen", "The Rolling Stones"], answer: 2, explanation: "Bohemian Rhapsody was written by Freddie Mercury and performed by Queen in 1975." },
  { id: 35, category: "Music", difficulty: "Medium", question: "Which artist released the album 'Thriller' (1982)?", options: ["Prince", "Michael Jackson", "David Bowie", "Stevie Wonder"], answer: 1, explanation: "Thriller is the best-selling album of all time with 66+ million copies sold." },
  { id: 36, category: "Music", difficulty: "Medium", question: "What nationality was the composer Ludwig van Beethoven?", options: ["Austrian", "German", "Italian", "French"], answer: 1, explanation: "Beethoven was born in Bonn, Germany in 1770." },

  // GENERAL
  { id: 37, category: "General", difficulty: "Easy", question: "How many sides does a hexagon have?", options: ["5", "6", "7", "8"], answer: 1, explanation: "A hexagon has 6 sides. 'Hex' is Greek for six." },
  { id: 38, category: "General", difficulty: "Medium", question: "What is the currency of Japan?", options: ["Yuan", "Won", "Rupee", "Yen"], answer: 3, explanation: "Japan's currency is the Japanese Yen (¥), introduced in 1871." },
  { id: 39, category: "General", difficulty: "Medium", question: "What does 'URL' stand for?", options: ["Uniform Resource Locator", "Universal Reference Link", "Unified Remote Library", "Uniform Routing Label"], answer: 0, explanation: "URL = Uniform Resource Locator — the web address typed in a browser." },
  { id: 40, category: "General", difficulty: "Hard", question: "What is the most spoken language by native speakers?", options: ["English", "Hindi", "Spanish", "Mandarin Chinese"], answer: 3, explanation: "Mandarin Chinese has ~920 million native speakers. English leads in total speakers." },
  { id: 41, category: "General", difficulty: "Hard", question: "Which element is liquid at room temperature besides Mercury?", options: ["Bromine", "Fluorine", "Chlorine", "Phosphorus"], answer: 0, explanation: "Bromine is one of only two elements liquid at room temperature (along with Mercury)." },
  { id: 42, category: "General", difficulty: "Medium", question: "How many time zones does Russia span?", options: ["9", "10", "11", "12"], answer: 2, explanation: "Russia spans 11 time zones — the most of any country." },
];

const CATEGORY_COLORS = {
  Science: 'var(--neon-cyan)',
  History: 'var(--neon-purple)',
  Geography: 'var(--neon-green)',
  Sports: 'var(--neon-amber)',
  Entertainment: 'var(--neon-pink)',
  Music: '#ffb700',
  General: 'var(--text-secondary)',
};

export class GeneralQuizGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.questions = [...GK_QUESTIONS].sort(() => Math.random() - 0.5).slice(0, 20);
    this.currentIndex = 0;
    this.score = 0;
    this.streak = 0;
    this.maxStreak = 0;
    this.correctCount = 0;

    this.timeLeft = 30;
    this.maxTime = 30;
    this.timerInterval = null;
    this.answered = false;

    this.lifelines = { fiftyFifty: true, timeBoost: true, skip: true };
    this.hiddenOptions = [];

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
    const catColor = CATEGORY_COLORS[q.category] || 'var(--neon-cyan)';
    const diffColor = q.difficulty === 'Easy' ? 'var(--neon-green)'
      : q.difficulty === 'Medium' ? 'var(--neon-amber)'
        : 'var(--neon-red)';

    this.container.innerHTML = `
      <div class="quiz-container">
        <!-- Top Bar -->
        <div class="quiz-top-bar">
          <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <span class="card-tag" style="background: rgba(0,0,0,0.4); color: ${catColor}; border-left: 3px solid ${catColor};">
              📌 ${q.category}
            </span>
            <span class="card-tag" style="color: ${diffColor};">
              ⚡ ${q.difficulty}
            </span>
          </div>
          <div style="font-family: var(--font-mono); font-weight: 800; color: var(--neon-amber); white-space: nowrap;">
            SCORE: <span id="gkq-score">${this.score}</span> &nbsp;🔥${this.streak}
          </div>
        </div>

        <!-- Timer Bar -->
        <div class="timer-track">
          <div class="timer-fill" id="gkq-timer-bar" style="width: 100%;"></div>
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-muted); text-align: right; margin-bottom: 6px;">
          Q ${this.currentIndex + 1} / ${this.questions.length} &nbsp;|&nbsp; <span id="gkq-time">${Math.ceil(this.timeLeft)}s</span>
        </div>

        <!-- Lifelines -->
        <div class="quiz-lifelines">
          <button class="lifeline-btn" id="gkq-fifty" ${this.lifelines.fiftyFifty ? '' : 'disabled'}>⚡ 50/50</button>
          <button class="lifeline-btn" id="gkq-time" ${this.lifelines.timeBoost ? '' : 'disabled'}>⏳ +15s</button>
          <button class="lifeline-btn" id="gkq-skip" ${this.lifelines.skip ? '' : 'disabled'}>⏭️ Skip</button>
        </div>

        <!-- Question Card -->
        <div class="quiz-card">
          <h3 class="quiz-question-text">${q.question}</h3>

          <!-- Options -->
          <div class="quiz-options-list" id="gkq-options">
            ${q.options.map((opt, idx) => `
              <button class="quiz-option-btn" data-idx="${idx}">
                <span style="font-family: var(--font-mono); font-weight: 800; color: var(--neon-cyan);">
                  ${String.fromCharCode(65 + idx)}.
                </span>
                <span>${opt}</span>
              </button>
            `).join('')}
          </div>
        </div>
      </div>
    `;

    this.attachEvents();
    this.startTimer();
  }

  attachEvents() {
    this.container.querySelectorAll('.quiz-option-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-idx'), 10);
        this.selectAnswer(idx);
      });
    });

    const llFifty = this.container.querySelector('#gkq-fifty');
    if (llFifty && this.lifelines.fiftyFifty) {
      llFifty.addEventListener('click', () => {
        sounds.click();
        this.lifelines.fiftyFifty = false;
        llFifty.setAttribute('disabled', 'true');
        const q = this.questions[this.currentIndex];
        const wrongs = [0, 1, 2, 3].filter(i => i !== q.answer).sort(() => Math.random() - 0.5);
        this.hiddenOptions = [wrongs[0], wrongs[1]];
        this.hiddenOptions.forEach(hIdx => {
          const b = this.container.querySelector(`.quiz-option-btn[data-idx="${hIdx}"]`);
          if (b) { b.style.opacity = '0.2'; b.setAttribute('disabled', 'true'); }
        });
      });
    }

    const llTime = this.container.querySelector('#gkq-time');
    if (llTime && this.lifelines.timeBoost) {
      llTime.addEventListener('click', () => {
        sounds.click();
        this.lifelines.timeBoost = false;
        llTime.setAttribute('disabled', 'true');
        this.timeLeft = Math.min(this.timeLeft + 15, this.maxTime);
      });
    }

    const llSkip = this.container.querySelector('#gkq-skip');
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
      const bar = this.container.querySelector('#gkq-timer-bar');
      const timeEl = this.container.querySelector('#gkq-time');
      if (bar) {
        const pct = Math.max(0, (this.timeLeft / this.maxTime) * 100);
        bar.style.width = `${pct}%`;
        bar.style.background = pct < 30 ? 'var(--neon-red)'
          : pct < 60 ? 'var(--neon-amber)'
            : 'linear-gradient(90deg, var(--neon-green), var(--neon-cyan))';
      }
      if (timeEl) timeEl.textContent = `${Math.ceil(Math.max(0, this.timeLeft))}s`;
      if (this.timeLeft <= 0) {
        clearInterval(this.timerInterval);
        this.selectAnswer(-1);
      }
    }, 100);
  }

  selectAnswer(selectedIdx) {
    if (this.answered) return;
    this.answered = true;
    clearInterval(this.timerInterval);

    const q = this.questions[this.currentIndex];
    const isCorrect = selectedIdx === q.answer;

    const selectedBtn = selectedIdx >= 0
      ? this.container.querySelector(`.quiz-option-btn[data-idx="${selectedIdx}"]`)
      : null;
    const correctBtn = this.container.querySelector(`.quiz-option-btn[data-idx="${q.answer}"]`);

    if (isCorrect) {
      sounds.correct();
      if (selectedBtn) selectedBtn.classList.add('correct');
      this.streak++;
      this.correctCount++;
      if (this.streak > this.maxStreak) this.maxStreak = this.streak;
      const pts = 100 + this.streak * 30 + Math.round(this.timeLeft * 2);
      this.score += pts;
    } else {
      sounds.wrong();
      if (selectedBtn) selectedBtn.classList.add('wrong');
      if (correctBtn) correctBtn.classList.add('correct');
      this.streak = 0;
    }

    // Disable all options
    this.container.querySelectorAll('.quiz-option-btn').forEach(b => b.setAttribute('disabled', 'true'));

    const scoreEl = this.container.querySelector('#gkq-score');
    if (scoreEl) scoreEl.textContent = this.score;

    // Explanation box
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
      <div style="font-weight: 800; color: ${isCorrect ? 'var(--neon-green)' : 'var(--neon-pink)'}; margin-bottom: 6px;">
        ${isCorrect ? '✓ CORRECT!' : selectedIdx === -1 ? '⏰ TIME\'S UP!' : '✗ INCORRECT'}
      </div>
      <div>💡 ${q.explanation}</div>
      <button class="play-btn" style="margin-top: 12px; width: 100%; justify-content: center;" id="gkq-next">
        ${this.currentIndex < this.questions.length - 1 ? 'Next Question ▶' : 'See Results 🏆'}
      </button>
    `;

    const quizCard = this.container.querySelector('.quiz-card');
    if (quizCard) quizCard.appendChild(expBox);

    expBox.querySelector('#gkq-next').addEventListener('click', () => {
      this.currentIndex++;
      this.renderQuestion();
    });
  }

  endQuiz() {
    clearInterval(this.timerInterval);
    sounds.vaultUnlock();
    if (this.onScoreUpdate) this.onScoreUpdate('general-quiz', this.score);

    const accuracy = Math.round((this.correctCount / this.questions.length) * 100);
    const grade = accuracy >= 90 ? '🏆 GENIUS!'
      : accuracy >= 70 ? '🌟 EXPERT'
        : accuracy >= 50 ? '👍 GOOD EFFORT'
          : '📚 KEEP LEARNING';

    const overlay = document.createElement('div');
    overlay.className = 'overlay-modal';
    overlay.innerHTML = `
      <div class="modal-content">
        <div style="font-size: 2.8rem;">${grade}</div>
        <h3 class="modal-title" style="color: var(--neon-cyan);">QUIZ COMPLETE!</h3>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: var(--font-mono); font-size: 0.85rem; margin: 10px 0;">
          <div style="background: var(--bg-card-alt); padding: 10px; border-radius: var(--radius-sm); text-align: center;">
            <div style="color: var(--text-muted); font-size: 0.7rem;">FINAL SCORE</div>
            <div style="font-size: 1.5rem; font-weight: 900; color: var(--neon-amber);">${this.score}</div>
          </div>
          <div style="background: var(--bg-card-alt); padding: 10px; border-radius: var(--radius-sm); text-align: center;">
            <div style="color: var(--text-muted); font-size: 0.7rem;">ACCURACY</div>
            <div style="font-size: 1.5rem; font-weight: 900; color: var(--neon-cyan);">${accuracy}%</div>
          </div>
          <div style="background: var(--bg-card-alt); padding: 10px; border-radius: var(--radius-sm); text-align: center;">
            <div style="color: var(--text-muted); font-size: 0.7rem;">CORRECT</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: var(--neon-green);">${this.correctCount} / ${this.questions.length}</div>
          </div>
          <div style="background: var(--bg-card-alt); padding: 10px; border-radius: var(--radius-sm); text-align: center;">
            <div style="color: var(--text-muted); font-size: 0.7rem;">BEST STREAK</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: var(--neon-amber);">🔥 ${this.maxStreak}x</div>
          </div>
        </div>

        <div style="display: flex; gap: 10px; margin-top: 8px;">
          <button class="nav-btn" style="flex: 1;" id="gkq-hub">Arcade Hub</button>
          <button class="play-btn" style="flex: 1; justify-content: center;" id="gkq-replay">Play Again</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#gkq-hub').addEventListener('click', () => {
      overlay.remove();
      this.destroy();
      if (this.onExit) this.onExit();
    });

    overlay.querySelector('#gkq-replay').addEventListener('click', () => {
      overlay.remove();
      this.score = 0;
      this.streak = 0;
      this.correctCount = 0;
      this.currentIndex = 0;
      this.maxStreak = 0;
      this.questions = [...GK_QUESTIONS].sort(() => Math.random() - 0.5).slice(0, 20);
      this.lifelines = { fiftyFifty: true, timeBoost: true, skip: true };
      this.renderQuestion();
    });
  }

  destroy() {
    clearInterval(this.timerInterval);
  }
}

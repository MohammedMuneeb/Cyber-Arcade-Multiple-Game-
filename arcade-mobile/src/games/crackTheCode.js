import { sounds } from '../audio.js';

export class CrackTheCodeGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.roundsTotal = 4;
    this.currentRound = 1;
    this.secretCode = [];
    this.currentGuess = [];
    this.history = [];
    this.totalScore = 0;
    this.isGameOver = false;

    this.init();
  }

  init() {
    this.generateSecretCode();
    this.render();
    this.attachEvents();
  }

  generateSecretCode() {
    this.secretCode = [];
    for (let i = 0; i < 6; i++) {
      this.secretCode.push(Math.floor(Math.random() * 10));
    }
  }

  render() {
    this.container.innerHTML = `
      <div class="ctc-container">
        <!-- HUD -->
        <div class="ctc-hud">
          <div>
            <span class="card-tag">CYBER VAULT BREAKER</span>
            <div style="font-weight: 800; font-size: 1.2rem; color: var(--neon-cyan); margin-top: 4px;">
              SCORE: <span id="ctc-score">${this.totalScore}</span>
            </div>
          </div>
          <div class="ctc-round-badge">
            ROUND ${this.currentRound} / ${this.roundsTotal}
          </div>
        </div>

        <!-- 6 Code Slots -->
        <div class="ctc-slots-box" id="ctc-slots">
          ${[0, 1, 2, 3, 4, 5]
            .map(
              (i) => `
            <div class="ctc-slot ${i === this.currentGuess.length ? 'active' : ''}" id="ctc-slot-${i}">
              ${this.currentGuess[i] !== undefined ? this.currentGuess[i] : '-'}
            </div>
          `
            )
            .join('')}
        </div>

        <!-- On-Screen Keypad -->
        <div class="ctc-keypad">
          ${[1, 2, 3, 4, 5, 6, 7, 8, 9]
            .map(
              (n) => `
            <button class="ctc-key" data-digit="${n}">${n}</button>
          `
            )
            .join('')}
          <button class="ctc-key action-key" id="ctc-clear">CLR</button>
          <button class="ctc-key" data-digit="0">0</button>
          <button class="ctc-key action-key" id="ctc-backspace">⌫</button>
        </div>

        <button class="ctc-submit-btn" id="ctc-submit" ${
          this.currentGuess.length === 6 ? '' : 'disabled style="opacity: 0.5;"'
        }>
          SUBMIT GUESS [ENTER]
        </button>

        <!-- Mission History -->
        <div class="ctc-history" id="ctc-history">
          <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Mission Attempt History</div>
          ${
            this.history.length === 0
              ? '<div style="font-size: 0.85rem; color: var(--text-muted);">Enter 6 digits to begin hacking...</div>'
              : this.history
                  .map(
                    (h, idx) => `
                <div class="ctc-history-item">
                  <span>R${idx + 1}: ${h.guess.join('-')}</span>
                  <span style="color: ${h.matches > 0 ? 'var(--neon-green)' : 'var(--text-muted)'}">
                    ${h.matches} Match (${h.score} pts)
                  </span>
                </div>
              `
                  )
                  .join('')
          }
        </div>
      </div>
    `;
  }

  attachEvents() {
    // Keypad clicks
    this.container.querySelectorAll('.ctc-key[data-digit]').forEach((btn) => {
      btn.addEventListener('click', () => {
        this.addDigit(parseInt(btn.getAttribute('data-digit'), 10));
      });
    });

    const clearBtn = this.container.querySelector('#ctc-clear');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        sounds.click();
        this.currentGuess = [];
        this.updateSlots();
      });
    }

    const backBtn = this.container.querySelector('#ctc-backspace');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        sounds.click();
        this.currentGuess.pop();
        this.updateSlots();
      });
    }

    const submitBtn = this.container.querySelector('#ctc-submit');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => {
        this.submitGuess();
      });
    }

    // Physical keyboard listener
    this.keyHandler = (e) => {
      if (this.isGameOver) return;
      if (e.key >= '0' && e.key <= '9') {
        this.addDigit(parseInt(e.key, 10));
      } else if (e.key === 'Backspace') {
        sounds.click();
        this.currentGuess.pop();
        this.updateSlots();
      } else if (e.key === 'Enter' && this.currentGuess.length === 6) {
        this.submitGuess();
      }
    };
    window.addEventListener('keydown', this.keyHandler);
  }

  addDigit(digit) {
    if (this.currentGuess.length < 6) {
      sounds.keypadPress();
      this.currentGuess.push(digit);
      this.updateSlots();
    }
  }

  updateSlots() {
    for (let i = 0; i < 6; i++) {
      const slot = this.container.querySelector(`#ctc-slot-${i}`);
      if (slot) {
        slot.textContent = this.currentGuess[i] !== undefined ? this.currentGuess[i] : '-';
        if (i === this.currentGuess.length) {
          slot.classList.add('active');
        } else {
          slot.classList.remove('active');
        }
      }
    }

    const submitBtn = this.container.querySelector('#ctc-submit');
    if (submitBtn) {
      if (this.currentGuess.length === 6) {
        submitBtn.removeAttribute('disabled');
        submitBtn.style.opacity = '1';
      } else {
        submitBtn.setAttribute('disabled', 'true');
        submitBtn.style.opacity = '0.5';
      }
    }
  }

  submitGuess() {
    if (this.currentGuess.length !== 6 || this.isGameOver) return;

    let roundScore = 0;
    let matchCount = 0;
    const matchIndices = [];

    for (let i = 0; i < 6; i++) {
      if (this.currentGuess[i] === this.secretCode[i]) {
        roundScore += this.currentGuess[i];
        matchCount++;
        matchIndices.push(i);
      }
    }

    if (matchCount > 0) {
      sounds.match();
    } else {
      sounds.wrong();
    }

    this.totalScore += roundScore;
    this.history.unshift({
      guess: [...this.currentGuess],
      matches: matchCount,
      score: roundScore
    });

    // Animate matching slots
    matchIndices.forEach((idx) => {
      const slot = this.container.querySelector(`#ctc-slot-${idx}`);
      if (slot) slot.classList.add('match');
    });

    if (matchCount === 6) {
      // Perfect crack!
      sounds.vaultUnlock();
      this.endGame(true);
      return;
    }

    if (this.currentRound >= this.roundsTotal) {
      // 4 rounds over
      this.endGame(false);
      return;
    }

    // Advance round
    this.currentRound++;
    setTimeout(() => {
      this.currentGuess = [];
      this.render();
      this.attachEvents();
    }, 700);
  }

  endGame(isPerfect) {
    this.isGameOver = true;
    let rank = 'Rookie Breaker';
    if (isPerfect || this.totalScore >= 35) rank = 'Grandmaster Hacker';
    else if (this.totalScore >= 24) rank = 'Cyber Mastermind';
    else if (this.totalScore >= 12) rank = 'Cryptographer';

    // Update global score
    if (this.onScoreUpdate) {
      this.onScoreUpdate('crack-the-code', this.totalScore);
    }

    const overlay = document.createElement('div');
    overlay.className = 'overlay-modal';
    overlay.innerHTML = `
      <div class="modal-content">
        <div style="font-size: 3rem;">${isPerfect ? '🔓🎉' : '🔐'}</div>
        <h3 class="modal-title" style="color: ${isPerfect ? 'var(--neon-green)' : 'var(--neon-cyan)'};">
          ${isPerfect ? 'VAULT CRACKED!' : 'MISSION COMPLETE'}
        </h3>
        <p style="color: var(--text-secondary);">
          Secret Code was: <strong style="color: var(--neon-cyan); letter-spacing: 2px;">${this.secretCode.join(' ')}</strong>
        </p>
        <div style="background: rgba(0,0,0,0.4); padding: 14px; border-radius: var(--radius-md);">
          <div style="font-size: 0.8rem; color: var(--text-muted);">FINAL SCORE</div>
          <div style="font-size: 2rem; font-weight: 900; color: var(--neon-amber);">${this.totalScore} PTS</div>
          <div style="font-size: 0.85rem; color: var(--neon-purple); font-weight: 800; margin-top: 4px;">RANK: ${rank}</div>
        </div>
        <div style="display: flex; gap: 10px; margin-top: 8px;">
          <button class="nav-btn" style="flex: 1;" id="ctc-modal-hub">Arcade Hub</button>
          <button class="play-btn" style="flex: 1;" id="ctc-modal-replay">Play Again</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#ctc-modal-hub').addEventListener('click', () => {
      overlay.remove();
      this.destroy();
      this.onExit();
    });

    overlay.querySelector('#ctc-modal-replay').addEventListener('click', () => {
      overlay.remove();
      this.currentRound = 1;
      this.totalScore = 0;
      this.history = [];
      this.currentGuess = [];
      this.isGameOver = false;
      this.generateSecretCode();
      this.render();
      this.attachEvents();
    });
  }

  destroy() {
    if (this.keyHandler) {
      window.removeEventListener('keydown', this.keyHandler);
    }
  }
}

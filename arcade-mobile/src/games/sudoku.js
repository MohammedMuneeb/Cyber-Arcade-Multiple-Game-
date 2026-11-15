import { sounds } from '../audio.js';

// Predefined validated boards for performance and reliability
const BOARDS = {
  easy: {
    initial: [
      [5, 3, 0, 0, 7, 0, 0, 0, 0],
      [6, 0, 0, 1, 9, 5, 0, 0, 0],
      [0, 9, 8, 0, 0, 0, 0, 6, 0],
      [8, 0, 0, 0, 6, 0, 0, 0, 3],
      [4, 0, 0, 8, 0, 3, 0, 0, 1],
      [7, 0, 0, 0, 2, 0, 0, 0, 6],
      [0, 6, 0, 0, 0, 0, 2, 8, 0],
      [0, 0, 0, 4, 1, 9, 0, 0, 5],
      [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
  },
  medium: {
    initial: [
      [0, 0, 0, 6, 0, 0, 4, 0, 0],
      [7, 0, 0, 0, 0, 3, 6, 0, 0],
      [0, 0, 0, 0, 9, 1, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 5, 0, 1, 8, 0, 0, 0, 3],
      [0, 0, 0, 3, 0, 6, 0, 4, 5],
      [0, 4, 0, 2, 0, 0, 0, 6, 0],
      [9, 0, 3, 0, 0, 0, 0, 0, 0],
      [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ]
  }
};

export class SudokuGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.difficulty = 'easy';
    this.board = [];
    this.initial = [];
    this.selected = { r: -1, c: -1 };
    this.mistakes = 0;
    this.timer = 0;

    this.init();
  }

  init() {
    this.loadBoard();
    this.render();
    this.attachEvents();
    this.startTimer();
  }

  loadBoard() {
    const raw = BOARDS[this.difficulty].initial;
    this.initial = raw.map((r) => [...r]);
    this.board = raw.map((r) => [...r]);
    this.selected = { r: -1, c: -1 };
    this.mistakes = 0;
  }

  render() {
    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; width: 100%; max-width: 440px; margin: 0 auto; gap: 12px;">
        <!-- Top Info -->
        <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono);">
          <div>
            <span class="card-tag">SUDOKU MASTER</span>
            <span style="color: var(--neon-cyan); margin-left: 6px; text-transform: uppercase;">${this.difficulty}</span>
          </div>
          <div style="color: var(--neon-amber); font-weight: 800;">
            ⏱️ <span id="sdk-timer">00:00</span>
          </div>
        </div>

        <!-- 9x9 Grid -->
        <div class="sdk-grid" style="
          display: grid;
          grid-template-columns: repeat(9, 1fr);
          background: #080b12;
          padding: 6px;
          border-radius: var(--radius-md);
          border: 2px solid var(--border-glow);
          gap: 2px;
        ">
          ${this.board
            .map((row, r) =>
              row
                .map((val, c) => {
                  const isFixed = this.initial[r][c] !== 0;
                  const isSelected = this.selected.r === r && this.selected.c === c;
                  const borderRight = (c + 1) % 3 === 0 && c !== 8 ? '2px solid var(--neon-cyan)' : '1px solid rgba(255,255,255,0.06)';
                  const borderBottom = (r + 1) % 3 === 0 && r !== 8 ? '2px solid var(--neon-cyan)' : '1px solid rgba(255,255,255,0.06)';

                  return `
                    <button class="sdk-cell" data-r="${r}" data-c="${c}" style="
                      aspect-ratio: 1/1;
                      background: ${isSelected ? 'rgba(0, 229, 255, 0.25)' : isFixed ? 'rgba(255, 255, 255, 0.04)' : 'transparent'};
                      border: none;
                      border-right: ${borderRight};
                      border-bottom: ${borderBottom};
                      color: ${isFixed ? 'var(--text-secondary)' : 'var(--neon-green)'};
                      font-weight: 900;
                      font-family: var(--font-mono);
                      font-size: 1.2rem;
                      cursor: pointer;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                    ">
                      ${val !== 0 ? val : ''}
                    </button>
                  `;
                })
                .join('')
            )
            .join('')}
        </div>

        <!-- Touch Number Pad -->
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px;">
          ${[1, 2, 3, 4, 5, 6, 7, 8, 9]
            .map(
              (n) => `
            <button class="ctc-key sdk-numpad" data-val="${n}" style="padding: 10px 0; font-size: 1.2rem;">${n}</button>
          `
            )
            .join('')}
          <button class="ctc-key action-key" id="sdk-clear" style="padding: 10px 0;">CLR</button>
        </div>
      </div>
    `;
  }

  attachEvents() {
    this.container.querySelectorAll('.sdk-cell').forEach((cell) => {
      cell.addEventListener('click', () => {
        sounds.click();
        const r = parseInt(cell.getAttribute('data-r'), 10);
        const c = parseInt(cell.getAttribute('data-c'), 10);
        this.selected = { r, c };
        this.render();
        this.attachEvents();
      });
    });

    this.container.querySelectorAll('.sdk-numpad').forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = parseInt(btn.getAttribute('data-val'), 10);
        this.setCellValue(val);
      });
    });

    const clr = this.container.querySelector('#sdk-clear');
    if (clr) {
      clr.addEventListener('click', () => {
        sounds.click();
        this.setCellValue(0);
      });
    }
  }

  setCellValue(val) {
    const { r, c } = this.selected;
    if (r === -1 || c === -1) return;
    if (this.initial[r][c] !== 0) return; // Cannot edit initial fixed cell

    sounds.keypadPress();
    this.board[r][c] = val;
    this.render();
    this.attachEvents();

    if (this.checkComplete()) {
      sounds.vaultUnlock();
      if (this.onScoreUpdate) {
        this.onScoreUpdate('sudoku', 500);
      }
    }
  }

  checkComplete() {
    return this.board.every((row) => row.every((val) => val > 0));
  }

  startTimer() {
    this.timerInterval = setInterval(() => {
      this.timer++;
      const el = this.container.querySelector('#sdk-timer');
      if (el) {
        const m = String(Math.floor(this.timer / 60)).padStart(2, '0');
        const s = String(this.timer % 60).padStart(2, '0');
        el.textContent = `${m}:${s}`;
      }
    }, 1000);
  }

  destroy() {
    clearInterval(this.timerInterval);
  }
}

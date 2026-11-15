import { sounds } from '../audio.js';

export class TicTacToeGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.board = Array(9).fill(null);
    this.currentPlayer = 'X';
    this.vsAI = true;
    this.scores = { X: 0, O: 0, ties: 0 };
    this.gameOver = false;
    this.winningCombo = null;

    this.init();
  }

  init() {
    this.render();
    this.attachEvents();
  }

  render() {
    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; width: 100%; max-width: 420px; margin: 0 auto; gap: 16px;">
        <!-- Top Bar -->
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <button class="nav-btn" id="ttt-mode-btn">
            Mode: ${this.vsAI ? '🤖 vs Smart AI' : '👥 2-Player'}
          </button>
          <div style="font-family: var(--font-mono); font-weight: 800; color: var(--neon-cyan);">
            TURN: <span style="color: ${this.currentPlayer === 'X' ? 'var(--neon-cyan)' : 'var(--neon-pink)'}">${this.currentPlayer}</span>
          </div>
        </div>

        <!-- Scoreboard -->
        <div style="display: flex; gap: 10px; justify-content: space-around; background: var(--bg-card); padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--border-color); font-family: var(--font-mono); font-weight: 800;">
          <div style="color: var(--neon-cyan);">X: ${this.scores.X}</div>
          <div style="color: var(--text-muted);">TIES: ${this.scores.ties}</div>
          <div style="color: var(--neon-pink);">O: ${this.scores.O}</div>
        </div>

        <!-- 3x3 Grid -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; aspect-ratio: 1/1;">
          ${this.board
            .map(
              (cell, idx) => `
            <button class="ttt-cell ${this.winningCombo && this.winningCombo.includes(idx) ? 'win' : ''}" 
                    data-cell-idx="${idx}"
                    style="
                      background: var(--bg-card);
                      border: 2px solid ${cell === 'X' ? 'var(--neon-cyan)' : cell === 'O' ? 'var(--neon-pink)' : 'var(--border-color)'};
                      border-radius: var(--radius-md);
                      font-size: 2.8rem;
                      font-weight: 900;
                      font-family: var(--font-mono);
                      color: ${cell === 'X' ? 'var(--neon-cyan)' : 'var(--neon-pink)'};
                      cursor: pointer;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                      box-shadow: ${cell ? (cell === 'X' ? 'var(--shadow-glow-cyan)' : 'var(--shadow-glow-purple)') : 'none'};
                      transition: all 0.15s;
                    ">
              ${cell || ''}
            </button>
          `
            )
            .join('')}
        </div>

        <button class="nav-btn" id="ttt-reset-btn" style="width: 100%; justify-content: center; margin-top: 6px;">
          🔄 Reset Board
        </button>
      </div>
    `;
  }

  attachEvents() {
    this.container.querySelectorAll('.ttt-cell').forEach((cell) => {
      cell.addEventListener('click', () => {
        const idx = parseInt(cell.getAttribute('data-cell-idx'), 10);
        this.makeMove(idx);
      });
    });

    const modeBtn = this.container.querySelector('#ttt-mode-btn');
    if (modeBtn) {
      modeBtn.addEventListener('click', () => {
        sounds.click();
        this.vsAI = !this.vsAI;
        this.resetGame();
      });
    }

    const resetBtn = this.container.querySelector('#ttt-reset-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        sounds.click();
        this.resetGame();
      });
    }
  }

  makeMove(idx) {
    if (this.board[idx] || this.gameOver) return;

    sounds.keypadPress();
    this.board[idx] = this.currentPlayer;

    const winner = this.checkWinner();
    if (winner) {
      this.handleEnd(winner);
      return;
    }

    if (this.board.every((c) => c !== null)) {
      this.handleEnd('tie');
      return;
    }

    this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
    this.render();
    this.attachEvents();

    if (this.vsAI && this.currentPlayer === 'O' && !this.gameOver) {
      setTimeout(() => this.makeAIMove(), 350);
    }
  }

  makeAIMove() {
    // Minimax optimal move
    const bestMove = this.getBestMove();
    if (bestMove !== -1) {
      this.makeMove(bestMove);
    }
  }

  getBestMove() {
    // 1. Can AI win now?
    for (let i = 0; i < 9; i++) {
      if (!this.board[i]) {
        this.board[i] = 'O';
        if (this.checkWinner() === 'O') {
          this.board[i] = null;
          return i;
        }
        this.board[i] = null;
      }
    }
    // 2. Can player win? Block!
    for (let i = 0; i < 9; i++) {
      if (!this.board[i]) {
        this.board[i] = 'X';
        if (this.checkWinner() === 'X') {
          this.board[i] = null;
          return i;
        }
        this.board[i] = null;
      }
    }
    // 3. Take Center
    if (!this.board[4]) return 4;
    // 4. Take Corners
    const corners = [0, 2, 6, 8].filter((c) => !this.board[c]);
    if (corners.length > 0) return corners[Math.floor(Math.random() * corners.length)];
    // 5. Any open
    const open = [1, 3, 5, 7].filter((c) => !this.board[c]);
    return open[0] !== undefined ? open[0] : -1;
  }

  checkWinner() {
    const lines = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6]
    ];
    for (const combo of lines) {
      const [a, b, c] = combo;
      if (this.board[a] && this.board[a] === this.board[b] && this.board[a] === this.board[c]) {
        this.winningCombo = combo;
        return this.board[a];
      }
    }
    return null;
  }

  handleEnd(result) {
    this.gameOver = true;
    if (result === 'tie') {
      sounds.wrong();
      this.scores.ties++;
    } else {
      sounds.match();
      this.scores[result]++;
      if (this.onScoreUpdate && result === 'X') {
        this.onScoreUpdate('tictactoe', this.scores.X * 50);
      }
    }
    this.render();
    this.attachEvents();
  }

  resetGame() {
    this.board = Array(9).fill(null);
    this.currentPlayer = 'X';
    this.gameOver = false;
    this.winningCombo = null;
    this.render();
    this.attachEvents();
  }

  destroy() {}
}

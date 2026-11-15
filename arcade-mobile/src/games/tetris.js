import { sounds } from '../audio.js';

const SHAPES = [
  [[1, 1, 1, 1]], // I
  [[1, 1], [1, 1]], // O
  [[0, 1, 0], [1, 1, 1]], // T
  [[0, 0, 1], [1, 1, 1]], // L
  [[1, 0, 0], [1, 1, 1]], // J
  [[0, 1, 1], [1, 1, 0]], // S
  [[1, 1, 0], [0, 1, 1]] // Z
];

const COLORS = [
  '#00e5ff', // cyan
  '#ffb700', // yellow
  '#bd00ff', // purple
  '#ff8800', // orange
  '#0066ff', // blue
  '#00ff9d', // green
  '#ff4757' // red
];

export class TetrisGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.cols = 10;
    this.rows = 20;
    this.grid = Array.from({ length: this.rows }, () => Array(this.cols).fill(0));

    this.score = 0;
    this.lines = 0;
    this.level = 1;
    this.gameOver = false;
    this.dropInterval = 800;
    this.lastDrop = 0;

    this.currentPiece = null;
    this.nextPiece = null;

    this.init();
  }

  init() {
    this.render();
    this.setupCanvas();
    this.currentPiece = this.getPiece();
    this.nextPiece = this.getPiece();
    this.attachControls();
    this.startLoop();
  }

  render() {
    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; width: 100%; height: 100%; align-items: center;">
        <div style="display: flex; justify-content: space-between; width: 100%; max-width: 380px; margin-bottom: 8px; font-family: var(--font-mono);">
          <div style="color: var(--neon-cyan); font-weight: 800;">SCORE: <span id="tetris-score">${this.score}</span></div>
          <div style="color: var(--neon-amber); font-weight: 700;">LVL: <span id="tetris-level">${this.level}</span></div>
          <div style="color: var(--neon-green); font-weight: 700;">LINES: <span id="tetris-lines">${this.lines}</span></div>
        </div>

        <div class="canvas-wrapper" style="aspect-ratio: 1/2; max-width: 340px; max-height: 58vh;">
          <canvas class="game-canvas" id="tetris-canvas"></canvas>
        </div>

        <!-- Mobile Touch Controls -->
        <div class="touch-controls-bar" style="max-width: 360px; width: 100%;">
          <div class="dpad-group">
            <button class="touch-btn" id="tet-left">◀</button>
            <button class="touch-btn" id="tet-down">▼</button>
            <button class="touch-btn" id="tet-right">▶</button>
          </div>
          <div class="action-group">
            <button class="touch-btn" id="tet-rotate" style="background: rgba(189, 0, 255, 0.2); border-color: var(--neon-purple); color: var(--neon-purple);">↻</button>
            <button class="touch-btn fire-btn" id="tet-hard-drop">⏬</button>
          </div>
        </div>
      </div>
    `;
  }

  setupCanvas() {
    this.canvas = this.container.querySelector('#tetris-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.blockSize = 26;
    this.canvas.width = this.cols * this.blockSize;
    this.canvas.height = this.rows * this.blockSize;
  }

  getPiece() {
    const idx = Math.floor(Math.random() * SHAPES.length);
    const shape = SHAPES[idx];
    return {
      shape,
      color: COLORS[idx],
      colorIdx: idx + 1,
      x: Math.floor((this.cols - shape[0].length) / 2),
      y: 0
    };
  }

  attachControls() {
    this.keyHandler = (e) => {
      if (this.gameOver) return;
      if (e.code === 'ArrowLeft' || e.code === 'KeyA') this.move(-1);
      else if (e.code === 'ArrowRight' || e.code === 'KeyD') this.move(1);
      else if (e.code === 'ArrowDown' || e.code === 'KeyS') this.drop();
      else if (e.code === 'ArrowUp' || e.code === 'KeyW') this.rotate();
      else if (e.code === 'Space') {
        this.hardDrop();
        e.preventDefault();
      }
    };
    window.addEventListener('keydown', this.keyHandler);

    // Touch Bindings
    const bindBtn = (id, fn) => {
      const btn = this.container.querySelector(id);
      if (btn) {
        btn.addEventListener('pointerdown', (e) => {
          e.preventDefault();
          fn();
        });
      }
    };

    bindBtn('#tet-left', () => this.move(-1));
    bindBtn('#tet-right', () => this.move(1));
    bindBtn('#tet-down', () => this.drop());
    bindBtn('#tet-rotate', () => this.rotate());
    bindBtn('#tet-hard-drop', () => this.hardDrop());
  }

  collide(piece, offset = { x: 0, y: 0 }) {
    for (let r = 0; r < piece.shape.length; r++) {
      for (let c = 0; c < piece.shape[r].length; c++) {
        if (piece.shape[r][c]) {
          const nx = piece.x + c + offset.x;
          const ny = piece.y + r + offset.y;
          if (nx < 0 || nx >= this.cols || ny >= this.rows) return true;
          if (ny >= 0 && this.grid[ny][nx]) return true;
        }
      }
    }
    return false;
  }

  move(dir) {
    if (!this.collide(this.currentPiece, { x: dir, y: 0 })) {
      sounds.click();
      this.currentPiece.x += dir;
    }
  }

  rotate() {
    const rotated = this.currentPiece.shape[0].map((_, i) =>
      this.currentPiece.shape.map((row) => row[i]).reverse()
    );
    const test = { ...this.currentPiece, shape: rotated };
    if (!this.collide(test)) {
      sounds.keypadPress();
      this.currentPiece.shape = rotated;
    }
  }

  drop() {
    if (!this.collide(this.currentPiece, { x: 0, y: 1 })) {
      this.currentPiece.y++;
    } else {
      this.lockPiece();
    }
  }

  hardDrop() {
    sounds.keypadPress();
    while (!this.collide(this.currentPiece, { x: 0, y: 1 })) {
      this.currentPiece.y++;
    }
    this.lockPiece();
  }

  lockPiece() {
    sounds.click();
    for (let r = 0; r < this.currentPiece.shape.length; r++) {
      for (let c = 0; c < this.currentPiece.shape[r].length; c++) {
        if (this.currentPiece.shape[r][c]) {
          const ny = this.currentPiece.y + r;
          const nx = this.currentPiece.x + c;
          if (ny < 0) {
            this.endGame();
            return;
          }
          this.grid[ny][nx] = this.currentPiece.colorIdx;
        }
      }
    }

    this.clearLines();
    this.currentPiece = this.nextPiece;
    this.nextPiece = this.getPiece();

    if (this.collide(this.currentPiece)) {
      this.endGame();
    }
  }

  clearLines() {
    let cleared = 0;
    for (let r = this.rows - 1; r >= 0; r--) {
      if (this.grid[r].every((cell) => cell > 0)) {
        this.grid.splice(r, 1);
        this.grid.unshift(Array(this.cols).fill(0));
        cleared++;
        r++;
      }
    }

    if (cleared > 0) {
      sounds.match();
      this.lines += cleared;
      const pts = [0, 100, 300, 500, 800][cleared] * this.level;
      this.score += pts;
      this.level = Math.floor(this.lines / 10) + 1;
      this.dropInterval = Math.max(150, 800 - (this.level - 1) * 60);

      this.updateHud();
    }
  }

  updateHud() {
    const s = this.container.querySelector('#tetris-score');
    if (s) s.textContent = this.score;
    const l = this.container.querySelector('#tetris-level');
    if (l) l.textContent = this.level;
    const ln = this.container.querySelector('#tetris-lines');
    if (ln) ln.textContent = this.lines;
  }

  startLoop() {
    this.loop = (time = 0) => {
      if (!this.lastDrop) this.lastDrop = time;
      if (time - this.lastDrop > this.dropInterval && !this.gameOver) {
        this.drop();
        this.lastDrop = time;
      }
      this.draw();
      if (!this.destroyed) {
        this.animFrame = requestAnimationFrame(this.loop);
      }
    };
    this.animFrame = requestAnimationFrame(this.loop);
  }

  draw() {
    this.ctx.fillStyle = '#0a0d14';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw Grid
    this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    this.ctx.lineWidth = 1;
    for (let x = 0; x <= this.canvas.width; x += this.blockSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.canvas.height);
      this.ctx.stroke();
    }
    for (let y = 0; y <= this.canvas.height; y += this.blockSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.canvas.width, y);
      this.ctx.stroke();
    }

    // Draw placed blocks
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        if (this.grid[r][c]) {
          this.drawBlock(c, r, COLORS[this.grid[r][c] - 1]);
        }
      }
    }

    // Draw Current Piece
    if (this.currentPiece && !this.gameOver) {
      for (let r = 0; r < this.currentPiece.shape.length; r++) {
        for (let c = 0; c < this.currentPiece.shape[r].length; c++) {
          if (this.currentPiece.shape[r][c]) {
            this.drawBlock(this.currentPiece.x + c, this.currentPiece.y + r, this.currentPiece.color);
          }
        }
      }
    }
  }

  drawBlock(x, y, color) {
    const px = x * this.blockSize;
    const py = y * this.blockSize;
    this.ctx.fillStyle = color;
    this.ctx.fillRect(px + 1, py + 1, this.blockSize - 2, this.blockSize - 2);

    this.ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
    this.ctx.fillRect(px + 1, py + 1, this.blockSize - 2, 3);
  }

  endGame() {
    this.gameOver = true;
    sounds.gameOver();

    if (this.onScoreUpdate) {
      this.onScoreUpdate('tetris', this.score);
    }

    const overlay = document.createElement('div');
    overlay.className = 'overlay-modal';
    overlay.innerHTML = `
      <div class="modal-content">
        <div style="font-size: 3rem;">🧱👾</div>
        <h3 class="modal-title" style="color: var(--neon-amber);">GAME OVER</h3>
        <p style="color: var(--text-secondary);">Playfield reached top limit!</p>
        <div style="background: rgba(0,0,0,0.4); padding: 14px; border-radius: var(--radius-md);">
          <div style="font-size: 0.8rem; color: var(--text-muted);">FINAL SCORE</div>
          <div style="font-size: 2.2rem; font-weight: 900; color: var(--neon-amber);">${this.score} PTS</div>
          <div style="font-size: 0.85rem; color: var(--neon-green); font-weight: 700; margin-top: 4px;">
            Lines Cleared: ${this.lines}
          </div>
        </div>
        <div style="display: flex; gap: 10px; margin-top: 8px;">
          <button class="nav-btn" style="flex: 1;" id="tet-modal-hub">Arcade Hub</button>
          <button class="play-btn" style="flex: 1;" id="tet-modal-replay">Play Again</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#tet-modal-hub').addEventListener('click', () => {
      overlay.remove();
      this.destroy();
      this.onExit();
    });

    overlay.querySelector('#tet-modal-replay').addEventListener('click', () => {
      overlay.remove();
      this.grid = Array.from({ length: this.rows }, () => Array(this.cols).fill(0));
      this.score = 0;
      this.lines = 0;
      this.level = 1;
      this.gameOver = false;
      this.currentPiece = this.getPiece();
      this.nextPiece = this.getPiece();
      this.updateHud();
    });
  }

  destroy() {
    this.destroyed = true;
    if (this.animFrame) cancelAnimationFrame(this.animFrame);
    window.removeEventListener('keydown', this.keyHandler);
  }
}

import { sounds } from '../audio.js';

export class AsteroidsGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.score = 0;
    this.lives = 3;
    this.wave = 1;
    this.gameOver = false;

    this.keys = { left: false, right: false, thrust: false, fire: false };
    this.lasers = [];
    this.asteroids = [];
    this.particles = [];

    this.init();
  }

  init() {
    this.render();
    this.setupCanvas();
    this.resetShip();
    this.spawnAsteroids(4);
    this.attachControls();
    this.startLoop();
  }

  render() {
    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; width: 100%; height: 100%;">
        <!-- Top HUD -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-family: var(--font-mono);">
          <div style="font-size: 1.1rem; color: var(--neon-cyan); font-weight: 800;">
            SCORE: <span id="ast-score">${this.score}</span>
          </div>
          <div style="font-size: 0.95rem; color: var(--neon-amber); font-weight: 700;">
            WAVE <span id="ast-wave">${this.wave}</span>
          </div>
          <div style="font-size: 1.1rem; color: var(--neon-pink);">
            LIVES: <span id="ast-lives">${'▲ '.repeat(this.lives)}</span>
          </div>
        </div>

        <!-- Canvas Wrapper -->
        <div class="canvas-wrapper" id="ast-wrapper">
          <canvas class="game-canvas" id="ast-canvas"></canvas>
        </div>

        <!-- Mobile Touch Controls Bar -->
        <div class="touch-controls-bar">
          <div class="dpad-group">
            <button class="touch-btn" id="btn-rot-left" aria-label="Rotate Left">◀</button>
            <button class="touch-btn" id="btn-rot-right" aria-label="Rotate Right">▶</button>
          </div>
          <div class="action-group">
            <button class="touch-btn" id="btn-thrust" aria-label="Thrust Ship">🚀</button>
            <button class="touch-btn fire-btn" id="btn-fire" aria-label="Fire Cannon">💥</button>
          </div>
        </div>
      </div>
    `;
  }

  setupCanvas() {
    this.canvas = this.container.querySelector('#ast-canvas');
    this.ctx = this.canvas.getContext('2d');

    // Internal virtual resolution
    this.width = 800;
    this.height = 600;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  resetShip() {
    this.ship = {
      x: this.width / 2,
      y: this.height / 2,
      angle: 0, // facing up
      vx: 0,
      vy: 0,
      radius: 14,
      rotationSpeed: 0.08,
      acceleration: 0.25,
      friction: 0.985,
      maxSpeed: 7,
      isThrusting: false,
      invulnerable: 90
    };
  }

  spawnAsteroids(count) {
    for (let i = 0; i < count; i++) {
      let x, y, dist;
      do {
        x = Math.random() * this.width;
        y = Math.random() * this.height;
        dist = Math.hypot(x - this.ship.x, y - this.ship.y);
      } while (dist < 150);

      this.asteroids.push(this.createAsteroid(x, y, 36, 1));
    }
  }

  createAsteroid(x, y, radius, level) {
    const vertexCount = Math.floor(Math.random() * 5) + 8;
    const offsets = [];
    for (let i = 0; i < vertexCount; i++) {
      offsets.push(radius * (0.75 + Math.random() * 0.5));
    }

    const angle = Math.random() * Math.PI * 2;
    const speed = (0.8 + Math.random() * 1.4) * (4 / level);

    return {
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      radius,
      level,
      rotAngle: 0,
      rotSpeed: (Math.random() - 0.5) * 0.03,
      vertexCount,
      offsets
    };
  }

  attachControls() {
    // Keyboard handlers
    this.keyDown = (e) => {
      if (e.code === 'ArrowLeft' || e.code === 'KeyA') this.keys.left = true;
      if (e.code === 'ArrowRight' || e.code === 'KeyD') this.keys.right = true;
      if (e.code === 'ArrowUp' || e.code === 'KeyW') this.keys.thrust = true;
      if (e.code === 'Space') {
        this.fireLaser();
        e.preventDefault();
      }
    };

    this.keyUp = (e) => {
      if (e.code === 'ArrowLeft' || e.code === 'KeyA') this.keys.left = false;
      if (e.code === 'ArrowRight' || e.code === 'KeyD') this.keys.right = false;
      if (e.code === 'ArrowUp' || e.code === 'KeyW') this.keys.thrust = false;
    };

    window.addEventListener('keydown', this.keyDown);
    window.addEventListener('keyup', this.keyUp);

    // Touch Buttons
    const bindTouch = (id, keyName, isPulse = false) => {
      const btn = this.container.querySelector(id);
      if (!btn) return;

      const start = (e) => {
        e.preventDefault();
        btn.classList.add('pressed');
        if (isPulse) {
          this.fireLaser();
        } else {
          this.keys[keyName] = true;
        }
      };

      const end = (e) => {
        e.preventDefault();
        btn.classList.remove('pressed');
        if (!isPulse) {
          this.keys[keyName] = false;
        }
      };

      btn.addEventListener('pointerdown', start);
      btn.addEventListener('pointerup', end);
      btn.addEventListener('pointercancel', end);
      btn.addEventListener('pointerleave', end);
    };

    bindTouch('#btn-rot-left', 'left');
    bindTouch('#btn-rot-right', 'right');
    bindTouch('#btn-thrust', 'thrust');
    bindTouch('#btn-fire', null, true);
  }

  fireLaser() {
    if (this.gameOver) return;
    if (this.lasers.length >= 8) return;

    sounds.laser();

    const tipX = this.ship.x + Math.sin(this.ship.angle) * 18;
    const tipY = this.ship.y - Math.cos(this.ship.angle) * 18;

    this.lasers.push({
      x: tipX,
      y: tipY,
      vx: Math.sin(this.ship.angle) * 10 + this.ship.vx * 0.4,
      vy: -Math.cos(this.ship.angle) * 10 + this.ship.vy * 0.4,
      life: 45
    });
  }

  spawnExplosion(x, y, count = 15, color = '#00e5ff') {
    sounds.explosion();
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 4 + 1;
      this.particles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 30 + Math.random() * 20,
        color
      });
    }
  }

  startLoop() {
    this.loop = () => {
      this.update();
      this.draw();
      if (!this.destroyed) {
        this.animationFrame = requestAnimationFrame(this.loop);
      }
    };
    this.animationFrame = requestAnimationFrame(this.loop);
  }

  update() {
    if (this.gameOver) return;

    // Ship rotation & thrust
    if (this.keys.left) this.ship.angle -= this.ship.rotationSpeed;
    if (this.keys.right) this.ship.angle += this.ship.rotationSpeed;

    this.ship.isThrusting = this.keys.thrust;
    if (this.ship.isThrusting) {
      this.ship.vx += Math.sin(this.ship.angle) * this.ship.acceleration;
      this.ship.vy -= Math.cos(this.ship.angle) * this.ship.acceleration;

      const speed = Math.hypot(this.ship.vx, this.ship.vy);
      if (speed > this.ship.maxSpeed) {
        this.ship.vx = (this.ship.vx / speed) * this.ship.maxSpeed;
        this.ship.vy = (this.ship.vy / speed) * this.ship.maxSpeed;
      }
    }

    this.ship.x += this.ship.vx;
    this.ship.y += this.ship.vy;
    this.ship.vx *= this.ship.friction;
    this.ship.vy *= this.ship.friction;

    // Ship screen wrap
    if (this.ship.x < 0) this.ship.x = this.width;
    else if (this.ship.x > this.width) this.ship.x = 0;
    if (this.ship.y < 0) this.ship.y = this.height;
    else if (this.ship.y > this.height) this.ship.y = 0;

    if (this.ship.invulnerable > 0) this.ship.invulnerable--;

    // Update lasers
    for (let i = this.lasers.length - 1; i >= 0; i--) {
      const l = this.lasers[i];
      l.x += l.vx;
      l.y += l.vy;
      l.life--;

      if (l.x < 0) l.x = this.width;
      else if (l.x > this.width) l.x = 0;
      if (l.y < 0) l.y = this.height;
      else if (l.y > this.height) l.y = 0;

      if (l.life <= 0) {
        this.lasers.splice(i, 1);
      }
    }

    // Update asteroids
    for (const a of this.asteroids) {
      a.x += a.vx;
      a.y += a.vy;
      a.rotAngle += a.rotSpeed;

      if (a.x < -a.radius) a.x = this.width + a.radius;
      else if (a.x > this.width + a.radius) a.x = -a.radius;
      if (a.y < -a.radius) a.y = this.height + a.radius;
      else if (a.y > this.height + a.radius) a.y = -a.radius;
    }

    // Update particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life--;
      if (p.life <= 0) this.particles.splice(i, 1);
    }

    // Collisions: Lasers vs Asteroids
    for (let i = this.lasers.length - 1; i >= 0; i--) {
      const l = this.lasers[i];
      for (let j = this.asteroids.length - 1; j >= 0; j--) {
        const a = this.asteroids[j];
        if (Math.hypot(l.x - a.x, l.y - a.y) < a.radius) {
          // Hit!
          this.lasers.splice(i, 1);
          this.spawnExplosion(a.x, a.y, 16, '#00e5ff');

          // Score
          const pts = a.level === 1 ? 20 : a.level === 2 ? 50 : 100;
          this.score += pts;
          this.updateHud();

          // Split asteroid
          if (a.level < 3) {
            this.asteroids.push(this.createAsteroid(a.x, a.y, a.radius * 0.6, a.level + 1));
            this.asteroids.push(this.createAsteroid(a.x, a.y, a.radius * 0.6, a.level + 1));
          }
          this.asteroids.splice(j, 1);
          break;
        }
      }
    }

    // Collisions: Ship vs Asteroids
    if (this.ship.invulnerable === 0) {
      for (let i = 0; i < this.asteroids.length; i++) {
        const a = this.asteroids[i];
        if (Math.hypot(this.ship.x - a.x, this.ship.y - a.y) < this.ship.radius + a.radius * 0.75) {
          // Ship hit!
          this.spawnExplosion(this.ship.x, this.ship.y, 25, '#ff4757');
          this.lives--;
          this.updateHud();

          if (this.lives <= 0) {
            this.endGame();
          } else {
            this.resetShip();
          }
          break;
        }
      }
    }

    // Next wave check
    if (this.asteroids.length === 0) {
      this.wave++;
      this.updateHud();
      this.spawnAsteroids(3 + this.wave);
    }
  }

  updateHud() {
    const s = this.container.querySelector('#ast-score');
    if (s) s.textContent = this.score;
    const w = this.container.querySelector('#ast-wave');
    if (w) w.textContent = this.wave;
    const l = this.container.querySelector('#ast-lives');
    if (l) l.textContent = '▲ '.repeat(Math.max(0, this.lives));
  }

  draw() {
    this.ctx.fillStyle = '#06080e';
    this.ctx.fillRect(0, 0, this.width, this.height);

    // Draw Ship
    if (!this.gameOver && (this.ship.invulnerable % 8 < 4)) {
      this.ctx.save();
      this.ctx.translate(this.ship.x, this.ship.y);
      this.ctx.rotate(this.ship.angle);

      this.ctx.strokeStyle = '#00e5ff';
      this.ctx.lineWidth = 2.5;
      this.ctx.beginPath();
      this.ctx.moveTo(0, -18);
      this.ctx.lineTo(-12, 14);
      this.ctx.lineTo(12, 14);
      this.ctx.closePath();
      this.ctx.stroke();

      // Thruster flame
      if (this.ship.isThrusting) {
        this.ctx.strokeStyle = '#ffb700';
        this.ctx.beginPath();
        this.ctx.moveTo(-6, 15);
        this.ctx.lineTo(0, 24 + Math.random() * 6);
        this.ctx.lineTo(6, 15);
        this.ctx.stroke();
      }

      this.ctx.restore();
    }

    // Draw Lasers
    this.ctx.fillStyle = '#00ff9d';
    this.ctx.shadowBlur = 8;
    this.ctx.shadowColor = '#00ff9d';
    for (const l of this.lasers) {
      this.ctx.beginPath();
      this.ctx.arc(l.x, l.y, 3, 0, Math.PI * 2);
      this.ctx.fill();
    }
    this.ctx.shadowBlur = 0;

    // Draw Asteroids
    this.ctx.strokeStyle = '#c0d0e6';
    this.ctx.lineWidth = 2;
    for (const a of this.asteroids) {
      this.ctx.save();
      this.ctx.translate(a.x, a.y);
      this.ctx.rotate(a.rotAngle);

      this.ctx.beginPath();
      for (let i = 0; i < a.vertexCount; i++) {
        const theta = (i / a.vertexCount) * Math.PI * 2;
        const r = a.offsets[i];
        const px = Math.cos(theta) * r;
        const py = Math.sin(theta) * r;
        if (i === 0) this.ctx.moveTo(px, py);
        else this.ctx.lineTo(px, py);
      }
      this.ctx.closePath();
      this.ctx.stroke();
      this.ctx.restore();
    }

    // Draw Particles
    for (const p of this.particles) {
      this.ctx.fillStyle = p.color;
      this.ctx.fillRect(p.x, p.y, 2.5, 2.5);
    }
  }

  endGame() {
    this.gameOver = true;
    sounds.gameOver();

    if (this.onScoreUpdate) {
      this.onScoreUpdate('asteroids', this.score);
    }

    const overlay = document.createElement('div');
    overlay.className = 'overlay-modal';
    overlay.innerHTML = `
      <div class="modal-content">
        <div style="font-size: 3rem;">💥🚀</div>
        <h3 class="modal-title" style="color: var(--neon-red);">SPACE ODYSSEY ENDED</h3>
        <p style="color: var(--text-secondary);">Your ship was destroyed in Wave ${this.wave}.</p>
        <div style="background: rgba(0,0,0,0.4); padding: 14px; border-radius: var(--radius-md);">
          <div style="font-size: 0.8rem; color: var(--text-muted);">FINAL SCORE</div>
          <div style="font-size: 2.2rem; font-weight: 900; color: var(--neon-amber);">${this.score} PTS</div>
        </div>
        <div style="display: flex; gap: 10px; margin-top: 8px;">
          <button class="nav-btn" style="flex: 1;" id="ast-modal-hub">Arcade Hub</button>
          <button class="play-btn" style="flex: 1;" id="ast-modal-replay">Play Again</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#ast-modal-hub').addEventListener('click', () => {
      overlay.remove();
      this.destroy();
      this.onExit();
    });

    overlay.querySelector('#ast-modal-replay').addEventListener('click', () => {
      overlay.remove();
      this.score = 0;
      this.lives = 3;
      this.wave = 1;
      this.gameOver = false;
      this.asteroids = [];
      this.lasers = [];
      this.particles = [];
      this.resetShip();
      this.spawnAsteroids(4);
      this.updateHud();
    });
  }

  destroy() {
    this.destroyed = true;
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
    window.removeEventListener('keydown', this.keyDown);
    window.removeEventListener('keyup', this.keyUp);
  }
}

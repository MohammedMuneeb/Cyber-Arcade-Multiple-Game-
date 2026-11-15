import { sounds } from '../audio.js';
export class ShootingClubGame {

  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.score = 0;
    this.shotsFired = 0;
    this.shotsHit = 0;
    this.streak = 0;
    this.bestStreak = 0;
    this.timeLeft = 60;
    this.isGameOver = false;
    this.destroyed = false;

    // Weapon profiles matching shooting_club.py
    this.weapons = {
      pistol: {
        id: 'pistol',
        name: 'P-9 Pistol',
        icon: '🔫',
        maxAmmo: 15,
        damage: 40,
        pellets: 1,
        spread: 0,
        recoilKick: 4,
        cooldown: 180
      },
      shotgun: {
        id: 'shotgun',
        name: '12G Breacher',
        icon: '💥',
        maxAmmo: 6,
        damage: 90,
        pellets: 6,
        spread: 28,
        recoilKick: 10,
        cooldown: 400
      },
      rifle: {
        id: 'rifle',
        name: 'Viper AR-15',
        icon: '⚡',
        maxAmmo: 30,
        damage: 50,
        pellets: 1,
        spread: 2,
        recoilKick: 5,
        cooldown: 120
      },
      sniper: {
        id: 'sniper',
        name: 'Hawkeye .308',
        icon: '🎯',
        maxAmmo: 5,
        damage: 130,
        pellets: 1,
        spread: 0,
        recoilKick: 12,
        cooldown: 600
      }
    };

    this.currentWeaponKey = 'pistol';
    this.ammo = this.weapons.pistol.maxAmmo;
    this.isReloading = false;
    this.lastShotTime = 0;

    this.targets = [];
    this.decals = []; // bullet holes
    this.particles = []; // hit sparks & dust
    this.popups = []; // floating score notifications

    this.canvas = null;
    this.ctx = null;
    this.animationId = null;
    this.timerInterval = null;
    this.targetSpawnInterval = null;

    this.screenKick = { x: 0, y: 0 };
    this.crosshairPos = { x: 0, y: 0 };

    this.init();
  }

  get currentWeapon() {
    return this.weapons[this.currentWeaponKey];
  }

  init() {
    this.render();
    this.setupCanvas();
    this.setupEvents();
    this.startTimers();
    this.startLoop();
  }

  render() {
    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; width: 100%; height: 100%; max-width: 800px; margin: 0 auto; gap: 8px;">
        <!-- Top HUD -->
        <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-card); padding: 8px 14px; border-radius: var(--radius-md); border: 1px solid var(--border-color); font-family: var(--font-mono);">
          <div style="display: flex; flex-direction: column;">
            <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase;">SCORE</span>
            <span style="font-size: 1.15rem; font-weight: 800; color: var(--neon-cyan);" id="sc-score">${this.score}</span>
          </div>

          <div style="display: flex; flex-direction: column; align-items: center;">
            <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase;">TIME LEFT</span>
            <span style="font-size: 1.15rem; font-weight: 800; color: ${this.timeLeft <= 10 ? 'var(--neon-red)' : 'var(--neon-amber)'};" id="sc-timer">${this.timeLeft}s</span>
          </div>

          <div style="display: flex; flex-direction: column; align-items: flex-end;">
            <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase;">STREAK</span>
            <span style="font-size: 1.15rem; font-weight: 800; color: var(--neon-green);" id="sc-streak">${this.streak}x</span>
          </div>
        </div>

        <!-- Weapon Tabs Bar -->
        <div style="display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding-bottom: 2px;">
          ${Object.values(this.weapons)
        .map(
          (w) => `
            <button class="sc-weapon-tab ${w.id === this.currentWeaponKey ? 'active' : ''}" data-weapon="${w.id}" style="
              flex: 1;
              min-width: 70px;
              background: ${w.id === this.currentWeaponKey ? 'rgba(0, 229, 255, 0.15)' : 'var(--bg-card)'};
              border: 1px solid ${w.id === this.currentWeaponKey ? 'var(--neon-cyan)' : 'var(--border-color)'};
              color: ${w.id === this.currentWeaponKey ? 'var(--neon-cyan)' : 'var(--text-secondary)'};
              padding: 6px 4px;
              border-radius: var(--radius-sm);
              cursor: pointer;
              font-family: var(--font-main);
              font-size: 0.75rem;
              font-weight: 700;
              display: flex;
              align-items: center;
              justify-content: center;
              gap: 4px;
            ">
              <span>${w.icon}</span>
              <span>${w.name.split(' ')[0]}</span>
            </button>
          `
        )
        .join('')}
        </div>

        <!-- Canvas Range Display -->
        <div style="position: relative; width: 100%; aspect-ratio: 16/10; max-height: 52vh; background: #0c0f17; border-radius: var(--radius-md); border: 2px solid var(--border-color); overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.6);" id="sc-canvas-box">
          <canvas id="sc-canvas" style="width: 100%; height: 100%; display: block; cursor: crosshair;"></canvas>
        </div>

        <!-- Bottom Mobile Action Bar (Ammo + Reload + Exit) -->
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 4px;">
          <!-- Ammo Indicator -->
          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 8px 16px; display: flex; align-items: center; gap: 8px; font-family: var(--font-mono);">
            <span style="font-size: 1.2rem;">⚡</span>
            <div style="display: flex; flex-direction: column;">
              <span style="font-size: 0.65rem; color: var(--text-muted);">AMMO</span>
              <span style="font-size: 1.1rem; font-weight: 800; color: ${this.ammo === 0 ? 'var(--neon-red)' : 'var(--neon-cyan)'};" id="sc-ammo">
                ${this.isReloading ? 'RELOADING...' : `${this.ammo} / ${this.currentWeapon.maxAmmo}`}
              </span>
            </div>
          </div>

          <!-- Quick Reload Button -->
          <button id="btn-sc-reload" class="play-btn" style="background: var(--neon-amber); color: #000; font-size: 0.85rem; padding: 10px 18px;" ${this.isReloading || this.ammo === this.currentWeapon.maxAmmo ? 'disabled' : ''}>
            🔄 RELOAD
          </button>

          <!-- Back Hub Button -->
          <button id="btn-sc-exit" class="nav-btn">
            ◀ Arcade
          </button>
        </div>
      </div>
    `;
  }

  setupCanvas() {
    this.canvas = this.container.querySelector('#sc-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width * (window.devicePixelRatio || 1);
    this.canvas.height = rect.height * (window.devicePixelRatio || 1);
    this.ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);

    this.crosshairPos = { x: rect.width / 2, y: rect.height / 2 };

    // Initial targets
    for (let i = 0; i < 4; i++) {
      this.spawnTarget();
    }
  }

  setupEvents() {
    // Weapon tab clicks
    const tabs = this.container.querySelectorAll('.sc-weapon-tab');
    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const weaponKey = tab.dataset.weapon;
        if (weaponKey !== this.currentWeaponKey && !this.isReloading) {
          sounds.click();
          this.currentWeaponKey = weaponKey;
          this.ammo = this.currentWeapon.maxAmmo;
          this.render();
          this.setupCanvas();
          this.setupEvents();
        }
      });
    });

    // Reload button
    const reloadBtn = this.container.querySelector('#btn-sc-reload');
    if (reloadBtn) {
      reloadBtn.addEventListener('click', () => this.reload());
    }

    // Exit button
    const exitBtn = this.container.querySelector('#btn-sc-exit');
    if (exitBtn) {
      exitBtn.addEventListener('click', () => {
        sounds.click();
        this.destroy();
        if (this.onExit) this.onExit();
      });
    }

    // Touch / Mouse on Canvas
    if (this.canvas) {
      const handleShoot = (e) => {
        e.preventDefault();
        if (this.isGameOver || this.isReloading) return;

        const rect = this.canvas.getBoundingClientRect();
        let clientX = e.clientX;
        let clientY = e.clientY;

        if (e.touches && e.touches.length > 0) {
          clientX = e.touches[0].clientX;
          clientY = e.touches[0].clientY;
        }

        const x = clientX - rect.left;
        const y = clientY - rect.top;
        this.crosshairPos = { x, y };

        this.fire(x, y);
      };

      this.canvas.addEventListener('pointerdown', handleShoot);
      this.canvas.addEventListener('pointermove', (e) => {
        const rect = this.canvas.getBoundingClientRect();
        this.crosshairPos = {
          x: e.clientX - rect.left,
          y: e.clientY - rect.top
        };
      });
    }
  }

  fire(x, y) {
    const now = Date.now();
    if (now - this.lastShotTime < this.currentWeapon.cooldown) return;

    if (this.ammo <= 0) {
      sounds.wrong();
      this.reload();
      return;
    }

    this.lastShotTime = now;
    this.ammo--;
    this.shotsFired++;
    sounds.gunshot(this.currentWeaponKey);

    // Apply screen kick recoil
    this.screenKick = {
      x: (Math.random() - 0.5) * this.currentWeapon.recoilKick,
      y: -this.currentWeapon.recoilKick * 1.5
    };

    let hitAny = false;
    const pellets = this.currentWeapon.pellets;

    for (let p = 0; p < pellets; p++) {
      const spreadX = (Math.random() - 0.5) * this.currentWeapon.spread;
      const spreadY = (Math.random() - 0.5) * this.currentWeapon.spread;
      const targetX = x + spreadX;
      const targetY = y + spreadY;

      // Add bullet hole decal
      this.decals.push({ x: targetX, y: targetY, life: 1.0 });

      // Check hit against active targets
      for (let i = this.targets.length - 1; i >= 0; i--) {
        const target = this.targets[i];
        const dist = Math.hypot(targetX - target.x, targetY - target.y);

        if (dist <= target.radius) {
          hitAny = true;
          this.handleTargetHit(target, targetX, targetY, dist);
          if (target.health <= 0) {
            this.targets.splice(i, 1);
          }
          break;
        }
      }
    }

    if (hitAny) {
      this.shotsHit++;
      this.streak++;
      if (this.streak > this.bestStreak) this.bestStreak = this.streak;
    } else {
      this.streak = 0;
    }

    this.updateHUD();
  }

  handleTargetHit(target, hitX, hitY, dist) {
    if (target.type === 'hostage') {
      // Hostage hit: heavy penalty!
      target.health = 0;
      this.score = Math.max(0, this.score - 200);
      this.streak = 0;
      sounds.wrong();
      this.addPopup(hitX, hitY, 'NO-SHOOT! -200', 'var(--neon-red)');
      this.createParticles(hitX, hitY, '#ff4757', 15);
      return;
    }

    // Steel or Bullseye or Skeet
    sounds.ding();
    target.health -= this.currentWeapon.damage;

    // Precision calculation based on center proximity
    let basePoints = 50;
    let label = '+50';
    const accuracyRatio = 1 - dist / target.radius;

    if (accuracyRatio > 0.75) {
      basePoints = 150;
      label = 'BULLSEYE! +150';
      sounds.correct();
    } else if (accuracyRatio > 0.45) {
      basePoints = 100;
      label = 'GREAT! +100';
    }

    const multiplier = 1 + Math.min(Math.floor(this.streak / 3) * 0.2, 2.0);
    const awarded = Math.round(basePoints * multiplier);

    this.score += awarded;
    this.addPopup(hitX, hitY, `${label} (x${multiplier.toFixed(1)})`, 'var(--neon-green)');
    this.createParticles(hitX, hitY, target.type === 'steel' ? '#ffffff' : '#00e5ff', 12);
  }

  addPopup(x, y, text, color) {
    this.popups.push({ x, y, text, color, alpha: 1.0, dy: -1.2 });
  }

  createParticles(x, y, color, count = 8) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1 + Math.random() * 4;
      this.particles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        radius: 2 + Math.random() * 2.5,
        color,
        alpha: 1.0,
        decay: 0.03 + Math.random() * 0.04
      });
    }
  }

  reload() {
    if (this.isReloading) return;
    this.isReloading = true;
    sounds.reload();
    this.updateHUD();

    setTimeout(() => {
      this.ammo = this.currentWeapon.maxAmmo;
      this.isReloading = false;
      this.updateHUD();
    }, 900);
  }

  spawnTarget() {
    if (this.isGameOver || this.destroyed || !this.canvas) return;

    const rect = this.canvas.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;

    const r = Math.random();
    let type = 'bullseye';
    if (r < 0.4) type = 'steel';
    else if (r < 0.75) type = 'bullseye';
    else if (r < 0.9) type = 'skeet';
    else type = 'hostage';

    const radius = type === 'skeet' ? 18 : type === 'steel' ? 24 : 28;
    const padding = 40;

    let target = {
      x: padding + Math.random() * (width - padding * 2),
      y: padding + Math.random() * (height - padding * 2),
      radius,
      type,
      health: type === 'steel' ? 120 : 40,
      vx: type === 'skeet' ? (Math.random() > 0.5 ? 2.5 : -2.5) : 0,
      vy: type === 'skeet' ? (Math.random() - 0.5) * 1.5 : 0,
      lifespan: type === 'skeet' ? 3000 : 4500,
      born: Date.now()
    };

    this.targets.push(target);
  }

  startTimers() {
    // 60-second countdown
    this.timerInterval = setInterval(() => {
      if (this.timeLeft > 0) {
        this.timeLeft--;
        this.updateHUD();
      } else {
        this.endGame();
      }
    }, 1000);

    // Dynamic target spawner
    this.targetSpawnInterval = setInterval(() => {
      if (this.targets.length < 5) {
        this.spawnTarget();
      }
    }, 1200);
  }

  updateHUD() {
    const scoreEl = this.container.querySelector('#sc-score');
    if (scoreEl) scoreEl.textContent = this.score;

    const timerEl = this.container.querySelector('#sc-timer');
    if (timerEl) {
      timerEl.textContent = `${this.timeLeft}s`;
      timerEl.style.color = this.timeLeft <= 10 ? 'var(--neon-red)' : 'var(--neon-amber)';
    }

    const streakEl = this.container.querySelector('#sc-streak');
    if (streakEl) streakEl.textContent = `${this.streak}x`;

    const ammoEl = this.container.querySelector('#sc-ammo');
    if (ammoEl) {
      ammoEl.textContent = this.isReloading ? 'RELOADING...' : `${this.ammo} / ${this.currentWeapon.maxAmmo}`;
      ammoEl.style.color = this.ammo === 0 ? 'var(--neon-red)' : 'var(--neon-cyan)';
    }

    const reloadBtn = this.container.querySelector('#btn-sc-reload');
    if (reloadBtn) {
      reloadBtn.disabled = this.isReloading || this.ammo === this.currentWeapon.maxAmmo;
    }
  }

  startLoop() {
    const loop = () => {
      if (this.destroyed) return;
      this.updateAndDraw();
      this.animationId = requestAnimationFrame(loop);
    };
    this.animationId = requestAnimationFrame(loop);
  }

  updateAndDraw() {
    if (!this.canvas || !this.ctx) return;
    const rect = this.canvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;

    this.ctx.save();
    this.ctx.clearRect(0, 0, w, h);

    // Recoil recovery
    this.screenKick.x *= 0.8;
    this.screenKick.y *= 0.8;
    this.ctx.translate(this.screenKick.x, this.screenKick.y);

    // Background Tactical Shooting Range Grid
    this.ctx.fillStyle = '#0a0d14';
    this.ctx.fillRect(-20, -20, w + 40, h + 40);

    // Range distance markings
    this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    this.ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, h);
      this.ctx.stroke();
    }
    for (let y = 0; y < h; y += 40) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(w, y);
      this.ctx.stroke();
    }

    // Draw Bullet Holes
    this.ctx.fillStyle = '#1e2430';
    for (let i = this.decals.length - 1; i >= 0; i--) {
      const d = this.decals[i];
      this.ctx.beginPath();
      this.ctx.arc(d.x, d.y, 3, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.strokeStyle = 'rgba(0, 229, 255, 0.4)';
      this.ctx.stroke();
      d.life -= 0.005;
      if (d.life <= 0) this.decals.splice(i, 1);
    }

    // Draw Targets
    const now = Date.now();
    for (let i = this.targets.length - 1; i >= 0; i--) {
      const t = this.targets[i];
      // Update moving targets
      t.x += t.vx;
      t.y += t.vy;

      // Bounce skeet off edges
      if (t.x < t.radius || t.x > w - t.radius) t.vx *= -1;

      // Age expiry
      if (now - t.born > t.lifespan) {
        this.targets.splice(i, 1);
        continue;
      }

      this.drawTarget(t);
    }

    // Draw Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.alpha -= p.decay;

      if (p.alpha <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      this.ctx.save();
      this.ctx.globalAlpha = p.alpha;
      this.ctx.fillStyle = p.color;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    }

    // Draw Popups
    for (let i = this.popups.length - 1; i >= 0; i--) {
      const pop = this.popups[i];
      pop.y += pop.dy;
      pop.alpha -= 0.02;

      if (pop.alpha <= 0) {
        this.popups.splice(i, 1);
        continue;
      }

      this.ctx.save();
      this.ctx.globalAlpha = pop.alpha;
      this.ctx.font = 'bold 14px var(--font-mono)';
      this.ctx.fillStyle = pop.color;
      this.ctx.shadowColor = pop.color;
      this.ctx.shadowBlur = 8;
      this.ctx.textAlign = 'center';
      this.ctx.fillText(pop.text, pop.x, pop.y);
      this.ctx.restore();
    }

    // Draw Crosshair at pointer position
    this.drawCrosshair(this.crosshairPos.x, this.crosshairPos.y);

    this.ctx.restore();
  }

  drawTarget(target) {
    const { x, y, radius, type } = target;

    this.ctx.save();
    if (type === 'bullseye') {
      // Concentric rings
      const rings = [
        { r: radius, color: '#f0f4fc' },
        { r: radius * 0.75, color: '#101520' },
        { r: radius * 0.5, color: '#00e5ff' },
        { r: radius * 0.25, color: '#ff0077' }
      ];
      rings.forEach((ring) => {
        this.ctx.beginPath();
        this.ctx.arc(x, y, ring.r, 0, Math.PI * 2);
        this.ctx.fillStyle = ring.color;
        this.ctx.fill();
        this.ctx.strokeStyle = '#0a0d14';
        this.ctx.lineWidth = 1.5;
        this.ctx.stroke();
      });
    } else if (type === 'steel') {
      // Reactive steel plate
      this.ctx.beginPath();
      this.ctx.arc(x, y, radius, 0, Math.PI * 2);
      this.ctx.fillStyle = '#94a3b8';
      this.ctx.fill();
      this.ctx.strokeStyle = '#cbd5e1';
      this.ctx.lineWidth = 3;
      this.ctx.stroke();

      // Steel center bolt
      this.ctx.beginPath();
      this.ctx.arc(x, y, 4, 0, Math.PI * 2);
      this.ctx.fillStyle = '#334155';
      this.ctx.fill();
    } else if (type === 'skeet') {
      // Fluorescent clay pigeon
      this.ctx.beginPath();
      this.ctx.ellipse(x, y, radius, radius * 0.6, 0, 0, Math.PI * 2);
      this.ctx.fillStyle = '#ff6b2b';
      this.ctx.fill();
      this.ctx.strokeStyle = '#ffb700';
      this.ctx.lineWidth = 2;
      this.ctx.stroke();
    } else if (type === 'hostage') {
      // No shoot hostage silhouette
      this.ctx.beginPath();
      this.ctx.arc(x, y, radius, 0, Math.PI * 2);
      this.ctx.fillStyle = '#ff4757';
      this.ctx.fill();
      this.ctx.strokeStyle = '#fff';
      this.ctx.lineWidth = 2;
      this.ctx.stroke();

      this.ctx.fillStyle = '#fff';
      this.ctx.font = 'bold 16px var(--font-mono)';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText('⛔', x, y);
    }
    this.ctx.restore();
  }

  drawCrosshair(x, y) {
    this.ctx.save();
    this.ctx.strokeStyle = this.ammo === 0 ? 'var(--neon-red)' : 'var(--neon-cyan)';
    this.ctx.lineWidth = 1.5;

    // Crosshair circle
    this.ctx.beginPath();
    this.ctx.arc(x, y, 16, 0, Math.PI * 2);
    this.ctx.stroke();

    // Crosshair ticks
    this.ctx.beginPath();
    this.ctx.moveTo(x - 24, y);
    this.ctx.lineTo(x - 8, y);
    this.ctx.moveTo(x + 8, y);
    this.ctx.lineTo(x + 24, y);
    this.ctx.moveTo(x, y - 24);
    this.ctx.lineTo(x, y - 8);
    this.ctx.moveTo(x, y + 8);
    this.ctx.lineTo(x, y + 24);
    this.ctx.stroke();

    // Center dot
    this.ctx.fillStyle = this.ammo === 0 ? 'var(--neon-red)' : 'var(--neon-cyan)';
    this.ctx.beginPath();
    this.ctx.arc(x, y, 2, 0, Math.PI * 2);
    this.ctx.fill();

    this.ctx.restore();
  }

  endGame() {
    this.isGameOver = true;
    sounds.gameOver();
    clearInterval(this.timerInterval);
    clearInterval(this.targetSpawnInterval);

    const accuracy = this.shotsFired > 0 ? Math.round((this.shotsHit / this.shotsFired) * 100) : 0;

    if (this.onScoreUpdate) {
      this.onScoreUpdate('shooting-club', this.score);
    }

    const modal = document.createElement('div');
    modal.className = 'overlay-modal';
    modal.innerHTML = `
      <div class="modal-content">
        <h2 class="modal-title" style="color: var(--neon-cyan);">RANGE SESSION COMPLETE</h2>
        <div style="font-size: 2.8rem; font-weight: 900; color: var(--neon-amber); font-family: var(--font-mono);">${this.score}</div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-family: var(--font-mono); font-size: 0.85rem; margin: 8px 0;">
          <div style="background: var(--bg-card-alt); padding: 8px; border-radius: var(--radius-sm);">
            <div style="color: var(--text-muted); font-size: 0.7rem;">ACCURACY</div>
            <div style="font-weight: 800; color: var(--neon-green); font-size: 1.1rem;">${accuracy}%</div>
          </div>
          <div style="background: var(--bg-card-alt); padding: 8px; border-radius: var(--radius-sm);">
            <div style="color: var(--text-muted); font-size: 0.7rem;">BEST STREAK</div>
            <div style="font-weight: 800; color: var(--neon-cyan); font-size: 1.1rem;">${this.bestStreak}x</div>
          </div>
        </div>

        <div style="display: flex; gap: 10px;">
          <button id="modal-retry-btn" class="play-btn" style="flex: 1; justify-content: center;">Play Again</button>
          <button id="modal-exit-btn" class="nav-btn" style="flex: 1; justify-content: center;">Arcade Hub</button>
        </div>
      </div>
    `;

    this.container.appendChild(modal);

    modal.querySelector('#modal-retry-btn').addEventListener('click', () => {
      modal.remove();
      this.destroy();
      new ShootingClubGame(this.container, this.onExit, this.onScoreUpdate);
    });

    modal.querySelector('#modal-exit-btn').addEventListener('click', () => {
      modal.remove();
      this.destroy();
      if (this.onExit) this.onExit();
    });
  }

  destroy() {
    this.destroyed = true;
    clearInterval(this.timerInterval);
    clearInterval(this.targetSpawnInterval);
    if (this.animationId) cancelAnimationFrame(this.animationId);
  }
}

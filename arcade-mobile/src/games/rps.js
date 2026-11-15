import { sounds } from '../audio.js';

export class RockPaperScissorsGame {
  constructor(container, onExit, onScoreUpdate) {
    this.container = container;
    this.onExit = onExit;
    this.onScoreUpdate = onScoreUpdate;

    this.userScore = 0;
    this.cpuScore = 0;
    this.ties = 0;
    this.streak = 0;
    this.bestStreak = parseInt(localStorage.getItem('rps_best_streak') || '0', 10);
    this.totalScore = 0;

    this.isPlaying = false;
    this.lastResult = null; // 'win', 'lose', 'tie'
    this.lastUserPick = null;
    this.lastCpuPick = null;
    this.countdown = null;

    this.choices = [
      { id: 'rock', name: 'Rock', emoji: '✊', beats: 'scissors', color: 'var(--neon-pink)' },
      { id: 'paper', name: 'Paper', emoji: '✋', beats: 'rock', color: 'var(--neon-cyan)' },
      { id: 'scissors', name: 'Scissors', emoji: '✌️', beats: 'paper', color: 'var(--neon-amber)' }
    ];

    this.init();
  }

  init() {
    this.render();
    this.attachEvents();
  }

  render() {
    this.container.innerHTML = `
      <div style="display: flex; flex-direction: column; width: 100%; max-width: 460px; margin: 0 auto; gap: 16px;">
        <!-- Top Stats Bar -->
        <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-card); padding: 12px 16px; border-radius: var(--radius-md); border: 1px solid var(--border-color); font-family: var(--font-mono);">
          <div style="display: flex; flex-direction: column;">
            <span style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Win Streak</span>
            <span style="font-size: 1.2rem; font-weight: 800; color: var(--neon-cyan);">🔥 ${this.streak} <span style="font-size: 0.8rem; color: var(--text-secondary);">(Best: ${this.bestStreak})</span></span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: flex-end;">
            <span style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Arcade Score</span>
            <span style="font-size: 1.2rem; font-weight: 800; color: var(--neon-amber);">${this.totalScore}</span>
          </div>
        </div>

        <!-- Scoreboard Matrix -->
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; text-align: center; font-family: var(--font-mono); font-weight: 800; font-size: 0.9rem;">
          <div style="background: rgba(0, 229, 255, 0.08); border: 1px solid rgba(0, 229, 255, 0.3); padding: 8px; border-radius: var(--radius-sm); color: var(--neon-cyan);">
            YOU: ${this.userScore}
          </div>
          <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border-color); padding: 8px; border-radius: var(--radius-sm); color: var(--text-muted);">
            TIES: ${this.ties}
          </div>
          <div style="background: rgba(255, 0, 119, 0.08); border: 1px solid rgba(255, 0, 119, 0.3); padding: 8px; border-radius: var(--radius-sm); color: var(--neon-pink);">
            CPU: ${this.cpuScore}
          </div>
        </div>

        <!-- Battle Arena Ring -->
        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 24px 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 200px; position: relative; overflow: hidden; box-shadow: inset 0 2px 12px rgba(0,0,0,0.5);">
          ${this.renderArenaContent()}
        </div>

        <!-- Choice Selector Heading -->
        <div style="text-align: center; margin-top: 4px;">
          <span style="font-size: 0.8rem; font-weight: 800; letter-spacing: 1.5px; color: var(--text-muted); text-transform: uppercase;">
            ${this.isPlaying ? 'STAND BY...' : 'CHOOSE YOUR WEAPON'}
          </span>
        </div>

        <!-- 3 Choice Buttons -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
          ${this.choices
            .map(
              (c) => `
            <button class="rps-choice-btn" data-choice="${c.id}" ${this.isPlaying ? 'disabled' : ''} style="
              background: var(--bg-card);
              border: 2px solid ${c.color};
              border-radius: var(--radius-md);
              padding: 16px 8px;
              cursor: pointer;
              display: flex;
              flex-direction: column;
              align-items: center;
              gap: 8px;
              transition: all 0.2s;
              box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            ">
              <span style="font-size: 2.6rem;">${c.emoji}</span>
              <span style="font-family: var(--font-mono); font-weight: 800; font-size: 0.9rem; color: var(--text-primary);">${c.name}</span>
            </button>
          `
            )
            .join('')}
        </div>

        <!-- Controls row -->
        <div style="display: flex; gap: 10px; margin-top: 6px;">
          <button id="btn-rps-reset" class="nav-btn" style="flex: 1; justify-content: center;">
            ↺ Reset Scores
          </button>
          <button id="btn-rps-exit" class="nav-btn" style="flex: 1; justify-content: center;">
            ◀ Arcade Hub
          </button>
        </div>
      </div>
    `;
  }

  renderArenaContent() {
    if (this.countdown !== null) {
      return `
        <div style="display: flex; flex-direction: column; align-items: center; gap: 10px; animation: pulse 0.5s infinite;">
          <span style="font-size: 3.5rem; font-weight: 900; font-family: var(--font-mono); color: var(--neon-amber);">
            ${this.countdown}
          </span>
          <span style="font-size: 0.85rem; letter-spacing: 2px; color: var(--neon-cyan); font-weight: 800;">
            CALCULATING MOVE...
          </span>
        </div>
      `;
    }

    if (!this.lastResult) {
      return `
        <div style="display: flex; flex-direction: column; align-items: center; gap: 8px; opacity: 0.8;">
          <div style="display: flex; gap: 24px; font-size: 3rem;">
            <span>👤</span>
            <span style="color: var(--neon-cyan); font-weight: 900;">VS</span>
            <span>🤖</span>
          </div>
          <p style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 6px;">Tap Rock, Paper, or Scissors to clash!</p>
        </div>
      `;
    }

    const userObj = this.choices.find((c) => c.id === this.lastUserPick);
    const cpuObj = this.choices.find((c) => c.id === this.lastCpuPick);

    let resultBanner = '';
    if (this.lastResult === 'win') {
      resultBanner = `<div style="background: rgba(0, 255, 157, 0.2); border: 1px solid var(--neon-green); color: var(--neon-green); font-weight: 900; font-size: 1.1rem; padding: 6px 16px; border-radius: var(--radius-full); margin-bottom: 12px; letter-spacing: 1px;">ROUND VICTORY! (+100)</div>`;
    } else if (this.lastResult === 'lose') {
      resultBanner = `<div style="background: rgba(255, 71, 87, 0.2); border: 1px solid var(--neon-red); color: var(--neon-red); font-weight: 900; font-size: 1.1rem; padding: 6px 16px; border-radius: var(--radius-full); margin-bottom: 12px; letter-spacing: 1px;">ROUND DEFEAT</div>`;
    } else {
      resultBanner = `<div style="background: rgba(255, 183, 0, 0.2); border: 1px solid var(--neon-amber); color: var(--neon-amber); font-weight: 900; font-size: 1.1rem; padding: 6px 16px; border-radius: var(--radius-full); margin-bottom: 12px; letter-spacing: 1px;">DRAW / STALEMATE</div>`;
    }

    return `
      ${resultBanner}
      <div style="display: flex; align-items: center; justify-content: space-around; width: 100%;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
          <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">YOU</span>
          <span style="font-size: 3.2rem;">${userObj?.emoji || '❓'}</span>
          <span style="font-family: var(--font-mono); font-size: 0.85rem; font-weight: 800; color: var(--neon-cyan);">${userObj?.name}</span>
        </div>

        <div style="font-family: var(--font-mono); font-size: 1.4rem; font-weight: 900; color: var(--border-glow);">
          ⚡
        </div>

        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
          <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">CPU</span>
          <span style="font-size: 3.2rem;">${cpuObj?.emoji || '❓'}</span>
          <span style="font-family: var(--font-mono); font-size: 0.85rem; font-weight: 800; color: var(--neon-pink);">${cpuObj?.name}</span>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const choiceBtns = this.container.querySelectorAll('.rps-choice-btn');
    choiceBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const choice = btn.dataset.choice;
        this.playRound(choice);
      });
    });

    const resetBtn = this.container.querySelector('#btn-rps-reset');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        sounds.click();
        this.userScore = 0;
        this.cpuScore = 0;
        this.ties = 0;
        this.streak = 0;
        this.totalScore = 0;
        this.lastResult = null;
        this.render();
        this.attachEvents();
      });
    }

    const exitBtn = this.container.querySelector('#btn-rps-exit');
    if (exitBtn) {
      exitBtn.addEventListener('click', () => {
        sounds.click();
        this.destroy();
        if (this.onExit) this.onExit();
      });
    }
  }

  playRound(userChoice) {
    if (this.isPlaying) return;
    this.isPlaying = true;
    sounds.click();

    // Trigger fast 3-count anticipation
    let count = 3;
    this.countdown = count;
    this.render();

    const interval = setInterval(() => {
      count--;
      if (count > 0) {
        this.countdown = count;
        sounds.playTone(400 + (3 - count) * 150, 'sine', 0.05, 0.1);
        this.render();
      } else {
        clearInterval(interval);
        this.countdown = null;
        this.resolveRound(userChoice);
      }
    }, 220);
  }

  resolveRound(userChoice) {
    // Intelligent CPU choice
    const r = Math.random();
    let cpuChoice = '';
    if (r < 0.333) {
      cpuChoice = 'rock';
    } else if (r < 0.666) {
      cpuChoice = 'paper';
    } else {
      cpuChoice = 'scissors';
    }

    this.lastUserPick = userChoice;
    this.lastCpuPick = cpuChoice;

    if (userChoice === cpuChoice) {
      this.lastResult = 'tie';
      this.ties++;
      sounds.ding();
    } else {
      const userObj = this.choices.find((c) => c.id === userChoice);
      if (userObj.beats === cpuChoice) {
        this.lastResult = 'win';
        this.userScore++;
        this.streak++;
        if (this.streak > this.bestStreak) {
          this.bestStreak = this.streak;
          localStorage.setItem('rps_best_streak', this.bestStreak.toString());
        }
        const points = 100 + (this.streak > 1 ? this.streak * 25 : 0);
        this.totalScore += points;
        sounds.match();

        if (this.onScoreUpdate) {
          this.onScoreUpdate('rps', this.totalScore);
        }
      } else {
        this.lastResult = 'lose';
        this.cpuScore++;
        this.streak = 0;
        sounds.wrong();
      }
    }

    this.isPlaying = false;
    this.render();
    this.attachEvents();
  }

  destroy() {
    this.isPlaying = false;
  }
}

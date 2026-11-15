import './style.css';
import { sounds } from './audio.js';

import { App } from '@capacitor/app';
import { StatusBar, Style } from '@capacitor/status-bar';
import { adService } from './ads.js';

// Import all 8 games 
import { TicTacToeGame } from './games/tictactoe.js';
import { RockPaperScissorsGame } from './games/rps.js';
import { SudokuGame } from './games/sudoku.js';
import { CrackTheCodeGame } from './games/crackTheCode.js';

import { AsteroidsGame } from './games/asteroids.js';
import { PythonQuizGame } from './games/pythonQuiz.js';
import { ShootingClubGame } from './games/shootingClub.js';
import { TetrisGame } from './games/tetris.js';
import { GeneralQuizGame } from './games/generalQuiz.js';

// Arcade Registry of Games
const GAMES = [
  {
    id: 'tictactoe',
    title: 'Tic-Tac-Toe',
    emoji: '❌⭕',
    iconClass: 'icon-tictactoe',
    category: 'classic',
    tag: 'Classic AI',
    desc: 'Tactical grid battle with Smart Minimax AI or 2-player mode.',
    color: 'var(--neon-cyan)',
    gameClass: TicTacToeGame
  },
  {
    id: 'rps',
    title: 'Rock Paper Scissors',
    emoji: '<span>✊</span><span>✋</span><span>✌️</span>',
    iconClass: 'icon-rps',
    category: 'classic',
    tag: 'Hand Duel',
    desc: 'High-speed gesture showdown with combo multipliers and streak records.',
    color: 'var(--neon-pink)',
    gameClass: RockPaperScissorsGame
  },
  {
    id: 'sudoku',
    title: 'Sudoku Master',
    emoji: '🧩',
    category: 'puzzle',
    tag: 'Logic Grid',
    desc: 'Clean 9x9 Japanese logic puzzle with mistake tracking & timer.',
    color: 'var(--neon-green)',
    gameClass: SudokuGame
  },
  {
    id: 'crack-the-code',
    title: 'Crack The Code',
    emoji: '🔐🔢',
    category: 'puzzle',
    tag: 'Cyber Vault',
    desc: 'Cyberpunk vault breaker digit-matching puzzle with exact position hints.',
    color: 'var(--neon-purple)',
    gameClass: CrackTheCodeGame
  },
  {
    id: 'asteroids',
    title: 'Asteroids Odyssey',
    emoji: '🚀☄️',
    category: 'action',
    tag: 'Space Vector',
    desc: 'Inertial space combat with physics thrust, rotating ship & asteroid blasting.',
    color: 'var(--neon-cyan)',
    gameClass: AsteroidsGame
  },
  {
    id: 'python-quiz',
    title: 'Python Dev Quiz',
    emoji: '🐍💻',
    category: 'trivia',
    tag: '⚡ CODER ONLY',
    tagClass: 'tag-coder-only',
    desc: 'Strict programming trivia for developers: closures, decorators, mutability & scope.',
    color: '#00e5ff',
    gameClass: PythonQuizGame
  },
  {
    id: 'shooting-club',
    title: 'Apex Shooting Club',
    emoji: '🎯🔫',
    category: 'action',
    tag: 'Tactical Range',
    desc: 'Precision target simulator with 4 firearms, reactive steel & skeet clays.',
    color: 'var(--neon-red)',
    gameClass: ShootingClubGame
  },
  {
    id: 'tetris',
    title: 'Tetris Classic',
    emoji: '🧱🕹️',
    category: 'puzzle',
    tag: 'Retro Arcade',
    desc: 'Legendary falling tetrominoes puzzle with dynamic levels & touch controls.',
    color: 'var(--neon-amber)',
    gameClass: TetrisGame
  },
  {
    id: 'general-quiz',
    title: 'General Trivia Quiz',
    emoji: '🌍🧠',
    category: 'trivia',
    tag: 'Trivia & GK',
    desc: 'Trivia for all players: Science, History, Geography, Pop Culture & Sports.',
    color: 'var(--neon-green)',
    gameClass: GeneralQuizGame
  }
];

class ArcadeApp {
  constructor() {
    this.activeGameInstance = null;
    this.currentFilter = 'all';

    // DOM Elements
    this.hubView = document.querySelector('#hub-view');
    this.gameView = document.querySelector('#game-view');
    this.gameStage = document.querySelector('#game-stage');
    this.gamesGrid = document.querySelector('#games-grid');
    this.btnBackHub = document.querySelector('#btn-back-hub');
    this.btnSoundToggle = document.querySelector('#btn-sound-toggle');
    this.soundIcon = document.querySelector('#sound-icon');
    this.globalTrophiesEl = document.querySelector('#global-trophies');
    this.gamesPlayedCount = 0;

    this.init();
  }

  init() {
    // 1. Immediately render games grid and attach UI handlers
    this.setupSoundButton();
    this.setupFilters();
    this.updateTrophiesDisplay();
    this.renderGamesGrid();

    if (this.btnBackHub) {
      this.btnBackHub.addEventListener('click', () => {
        sounds.click();
        this.returnToHub();
      });
    }

    // Expose global returnToHub and adService
    window.__returnToHub = () => this.returnToHub();
    window.adService = adService;

    // Initialize Google AdMob
    adService.init().then(() => {
      // Show bottom banner on hub
      adService.showBanner();
    });

    // 2. Non-blocking Capacitor setup (only when running inside native Capacitor APK)
    try {
      if (typeof StatusBar !== 'undefined' && StatusBar.setStyle) {
        StatusBar.setStyle({ style: Style.Dark }).catch(() => { });
        StatusBar.setBackgroundColor({ color: '#0a0d14' }).catch(() => { });
      }
    } catch (e) { }

    try {
      if (typeof App !== 'undefined' && App.addListener) {
        App.addListener('backButton', ({ canGoBack }) => {
          if (this.activeGameInstance) {
            this.returnToHub();
          } else if (canGoBack) {
            window.history.back();
          } else {
            App.exitApp();
          }
        }).catch(() => { });
      }
    } catch (e) { }
  }

  setupSoundButton() {
    this.updateSoundIcon();
    this.btnSoundToggle.addEventListener('click', () => {
      const isMuted = sounds.toggleMute();
      this.updateSoundIcon();
      if (!isMuted) sounds.click();
    });
  }

  updateSoundIcon() {
    if (sounds.isMuted()) {
      this.soundIcon.textContent = '🔇';
      this.btnSoundToggle.title = 'Sound Muted';
    } else {
      this.soundIcon.textContent = '🔊';
      this.btnSoundToggle.title = 'Sound On';
    }
  }

  setupFilters() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    filterTabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        sounds.click();
        filterTabs.forEach((t) => t.classList.remove('active'));
        tab.classList.add('active');
        this.currentFilter = tab.dataset.filter;
        this.renderGamesGrid();
      });
    });
  }

  getHighScore(gameId) {
    return parseInt(localStorage.getItem(`arcade_score_${gameId}`) || '0', 10);
  }

  setHighScore(gameId, score) {
    const current = this.getHighScore(gameId);
    if (score > current) {
      localStorage.setItem(`arcade_score_${gameId}`, score.toString());
      this.updateTrophiesDisplay();
      this.renderGamesGrid();
    }
  }

  updateTrophiesDisplay() {
    // Total trophies = 1 for each game where score > 0 + 1 for each 500 cumulative points
    let trophies = 0;
    let totalScore = 0;

    GAMES.forEach((g) => {
      const score = this.getHighScore(g.id);
      if (score > 0) trophies += 1;
      totalScore += score;
    });

    trophies += Math.floor(totalScore / 500);
    this.globalTrophiesEl.textContent = trophies;
  }

  renderGamesGrid() {
    const filtered = GAMES.filter((game) => {
      if (this.currentFilter === 'all') return true;
      return game.category === this.currentFilter;
    });

    this.gamesGrid.innerHTML = filtered
      .map((game) => {
        const highScore = this.getHighScore(game.id);
        return `
          <div class="game-card" style="--card-accent: ${game.color};">
            <div class="card-top">
              <div class="card-icon ${game.iconClass || ''}">${game.emoji}</div>
              <div class="card-header-info">
                <div class="card-badge-row">
                  <span class="card-tag ${game.tagClass || ''}" style="border-left: 3px solid ${game.color};">${game.tag}</span>
                </div>
                <h3 class="card-title">${game.title}</h3>
                <p class="card-desc">${game.desc}</p>
              </div>
            </div>

            <div class="card-bottom">
              <div class="card-meta">
                <span class="card-score-label">BEST RECORD</span>
                <span class="card-score-val">${highScore > 0 ? highScore : '—'}</span>
              </div>
              <button class="play-btn" data-game-id="${game.id}">
                PLAY <span>▶</span>
              </button>
            </div>
          </div>
        `;
      })
      .join('');

    // Attach click events on Play buttons
    this.gamesGrid.querySelectorAll('.play-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        sounds.click();
        const gameId = btn.dataset.gameId;
        this.launchGame(gameId);
      });
    });
  }

  launchGame(gameId) {
    const gameDef = GAMES.find((g) => g.id === gameId);
    if (!gameDef) return;

    // Switch view to Game
    this.hubView.classList.remove('active');
    this.hubView.classList.add('hidden');

    this.gameView.classList.remove('hidden');
    this.gameView.classList.add('active');

    this.btnBackHub.classList.remove('hidden');
    window.scrollTo(0, 0);

    // Clean previous game if any
    if (this.activeGameInstance && typeof this.activeGameInstance.destroy === 'function') {
      this.activeGameInstance.destroy();
    }
    this.gameStage.innerHTML = '';

    // Instantiate new game
    this.activeGameInstance = new gameDef.gameClass(
      this.gameStage,
      () => this.returnToHub(),
      (id, score) => this.setHighScore(id || gameId, score)
    );
  }

  returnToHub() {
    if (this.activeGameInstance && typeof this.activeGameInstance.destroy === 'function') {
      this.activeGameInstance.destroy();
      this.activeGameInstance = null;
    }

    this.gameStage.innerHTML = '';
    this.gameView.classList.remove('active');
    this.gameView.classList.add('hidden');

    this.hubView.classList.remove('hidden');
    this.hubView.classList.add('active');

    this.btnBackHub.classList.add('hidden');
    this.updateTrophiesDisplay();
    this.renderGamesGrid();
    window.scrollTo(0, 0);

    // Show banner back on hub
    adService.showBanner();

    // Show interstitial occasionally when returning to hub (every 2 games)
    this.gamesPlayedCount++;
    if (this.gamesPlayedCount % 2 === 0) {
      adService.showInterstitial();
    }
  }
}

function startApp() {
  if (window.__arcadeAppStarted) return;
  window.__arcadeAppStarted = true;
  window.arcadeApp = new ArcadeApp();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', startApp);
} else {
  startApp();
}

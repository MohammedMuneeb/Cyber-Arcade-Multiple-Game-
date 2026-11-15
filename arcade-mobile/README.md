# Cyber Arcade - Android & Mobile Mini Games Hub 🎮📱

Converted from the desktop Python/Pygame arcade launcher into a mobile-first application for Android using **Capacitor** and **Vite / Modern Web Standards**.

---

## 🕹️ Included Games (All 8 Classics)

| Game | Category | Type | Mobile Features |
|---|---|---|---|
| **Tic-Tac-Toe** | Classic | Turn-based AI | Smart Minimax AI + 2-Player local pass & play |
| **Rock Paper Scissors** | Classic | Gesture Duel | Rapid tap battle, win streaks & score multiplier |
| **Sudoku Master** | Puzzle | Logic | 9x9 Japanese grid, error counter, pencil marks |
| **Crack The Code** | Puzzle | Cyber Vault | 6-digit decryption puzzle with exact position feedback |
| **Asteroids Odyssey** | Action | Space Arcade | Inertial physics, mobile D-pad + thrust & laser buttons |
| **Python Master Quiz** | Trivia | Code Brain | Timed trivia with 50/50, Hint, Time Freeze lifelines |
| **Apex Shooting Club** | Action | Tactical Range | 4 firearms (Pistol, Shotgun, AR-15, Sniper), reload & steel targets |
| **Tetris Classic** | Puzzle | Retro Arcade | Falling tetrominoes, mobile D-pad, hard drop & line clears |

---

## 🚀 How to Run & Build for Android

### Method 1: Open in Android Studio (Build APK / Run on Emulator or USB Phone)

1. Ensure **Android Studio** is installed.
2. Inside `arcade-mobile/`, run:
   ```bash
   npx cap open android
   ```
3. In Android Studio:
   - Click **Run** (`Shift + F10`) to launch on a connected Android phone or emulator.
   - Or click **Build > Build Bundle(s) / APK(s) > Build APK(s)** to export a standalone `.apk` install file!

### Method 2: Command Line APK Build (with Gradle & JDK)

```bash
npm run build
npx cap sync android
cd android
./gradlew assembleDebug
```
The output APK will be generated at:
`android/app/build/outputs/apk/debug/app-debug.apk`

### Method 3: Instant Progressive Web App (PWA) Install on Any Android Device

No Android Studio or SDK required:
1. Start the local server:
   ```bash
   npm run dev -- --host
   ```
2. Open Chrome on your Android phone connected to the same Wi-Fi (e.g. `http://<your-pc-ip>:5173`).
3. Tap the **3 dots menu** in Chrome and select **"Add to Home screen"** or **"Install app"**.
4. The Cyber Arcade will install as a standalone full-screen app with offline support, app icon, and no browser address bar!

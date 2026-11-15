""" 
============================================================================= 

                     CRACK THE CODE - PYGAME VAULT BREAKER 
=============================================================================
Rules:
1. The system generates a secret random 6-digit number.
2. The user has 4 rounds to enter a 6-digit guess.
3. If any digit matches the secret code in the EXACT SAME POSITION:
   - The user scores the numerical value of that matched digit!
   - (e.g., matching '9' at position 3 scores 9 points).
4. After 4 rounds, all round scores are summed up for the Final Total Score.
5. Features:
   - Full keyboard and on-screen clickable cyber keypad support.
   - Built-in procedural sound synthesis (no external audio files required).
   - Real-time slot animations, match breakdown, and mission history log.
   - Dramatic secret code reveal and rank evaluation at game end.
=============================================================================
"""

import pygame
import random

import math 
import io
import wave
import struct
import sys

# ---------------------------------------------------------------------------
# INITIALIZATION & CONSTANTS
# ---------------------------------------------------------------------------
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

SCREEN_WIDTH = 1040
SCREEN_HEIGHT = 720
FPS = 60

pygame.display.set_caption("Crack The Code // Cyber Vault Breaker")

# ---------------------------------------------------------------------------
# COLOR PALETTE (Cyberpunk Dark Vault Aesthetic)
# ---------------------------------------------------------------------------
COLOR_BG_DARK       = (13, 17, 23)
COLOR_PANEL_BG      = (22, 27, 34)
COLOR_PANEL_ALT     = (18, 22, 30)
COLOR_PANEL_BORDER  = (48, 54, 61)
COLOR_ACCENT_CYAN   = (0, 229, 255)
COLOR_ACCENT_GREEN  = (0, 255, 157)
COLOR_ACCENT_AMBER  = (255, 196, 0)
COLOR_ACCENT_RED    = (255, 75, 75)
COLOR_ACCENT_PURPLE = (189, 0, 255)
COLOR_TEXT_WHITE    = (240, 246, 252)
COLOR_TEXT_MUTED    = (139, 148, 158)
COLOR_SLOT_EMPTY    = (30, 36, 46)
COLOR_SLOT_ACTIVE   = (0, 229, 255)
COLOR_BTN_NORMAL    = (33, 38, 45)
COLOR_BTN_HOVER     = (48, 54, 61)
COLOR_BTN_ACTIVE    = (60, 68, 77)

# ---------------------------------------------------------------------------
# TYPOGRAPHY
# ---------------------------------------------------------------------------
def get_font(size, bold=False):
    for name in ["consolas", "trebuchetms", "segoeui", "arial"]:
        font = pygame.font.SysFont(name, size, bold=bold)
        if font:

            return font 
    return pygame.font.Font (None , size ) 
FONT_TITLE = get_font(32, bold=True)
FONT_SUBTITLE = get_font(18, bold=True)
FONT_DIGIT = get_font(42, bold=True)
FONT_KEYPAD = get_font(24, bold=True)
FONT_BODY = get_font(16, bold=False)
FONT_BODY_BOLD = get_font(16, bold=True)
FONT_SMALL = get_font(13, bold=False)
FONT_SCORE = get_font(28, bold=True)
FONT_BIG_RESULT = get_font(48, bold=True)

# ---------------------------------------------------------------------------
# PROCEDURAL AUDIO SYNTHESIZER
# ---------------------------------------------------------------------------
class SoundEngine:
    def __init__(self):
        self.muted = False
        self.sounds = {}
        if AUDIO_AVAILABLE:
            self._generate_sounds()

    def _generate_wav(self, sample_generator, duration_sec=0.1, volume=0.4):
        sample_rate = 44100
        total_samples = int(sample_rate * duration_sec)
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            raw_bytes = bytearray()
            for i in range(total_samples):
                val = sample_generator(i, total_samples, sample_rate)
                val = max(-1.0, min(1.0, val)) * volume
                sample_int = int(val * 32767)
                raw_bytes.extend(struct.pack('<h', sample_int))
            wf.writeframes(raw_bytes)
        buffer.seek(0)
        return pygame.mixer.Sound(buffer)

    def _generate_sounds(self):
        try:
            # Key click
            def click_gen(i, total, rate):
                env = math.exp(-i / (rate * 0.02))
                return math.sin(2 * math.pi * 880 * (i / rate)) * env
            self.sounds["click"] = self._generate_wav(click_gen, 0.05, 0.25)

            # Match Chime (high pure tone)
            def match_gen(i, total, rate):
                t = i / rate
                env = math.exp(-t * 8)
                return (math.sin(2 * math.pi * 659.25 * t) + 0.5 * math.sin(2 * math.pi * 1318.5 * t)) * env
            self.sounds["match"] = self._generate_wav(match_gen, 0.35, 0.35)

            # Error Buzz
            def error_gen(i, total, rate):
                t = i / rate
                env = math.exp(-t * 10)
                wave_sq = 1.0 if (int(t * 140) % 2 == 0) else -1.0
                return wave_sq * env
            self.sounds["error"] = self._generate_wav(error_gen, 0.2, 0.25)

            # Round Complete (positive arpeggio)
            def round_gen(i, total, rate):
                t = i / rate
                freq = 523.25 if t < 0.1 else (659.25 if t < 0.2 else 783.99)
                env = math.exp(-(t % 0.1) * 12)
                return math.sin(2 * math.pi * freq * t) * env
            self.sounds["round_done"] = self._generate_wav(round_gen, 0.35, 0.3)

            # Vault cracked / Victory fanfare
            def victory_gen(i, total, rate):
                t = i / rate
                freq = 440 + math.sin(t * 15) * 80 + t * 400
                env = min(1.0, (total - i) / (rate * 0.2))
                return math.sin(2 * math.pi * freq * t) * env * 0.4
            self.sounds["victory"] = self._generate_wav(victory_gen, 0.8, 0.35)

            # Game over chime
            def gameover_gen(i, total, rate):
                t = i / rate
                freq = 400 - t * 150
                env = math.exp(-t * 4)
                return math.sin(2 * math.pi * freq * t) * env
            self.sounds["gameover"] = self._generate_wav(gameover_gen, 0.6, 0.3)

        except Exception as e:
            print("Sound synthesis error:", e)

    def play(self, name):
        if not self.muted and name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception:
                pass

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted

# ---------------------------------------------------------------------------
# UI WIDGETS
# ---------------------------------------------------------------------------
class Button:
    def __init__(self, rect, text, subtext="", color_bg=COLOR_BTN_NORMAL,
                 color_hover=COLOR_BTN_HOVER, color_text=COLOR_TEXT_WHITE,
                 border_color=COLOR_PANEL_BORDER, radius=6):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.subtext = subtext
        self.color_bg = color_bg
        self.color_hover = color_hover
        self.color_text = color_text
        self.border_color = border_color
        self.radius = radius
        self.hovered = False
        self.pressed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.pressed
            self.pressed = False
            if was_pressed and self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        bg = self.color_hover if self.hovered else self.color_bg
        if self.pressed:
            bg = COLOR_BTN_ACTIVE
        
        # Border & Box
        pygame.draw.rect(surface, bg, self.rect, border_radius=self.radius)
        border_c = COLOR_ACCENT_CYAN if self.hovered else self.border_color
        pygame.draw.rect(surface, border_c, self.rect, width=2 if self.hovered else 1, border_radius=self.radius)

        # Main Text
        txt_surf = FONT_KEYPAD.render(self.text, True, self.color_text)
        txt_rect = txt_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (4 if self.subtext else 0)))
        surface.blit(txt_surf, txt_rect)

        # Optional Subtext
        if self.subtext:
            sub_surf = FONT_SMALL.render(self.subtext, True, COLOR_TEXT_MUTED)
            sub_rect = sub_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - 10))
            surface.blit(sub_surf, sub_rect)

# ---------------------------------------------------------------------------
# MAIN GAME CLASS
# ---------------------------------------------------------------------------
class CrackTheCodeGame:
    TOTAL_ROUNDS = 4
    CODE_LENGTH = 6

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.audio = SoundEngine()
        
        # Game States: 'PLAYING', 'ROUND_FEEDBACK', 'GAME_OVER', 'HELP_MODAL'
        self.state = 'PLAYING'
        self.show_help = False
        
        # Keypad buttons
        self.buttons = []
        self._setup_keypad()
        self._setup_control_buttons()

        # Shake effect on input error
        self.shake_offset = 0
        self.shake_timer = 0

        # Start game session
        self.new_game()

    def new_game(self):
        # Generate 6 random digits (0-9)
        self.secret_code = [random.randint(0, 9) for _ in range(self.CODE_LENGTH)]
        # For development verification: print to console
        print(f"[SYSTEM DEBUG] Secret Code Generated: {''.join(map(str, self.secret_code))}")
        
        self.current_round = 1
        self.current_guess = []
        self.round_history = []
        self.total_score = 0
        self.state = 'PLAYING'
        self.last_round_result = None
        self.reveal_progress = 0  # Animation for end game code reveal
        self.perfect_crack = False

    def _setup_keypad(self):
        self.keypad_buttons = []
        # Keypad position in Left/Center Panel
        kp_x = 75
        kp_y = 390
        btn_w = 90
        btn_h = 60
        gap_x = 18
        gap_y = 12

        # 3x3 layout for 1-9
        for num in range(1, 10):
            row = (num - 1) // 3
            col = (num - 1) % 3
            rx = kp_x + col * (btn_w + gap_x)
            ry = kp_y + row * (btn_h + gap_y)
            btn = Button((rx, ry, btn_w, btn_h), str(num))
            self.keypad_buttons.append((str(num), btn))

        # Bottom row: [CLEAR] [0] [BACKSPACE]
        by = kp_y + 3 * (btn_h + gap_y)
        
        # Clear button
        btn_clear = Button((kp_x, by, btn_w, btn_h), "CLR", "Clear", color_text=COLOR_ACCENT_AMBER)
        self.keypad_buttons.append(("CLEAR", btn_clear))

        # 0 Button
        btn_zero = Button((kp_x + 1 * (btn_w + gap_x), by, btn_w, btn_h), "0")
        self.keypad_buttons.append(("0", btn_zero))

        # Backspace button
        btn_back = Button((kp_x + 2 * (btn_w + gap_x), by, btn_w, btn_h), "DEL", "Back", color_text=COLOR_ACCENT_RED)
        self.keypad_buttons.append(("DEL", btn_back))

        # Submit button spanning bottom
        submit_y = by + btn_h + 12
        submit_w = 3 * btn_w + 2 * gap_x
        btn_submit = Button((kp_x, submit_y, submit_w, 55), "SUBMIT GUESS", "Enter Code", 
                            color_bg=(16, 52, 42), color_hover=(24, 76, 61), 
                            color_text=COLOR_ACCENT_GREEN, border_color=COLOR_ACCENT_GREEN)
        self.keypad_buttons.append(("SUBMIT", btn_submit))

    def _setup_control_buttons(self):
        # Audio Mute & Help buttons on top-right header
        self.btn_audio = Button((910, 15, 45, 35), "VOL", radius=4)
        self.btn_help = Button((965, 15, 45, 35), "?", radius=4)
        
        # Play Again button on game over
        self.btn_play_again = Button((SCREEN_WIDTH // 2 - 160, 610, 320, 56), 
                                     "PLAY AGAIN", "Start New Crack Attempt",
                                     color_bg=(16, 52, 42), color_hover=(24, 76, 61),
                                     color_text=COLOR_ACCENT_GREEN, border_color=COLOR_ACCENT_GREEN)

    # -----------------------------------------------------------------------
    # INPUT ACTIONS
    # -----------------------------------------------------------------------
    def add_digit(self, digit_str):
        if self.state == 'PLAYING' and len(self.current_guess) < self.CODE_LENGTH:
            self.current_guess.append(int(digit_str))
            self.audio.play("click")
        else:
            self.trigger_shake()
            self.audio.play("error")

    def backspace(self):
        if self.state == 'PLAYING' and len(self.current_guess) > 0:
            self.current_guess.pop()
            self.audio.play("click")
        else:
            self.audio.play("error")

    def clear_guess(self):
        if self.state == 'PLAYING' and len(self.current_guess) > 0:
            self.current_guess.clear()
            self.audio.play("click")

    def trigger_shake(self):
        self.shake_timer = 15

    def submit_guess(self):
        if self.state != 'PLAYING':
            return

        if len(self.current_guess) != self.CODE_LENGTH:
            self.trigger_shake()
            self.audio.play("error")
            return

        # -------------------------------------------------------------------
        # MATCHING & SCORING LOGIC
        # "compare if there are some same digits in same positions user scores those digits ;
        # after 4 rounds of user guessing add total scores as final score"
        # -------------------------------------------------------------------
        matches = [False] * self.CODE_LENGTH
        matched_digits = []
        round_score = 0

        for i in range(self.CODE_LENGTH):
            if self.current_guess[i] == self.secret_code[i]:
                matches[i] = True
                matched_digits.append(self.current_guess[i])
                round_score += self.current_guess[i]

        self.total_score += round_score

        result_data = {
            "round": self.current_round,
            "guess": list(self.current_guess),
            "matches": matches,
            "matched_digits": matched_digits,
            "round_score": round_score,
            "running_total": self.total_score
        }
        self.round_history.append(result_data)
        self.last_round_result = result_data

        if all(matches):
            self.perfect_crack = True

        if round_score > 0:
            self.audio.play("match")
        else:
            self.audio.play("round_done")

        # Advance round or finalize game
        if self.current_round >= self.TOTAL_ROUNDS or self.perfect_crack:
            self.state = 'GAME_OVER'
            self.audio.play("victory" if (self.perfect_crack or self.total_score >= 50) else "gameover")
        else:
            self.current_round += 1
            self.current_guess.clear()

    # -----------------------------------------------------------------------
    # EVENT HANDLING
    # -----------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Global header controls
            if self.btn_audio.handle_event(event):
                is_muted = self.audio.toggle_mute()
                self.btn_audio.text = "MUT" if is_muted else "VOL"
                continue

            if self.btn_help.handle_event(event):
                self.show_help = not self.show_help
                self.audio.play("click")
                continue

            # If help modal is active, close it on any click or ESC/H
            if self.show_help:
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_h):
                    self.show_help = False
                    self.audio.play("click")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.show_help = False
                    self.audio.play("click")
                continue

            # Game Over State interactions
            if self.state == 'GAME_OVER':
                if self.btn_play_again.handle_event(event):
                    self.audio.play("click")
                    self.new_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_r):
                        self.audio.play("click")
                        self.new_game()
                continue

            # Playing State - Virtual Keypad Buttons
            for key, btn in self.keypad_buttons:
                if btn.handle_event(event):
                    if key.isdigit():
                        self.add_digit(key)
                    elif key == "DEL":
                        self.backspace()
                    elif key == "CLEAR":
                        self.clear_guess()
                    elif key == "SUBMIT":
                        self.submit_guess()

            # Physical Keyboard Input
            if event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    digit = str(event.key - pygame.K_0)
                    self.add_digit(digit)
                elif pygame.K_KP0 <= event.key <= pygame.K_KP9:
                    digit = str(event.key - pygame.K_KP0)
                    self.add_digit(digit)
                elif event.key == pygame.K_BACKSPACE:
                    self.backspace()
                elif event.key == pygame.K_DELETE or event.key == pygame.K_c:
                    self.clear_guess()
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.submit_guess()
                elif event.key == pygame.K_h:
                    self.show_help = True
                    self.audio.play("click")

    # -----------------------------------------------------------------------
    # RENDERING METHODS
    # -----------------------------------------------------------------------
    def update(self):
        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.shake_offset = math.sin(self.shake_timer * 1.5) * 8
        else:
            self.shake_offset = 0

    def draw(self):
        self.screen.fill(COLOR_BG_DARK)

        # Draw decorative background cyber grid lines
        self._draw_background_decor()

        # Draw Top Navigation & Status Bar
        self._draw_header()

        if self.state == 'PLAYING':
            # Draw Left/Center Panel (Active Input & Virtual Keypad)
            self._draw_input_panel()
            # Draw Right Panel (History of 4 Rounds)
            self._draw_history_panel()
        elif self.state == 'GAME_OVER':
            # Draw Game Over & Final Score Summary Screen
            self._draw_game_over_screen()

        # Help modal overlay
        if self.show_help:
            self._draw_help_modal()

        pygame.display.flip()

    def _draw_background_decor(self):
        # Subtle horizontal circuit lines
        for y in range(80, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (18, 24, 34), (0, y), (SCREEN_WIDTH, y), 1)

    def _draw_header(self):
        # Header bar background
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 64)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, header_rect)
        pygame.draw.line(self.screen, COLOR_PANEL_BORDER, (0, 64), (SCREEN_WIDTH, 64), 2)

        # Title
        title_surf = FONT_TITLE.render("CRACK THE CODE", True, COLOR_ACCENT_CYAN)
        self.screen.blit(title_surf, (24, 14))

        tag_surf = FONT_SMALL.render("CYBER VAULT DECRYPTION PROTOCOL", True, COLOR_TEXT_MUTED)
        self.screen.blit(tag_surf, (330, 26))

        # Round Badge
        round_txt = f"ROUND: {min(self.current_round, self.TOTAL_ROUNDS)} / {self.TOTAL_ROUNDS}"
        round_surf = FONT_SUBTITLE.render(round_txt, True, COLOR_ACCENT_AMBER)
        round_rect = round_surf.get_rect(center=(680, 32))
        
        # Round box pill
        pill_rect = round_rect.inflate(24, 12)
        pygame.draw.rect(self.screen, (35, 30, 20), pill_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_ACCENT_AMBER, pill_rect, width=1, border_radius=12)
        self.screen.blit(round_surf, round_rect)

        # Total score in header
        score_txt = f"SCORE: {self.total_score}"
        score_surf = FONT_SUBTITLE.render(score_txt, True, COLOR_ACCENT_GREEN)
        score_rect = score_surf.get_rect(center=(820, 32))
        pill_score = score_rect.inflate(20, 12)
        pygame.draw.rect(self.screen, (16, 40, 30), pill_score, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_ACCENT_GREEN, pill_score, width=1, border_radius=12)
        self.screen.blit(score_surf, score_rect)

        # Control buttons
        self.btn_audio.draw(self.screen)
        self.btn_help.draw(self.screen)

    def _draw_input_panel(self):
        # Main Left Card
        panel_rect = pygame.Rect(35 + self.shake_offset, 85, 490, 605)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, panel_rect, width=1, border_radius=10)

        # Panel Header / Instructions
        prompt_txt = f"ENTER 6-DIGIT CODE (ATTEMPT {self.current_round} OF {self.TOTAL_ROUNDS})"
        p_surf = FONT_SUBTITLE.render(prompt_txt, True, COLOR_TEXT_WHITE)
        self.screen.blit(p_surf, (panel_rect.x + 24, panel_rect.y + 20))

        sub_prompt = "Match the exact digit at the exact position to score its value!"
        sp_surf = FONT_SMALL.render(sub_prompt, True, COLOR_TEXT_MUTED)
        self.screen.blit(sp_surf, (panel_rect.x + 24, panel_rect.y + 48))

        # -------------------------------------------------------------------
        # 6 DIGIT INPUT SLOTS
        # -------------------------------------------------------------------
        slot_w = 64
        slot_h = 76
        slot_gap = 12
        start_x = panel_rect.x + 23
        start_y = panel_rect.y + 78

        for i in range(self.CODE_LENGTH):
            sx = start_x + i * (slot_w + slot_gap)
            sy = start_y
            s_rect = pygame.Rect(sx, sy, slot_w, slot_h)

            is_active = (i == len(self.current_guess))
            has_digit = (i < len(self.current_guess))

            # Slot box background
            bg_color = (25, 34, 48) if is_active else COLOR_SLOT_EMPTY
            pygame.draw.rect(self.screen, bg_color, s_rect, border_radius=8)

            # Border
            if is_active:
                # Pulsing cyan glow
                glow_val = int(180 + 75 * math.sin(pygame.time.get_ticks() * 0.008))
                border_col = (0, glow_val, 255)
                pygame.draw.rect(self.screen, border_col, s_rect, width=2, border_radius=8)
            elif has_digit:
                pygame.draw.rect(self.screen, COLOR_ACCENT_CYAN, s_rect, width=1, border_radius=8)
            else:
                pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, s_rect, width=1, border_radius=8)

            # Position indicator index (1..6)
            pos_label = FONT_SMALL.render(f"POS {i+1}", True, (90, 105, 125))
            self.screen.blit(pos_label, (sx + 14, sy + 6))

            # Render Digit
            if has_digit:
                digit_str = str(self.current_guess[i])
                d_surf = FONT_DIGIT.render(digit_str, True, COLOR_ACCENT_CYAN)
                d_rect = d_surf.get_rect(center=(sx + slot_w // 2, sy + slot_h // 2 + 8))
                self.screen.blit(d_surf, d_rect)
            elif is_active:
                # Blinking cursor bar
                if (pygame.time.get_ticks() // 400) % 2 == 0:
                    cursor_y = sy + slot_h // 2 + 6
                    pygame.draw.line(self.screen, COLOR_ACCENT_CYAN, (sx + 18, cursor_y), (sx + slot_w - 18, cursor_y), 3)

        # Status / Feedback Banner below input slots
        feedback_rect = pygame.Rect(panel_rect.x + 23, start_y + slot_h + 16, 444, 48)
        pygame.draw.rect(self.screen, COLOR_PANEL_ALT, feedback_rect, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, feedback_rect, width=1, border_radius=6)

        if self.last_round_result:
            matches_count = sum(self.last_round_result["matches"])
            pts = self.last_round_result["round_score"]
            digits_matched = self.last_round_result["matched_digits"]
            if matches_count > 0:
                digits_str = " + ".join(map(str, digits_matched))
                feed_text = f"Round {self.last_round_result['round']} Match: {digits_str} = +{pts} pts!"
                feed_color = COLOR_ACCENT_GREEN
            else:
                feed_text = f"Round {self.last_round_result['round']}: No matches at same positions. (0 pts)"
                feed_color = COLOR_ACCENT_RED
        else:
            feed_text = "Key in 6 digits using the keypad or keyboard numbers, then SUBMIT."
            feed_color = COLOR_TEXT_MUTED

        f_surf = FONT_BODY_BOLD.render(feed_text, True, feed_color)
        f_rect = f_surf.get_rect(center=feedback_rect.center)
        self.screen.blit(f_surf, f_rect)

        # -------------------------------------------------------------------
        # VIRTUAL KEYPAD
        # -------------------------------------------------------------------
        for key, btn in self.keypad_buttons:
            # Apply shake offset to button positions during rendering
            orig_x = btn.rect.x
            btn.rect.x += self.shake_offset
            btn.draw(self.screen)
            btn.rect.x = orig_x

    def _draw_history_panel(self):
        # Right Card: Attempt History & Analysis
        panel_rect = pygame.Rect(550, 85, 455, 605)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, panel_rect, width=1, border_radius=10)

        # Header
        h_title = FONT_SUBTITLE.render("ATTEMPT LOG & CODE ANALYSIS", True, COLOR_TEXT_WHITE)
        self.screen.blit(h_title, (panel_rect.x + 20, panel_rect.y + 18))

        h_sub = FONT_SMALL.render("Green slot = Exact match & points scored! Dim = No match.", True, COLOR_TEXT_MUTED)
        self.screen.blit(h_sub, (panel_rect.x + 20, panel_rect.y + 44))

        # Draw 4 Round Slots in table format
        start_y = panel_rect.y + 72
        row_h = 104
        gap = 14

        for r in range(1, self.TOTAL_ROUNDS + 1):
            ry = start_y + (r - 1) * (row_h + gap)
            card_rect = pygame.Rect(panel_rect.x + 18, ry, panel_rect.width - 36, row_h)

            # Round card background
            is_current = (r == self.current_round and self.state == 'PLAYING')
            has_data = (r <= len(self.round_history))

            card_bg = (28, 35, 48) if is_current else COLOR_PANEL_ALT
            pygame.draw.rect(self.screen, card_bg, card_rect, border_radius=8)
            border_c = COLOR_ACCENT_CYAN if is_current else COLOR_PANEL_BORDER
            pygame.draw.rect(self.screen, border_c, card_rect, width=1, border_radius=8)

            # Round Label
            r_label_txt = f"ROUND {r}"
            r_col = COLOR_ACCENT_AMBER if is_current else (COLOR_ACCENT_CYAN if has_data else COLOR_TEXT_MUTED)
            r_label = FONT_BODY_BOLD.render(r_label_txt, True, r_col)
            self.screen.blit(r_label, (card_rect.x + 14, card_rect.y + 10))

            if has_data:
                record = self.round_history[r - 1]
                guess = record["guess"]
                matches = record["matches"]
                score = record["round_score"]

                # Score tag on top-right of card
                score_tag = f"+{score} PTS" if score > 0 else "0 PTS"
                st_col = COLOR_ACCENT_GREEN if score > 0 else COLOR_TEXT_MUTED
                st_surf = FONT_BODY_BOLD.render(score_tag, True, st_col)
                self.screen.blit(st_surf, (card_rect.right - st_surf.get_width() - 14, card_rect.y + 10))

                # Display 6 mini boxes for guessed digits with color feedback
                slot_w = 42
                slot_h = 44
                slot_gap = 10
                bx_start = card_rect.x + 14
                by = card_rect.y + 36

                for idx in range(self.CODE_LENGTH):
                    bx = bx_start + idx * (slot_w + slot_gap)
                    box_rect = pygame.Rect(bx, by, slot_w, slot_h)
                    is_match = matches[idx]

                    box_bg = (10, 50, 30) if is_match else (30, 20, 20)
                    pygame.draw.rect(self.screen, box_bg, box_rect, border_radius=5)
                    box_border = COLOR_ACCENT_GREEN if is_match else (80, 50, 50)
                    pygame.draw.rect(self.screen, box_border, box_rect, width=1, border_radius=5)

                    # Number inside mini box
                    digit_color = COLOR_ACCENT_GREEN if is_match else COLOR_TEXT_MUTED
                    d_txt = FONT_KEYPAD.render(str(guess[idx]), True, digit_color)
                    d_r = d_txt.get_rect(center=box_rect.center)
                    self.screen.blit(d_txt, d_r)

                    # Small checkmark or cross indicator
                    ind_sym = "+" if is_match else "-"
                    ind_surf = FONT_SMALL.render(ind_sym, True, digit_color)
                    self.screen.blit(ind_surf, (bx + slot_w - 12, by + 2))

                # Detail label on bottom
                matched_digits = record["matched_digits"]
                if matched_digits:
                    detail_str = f"Matches: {', '.join(map(str, matched_digits))}  (Points: {sum(matched_digits)})"
                else:
                    detail_str = "No position matches"
                dt_surf = FONT_SMALL.render(detail_str, True, COLOR_TEXT_MUTED)
                self.screen.blit(dt_surf, (card_rect.x + 14, card_rect.bottom - 18))

            elif is_current:
                # Active in-progress indicator
                active_txt = FONT_BODY.render(">> ENTERING GUESS NOW...", True, COLOR_ACCENT_CYAN)
                self.screen.blit(active_txt, (card_rect.x + 14, card_rect.y + 44))
            else:
                # Locked / upcoming round
                locked_txt = FONT_BODY.render("[ AWAITING PREVIOUS ROUNDS ]", True, (80, 90, 105))
                self.screen.blit(locked_txt, (card_rect.x + 14, card_rect.y + 44))

        # Bottom Total Score Counter Card
        total_card = pygame.Rect(panel_rect.x + 18, panel_rect.bottom - 60, panel_rect.width - 36, 46)
        pygame.draw.rect(self.screen, (16, 22, 32), total_card, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, total_card, width=1, border_radius=6)

        tot_label = FONT_BODY_BOLD.render("CUMULATIVE TOTAL SCORE:", True, COLOR_TEXT_WHITE)
        self.screen.blit(tot_label, (total_card.x + 14, total_card.y + 14))

        tot_val = FONT_SCORE.render(f"{self.total_score} PTS", True, COLOR_ACCENT_GREEN)
        self.screen.blit(tot_val, (total_card.right - tot_val.get_width() - 14, total_card.y + 8))

    # -----------------------------------------------------------------------
    # GAME OVER / FINAL SUMMARY SCREEN
    # -----------------------------------------------------------------------
    def _draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 20, 240))
        self.screen.blit(overlay, (0, 0))

        # Summary Modal Card
        card_w = 760
        card_h = 580
        card_rect = pygame.Rect((SCREEN_WIDTH - card_w) // 2, 70, card_w, card_h)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, card_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_ACCENT_CYAN, card_rect, width=2, border_radius=12)

        # Header Status Banner
        if self.perfect_crack:
            head_txt = "VAULT CRACKED // CODE BREACHED!"
            head_col = COLOR_ACCENT_GREEN
        else:
            head_txt = "DECRYPTION COMPLETE // 4 ROUNDS CONCLUDED"
            head_col = COLOR_ACCENT_CYAN

        h_surf = FONT_TITLE.render(head_txt, True, head_col)
        h_rect = h_surf.get_rect(center=(card_rect.centerx, card_rect.y + 42))
        self.screen.blit(h_surf, h_rect)

        # Revealed Secret Code Section
        sec_label = FONT_SUBTITLE.render("ORIGINAL SECRET CODE:", True, COLOR_TEXT_MUTED)
        self.screen.blit(sec_label, (card_rect.centerx - sec_label.get_width() // 2, card_rect.y + 78))

        # 6 Large Revealed Boxes
        slot_w = 58
        slot_h = 66
        gap = 14
        start_x = card_rect.centerx - ((6 * slot_w + 5 * gap) // 2)
        start_y = card_rect.y + 108

        for idx in range(self.CODE_LENGTH):
            bx = start_x + idx * (slot_w + gap)
            s_rect = pygame.Rect(bx, start_y, slot_w, slot_h)
            pygame.draw.rect(self.screen, (24, 38, 56), s_rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_ACCENT_CYAN, s_rect, width=2, border_radius=8)

            d_char = str(self.secret_code[idx])
            d_surf = FONT_DIGIT.render(d_char, True, COLOR_ACCENT_GREEN)
            d_r = d_surf.get_rect(center=s_rect.center)
            self.screen.blit(d_surf, d_r)

        # -------------------------------------------------------------------
        # 4 ROUNDS BREAKDOWN TABLE
        # -------------------------------------------------------------------
        table_y = start_y + slot_h + 24
        table_w = card_w - 60
        table_rect = pygame.Rect(card_rect.x + 30, table_y, table_w, 200)
        pygame.draw.rect(self.screen, COLOR_PANEL_ALT, table_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, table_rect, width=1, border_radius=8)

        # Table Header
        th_round = FONT_BODY_BOLD.render("ROUND", True, COLOR_TEXT_MUTED)
        th_guess = FONT_BODY_BOLD.render("YOUR GUESS", True, COLOR_TEXT_MUTED)
        th_match = FONT_BODY_BOLD.render("MATCHED DIGITS", True, COLOR_TEXT_MUTED)
        th_score = FONT_BODY_BOLD.render("SCORE EARNED", True, COLOR_TEXT_MUTED)

        self.screen.blit(th_round, (table_rect.x + 20, table_rect.y + 12))
        self.screen.blit(th_guess, (table_rect.x + 130, table_rect.y + 12))
        self.screen.blit(th_match, (table_rect.x + 300, table_rect.y + 12))
        self.screen.blit(th_score, (table_rect.right - 140, table_rect.y + 12))

        pygame.draw.line(self.screen, COLOR_PANEL_BORDER, (table_rect.x, table_rect.y + 36), (table_rect.right, table_rect.y + 36), 1)

        row_y = table_rect.y + 44
        for r_idx in range(len(self.round_history)):
            rec = self.round_history[r_idx]
            r_num_txt = FONT_BODY.render(f"Round {rec['round']}", True, COLOR_TEXT_WHITE)
            self.screen.blit(r_num_txt, (table_rect.x + 20, row_y))

            # Guess with matched digits highlighted
            guess_str = " ".join(str(d) for d in rec["guess"])
            g_txt = FONT_BODY_BOLD.render(guess_str, True, COLOR_ACCENT_CYAN)
            self.screen.blit(g_txt, (table_rect.x + 130, row_y))

            # Matched digits calculation
            m_digits = rec["matched_digits"]
            if m_digits:
                calc_str = f"{' + '.join(map(str, m_digits))} = {rec['round_score']}"
                m_txt = FONT_BODY_BOLD.render(calc_str, True, COLOR_ACCENT_GREEN)
            else:
                m_txt = FONT_BODY.render("None (0)", True, COLOR_TEXT_MUTED)
            self.screen.blit(m_txt, (table_rect.x + 300, row_y))

            # Score
            sc_txt = FONT_BODY_BOLD.render(f"+{rec['round_score']} pts", True, COLOR_ACCENT_GREEN if rec['round_score'] > 0 else COLOR_TEXT_MUTED)
            self.screen.blit(sc_txt, (table_rect.right - 140, row_y))

            row_y += 36

        # -------------------------------------------------------------------
        # FINAL TOTAL SCORE & EVALUATION BADGE
        # -------------------------------------------------------------------
        final_y = table_rect.bottom + 16
        tot_banner = pygame.Rect(card_rect.x + 30, final_y, table_w, 64)
        pygame.draw.rect(self.screen, (16, 42, 32), tot_banner, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_ACCENT_GREEN, tot_banner, width=2, border_radius=8)

        final_title = FONT_SUBTITLE.render("FINAL TOTAL SCORE (ALL 4 ROUNDS):", True, COLOR_TEXT_WHITE)
        self.screen.blit(final_title, (tot_banner.x + 20, tot_banner.y + 20))

        final_val = FONT_BIG_RESULT.render(f"{self.total_score} POINTS", True, COLOR_ACCENT_GREEN)
        self.screen.blit(final_val, (tot_banner.right - final_val.get_width() - 20, tot_banner.y + 6))

        # Rank determination
        if self.perfect_crack or self.total_score >= 100:
            rank_text = "RANK: CIPHER GRANDMASTER"
            rank_col = COLOR_ACCENT_PURPLE
        elif self.total_score >= 60:
            rank_text = "RANK: ELITE VAULT CRACKER"
            rank_col = COLOR_ACCENT_AMBER
        elif self.total_score >= 30:
            rank_text = "RANK: CYBER INFILTRATOR"
            rank_col = COLOR_ACCENT_CYAN
        else:
            rank_text = "RANK: SECURITY APPRENTICE"
            rank_col = COLOR_TEXT_MUTED

        rank_surf = FONT_BODY_BOLD.render(rank_text, True, rank_col)
        self.screen.blit(rank_surf, (card_rect.centerx - rank_surf.get_width() // 2, final_y + 74))

        # Play Again Button
        self.btn_play_again.draw(self.screen)

    # -----------------------------------------------------------------------
    # HELP & RULES MODAL
    # -----------------------------------------------------------------------
    def _draw_help_modal(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        modal_w = 640
        modal_h = 440
        modal_rect = pygame.Rect((SCREEN_WIDTH - modal_w) // 2, (SCREEN_HEIGHT - modal_h) // 2, modal_w, modal_h)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, modal_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_ACCENT_CYAN, modal_rect, width=2, border_radius=12)

        # Title
        t_surf = FONT_TITLE.render("HOW TO PLAY", True, COLOR_ACCENT_CYAN)
        self.screen.blit(t_surf, (modal_rect.x + 30, modal_rect.y + 25))

        lines = [
            "1. THE SECRET CODE: The vault computer generates a random 6-digit number.",
            "2. FOUR ROUNDS: You are given 4 guessing rounds to crack the code.",
            "3. ENTER YOUR GUESS: Key in 6 digits using your keyboard (0-9) or on-screen pad.",
            "4. POSITION MATCH & SCORING: If your digit matches the secret code at the",
            "   EXACT SAME POSITION, you score the numerical value of that digit!",
            "   Example: Secret is 5-9-1-0-4-7. Your guess is 5-2-1-8-4-0.",
            "   Matches at Pos 1 (5), Pos 3 (1), Pos 5 (4) -> Score = 5 + 1 + 4 = 10 pts!",
            "5. FINAL SCORE: After 4 rounds, all round scores are summed up.",
            "   Maximize your total score or crack all 6 digits to claim the Grandmaster rank!"
        ]

        y = modal_rect.y + 80
        for line in lines:
            col = COLOR_ACCENT_GREEN if "Example:" in line or "Matches at" in line else COLOR_TEXT_WHITE
            font = FONT_BODY_BOLD if "Example:" in line or "Matches at" in line else FONT_BODY
            s = font.render(line, True, col)
            self.screen.blit(s, (modal_rect.x + 30, y))
            y += 28

        close_hint = FONT_SMALL.render("[ Click anywhere or press ESC / H to close ]", True, COLOR_TEXT_MUTED)
        self.screen.blit(close_hint, (modal_rect.centerx - close_hint.get_width() // 2, modal_rect.bottom - 32))

    # -----------------------------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------------------------
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = CrackTheCodeGame()
    game.run()

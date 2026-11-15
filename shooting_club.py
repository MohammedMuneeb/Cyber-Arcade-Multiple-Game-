"""
=============================================================================

                      APEX SHOOTING CLUB - PYGAME 
=============================================================================
A premier tactical target shooting club simulator featuring:
 - 4 Realistic Firearms: P-9 Pistol, Breacher 12G Shotgun, Viper AR-15, Hawkeye .308 Sniper
 - 4 Diverse Club Modes: Bullseye Precision, Tactical Reflex, Skeet Clays, Armory Practice
 - Dynamic Weapon Handling: Recoil, screen kick, shell ejection, ADS / Sniper Scope mode
 - Realistic Targetry: Concentric paper rings, reactive steel plates, hostage no-shoots, clay skeet
 - Built-in Audio Synthesizer: Procedurally generated gunshots, steel dings, clacks & chimes
 - Live Grouping / MOA calculation, Combo multipliers, Ranks & Local High Scores
=============================================================================
"""

import pygame
import math
import random
import time
import json
import os
import io
import wave
import struct

# Initialize Pygame & Mixer
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.display.set_caption("Apex Shooting Club - Tactical Range Simulator")

# Window Configuration
SCREEN_WIDTH = 1040
SCREEN_HEIGHT = 720
FPS = 60

# Palette / Color Scheme
COLOR_BG_DARK = (16, 18, 24)
COLOR_CEILING = (24, 27, 36)
COLOR_FLOOR = (28, 30, 38)
COLOR_WALL_LINE = (45, 52, 68)
COLOR_BENCH = (62, 45, 32)
COLOR_BENCH_TOP = (85, 62, 44)
COLOR_BENCH_EDGE = (110, 82, 58)
COLOR_ACCENT_YELLOW = (255, 195, 18)
COLOR_ACCENT_ORANGE = (255, 107, 43)
COLOR_ACCENT_CYAN = (0, 220, 255)
COLOR_ACCENT_GREEN = (46, 213, 115)
COLOR_ACCENT_RED = (255, 71, 87)
COLOR_TEXT_WHITE = (240, 243, 246)
COLOR_TEXT_MUTED = (140, 148, 165)
COLOR_PANEL_BG = (22, 26, 35, 230)
COLOR_STEEL = (175, 182, 195)
COLOR_STEEL_DARK = (100, 107, 120)
COLOR_CLAY = (255, 95, 30)

# Fonts setup
FONT_TITLE = pygame.font.SysFont("impact", 44)
FONT_HEADING = pygame.font.SysFont("trebuchetms", 26, bold=True)
FONT_SUBHEADING = pygame.font.SysFont("trebuchetms", 18, bold=True)
FONT_BODY = pygame.font.SysFont("trebuchetms", 14)
FONT_BODY_BOLD = pygame.font.SysFont("trebuchetms", 14, bold=True)
FONT_DIGIT = pygame.font.SysFont("consolas", 22, bold=True)
FONT_RETICLE = pygame.font.SysFont("consolas", 12)

# =============================================================================
# PROCEDURAL AUDIO SYNTHESIZER
# =============================================================================
class SoundSynth:
    """Generates punchy procedural sound effects with zero external audio assets."""
    def __init__(self):
        self.muted = False
        self.volume = 0.8
        self.sounds = {}
        self._generate_all_sounds()

    def _create_wav(self, duration_sec, sample_fn, sample_rate=44100):
        bio = io.BytesIO()
        with wave.open(bio, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            samples = bytearray()
            total_samples = int(sample_rate * duration_sec)
            for i in range(total_samples):
                t = i / sample_rate
                val = max(-1.0, min(1.0, sample_fn(t, duration_sec)))
                ival = int(val * 32767 * self.volume)
                samples.extend(struct.pack('<h', ival))
            wf.writeframes(samples)
        bio.seek(0)
        return pygame.mixer.Sound(bio)

    def _generate_all_sounds(self):
        try:
            # Pistol: snappy sharp pop + thump
            self.sounds['fire_pistol'] = self._create_wav(
                0.16,
                lambda t, d: (random.uniform(-1, 1) * math.exp(-t * 40) +
                              0.7 * math.sin(2 * math.pi * 170 * t) * math.exp(-t * 26))
            )
            # Shotgun: deep booming punch + multi-pellet blast
            self.sounds['fire_shotgun'] = self._create_wav(
                0.36,
                lambda t, d: (random.uniform(-1, 1) * 0.9 * math.exp(-t * 16) +
                              1.0 * math.sin(2 * math.pi * 85 * t) * math.exp(-t * 12))
            )
            # Rifle: sharp supersonic crack + body
            self.sounds['fire_rifle'] = self._create_wav(
                0.14,
                lambda t, d: (random.uniform(-1, 1) * math.exp(-t * 45) +
                              0.8 * math.sin(2 * math.pi * 230 * t) * math.exp(-t * 32))
            )
            # Sniper: thunderous cannon crack + long reverberation
            self.sounds['fire_sniper'] = self._create_wav(
                0.55,
                lambda t, d: (random.uniform(-1, 1) * math.exp(-t * 14) +
                              math.sin(2 * math.pi * 70 * t) * math.exp(-t * 7) +
                              0.3 * math.sin(2 * math.pi * 140 * t) * math.exp(-t * 10))
            )
            # Steel hit gong / bell ping
            self.sounds['hit_steel'] = self._create_wav(
                0.35,
                lambda t, d: math.exp(-t * 14) * (0.65 * math.sin(2 * math.pi * 1380 * t) +
                                                  0.35 * math.sin(2 * math.pi * 2760 * t))
            )
            # Paper hit punch
            self.sounds['hit_paper'] = self._create_wav(
                0.08,
                lambda t, d: random.uniform(-0.9, 0.9) * math.exp(-t * 65)
            )
            # Clay smash crunch
            self.sounds['hit_clay'] = self._create_wav(
                0.22,
                lambda t, d: (random.uniform(-1, 1) * math.exp(-t * 22) +
                              0.5 * math.sin(2 * math.pi * 650 * t) * math.exp(-t * 30))
            )
            # Reload Mag Out
            self.sounds['mag_out'] = self._create_wav(
                0.09,
                lambda t, d: (math.sin(2 * math.pi * 750 * t) + random.uniform(-0.3, 0.3)) * math.exp(-t * 45)
            )
            # Reload Mag In
            self.sounds['mag_in'] = self._create_wav(
                0.11,
                lambda t, d: (math.sin(2 * math.pi * 420 * t) + random.uniform(-0.3, 0.3)) * math.exp(-t * 35)
            )
            # Slide rack
            self.sounds['slide_rack'] = self._create_wav(
                0.18,
                lambda t, d: (math.sin(2 * math.pi * (280 + 350 * t) * t) + random.uniform(-0.4, 0.4)) * math.exp(-t * 18)
            )
            # Dry Fire Click
            self.sounds['dry_fire'] = self._create_wav(
                0.04,
                lambda t, d: math.sin(2 * math.pi * 2200 * t) * math.exp(-t * 80)
            )
            # Bullseye chime / headshot
            self.sounds['bullseye'] = self._create_wav(
                0.38,
                lambda t, d: math.exp(-t * 10) * (0.6 * math.sin(2 * math.pi * 1760 * t) +
                                                  0.4 * math.sin(2 * math.pi * 2640 * t))
            )
            # Hostage penalty buzzer
            self.sounds['penalty'] = self._create_wav(
                0.28,
                lambda t, d: (0.4 if math.sin(2 * math.pi * 140 * t) > 0 else -0.4) * math.exp(-t * 5)
            )
            # Countdown beep
            self.sounds['beep'] = self._create_wav(
                0.12,
                lambda t, d: math.sin(2 * math.pi * 880 * t) * math.exp(-t * 15)
            )
            # Shell casing bounce
            self.sounds['casing_ping'] = self._create_wav(
                0.06,
                lambda t, d: math.sin(2 * math.pi * 3200 * t) * math.exp(-t * 70) * 0.25
            )
        except Exception as e:
            print(f"[SoundSynth] Warning: could not synthesize all sounds: {e}")

    def play(self, sound_name):
        if self.muted:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            snd.play()

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted

AUDIO = SoundSynth()

# =============================================================================
# PARTICLE & EFFECTS ENGINE
# =============================================================================
class Particle:
    def __init__(self, x, y, vx, vy, color, size, life, decay, gravity=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.max_life = life
        self.life = life
        self.decay = decay
        self.gravity = gravity

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= self.decay
        return self.life > 0

    def draw(self, surface):
        alpha_pct = max(0.0, self.life / self.max_life)
        cur_size = max(1, int(self.size * alpha_pct))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), cur_size)

class CasingParticle:
    """Ejected brass shell casing bouncing off the shooting bench."""
    def __init__(self, x, y, caliber='9mm'):
        self.x = x
        self.y = y
        self.vx = random.uniform(3.5, 7.5)
        self.vy = random.uniform(-4.5, -2.0)
        self.angle = random.uniform(0, 360)
        self.v_rot = random.uniform(15, 30)
        self.bounce_y = random.uniform(SCREEN_HEIGHT - 120, SCREEN_HEIGHT - 60)
        self.bounces = 0
        self.max_bounces = 3
        self.life = 120
        self.length = 10 if caliber == '9mm' else (14 if caliber == '12g' else 12)
        self.width = 4 if caliber != '12g' else 6
        self.color = (235, 190, 75) if caliber != '12g' else (180, 40, 40)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.45  # Gravity
        self.angle += self.v_rot

        # Bounce on bench
        if self.y >= self.bounce_y and self.bounces < self.max_bounces:
            self.y = self.bounce_y
            self.vy = -self.vy * 0.45
            self.vx *= 0.65
            self.v_rot *= 0.5
            self.bounces += 1
            if self.bounces == 1:
                AUDIO.play('casing_ping')

        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        rad = math.radians(self.angle)
        dx = math.cos(rad) * (self.length / 2)
        dy = math.sin(rad) * (self.length / 2)
        p1 = (int(self.x - dx), int(self.y - dy))
        p2 = (int(self.x + dx), int(self.y + dy))
        pygame.draw.line(surface, self.color, p1, p2, self.width)
        # Primer brass head
        pygame.draw.circle(surface, (255, 230, 140), p1, max(1, self.width // 2))

class FloatingText:
    def __init__(self, x, y, text, color, font=FONT_HEADING, duration=50):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.life = duration
        self.max_life = duration
        self.vy = -1.2

    def update(self):
        self.y += self.vy
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        rect = text_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text_surf, rect)

class BulletHoleDecal:
    def __init__(self, rel_x, rel_y, is_center=False):
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.is_center = is_center

# =============================================================================
# WEAPONS DEFINITION & HANDLING
# =============================================================================
class Weapon:
    def __init__(self, name, caliber, mag_size, fire_rate, reload_time, recoil_kick,
                 pellet_count=1, spread=0, is_auto=False, can_scope=False, sound_key='fire_pistol'):
        self.name = name
        self.caliber = caliber
        self.mag_size = mag_size
        self.current_ammo = mag_size
        self.total_ammo = 999  # Range reserves
        self.fire_rate = fire_rate  # Seconds between shots
        self.reload_time = reload_time
        self.recoil_kick = recoil_kick
        self.pellet_count = pellet_count
        self.spread = spread
        self.is_auto = is_auto
        self.can_scope = can_scope
        self.sound_key = sound_key

        self.last_shot_time = 0.0
        self.is_reloading = False
        self.reload_start_time = 0.0
        self.reload_progress = 0.0
        self.shots_fired = 0
        self.shots_hit = 0

    def can_fire(self, current_time):
        if self.is_reloading:
            return False
        if current_time - self.last_shot_time < self.fire_rate:
            return False
        return True

    def shoot(self, current_time):
        if not self.can_fire(current_time):
            return False
        if self.current_ammo <= 0:
            AUDIO.play('dry_fire')
            self.start_reload(current_time)
            return False

        self.current_ammo -= 1
        self.last_shot_time = current_time
        self.shots_fired += 1
        AUDIO.play(self.sound_key)
        return True

    def start_reload(self, current_time):
        if self.is_reloading or self.current_ammo == self.mag_size:
            return
        self.is_reloading = True
        self.reload_start_time = current_time
        AUDIO.play('mag_out')

    def update(self, current_time):
        if self.is_reloading:
            elapsed = current_time - self.reload_start_time
            self.reload_progress = min(1.0, elapsed / self.reload_time)
            # Intermediate audio cues
            if 0.45 <= self.reload_progress <= 0.52 and not getattr(self, '_played_in', False):
                AUDIO.play('mag_in')
                self._played_in = True
            if self.reload_progress >= 1.0:
                self.current_ammo = self.mag_size
                self.is_reloading = False
                self.reload_progress = 0.0
                self._played_in = False
                AUDIO.play('slide_rack')

def create_armory():
    return [
        Weapon(
            name="P-9 Tactix",
            caliber="9mm Parabellum",
            mag_size=15,
            fire_rate=0.18,
            reload_time=1.2,
            recoil_kick=4.0,
            pellet_count=1,
            spread=0,
            is_auto=False,
            can_scope=False,
            sound_key='fire_pistol'
        ),
        Weapon(
            name="Breacher 12G",
            caliber="12-Gauge Buck",
            mag_size=6,
            fire_rate=0.75,
            reload_time=2.1,
            recoil_kick=11.0,
            pellet_count=8,
            spread=26,
            is_auto=False,
            can_scope=False,
            sound_key='fire_shotgun'
        ),
        Weapon(
            name="Viper AR-15",
            caliber="5.56x45mm NATO",
            mag_size=30,
            fire_rate=0.10,
            reload_time=1.6,
            recoil_kick=3.2,
            pellet_count=1,
            spread=2,
            is_auto=True,
            can_scope=False,
            sound_key='fire_rifle'
        ),
        Weapon(
            name="Hawkeye .308",
            caliber=".308 Match Bolt",
            mag_size=5,
            fire_rate=1.1,
            reload_time=2.3,
            recoil_kick=13.0,
            pellet_count=1,
            spread=0,
            is_auto=False,
            can_scope=True,
            sound_key='fire_sniper'
        )
    ]

# =============================================================================
# TARGET CLASSES
# =============================================================================
class Target:
    def __init__(self, x, y, distance_meters=25):
        self.x = x
        self.y = y
        self.distance = distance_meters
        self.scale = max(0.4, 1.0 - (distance_meters - 15) * 0.012)
        self.decals = []
        self.is_dead = False
        self.score_value = 0

    def check_hit(self, hit_x, hit_y):
        return None

class PaperBullseyeTarget(Target):
    """Concentric Olympic/ISU target rings with precise coordinate scoring."""
    def __init__(self, x, y, distance_meters=25, speed=0.0):
        super().__init__(x, y, distance_meters)
        self.base_radius = 54
        self.radius = int(self.base_radius * self.scale)
        self.speed = speed
        self.min_x = 180
        self.max_x = SCREEN_WIDTH - 180

    def update(self):
        if self.speed != 0:
            self.x += self.speed
            if self.x > self.max_x:
                self.x = self.max_x
                self.speed = -abs(self.speed)
            elif self.x < self.min_x:
                self.x = self.min_x
                self.speed = abs(self.speed)

    def check_hit(self, hit_x, hit_y):
        dx = hit_x - self.x
        dy = hit_y - self.y
        dist = math.hypot(dx, dy)
        if dist <= self.radius:
            # Normalized score from 10 down to 1
            norm_dist = dist / self.radius
            if norm_dist <= 0.12:
                points = 100
                ring_name = "X-BULLSEYE!"
                is_x = True
            elif norm_dist <= 0.28:
                points = 80
                ring_name = "10 RING"
                is_x = False
            elif norm_dist <= 0.48:
                points = 60
                ring_name = "9 RING"
                is_x = False
            elif norm_dist <= 0.70:
                points = 40
                ring_name = "8 RING"
                is_x = False
            else:
                points = 20
                ring_name = "OUTER RING"
                is_x = False

            self.decals.append(BulletHoleDecal(dx, dy, is_x))
            return {
                'points': points,
                'name': ring_name,
                'is_bullseye': is_x,
                'target_type': 'paper',
                'hit_x': hit_x,
                'hit_y': hit_y
            }
        return None

    def draw(self, surface):
        # Target hanger frame / cable
        pygame.draw.line(surface, (60, 65, 75), (int(self.x), 0), (int(self.x), int(self.y - self.radius - 10)), 2)
        hanger_rect = pygame.Rect(int(self.x - 14 * self.scale), int(self.y - self.radius - 12 * self.scale),
                                  int(28 * self.scale), int(12 * self.scale))
        pygame.draw.rect(surface, (90, 95, 105), hanger_rect, border_radius=2)

        # Backboard card
        card_w = int(self.radius * 2.3)
        card_h = int(self.radius * 2.6)
        card_rect = pygame.Rect(int(self.x - card_w / 2), int(self.y - card_h / 2), card_w, card_h)
        pygame.draw.rect(surface, (230, 225, 210), card_rect)
        pygame.draw.rect(surface, (180, 175, 160), card_rect, 2)

        # Rings drawing (Concentric white / black / red rings)
        ring_colors = [
            (255, 255, 255), (255, 255, 255), (30, 30, 35), (30, 30, 35), (230, 50, 50)
        ]
        fractions = [1.0, 0.75, 0.50, 0.28, 0.12]
        for color, frac in zip(ring_colors, fractions):
            r = int(self.radius * frac)
            if r > 0:
                pygame.draw.circle(surface, color, (int(self.x), int(self.y)), r)
                border_col = (40, 40, 40) if color != (30, 30, 35) else (180, 180, 180)
                pygame.draw.circle(surface, border_col, (int(self.x), int(self.y)), r, 1)

        # Inner crosshair on target
        cross_len = int(self.radius * 0.18)
        pygame.draw.line(surface, (255, 255, 255), (int(self.x - cross_len), int(self.y)),
                         (int(self.x + cross_len), int(self.y)), 1)
        pygame.draw.line(surface, (255, 255, 255), (int(self.x), int(self.y - cross_len)),
                         (int(self.x), int(self.y + cross_len)), 1)

        # Bullet holes on target
        for decal in self.decals:
            hx = int(self.x + decal.rel_x)
            hy = int(self.y + decal.rel_y)
            pygame.draw.circle(surface, (20, 20, 25), (hx, hy), 3)
            pygame.draw.circle(surface, (80, 80, 85), (hx, hy), 4, 1)

class SteelSilhouetteTarget(Target):
    """Reactive steel popper (IDPA silhouette) that knocks backward and dings."""
    def __init__(self, x, y, distance_meters=25, is_hostage=False, lifetime=3.0):
        super().__init__(x, y, distance_meters)
        self.is_hostage = is_hostage
        self.lifetime = lifetime
        self.spawn_time = time.time()
        self.hit_state = 0.0  # 0.0 upright -> 1.0 knocked down
        self.width = int(58 * self.scale)
        self.height = int(96 * self.scale)
        self.head_radius = int(16 * self.scale)
        self.is_popping = True
        self.pop_progress = 0.0

    def update(self):
        now = time.time()
        if self.is_popping:
            self.pop_progress += 0.14
            if self.pop_progress >= 1.0:
                self.pop_progress = 1.0
                self.is_popping = False

        if not self.is_dead:
            if now - self.spawn_time > self.lifetime:
                self.is_dead = True
        else:
            self.hit_state = min(1.0, self.hit_state + 0.18)

    def check_hit(self, hit_x, hit_y):
        if self.is_dead or self.hit_state > 0:
            return None

        head_cy = self.y - self.height / 2 + self.head_radius
        dx_head = hit_x - self.x
        dy_head = hit_y - head_cy

        # Check Headshot
        if math.hypot(dx_head, dy_head) <= self.head_radius:
            self.is_dead = True
            if self.is_hostage:
                return {'points': -120, 'name': 'CIVILIAN CASUALTY!', 'is_hostage': True,
                        'target_type': 'hostage', 'hit_x': hit_x, 'hit_y': hit_y}
            else:
                return {'points': 150, 'name': 'STEEL HEADSHOT!', 'is_headshot': True,
                        'target_type': 'steel', 'hit_x': hit_x, 'hit_y': hit_y}

        # Check Torso
        torso_rect = pygame.Rect(
            int(self.x - self.width / 2),
            int(head_cy + self.head_radius),
            self.width,
            int(self.height - self.head_radius * 2)
        )
        if torso_rect.collidepoint(hit_x, hit_y):
            self.is_dead = True
            if self.is_hostage:
                return {'points': -100, 'name': 'CIVILIAN HIT!', 'is_hostage': True,
                        'target_type': 'hostage', 'hit_x': hit_x, 'hit_y': hit_y}
            else:
                return {'points': 75, 'name': 'STEEL HIT!', 'is_headshot': False,
                        'target_type': 'steel', 'hit_x': hit_x, 'hit_y': hit_y}

        return None

    def draw(self, surface):
        if self.hit_state >= 1.0:
            return

        # Target stand post
        stand_top = int(self.y + self.height / 2)
        stand_bottom = stand_top + int(45 * self.scale)
        pygame.draw.line(surface, (70, 75, 85), (int(self.x), stand_top), (int(self.x), stand_bottom), 4)

        # Calculate knockback pivot
        drop_offset_y = int(self.hit_state * 30 * self.scale)
        tilt = self.hit_state * 0.45

        # Colors based on type
        if self.is_hostage:
            plate_color = (235, 235, 240)
            edge_color = (255, 75, 75)
        else:
            plate_color = COLOR_STEEL
            edge_color = COLOR_STEEL_DARK

        head_cy = int(self.y - self.height / 2 + self.head_radius + drop_offset_y)
        torso_top = head_cy + self.head_radius
        torso_h = int((self.height - self.head_radius * 2) * (1.0 - tilt))
        torso_w = int(self.width)

        # Draw Torso
        torso_rect = pygame.Rect(int(self.x - torso_w / 2), torso_top, torso_w, torso_h)
        pygame.draw.rect(surface, plate_color, torso_rect, border_radius=int(6 * self.scale))
        pygame.draw.rect(surface, edge_color, torso_rect, 2, border_radius=int(6 * self.scale))

        # Draw Head
        pygame.draw.circle(surface, plate_color, (int(self.x), head_cy), self.head_radius)
        pygame.draw.circle(surface, edge_color, (int(self.x), head_cy), self.head_radius, 2)

        # Hostage warning cross symbol
        if self.is_hostage:
            hw = int(self.width * 0.35)
            hh = int(self.height * 0.22)
            cy = torso_top + torso_h // 2
            pygame.draw.line(surface, COLOR_ACCENT_RED, (int(self.x - hw), int(cy - hh)),
                             (int(self.x + hw), int(cy + hh)), 4)
            pygame.draw.line(surface, COLOR_ACCENT_RED, (int(self.x + hw), int(cy - hh)),
                             (int(self.x - hw), int(cy + hh)), 4)
            badge_surf = FONT_RETICLE.render("NO SHOOT", True, COLOR_ACCENT_RED)
            b_rect = badge_surf.get_rect(center=(int(self.x), torso_top + 10))
            surface.blit(badge_surf, b_rect)
        else:
            # IDPA Center A-Zone ring
            a_zone_r = int(self.head_radius * 0.9)
            pygame.draw.circle(surface, (140, 145, 155), (int(self.x), torso_top + torso_h // 2), a_zone_r, 1)

class ClayPigeon(Target):
    """Clay disc catapulted in an aerodynamic parabolic arc."""
    def __init__(self, start_x, start_y, vx, vy):
        super().__init__(start_x, start_y, distance_meters=35)
        self.vx = vx
        self.vy = vy
        self.gravity = 0.26
        self.radius = 18
        self.spin_angle = 0
        self.is_dead = False

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.spin_angle += 14

        # Dead if touches ground or goes off-screen
        if self.y > SCREEN_HEIGHT - 130 or self.x < -40 or self.x > SCREEN_WIDTH + 40:
            self.is_dead = True

    def check_hit(self, hit_x, hit_y):
        if self.is_dead:
            return None
        dist = math.hypot(hit_x - self.x, hit_y - self.y)
        if dist <= self.radius + 6:
            self.is_dead = True
            return {
                'points': 80,
                'name': 'CLAY SHATTER!',
                'target_type': 'clay',
                'hit_x': hit_x,
                'hit_y': hit_y
            }
        return None

    def draw(self, surface):
        if self.is_dead:
            return
        # Elliptical disk projection
        ellipse_w = int(self.radius * 2)
        ellipse_h = int(self.radius * 0.95)
        clay_rect = pygame.Rect(int(self.x - ellipse_w / 2), int(self.y - ellipse_h / 2), ellipse_w, ellipse_h)
        pygame.draw.ellipse(surface, COLOR_CLAY, clay_rect)
        pygame.draw.ellipse(surface, (255, 170, 50), clay_rect, 2)
        inner_rect = pygame.Rect(int(self.x - ellipse_w * 0.28), int(self.y - ellipse_h * 0.28),
                                 int(ellipse_w * 0.56), int(ellipse_h * 0.56))
        pygame.draw.ellipse(surface, (200, 60, 20), inner_rect, 1)

# =============================================================================
# ENVIRONMENT RENDERER (TACTICAL INDOOR/OUTDOOR SHOOTING CLUB)
# =============================================================================
class RangeEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spotlights = [
            (220, 40), (520, 40), (820, 40)
        ]

    def draw(self, surface, is_scoped=False):
        # 1. Back Wall / Distant Target Berm
        pygame.draw.rect(surface, COLOR_BG_DARK, (0, 0, self.width, self.height))

        # Distant bullet-trap berm (textured gravel/rubber backstop)
        berm_rect = pygame.Rect(60, 110, self.width - 120, 390)
        pygame.draw.rect(surface, (22, 25, 33), berm_rect)
        pygame.draw.rect(surface, (35, 40, 52), berm_rect, 3)

        # Distance lane markings
        dist_labels = [("15m", 440), ("25m", 320), ("50m", 210), ("100m", 140)]
        for label, y_pos in dist_labels:
            pygame.draw.line(surface, (36, 42, 56), (70, y_pos), (self.width - 70, y_pos), 1)
            marker = FONT_RETICLE.render(f"--- {label} LINE ---", True, (65, 75, 95))
            surface.blit(marker, (85, y_pos - 14))

        # Vertical lane divider wires & overhead tracks
        for lx in [260, 520, 780]:
            pygame.draw.line(surface, (40, 46, 60), (lx, 80), (lx, 490), 1)
            # Track trolley wire
            pygame.draw.line(surface, (65, 72, 90), (lx - 120, 110), (lx + 120, 110), 2)

        # 2. Ceiling acoustic baffles & fluorescent light fixtures
        pygame.draw.rect(surface, COLOR_CEILING, (0, 0, self.width, 95))
        for x in range(80, self.width, 160):
            # Acoustic baffle slates
            pygame.draw.rect(surface, (32, 36, 48), (x, 15, 110, 22), border_radius=3)
            # Fluorescent tube light
            light_rect = pygame.Rect(x + 10, 28, 90, 6)
            pygame.draw.rect(surface, (240, 245, 255), light_rect)
            # Soft ambient light cone down
            glow_surf = pygame.Surface((180, 200), pygame.SRCALPHA)
            pygame.draw.polygon(glow_surf, (255, 255, 255, 12), [
                (90, 0), (180, 200), (0, 200)
            ])
            surface.blit(glow_surf, (x - 45, 34))

        # 3. Floor shooting lane
        floor_rect = pygame.Rect(0, 500, self.width, self.height - 500)
        pygame.draw.rect(surface, COLOR_FLOOR, floor_rect)
        for i in range(0, self.width, 90):
            pygame.draw.line(surface, (38, 42, 54), (i, 500), (i + 30, self.height), 1)

        # 4. Shooting Stall Divider & Counter Table (Foreground)
        if not is_scoped:
            bench_top_y = self.height - 95
            bench_rect = pygame.Rect(0, bench_top_y, self.width, 95)
            pygame.draw.rect(surface, COLOR_BENCH, bench_rect)
            pygame.draw.rect(surface, COLOR_BENCH_TOP, (0, bench_top_y, self.width, 18))
            pygame.draw.line(surface, COLOR_BENCH_EDGE, (0, bench_top_y), (self.width, bench_top_y), 3)

            # Yellow/Black range safety hazard warning strip
            stripe_w = 24
            for sx in range(-20, self.width + 20, stripe_w * 2):
                pts = [
                    (sx, bench_top_y + 18),
                    (sx + 14, bench_top_y + 18),
                    (sx + 24, bench_top_y + 26),
                    (sx + 10, bench_top_y + 26)
                ]
                pygame.draw.polygon(surface, COLOR_ACCENT_YELLOW, pts)

            # Left and right booth partition columns
            pygame.draw.rect(surface, (35, 38, 48), (0, 70, 48, self.height))
            pygame.draw.rect(surface, (50, 55, 70), (45, 70, 4, self.height))
            pygame.draw.rect(surface, (35, 38, 48), (self.width - 48, 70, 48, self.height))
            pygame.draw.rect(surface, (50, 55, 70), (self.width - 49, 70, 4, self.height))

# =============================================================================
# MAIN GAME CONTROLLER & MODES
# =============================================================================
class ShootingClubGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.environment = RangeEnvironment(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.armory = create_armory()
        self.current_weapon_idx = 0
        self.active_weapon = self.armory[self.current_weapon_idx]

        # Particles & Effects
        self.particles = []
        self.casings = []
        self.floating_texts = []
        self.screen_shake = 0.0
        self.muzzle_flash_timer = 0
        self.recoil_offset_y = 0.0

        # Sniper ADS & Sway
        self.is_aiming_down_sights = False
        self.breath_held = False
        self.breath_meter = 100.0  # Max 100
        self.sway_time = 0.0

        # Game States
        # STATES: 'MENU', 'PLAYING', 'PAUSED', 'DEBRIEF'
        self.state = 'MENU'
        self.game_mode = 'BULLSEYE'  # 'BULLSEYE', 'REFLEX', 'CLAY', 'PRACTICE'

        # Score & Stats
        self.score = 0
        self.combo = 1
        self.max_combo = 1
        self.consecutive_hits = 0
        self.total_shots = 0
        self.total_hits = 0
        self.bullseyes_hit = 0
        self.reaction_times = []
        self.mode_timer = 60.0  # 60s rounds
        self.start_round_time = 0.0

        # Targets container
        self.targets = []
        self.next_spawn_time = 0.0

        # Practice mode metrics
        self.practice_shots = []  # Stores (x, y) coordinates of impacts
        self.practice_target = None
        self.practice_distance = 25

        # High Scores storage
        self.highscores_file = os.path.join(os.path.dirname(__file__), "shooting_club_scores.json")
        self.highscores = self.load_highscores()

    def load_highscores(self):
        default_scores = {'BULLSEYE': 1200, 'REFLEX': 1500, 'CLAY': 900}
        if os.path.exists(self.highscores_file):
            try:
                with open(self.highscores_file, 'r') as f:
                    return {**default_scores, **json.load(f)}
            except Exception:
                return default_scores
        return default_scores

    def save_highscores(self):
        try:
            with open(self.highscores_file, 'w') as f:
                json.dump(self.highscores, f)
        except Exception as e:
            print(f"Could not save scores: {e}")

    def start_mode(self, mode_name):
        self.game_mode = mode_name
        self.state = 'PLAYING'
        self.score = 0
        self.combo = 1
        self.max_combo = 1
        self.consecutive_hits = 0
        self.total_shots = 0
        self.total_hits = 0
        self.bullseyes_hit = 0
        self.reaction_times = []
        self.targets.clear()
        self.particles.clear()
        self.casings.clear()
        self.floating_texts.clear()
        self.practice_shots.clear()

        # Reset weapon ammo
        for w in self.armory:
            w.current_ammo = w.mag_size
            w.is_reloading = False

        now = time.time()
        self.start_round_time = now

        if mode_name == 'BULLSEYE':
            self.mode_timer = 60.0
            # Spawn 3 lane paper targets moving at different speeds & distances
            self.targets.append(PaperBullseyeTarget(260, 310, distance_meters=20, speed=1.4))
            self.targets.append(PaperBullseyeTarget(520, 240, distance_meters=35, speed=-1.8))
            self.targets.append(PaperBullseyeTarget(780, 370, distance_meters=15, speed=2.0))
        elif mode_name == 'REFLEX':
            self.mode_timer = 45.0
            self.next_spawn_time = now + 0.5
        elif mode_name == 'CLAY':
            self.mode_timer = 50.0
            self.next_spawn_time = now + 1.0
            # Switch to Shotgun for optimal skeet fun
            self.current_weapon_idx = 1
            self.active_weapon = self.armory[1]
        elif mode_name == 'PRACTICE':
            self.mode_timer = 9999.0
            self.setup_practice_target()

        AUDIO.play('beep')

    def setup_practice_target(self):
        self.targets.clear()
        self.practice_shots.clear()
        self.practice_target = PaperBullseyeTarget(SCREEN_WIDTH // 2, 300, distance_meters=self.practice_distance, speed=0)
        self.targets.append(self.practice_target)

    # -------------------------------------------------------------------------
    # FIRING & HIT SCAN LOGIC
    # -------------------------------------------------------------------------
    def fire_weapon(self):
        now = time.time()
        mx, my = pygame.mouse.get_pos()

        # Sniper scope sway offset
        if self.is_aiming_down_sights and self.active_weapon.can_scope:
            sway_factor = 0.2 if self.breath_held else 1.0
            sway_x = math.sin(self.sway_time * 2.2) * 9 * sway_factor
            sway_y = math.cos(self.sway_time * 3.1) * 6 * sway_factor
            mx += sway_x
            my += sway_y

        # Weapon recoil kick offset
        my -= self.recoil_offset_y

        if not self.active_weapon.shoot(now):
            return

        self.total_shots += 1
        self.screen_shake = min(18.0, self.screen_shake + self.active_weapon.recoil_kick * 0.9)
        self.muzzle_flash_timer = 3
        self.recoil_offset_y = min(24.0, self.recoil_offset_y + self.active_weapon.recoil_kick * 1.2)

        # Eject brass casing
        c_x = SCREEN_WIDTH // 2 + 120
        c_y = SCREEN_HEIGHT - 80
        self.casings.append(CasingParticle(c_x, c_y, caliber=self.active_weapon.caliber))

        # Check hits for pellets (Shotgun has 8, others have 1)
        shot_had_hit = False
        pellets = self.active_weapon.pellet_count
        spread_val = self.active_weapon.spread

        for p_idx in range(pellets):
            spread_x = 0
            spread_y = 0
            if spread_val > 0:
                ang = random.uniform(0, 2 * math.pi)
                dist = random.uniform(0, spread_val)
                spread_x = math.cos(ang) * dist
                spread_y = math.sin(ang) * dist

            hit_x = mx + spread_x
            hit_y = my + spread_y

            # In practice mode, record shot grouping
            if self.game_mode == 'PRACTICE':
                self.practice_shots.append((hit_x, hit_y))

            # Hit scan against all active targets
            hit_result = None
            for t in reversed(self.targets):
                res = t.check_hit(hit_x, hit_y)
                if res:
                    hit_result = res
                    break

            if hit_result:
                shot_had_hit = True
                self.handle_target_hit(hit_result, hit_x, hit_y)
            else:
                # Range wall impact puff
                self.spawn_wall_puff(hit_x, hit_y)

        if shot_had_hit:
            self.total_hits += 1
            self.consecutive_hits += 1
            if self.consecutive_hits % 3 == 0 and self.combo < 4:
                self.combo += 1
            if self.combo > self.max_combo:
                self.max_combo = self.combo
        else:
            # Miss resets streak & combo (except in practice mode)
            if self.game_mode != 'PRACTICE':
                self.combo = 1
                self.consecutive_hits = 0

    def handle_target_hit(self, result, hx, hy):
        pts = result['points']
        name = result['name']
        t_type = result.get('target_type', 'generic')

        # Multiplier
        if pts > 0:
            final_pts = pts * self.combo
            self.score += final_pts
            text_color = COLOR_ACCENT_GREEN if not result.get('is_bullseye') else COLOR_ACCENT_YELLOW
            self.floating_texts.append(FloatingText(hx, hy - 15, f"+{final_pts} {name}", text_color))
        else:
            # Penalty
            self.score = max(0, self.score + pts)
            self.combo = 1
            self.consecutive_hits = 0
            self.floating_texts.append(FloatingText(hx, hy - 15, f"{pts} {name}", COLOR_ACCENT_RED))
            AUDIO.play('penalty')

        # Sound effects and particle explosion
        if t_type == 'paper':
            AUDIO.play('hit_paper')
            if result.get('is_bullseye'):
                AUDIO.play('bullseye')
                self.bullseyes_hit += 1
            # Paper confetti
            for _ in range(7):
                self.particles.append(Particle(
                    hx, hy, random.uniform(-2, 2), random.uniform(-2.5, 1),
                    (240, 240, 230), random.randint(2, 4), 22, 1.0, gravity=0.1
                ))
        elif t_type == 'steel':
            AUDIO.play('hit_steel')
            if result.get('is_headshot'):
                AUDIO.play('bullseye')
            # Steel sparks
            for _ in range(16):
                ang = random.uniform(0, 2 * math.pi)
                spd = random.uniform(2, 6)
                self.particles.append(Particle(
                    hx, hy, math.cos(ang) * spd, math.sin(ang) * spd,
                    (255, 220, 60), random.randint(2, 4), 28, 1.2, gravity=0.15
                ))
        elif t_type == 'clay':
            AUDIO.play('hit_clay')
            # Clay ceramic shards
            for _ in range(14):
                ang = random.uniform(0, 2 * math.pi)
                spd = random.uniform(3, 7.5)
                self.particles.append(Particle(
                    hx, hy, math.cos(ang) * spd, math.sin(ang) * spd,
                    COLOR_CLAY, random.randint(3, 6), 36, 1.0, gravity=0.22
                ))
        elif t_type == 'hostage':
            # Harsh smoke & sparks
            for _ in range(12):
                self.particles.append(Particle(
                    hx, hy, random.uniform(-3, 3), random.uniform(-3, 1),
                    (255, 60, 60), random.randint(3, 5), 30, 1.0, gravity=0.15
                ))

    def spawn_wall_puff(self, x, y):
        # Bullet impact dust on back berm
        for _ in range(5):
            self.particles.append(Particle(
                x, y, random.uniform(-1.5, 1.5), random.uniform(-1.8, 0.5),
                (100, 105, 120), random.randint(3, 6), 18, 1.0, gravity=0.08
            ))

    # -------------------------------------------------------------------------
    # SPAWNING SYSTEM FOR MODES
    # -------------------------------------------------------------------------
    def update_spawns(self, now):
        if self.game_mode == 'REFLEX':
            # Filter dead targets
            self.targets = [t for t in self.targets if not (t.is_dead and t.hit_state >= 1.0)]

            if now >= self.next_spawn_time and len(self.targets) < 4:
                lanes = [220, 380, 540, 700, 860]
                dist = random.choice([15, 25, 40])
                lane_x = random.choice(lanes)
                # Ensure no lane overlap
                if not any(abs(t.x - lane_x) < 70 for t in self.targets):
                    is_hostage = (random.random() < 0.28)  # 28% hostage chance
                    life_dur = random.uniform(1.8, 2.8)
                    y_pos = 460 - int(dist * 3.8)
                    self.targets.append(SteelSilhouetteTarget(lane_x, y_pos, distance_meters=dist,
                                                            is_hostage=is_hostage, lifetime=life_dur))
                    AUDIO.play('slide_rack')
                self.next_spawn_time = now + random.uniform(0.7, 1.5)

        elif self.game_mode == 'CLAY':
            self.targets = [t for t in self.targets if not t.is_dead]
            if now >= self.next_spawn_time and len(self.targets) < 3:
                launch_left = random.choice([True, False])
                if launch_left:
                    sx = -20
                    vx = random.uniform(8.5, 13.0)
                else:
                    sx = SCREEN_WIDTH + 20
                    vx = random.uniform(-13.0, -8.5)
                sy = random.uniform(320, 420)
                vy = random.uniform(-10.0, -7.0)

                self.targets.append(ClayPigeon(sx, sy, vx, vy))
                # Double clay pull chance!
                if random.random() < 0.35:
                    self.targets.append(ClayPigeon(sx + (30 if launch_left else -30), sy + 30, vx * 0.9, vy * 0.95))

                self.next_spawn_time = now + random.uniform(1.8, 3.2)

        elif self.game_mode == 'BULLSEYE':
            # Keep targets moving
            for t in self.targets:
                if hasattr(t, 'update'):
                    t.update()

    # -------------------------------------------------------------------------
    # MAIN LOOP & EVENT HANDLING
    # -------------------------------------------------------------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            now = time.time()
            self.handle_events(now)
            self.update(dt, now)
            self.render()
        pygame.quit()

    def handle_events(self, now):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'PLAYING':
                        self.state = 'PAUSED'
                    elif self.state == 'PAUSED':
                        self.state = 'PLAYING'
                    elif self.state in ['DEBRIEF', 'MENU']:
                        if self.state == 'DEBRIEF':
                            self.state = 'MENU'

                elif event.key == pygame.K_m:
                    AUDIO.toggle_mute()

                elif event.key == pygame.K_r:
                    if self.state == 'PLAYING':
                        self.active_weapon.start_reload(now)

                # Weapon switching keys 1-4
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    idx = event.key - pygame.K_1
                    if idx < len(self.armory):
                        self.current_weapon_idx = idx
                        self.active_weapon = self.armory[idx]
                        self.is_aiming_down_sights = False
                        AUDIO.play('mag_out')

                # Practice distance hotkeys
                elif self.state == 'PLAYING' and self.game_mode == 'PRACTICE':
                    if event.key == pygame.K_c:
                        self.setup_practice_target()
                    elif event.key == pygame.K_UP:
                        self.practice_distance = min(100, self.practice_distance + 10)
                        self.setup_practice_target()
                    elif event.key == pygame.K_DOWN:
                        self.practice_distance = max(10, self.practice_distance - 10)
                        self.setup_practice_target()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Click: Fire or UI click
                    if self.state == 'MENU':
                        self.handle_menu_click(event.pos)
                    elif self.state == 'PLAYING':
                        mx, my = event.pos
                        # Check quickbar weapon slot click
                        quick_w = 260
                        quick_x = (SCREEN_WIDTH - quick_w) // 2
                        handled_ui = False
                        if SCREEN_HEIGHT - 46 <= my <= SCREEN_HEIGHT - 10:
                            for idx in range(len(self.armory)):
                                slot_x = quick_x + idx * 65
                                if slot_x <= mx <= slot_x + 58:
                                    self.current_weapon_idx = idx
                                    self.active_weapon = self.armory[idx]
                                    self.is_aiming_down_sights = False
                                    AUDIO.play('mag_out')
                                    handled_ui = True
                                    break
                        # Check reload card click
                        if not handled_ui and SCREEN_WIDTH - 260 <= mx <= SCREEN_WIDTH - 20 and SCREEN_HEIGHT - 90 <= my <= SCREEN_HEIGHT - 15:
                            self.active_weapon.start_reload(now)
                            handled_ui = True

                        if not handled_ui:
                            self.fire_weapon()
                    elif self.state == 'PAUSED':
                        self.handle_pause_click(event.pos)
                    elif self.state == 'DEBRIEF':
                        self.handle_debrief_click(event.pos)

                elif event.button == 3:  # Right Click: Toggle ADS / Scope
                    if self.state == 'PLAYING' and self.active_weapon.can_scope:
                        self.is_aiming_down_sights = not self.is_aiming_down_sights
                        AUDIO.play('slide_rack')

    def handle_menu_click(self, pos):
        mx, my = pos
        # Cards definition matching render_main_menu bounds
        cards = [
            ("BULLSEYE", 140, 240, 180, 270),
            ("REFLEX", 350, 240, 180, 270),
            ("CLAY", 560, 240, 180, 270),
            ("PRACTICE", 770, 240, 180, 270)
        ]
        for mode, x, y, w, h in cards:
            if pygame.Rect(x, y, w, h).collidepoint(mx, my):
                self.start_mode(mode)
                return

    def handle_pause_click(self, pos):
        mx, my = pos
        cx = SCREEN_WIDTH // 2
        if pygame.Rect(cx - 110, 320, 220, 48).collidepoint(mx, my):
            self.state = 'PLAYING'
        elif pygame.Rect(cx - 110, 385, 220, 48).collidepoint(mx, my):
            self.start_mode(self.game_mode)
        elif pygame.Rect(cx - 110, 450, 220, 48).collidepoint(mx, my):
            self.state = 'MENU'

    def handle_debrief_click(self, pos):
        mx, my = pos
        cx = SCREEN_WIDTH // 2
        if pygame.Rect(cx - 130, 540, 120, 45).collidepoint(mx, my):
            self.start_mode(self.game_mode)
        elif pygame.Rect(cx + 10, 540, 120, 45).collidepoint(mx, my):
            self.state = 'MENU'

    # -------------------------------------------------------------------------
    # UPDATE LOGIC
    # -------------------------------------------------------------------------
    def update(self, dt, now):
        # Update particles & casings always
        self.particles = [p for p in self.particles if p.update()]
        self.casings = [c for c in self.casings if c.update()]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

        # Trauma recovery
        if self.screen_shake > 0:
            self.screen_shake = max(0.0, self.screen_shake - 28.0 * dt)
        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= 1
        if self.recoil_offset_y > 0:
            self.recoil_offset_y = max(0.0, self.recoil_offset_y - 45.0 * dt)

        if self.state == 'PLAYING':
            # Full-auto weapons spray if mouse held
            if self.active_weapon.is_auto and pygame.mouse.get_pressed()[0]:
                self.fire_weapon()

            # Active weapon reload update
            self.active_weapon.update(now)

            # Breath holding & sway update
            keys = pygame.key.get_pressed()
            self.breath_held = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.breath_meter > 5
            if self.breath_held:
                self.breath_meter = max(0.0, self.breath_meter - 25.0 * dt)
            else:
                self.breath_meter = min(100.0, self.breath_meter + 18.0 * dt)
            self.sway_time += dt

            # Round Timer
            if self.game_mode != 'PRACTICE':
                self.mode_timer -= dt
                if self.mode_timer <= 0:
                    self.finish_session()

            # Spawns update
            self.update_spawns(now)

            # Target instances update
            for t in self.targets:
                if hasattr(t, 'update'):
                    t.update()

    def finish_session(self):
        self.state = 'DEBRIEF'
        AUDIO.play('bullseye')
        # Check and update high score
        if self.game_mode in self.highscores:
            if self.score > self.highscores[self.game_mode]:
                self.highscores[self.game_mode] = self.score
                self.save_highscores()

    # -------------------------------------------------------------------------
    # RENDERING METHODS
    # -------------------------------------------------------------------------
    def render(self):
        # Screen shake offset
        render_surf = self.screen
        shake_x = 0
        shake_y = 0
        if self.screen_shake > 0:
            shake_x = int(random.uniform(-self.screen_shake, self.screen_shake))
            shake_y = int(random.uniform(-self.screen_shake, self.screen_shake))

        # Main environment drawing
        is_scoped = self.is_aiming_down_sights and self.active_weapon.can_scope
        self.environment.draw(render_surf, is_scoped=is_scoped)

        # Draw Targets
        for t in self.targets:
            t.draw(render_surf)

        # Draw Casings & Particles
        for c in self.casings:
            c.draw(render_surf)
        for p in self.particles:
            p.draw(render_surf)

        # Muzzle Flash
        if self.muzzle_flash_timer > 0 and not is_scoped:
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 230, 160, 45))
            render_surf.blit(flash_surf, (0, 0))

        # Floating Popups
        for ft in self.floating_texts:
            ft.draw(render_surf)

        # Render Specific State UI
        if self.state == 'MENU':
            self.render_main_menu()
        elif self.state == 'PLAYING':
            self.render_hud(is_scoped)
            self.render_crosshair(is_scoped)
        elif self.state == 'PAUSED':
            self.render_hud(is_scoped)
            self.render_pause_overlay()
        elif self.state == 'DEBRIEF':
            self.render_debrief_screen()

        pygame.display.flip()

    # -------------------------------------------------------------------------
    # RETICLE & ADS / SCOPE RENDERER
    # -------------------------------------------------------------------------
    def render_crosshair(self, is_scoped):
        mx, my = pygame.mouse.get_pos()

        if is_scoped:
            # 3.5x Mil-dot Sniper Scope Mode
            scope_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # Black out perimeter
            scope_r = 230
            scope_surf.fill((0, 0, 0, 248))
            pygame.draw.circle(scope_surf, (0, 0, 0, 0), (mx, my), scope_r)
            # Outer steel scope ring
            pygame.draw.circle(scope_surf, (80, 85, 95), (mx, my), scope_r, 14)
            pygame.draw.circle(scope_surf, (20, 22, 28), (mx, my), scope_r - 7, 3)

            # Mil-dot reticle crosshairs
            pygame.draw.line(scope_surf, (20, 220, 40), (mx - scope_r + 10, my), (mx + scope_r - 10, my), 2)
            pygame.draw.line(scope_surf, (20, 220, 40), (mx, my - scope_r + 10), (mx, my + scope_r - 10), 2)

            # Mil-dots along axes
            for d in [-140, -100, -60, -25, 25, 60, 100, 140]:
                pygame.draw.circle(scope_surf, (20, 220, 40), (mx + d, my), 3)
                pygame.draw.circle(scope_surf, (20, 220, 40), (mx, my + d), 3)

            self.screen.blit(scope_surf, (0, 0))

            # Breath meter readout
            b_color = COLOR_ACCENT_CYAN if self.breath_held else COLOR_TEXT_MUTED
            breath_lbl = FONT_RETICLE.render(f"LUNG CAPACITY: {int(self.breath_meter)}%  [HOLD SHIFT TO STEADY]", True, b_color)
            self.screen.blit(breath_lbl, (mx - 130, my + scope_r + 18))
        else:
            # Dynamic Vector Crosshair based on weapon
            bloom = int(self.recoil_offset_y * 1.5)
            w_idx = self.current_weapon_idx

            if w_idx == 1:  # Shotgun: Wide tactical circle
                radius = 26 + bloom
                pygame.draw.circle(self.screen, COLOR_ACCENT_ORANGE, (mx, my), radius, 2)
                # 4 tick marks
                for dx, dy in [(0, -radius), (0, radius), (-radius, 0), (radius, 0)]:
                    pygame.draw.circle(self.screen, COLOR_ACCENT_ORANGE, (mx + dx, my + dy), 3)
            elif w_idx == 2:  # Rifle: Holographic EOTech style
                radius = 18 + bloom
                pygame.draw.circle(self.screen, COLOR_ACCENT_RED, (mx, my), radius, 1)
                pygame.draw.circle(self.screen, COLOR_ACCENT_RED, (mx, my), 2)
                pygame.draw.line(self.screen, COLOR_ACCENT_RED, (mx - radius - 6, my), (mx - radius + 2, my), 2)
                pygame.draw.line(self.screen, COLOR_ACCENT_RED, (mx + radius - 2, my), (mx + radius + 6, my), 2)
            else:  # Pistol / Sniper hipfire: Crisp precision brackets + red dot
                gap = 7 + bloom
                arm = 9
                color = COLOR_ACCENT_CYAN
                pygame.draw.line(self.screen, color, (mx - gap - arm, my), (mx - gap, my), 2)
                pygame.draw.line(self.screen, color, (mx + gap, my), (mx + gap + arm, my), 2)
                pygame.draw.line(self.screen, color, (mx, my - gap - arm), (mx, my - gap), 2)
                pygame.draw.line(self.screen, color, (mx, my + gap), (mx, my + gap + arm), 2)
                pygame.draw.circle(self.screen, (255, 60, 60), (mx, my), 2)

    # -------------------------------------------------------------------------
    # HUD RENDERER
    # -------------------------------------------------------------------------
    def render_hud(self, is_scoped):
        # 1. Top Tactical Bar
        bar_surf = pygame.Surface((SCREEN_WIDTH, 48), pygame.SRCALPHA)
        bar_surf.fill((16, 20, 28, 220))
        self.screen.blit(bar_surf, (0, 0))
        pygame.draw.line(self.screen, (38, 45, 60), (0, 48), (SCREEN_WIDTH, 48), 2)

        # Mode Badge
        mode_surf = FONT_SUBHEADING.render(f"MODE: {self.game_mode}", True, COLOR_ACCENT_YELLOW)
        self.screen.blit(mode_surf, (20, 13))

        # Time Remaining
        if self.game_mode != 'PRACTICE':
            timer_col = COLOR_ACCENT_RED if self.mode_timer <= 10 else COLOR_TEXT_WHITE
            timer_text = FONT_DIGIT.render(f"TIME: {max(0, int(self.mode_timer))}s", True, timer_col)
            t_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 24))
            self.screen.blit(timer_text, t_rect)

        # Score & Combo
        score_text = FONT_DIGIT.render(f"SCORE: {self.score}", True, COLOR_TEXT_WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 280, 12))

        combo_col = COLOR_ACCENT_ORANGE if self.combo > 1 else COLOR_TEXT_MUTED
        combo_text = FONT_SUBHEADING.render(f"x{self.combo}.0", True, combo_col)
        self.screen.blit(combo_text, (SCREEN_WIDTH - 100, 13))

        # 2. Bottom-Left Live Stats Card
        stats_surf = pygame.Surface((220, 75), pygame.SRCALPHA)
        stats_surf.fill((20, 24, 34, 210))
        pygame.draw.rect(stats_surf, (50, 58, 76), (0, 0, 220, 75), 1, border_radius=6)
        self.screen.blit(stats_surf, (20, SCREEN_HEIGHT - 90))

        acc = (self.total_hits / self.total_shots * 100) if self.total_shots > 0 else 0
        s1 = FONT_BODY_BOLD.render(f"ACCURACY: {acc:.1f}%", True, COLOR_ACCENT_GREEN if acc > 70 else COLOR_TEXT_WHITE)
        s2 = FONT_BODY.render(f"HITS: {self.total_hits} / SHOTS: {self.total_shots}", True, COLOR_TEXT_MUTED)
        s3 = FONT_BODY.render(f"BULLSEYES: {self.bullseyes_hit}  |  STREAK: {self.consecutive_hits}", True, COLOR_ACCENT_CYAN)
        self.screen.blit(s1, (30, SCREEN_HEIGHT - 85))
        self.screen.blit(s2, (30, SCREEN_HEIGHT - 66))
        self.screen.blit(s3, (30, SCREEN_HEIGHT - 48))

        # 3. Bottom-Right Weapon Card
        wpn_surf = pygame.Surface((240, 75), pygame.SRCALPHA)
        wpn_surf.fill((20, 24, 34, 210))
        pygame.draw.rect(wpn_surf, (50, 58, 76), (0, 0, 240, 75), 1, border_radius=6)
        self.screen.blit(wpn_surf, (SCREEN_WIDTH - 260, SCREEN_HEIGHT - 90))

        w_name = FONT_SUBHEADING.render(self.active_weapon.name, True, COLOR_TEXT_WHITE)
        self.screen.blit(w_name, (SCREEN_WIDTH - 248, SCREEN_HEIGHT - 85))

        cal_lbl = FONT_RETICLE.render(self.active_weapon.caliber, True, COLOR_TEXT_MUTED)
        self.screen.blit(cal_lbl, (SCREEN_WIDTH - 248, SCREEN_HEIGHT - 65))

        # Ammo Counter Display
        ammo_col = COLOR_ACCENT_RED if self.active_weapon.current_ammo <= 2 else COLOR_ACCENT_YELLOW
        ammo_str = f"{self.active_weapon.current_ammo} / {self.active_weapon.mag_size}"
        ammo_txt = FONT_DIGIT.render(ammo_str, True, ammo_col)
        self.screen.blit(ammo_txt, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 82))

        # Reloading Progress Indicator
        if self.active_weapon.is_reloading:
            pct = self.active_weapon.reload_progress
            prog_rect = pygame.Rect(SCREEN_WIDTH - 248, SCREEN_HEIGHT - 32, int(216 * pct), 8)
            pygame.draw.rect(self.screen, (40, 48, 64), (SCREEN_WIDTH - 248, SCREEN_HEIGHT - 32, 216, 8), border_radius=4)
            pygame.draw.rect(self.screen, COLOR_ACCENT_YELLOW, prog_rect, border_radius=4)
            rl_lbl = FONT_RETICLE.render(f"RELOADING... {int(pct*100)}%", True, COLOR_ACCENT_YELLOW)
            self.screen.blit(rl_lbl, (SCREEN_WIDTH - 248, SCREEN_HEIGHT - 48))
        else:
            hint_txt = FONT_RETICLE.render("[R] RELOAD  |  [1-4] SWITCH WEAPON", True, (90, 100, 120))
            self.screen.blit(hint_txt, (SCREEN_WIDTH - 248, SCREEN_HEIGHT - 32))

        # 4. Weapon Selection Quickbar (Center Bottom)
        quick_w = 260
        quick_x = (SCREEN_WIDTH - quick_w) // 2
        for idx, w in enumerate(self.armory):
            slot_x = quick_x + idx * 65
            slot_rect = pygame.Rect(slot_x, SCREEN_HEIGHT - 44, 58, 32)
            is_active = (idx == self.current_weapon_idx)
            slot_bg = (40, 48, 68) if is_active else (24, 28, 38)
            border_col = COLOR_ACCENT_CYAN if is_active else (50, 56, 72)
            pygame.draw.rect(self.screen, slot_bg, slot_rect, border_radius=4)
            pygame.draw.rect(self.screen, border_col, slot_rect, 2 if is_active else 1, border_radius=4)

            num_lbl = FONT_RETICLE.render(f"[{idx+1}]", True, COLOR_ACCENT_YELLOW if is_active else COLOR_TEXT_MUTED)
            self.screen.blit(num_lbl, (slot_x + 5, SCREEN_HEIGHT - 40))
            short_name = w.name.split()[0]
            sn_lbl = FONT_RETICLE.render(short_name, True, COLOR_TEXT_WHITE if is_active else COLOR_TEXT_MUTED)
            self.screen.blit(sn_lbl, (slot_x + 22, SCREEN_HEIGHT - 40))

        # Practice Mode Controls Banner
        if self.game_mode == 'PRACTICE':
            prac_surf = FONT_RETICLE.render(
                f"PRACTICE RANGE  |  DISTANCE: {self.practice_distance}m [UP/DOWN]  |  [C] RESET TARGET / CLEAR SHOTS",
                True, COLOR_ACCENT_YELLOW
            )
            p_rect = prac_surf.get_rect(center=(SCREEN_WIDTH // 2, 70))
            self.screen.blit(prac_surf, p_rect)

            # MOA / Group spread calculations
            if len(self.practice_shots) >= 3:
                xs = [p[0] for p in self.practice_shots]
                ys = [p[1] for p in self.practice_shots]
                group_w = max(xs) - min(xs)
                group_h = max(ys) - min(ys)
                spread_px = math.hypot(group_w, group_h)
                # MOA approximation at virtual distance
                moa = (spread_px / (self.practice_distance * 0.45))
                group_lbl = FONT_RETICLE.render(f"GROUP SIZE: {spread_px:.1f} px  (~{moa:.2f} MOA)", True, COLOR_ACCENT_GREEN)
                self.screen.blit(group_lbl, (SCREEN_WIDTH // 2 - 80, 88))

    # -------------------------------------------------------------------------
    # MAIN MENU SCREEN
    # -------------------------------------------------------------------------
    def render_main_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((12, 14, 20, 235))
        self.screen.blit(overlay, (0, 0))

        # Title Banner
        title_surf = FONT_TITLE.render("APEX SHOOTING CLUB", True, COLOR_ACCENT_YELLOW)
        t_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title_surf, t_rect)

        sub_surf = FONT_SUBHEADING.render("PRECISION TACTICAL TARGET SIMULATOR", True, COLOR_TEXT_MUTED)
        s_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 168))
        self.screen.blit(sub_surf, s_rect)

        # Mode Selection Cards
        modes_info = [
            {
                "id": "BULLSEYE", "title": "BULLSEYE", "icon": "🎯",
                "desc": "Concentric 60s timed paper precision test at variable ranges.",
                "color": COLOR_ACCENT_CYAN, "x": 140
            },
            {
                "id": "REFLEX", "title": "TACTICAL REFLEX", "icon": "⚡",
                "desc": "Reactive steel poppers & hostage no-shoots. Speed & trigger discipline!",
                "color": COLOR_ACCENT_RED, "x": 350
            },
            {
                "id": "CLAY", "title": "SKEET TRAP", "icon": "💥",
                "desc": "Flying orange clay pigeons in parabolic arcs. Shotgun mastery!",
                "color": COLOR_ACCENT_ORANGE, "x": 560
            },
            {
                "id": "PRACTICE", "title": "ARMORY PRACTICE", "icon": "🔧",
                "desc": "Zeroing, MOA grouping spread test, custom distance & recoil training.",
                "color": COLOR_ACCENT_GREEN, "x": 770
            }
        ]

        mx, my = pygame.mouse.get_pos()
        for m in modes_info:
            card_rect = pygame.Rect(m["x"], 240, 180, 270)
            is_hover = card_rect.collidepoint(mx, my)
            bg_col = (28, 34, 48) if is_hover else (20, 24, 34)
            border_col = m["color"] if is_hover else (45, 52, 70)

            pygame.draw.rect(self.screen, bg_col, card_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_col, card_rect, 2 if is_hover else 1, border_radius=8)

            # Icon & Title
            icon_s = FONT_TITLE.render(m["icon"], True, m["color"])
            self.screen.blit(icon_s, icon_s.get_rect(center=(m["x"] + 90, 285)))

            t_s = FONT_SUBHEADING.render(m["title"], True, COLOR_TEXT_WHITE)
            self.screen.blit(t_s, t_s.get_rect(center=(m["x"] + 90, 340)))

            # Description (word wrapped manually)
            words = m["desc"].split()
            lines = []
            curr = []
            for w in words:
                curr.append(w)
                if len(" ".join(curr)) > 20:
                    lines.append(" ".join(curr[:-1]))
                    curr = [w]
            if curr:
                lines.append(" ".join(curr))

            for l_idx, line in enumerate(lines):
                desc_s = FONT_BODY.render(line, True, COLOR_TEXT_MUTED)
                self.screen.blit(desc_s, desc_s.get_rect(center=(m["x"] + 90, 380 + l_idx * 18)))

            # High Score Display on Card
            if m["id"] in self.highscores:
                best_s = FONT_RETICLE.render(f"RECORD: {self.highscores[m['id']]}", True, COLOR_ACCENT_YELLOW)
                self.screen.blit(best_s, best_s.get_rect(center=(m["x"] + 90, 455)))

            # Play Button prompt
            btn_rect = pygame.Rect(m["x"] + 20, 475, 140, 26)
            btn_col = m["color"] if is_hover else (35, 42, 58)
            pygame.draw.rect(self.screen, btn_col, btn_rect, border_radius=4)
            btn_lbl = FONT_RETICLE.render("SELECT MODE ▶", True, (0, 0, 0) if is_hover else COLOR_TEXT_WHITE)
            self.screen.blit(btn_lbl, btn_lbl.get_rect(center=btn_rect.center))

        # Bottom Controls Guide
        guide_surf = FONT_BODY.render(
            "CONTROLS:  [L-CLICK] Fire  |  [R-CLICK] Sniper Scope (ADS)  |  [R] Reload  |  [1-4] Armory  |  [M] Mute Sound",
            True, (100, 110, 130)
        )
        self.screen.blit(guide_surf, guide_surf.get_rect(center=(SCREEN_WIDTH // 2, 590)))

    # -------------------------------------------------------------------------
    # PAUSE OVERLAY
    # -------------------------------------------------------------------------
    def render_pause_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 16, 210))
        self.screen.blit(overlay, (0, 0))

        cx = SCREEN_WIDTH // 2
        p_title = FONT_TITLE.render("RANGE PAUSED", True, COLOR_ACCENT_YELLOW)
        self.screen.blit(p_title, p_title.get_rect(center=(cx, 240)))

        buttons = [
            ("RESUME FIRING", 320, COLOR_ACCENT_GREEN),
            ("RESTART ROUND", 385, COLOR_ACCENT_YELLOW),
            ("RETURN TO LOBBY", 450, COLOR_ACCENT_RED)
        ]
        mx, my = pygame.mouse.get_pos()
        for text, y_pos, col in buttons:
            btn_rect = pygame.Rect(cx - 110, y_pos, 220, 48)
            is_hover = btn_rect.collidepoint(mx, my)
            pygame.draw.rect(self.screen, (32, 38, 52) if is_hover else (20, 24, 34), btn_rect, border_radius=6)
            pygame.draw.rect(self.screen, col if is_hover else (50, 58, 76), btn_rect, 2, border_radius=6)
            b_s = FONT_SUBHEADING.render(text, True, COLOR_TEXT_WHITE if not is_hover else col)
            self.screen.blit(b_s, b_s.get_rect(center=btn_rect.center))

    # -------------------------------------------------------------------------
    # DEBRIEF / RESULTS SCREEN
    # -------------------------------------------------------------------------
    def render_debrief_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 16, 235))
        self.screen.blit(overlay, (0, 0))

        cx = SCREEN_WIDTH // 2
        d_title = FONT_TITLE.render("SESSION DEBRIEF", True, COLOR_ACCENT_YELLOW)
        self.screen.blit(d_title, d_title.get_rect(center=(cx, 130)))

        # Card container
        card_rect = pygame.Rect(cx - 240, 180, 480, 330)
        pygame.draw.rect(self.screen, (22, 26, 38), card_rect, border_radius=10)
        pygame.draw.rect(self.screen, (50, 60, 80), card_rect, 2, border_radius=10)

        # Calculate Rank
        acc = (self.total_hits / self.total_shots * 100) if self.total_shots > 0 else 0
        if self.score >= 3200 and acc >= 75:
            rank_name = "🏅 CLUB LEGEND"
            rank_col = COLOR_ACCENT_YELLOW
        elif self.score >= 2200:
            rank_name = "🥇 MASTER GUNNER"
            rank_col = COLOR_ACCENT_CYAN
        elif self.score >= 1400:
            rank_name = "🥈 SHARPSHOOTER"
            rank_col = COLOR_ACCENT_GREEN
        elif self.score >= 700:
            rank_name = "🥉 MARKSMAN"
            rank_col = (200, 160, 80)
        else:
            rank_name = "🎖️ RECRUIT"
            rank_col = COLOR_TEXT_MUTED

        r_lbl = FONT_HEADING.render(f"AWARDED RANK: {rank_name}", True, rank_col)
        self.screen.blit(r_lbl, r_lbl.get_rect(center=(cx, 225)))

        # Metrics Table
        stats = [
            ("FINAL SCORE:", f"{self.score} PTS", COLOR_ACCENT_YELLOW),
            ("HIGH SCORE:", f"{self.highscores.get(self.game_mode, 0)} PTS", COLOR_TEXT_WHITE),
            ("SHOT ACCURACY:", f"{acc:.1f}% ({self.total_hits}/{self.total_shots})", COLOR_ACCENT_GREEN),
            ("MAX COMBO STREAK:", f"x{self.max_combo}.0", COLOR_ACCENT_ORANGE),
            ("BULLSEYES / HEADSHOTS:", f"{self.bullseyes_hit}", COLOR_ACCENT_CYAN)
        ]

        for s_idx, (label, val, col) in enumerate(stats):
            sy = 275 + s_idx * 38
            l_s = FONT_SUBHEADING.render(label, True, COLOR_TEXT_MUTED)
            v_s = FONT_SUBHEADING.render(val, True, col)
            self.screen.blit(l_s, (cx - 200, sy))
            self.screen.blit(v_s, (cx + 40, sy))

        # Bottom Buttons
        mx, my = pygame.mouse.get_pos()
        b_retry = pygame.Rect(cx - 130, 540, 120, 45)
        b_menu = pygame.Rect(cx + 10, 540, 120, 45)

        is_ret_hover = b_retry.collidepoint(mx, my)
        is_menu_hover = b_menu.collidepoint(mx, my)

        pygame.draw.rect(self.screen, (32, 40, 56) if is_ret_hover else (22, 28, 40), b_retry, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_ACCENT_GREEN if is_ret_hover else (50, 60, 80), b_retry, 2, border_radius=6)
        ret_s = FONT_SUBHEADING.render("RETRY ↺", True, COLOR_ACCENT_GREEN if is_ret_hover else COLOR_TEXT_WHITE)
        self.screen.blit(ret_s, ret_s.get_rect(center=b_retry.center))

        pygame.draw.rect(self.screen, (32, 40, 56) if is_menu_hover else (22, 28, 40), b_menu, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_ACCENT_YELLOW if is_menu_hover else (50, 60, 80), b_menu, 2, border_radius=6)
        menu_s = FONT_SUBHEADING.render("LOBBY ⌂", True, COLOR_ACCENT_YELLOW if is_menu_hover else COLOR_TEXT_WHITE)
        self.screen.blit(menu_s, menu_s.get_rect(center=b_menu.center))

# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    game = ShootingClubGame()
    game.run()

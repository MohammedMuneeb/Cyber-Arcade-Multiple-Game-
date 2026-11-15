import pygame 
import random 

import math 
pygame.init () 
pygame.font.init () 

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HIGHT = 600

# Colors (RGB) - Classic vector arcade style (Black & White/Neon Cyan)

BLACK = (10, 10, 15 ) 
WHITE = (255, 255, 255 ) 
CYAN = (0, 220, 255 ) 
RED = (255, 75, 75 ) 
GRAY = (120, 120, 140 ) 

class Spaceship : 
    def __init__(self , x , y ): 
        self.x = x 

        self.y = y 
        self.angle = 0  # Facing straight up initially
        self.velocity_x = 0
        self.velocity_y = 0
        self.radius = 16
        self.rotation_speed = 4.5
        self.acceleration = 0.15
        self.friction = 0.985
        self.max_speed = 7.0
        self.is_thrusting = False

    def rotate(self, dir):
        self.angle += dir * self.rotation_speed

    def thrust(self):
        rad = math.radians(self.angle)
        self.velocity_x += math.sin(rad) * self.acceleration
        self.velocity_y -= math.cos(rad) * self.acceleration
        
        # Cap max speed
        speed = math.hypot(self.velocity_x, self.velocity_y)
        if speed > self.max_speed:
            self.velocity_x = (self.velocity_x / speed) * self.max_speed
            self.velocity_y = (self.velocity_y / speed) * self.max_speed
        self.is_thrusting = True

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction

        # Screen wrapping
        if self.x < 0: self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH: self.x = 0
        if self.y < 0: self.y = SCREEN_HIGHT
        elif self.y > SCREEN_HIGHT: self.y = 0

    def draw(self, surface):
        rad = math.radians(self.angle)
        
        # Calculate triangle points for the ship
        tip_x = self.x + math.sin(rad) * 18
        tip_y = self.y - math.cos(rad) * 18
        
        left_x = self.x - math.sin(rad + math.radians(140)) * 14
        left_y = self.y + math.cos(rad + math.radians(140)) * 14
        
        right_x = self.x - math.sin(rad - math.radians(140)) * 14
        right_y = self.y + math.cos(rad - math.radians(140)) * 14

        pygame.draw.polygon(surface, CYAN, [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)], 2)

        # Draw thruster flame if active
        if self.is_thrusting:
            back_x = self.x - math.sin(rad) * 16
            back_y = self.y + math.cos(rad) * 16
            flame_x = self.x - math.sin(rad) * 24
            flame_y = self.y + math.cos(rad) * 24
            pygame.draw.line(surface, RED, (back_x, back_y), (flame_x, flame_y), 2)
            self.is_thrusting = False

class Laser:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10.0
        rad = math.radians(angle)
        self.velocity_x = math.sin(rad) * self.speed
        self.velocity_y = -math.cos(rad) * self.speed
        self.life_time = 50 # Frames before disappearing

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.life_time -= 1

        # Screen wrapping for lasers
        if self.x < 0: self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH: self.x = 0
        if self.y < 0: self.y = SCREEN_HIGHT
        elif self.y > SCREEN_HIGHT: self.y = 0

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 3)

class Asteroid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size # 3: Large, 2: Medium, 1: Small
        
        if size == 3:
            self.radius = 40
            self.score_value = 20
        elif size == 2:
            self.radius = 20
            self.score_value = 50
        else:
            self.radius = 10
            self.score_value = 100

        self.speed = random.uniform(1.0, 3.0) / (4 - size)
        self.angle = random.uniform(0, 360)
        rad = math.radians(random.uniform(0, 360))
        self.velocity_x = math.sin(rad) * self.speed
        self.velocity_y = math.cos(rad) * self.speed
        
        # Generate jagged vector shape offsets
        self.shape_offsets = [random.uniform(0.75, 1.25) for _ in range(10)]

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Screen wrapping
        if self.x < -self.radius: self.x = SCREEN_WIDTH + self.radius
        elif self.x > SCREEN_WIDTH + self.radius: self.x = -self.radius
        if self.y < -self.radius: self.y = SCREEN_HIGHT + self.radius
        elif self.y > SCREEN_HIGHT + self.radius: self.y = -self.radius

    def draw(self, surface):
        points = []
        num_points = len(self.shape_offsets)
        for i in range(num_points):
            angle = (i / num_points) * math.pi * 2
            r = self.radius * self.shape_offsets[i]
            px = self.x + math.cos(angle) * r
            py = self.y + math.sin(angle) * r
            points.append((px, py))
        pygame.draw.polygon(surface, WHITE, points, 2)

class AsteroidsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        pygame.display.set_caption("Classic Asteroids — Python Pygame")
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont("Courier", 16, bold=True)
        self.font_large = pygame.font.SysFont("Courier", 28, bold=True)

        self.reset_game()

    def reset_game(self):
        self.ship = Spaceship(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2)
        self.lasers = []
        self.asteroids = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.spawn_wave()

    def spawn_wave(self):
        self.asteroids = []
        num_asteroids = 3 + self.level * 2
        for _ in range(num_asteroids):
            # Spawn away from center where ship starts
            while True:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HIGHT)
                if math.hypot(x - self.ship.x, y - self.ship.y) > 150:
                    break
            self.asteroids.append(Asteroid(x, y, 3))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_SPACE:
                        if len(self.lasers) < 6:  # Max 6 lasers on screen
                            self.lasers.append(Laser(self.ship.x, self.ship.y, self.ship.angle))
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            if not self.game_over:
                # Continuous key handling for smooth movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.ship.rotate(-1)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.ship.rotate(1)
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.ship.thrust()

                # Update ship
                self.ship.update()

                # Update lasers
                for laser in self.lasers[:]:
                    laser.update()
                    if laser.life_time <= 0:
                        self.lasers.remove(laser)

                # Update asteroids
                for asteroid in self.asteroids:
                    asteroid.update()

                # Collision detection: Lasers vs Asteroids
                new_asteroids = []
                for laser in self.lasers[:]:
                    laser_removed = False
                    for asteroid in self.asteroids[:]:
                        if math.hypot(laser.x - asteroid.x, laser.y - asteroid.y) < asteroid.radius:
                            # Hit!
                            self.score += asteroid.score_value
                            if laser in self.lasers:
                                self.lasers.remove(laser)
                            laser_removed = True
                            
                            # Split asteroid
                            if asteroid.size > 1:
                                new_asteroids.append(Asteroid(asteroid.x, asteroid.y, asteroid.size - 1))
                                new_asteroids.append(Asteroid(asteroid.x, asteroid.y, asteroid.size - 1))
                            
                            self.asteroids.remove(asteroid)
                            break
                    if laser_removed:
                        pass

                self.asteroids.extend(new_asteroids)

                # Collision detection: Ship vs Asteroids
                for asteroid in self.asteroids:
                    if math.hypot(self.ship.x - asteroid.x, self.ship.y - asteroid.y) < self.ship.radius + asteroid.radius - 5:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over = True
                        else:
                            # Respawn ship in center safely
                            self.ship = Spaceship(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2)
                        break

                # Advance wave if all asteroids cleared
                if len(self.asteroids) == 0:
                    self.level += 1
                    self.spawn_wave()

            self.draw()

        pygame.quit()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw game entities
        if not self.game_over:
            self.ship.draw(self.screen)

        for laser in self.lasers:
            laser.draw(self.screen)

        for asteroid in self.asteroids:
            asteroid.draw(self.screen)

        # Draw HUD (Score, Lives, Level)
        score_surf = self.font_small.render(f"SCORE: {self.score}", True, WHITE)
        lives_surf = self.font_small.render(f"LIVES: {'▲ ' * self.lives}", True, CYAN)
        level_surf = self.font_small.render(f"WAVE: {self.level}", True, GRAY)

        self.screen.blit(score_surf, (20, 20))
        self.screen.blit(lives_surf, (20, 45))
        self.screen.blit(level_surf, (SCREEN_WIDTH - 120, 20))

        # Game Over Overlay
        if self.game_over:
            go_surf = self.font_large.render("GAME OVER", True, RED)
            restart_surf = self.font_small.render("PRESS 'R' TO RESTART", True, WHITE)
            
            self.screen.blit(go_surf, (SCREEN_WIDTH // 2 - go_surf.get_width() // 2, SCREEN_HIGHT // 2 - 30))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, SCREEN_HIGHT // 2 + 20))

        pygame.display.flip()

if __name__ == "__main__": 
    game = AsteroidsGame () 
    game.run ()  
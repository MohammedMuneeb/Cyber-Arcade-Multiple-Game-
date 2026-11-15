import pygame
import random

pygame.init () 
# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HIGHT = 600
BLOCK_SIZE = 30

# Playfield dimensions
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20

PLAYFIELD_X = 30
PLAYFIELD_Y = 30 
# Colors (RGB)
BLACK = (15, 15, 25)
DARK_GRAY = (30, 30, 45)
LIGHT_GRAY = (60, 60, 80)
WHITE = (255, 255, 255)
CYAN = (0, 210, 255)
YELLOW = (255, 230, 0)
MAGENTA = (200, 0, 255)
ORANGE = (255, 140, 0)
BLUE = (0, 100, 255)
GREEN = (46, 204, 113)
RED = (231, 76, 60)

SHAPES = [
    [[1, 1, 1, 1]],                 # I
    [[1, 1], [1, 1]],               # O
    [[0, 1, 0], [1, 1, 1]],         # T
    [[0, 0, 1], [1, 1, 1]],         # L
    [[1, 0, 0], [1, 1, 1]],         # J
    [[0, 1, 1], [1, 1, 0]],         # S
    [[1, 1, 0], [0, 1, 1]]          # Z
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class TetrisPiece:
    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.shape = SHAPES[shape_idx]
        self.color = SHAPE_COLORS[shape_idx]

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        pygame.display.set_caption("Classic Tetris — Python Pygame")
        self.clock = pygame.time.Clock()
        
        self.font_small = pygame.font.SysFont("Helvetica", 14, bold=True)
        self.font_med = pygame.font.SysFont("Helvetica", 18, bold=True)
        self.font_large = pygame.font.SysFont("Helvetica", 24, bold=True)

        self.grid = [[0 for _ in range(PLAYFIELD_WIDTH)] for _ in range(PLAYFIELD_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False

        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()

        self.fall_time = 0
        self.fall_speed = 500  # Milliseconds per drop

    def get_new_piece(self):
        idx = random.randint(0, len(SHAPES) - 1)
        # Spawn near top center
        return TetrisPiece(PLAYFIELD_WIDTH // 2 - len(SHAPES[idx][0]) // 2, 0, idx)

    def valid_move(self, piece, dx, dy, rotated_shape=None):
        shape = rotated_shape if rotated_shape else piece.shape
        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    new_x = piece.x + c + dx
                    new_y = piece.y + r + dy
                    if new_x < 0 or new_x >= PLAYFIELD_WIDTH or new_y >= PLAYFIELD_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False
        return True

    def merge_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, val in enumerate(row):
                if val:
                    if self.current_piece.y + r >= 0:
                        self.grid[self.current_piece.y + r][self.current_piece.x + c] = self.current_piece.color

    def clear_lines(self):
        full_rows = []
        for r, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                full_rows.append(r)

        if full_rows:
            for r in full_rows:
                del self.grid[r]
                self.grid.insert(0, [0 for _ in range(PLAYFIELD_WIDTH)])
            
            num_cleared = len(full_rows)
            self.lines_cleared += num_cleared
            self.score += (num_cleared * 100) * self.level
            self.level = 1 + self.lines_cleared // 10
            self.fall_speed = max(100, 500 - (self.level - 1) * 40)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)
            self.fall_time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, -1, 0):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, 1, 0):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, 0, 1):
                            self.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        # Rotate check
                        old_shape = self.current_piece.shape
                        self.current_piece.rotate()
                        if not self.valid_move(self.current_piece, 0, 0, self.current_piece.shape):
                            # Revert rotation if invalid
                            self.current_piece.shape = old_shape
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while self.valid_move(self.current_piece, 0, 1):
                            self.current_piece.y += 1
                        self.merge_piece()
                        self.clear_lines()
                        self.current_piece = self.next_piece
                        self.next_piece = self.get_new_piece()
                        if not self.valid_move(self.current_piece, 0, 0):
                            self.game_over = True
                elif event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()

            # Automatic falling
            if not self.game_over and self.fall_time >= self.fall_speed:
                self.fall_time = 0
                if self.valid_move(self.current_piece, 0, 1):
                    self.current_piece.y += 1
                else:
                    self.merge_piece()
                    self.clear_lines()
                    self.current_piece = self.next_piece
                    self.next_piece = self.get_new_piece()
                    if not self.valid_move(self.current_piece, 0, 0):
                        self.game_over = True

            self.draw()

        pygame.quit()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw Playfield Grid Background & Board blocks
        pygame.draw.rect(self.screen, DARK_GRAY, (PLAYFIELD_X, PLAYFIELD_Y, PLAYFIELD_WIDTH * BLOCK_SIZE, PLAYFIELD_HEIGHT * BLOCK_SIZE))
        
        for r in range(PLAYFIELD_HEIGHT):
            for c in range(PLAYFIELD_WIDTH):
                cell_color = self.grid[r][c]
                rect = pygame.Rect(PLAYFIELD_X + c * BLOCK_SIZE, PLAYFIELD_Y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if cell_color != 0:
                    pygame.draw.rect(self.screen, cell_color, rect)
                    pygame.draw.rect(self.screen, LIGHT_GRAY, rect, 1)
                else:
                    pygame.draw.rect(self.screen, (20, 20, 32), rect, 1)

        # Draw Current Falling Piece
        if not self.game_over:
            for r, row in enumerate(self.current_piece.shape):
                for c, val in enumerate(row):
                    if val:
                        px = PLAYFIELD_X + (self.current_piece.x + c) * BLOCK_SIZE
                        py = PLAYFIELD_Y + (self.current_piece.y + r) * BLOCK_SIZE
                        if py >= PLAYFIELD_Y:
                            rect = pygame.Rect(px, py, BLOCK_SIZE, BLOCK_SIZE)
                            pygame.draw.rect(self.screen, self.current_piece.color, rect)
                            pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Draw Sidebar UI (Score, Level, Next Piece Preview)
        sidebar_x = PLAYFIELD_X + PLAYFIELD_WIDTH * BLOCK_SIZE + 20
        
        title_surf = self.font_large.render("TETRIS", True, CYAN)
        self.screen.blit(title_surf, (sidebar_x, PLAYFIELD_Y))

        # Score Box
        pygame.draw.rect(self.screen, DARK_GRAY, (sidebar_x, PLAYFIELD_Y + 50, 110, 70), border_radius=6)
        self.screen.blit(self.font_small.render("SCORE", True, LIGHT_GRAY), (sidebar_x + 10, PLAYFIELD_Y + 58))
        self.screen.blit(self.font_med.render(str(self.score), True, WHITE), (sidebar_x + 10, PLAYFIELD_Y + 85))

        # Level & Lines Box
        pygame.draw.rect(self.screen, DARK_GRAY, (sidebar_x, PLAYFIELD_Y + 135, 110, 90), border_radius=6)
        self.screen.blit(self.font_small.render(f"LEVEL: {self.level}", True, WHITE), (sidebar_x + 10, PLAYFIELD_Y + 145))
        self.screen.blit(self.font_small.render(f"LINES: {self.lines_cleared}", True, WHITE), (sidebar_x + 10, PLAYFIELD_Y + 175))

        # Next Piece Preview Box
        self.screen.blit(self.font_small.render("NEXT PIECE", True, LIGHT_GRAY), (sidebar_x, PLAYFIELD_Y + 245))
        pygame.draw.rect(self.screen, DARK_GRAY, (sidebar_x, PLAYFIELD_Y + 270, 110, 110), border_radius=6)
        
        # Render Next Piece in Box
        np_shape = self.next_piece.shape
        np_color = self.next_piece.color
        np_rows = len(np_shape)
        np_cols = len(np_shape[0])
        block_sz = 20
        start_x = sidebar_x + 55 - (np_cols * block_sz) // 2
        start_y = PLAYFIELD_Y + 325 - (np_rows * block_sz) // 2

        for r, row in enumerate(np_shape):
            for c, val in enumerate(row):
                if val:
                    rect = pygame.Rect(start_x + c * block_sz, start_y + r * block_sz, block_sz, block_sz)
                    pygame.draw.rect(self.screen, np_color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Game Over Overlay
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HIGHT), pygame.SRCALPHA)
            overlay.fill((15, 15, 25, 220))
            self.screen.blit(overlay, (0, 0))

            go_surf = self.font_large.render("GAME OVER", True, RED)
            restart_surf = self.font_med.render("Press 'R' to Restart", True, WHITE)
            
            self.screen.blit(go_surf, (SCREEN_WIDTH // 2 - go_surf.get_width() // 2, SCREEN_HIGHT // 2 - 40))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, SCREEN_HIGHT // 2 + 10))

        pygame.display.flip()

    def reset_game(self):
        self.grid = [[0 for _ in range(PLAYFIELD_WIDTH)] for _ in range(PLAYFIELD_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = 500
        self.game_over = False
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()

if __name__ == "__main__": 

    game = TetrisGame () 
    game .run () 
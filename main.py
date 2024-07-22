# main.py

import pygame
import sys
from game_logic import Game2048

# Initialize Pygame
pygame.init()

# Constants
SIZE = WIDTH, HEIGHT = 400, 500  # Increase height to make space for the score and retry button
TILE_SIZE = WIDTH // 4
ANIMATION_FRAMES = 10
ANIMATION_DELAY = 20  # milliseconds

# Colors
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_TILE_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
FONT = pygame.font.Font(None, 55)
SMALL_FONT = pygame.font.Font(None, 30)
SCORE_FONT = pygame.font.Font(None, 45)

# Create the game
game = Game2048()

# Set up the display
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('2048')

def draw_rounded_rect(surface, color, rect, corner_radius):
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)

    # Create a temporary surface with transparent background
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0))
    
    pygame.draw.rect(temp_surface, color, (0, 0, rect.width, rect.height), border_radius=corner_radius)
    surface.blit(temp_surface, rect.topleft)

def draw_grid():
    for r in range(4):
        for c in range(4):
            value = game.grid[r][c]
            color = TILE_COLORS.get(value, EMPTY_TILE_COLOR)
            draw_rounded_rect(screen, color, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE), 10)
            if value != 0:
                text = FONT.render(str(value), True, (119, 110, 101))
                text_rect = text.get_rect(center=(c * TILE_SIZE + TILE_SIZE / 2, r * TILE_SIZE + TILE_SIZE / 2))
                screen.blit(text, text_rect)

def draw_score():
    score_text = SCORE_FONT.render(f"Score: {game.score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 410))

def draw_retry_button():
    retry_rect = pygame.Rect(250, 410, 130, 60)
    pygame.draw.rect(screen, (119, 110, 101), retry_rect, border_radius=10)
    retry_text = SMALL_FONT.render("Retry", True, (255, 255, 255))
    retry_text_rect = retry_text.get_rect(center=retry_rect.center)
    screen.blit(retry_text, retry_text_rect)
    return retry_rect

def animate_movement():
    for step in range(ANIMATION_FRAMES):
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_score()
        draw_retry_button()
        for r in range(4):
            for c in range(4):
                value = game.grid[r][c]
                if value == 0:
                    continue
                color = TILE_COLORS.get(value, EMPTY_TILE_COLOR)
                target_rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                for (move_r, move_c, action) in game.movement_data:
                    if action == 'move' and (r, c) == (move_r, move_c):
                        initial_pos = (c * TILE_SIZE, r * TILE_SIZE)
                        final_pos = (move_c * TILE_SIZE, move_r * TILE_SIZE)
                        current_pos = (
                            initial_pos[0] + (final_pos[0] - initial_pos[0]) * (step / ANIMATION_FRAMES),
                            initial_pos[1] + (final_pos[1] - initial_pos[1]) * (step / ANIMATION_FRAMES)
                        )
                        target_rect = pygame.Rect(current_pos[0], current_pos[1], TILE_SIZE, TILE_SIZE)
                draw_rounded_rect(screen, color, target_rect, 10)
                if value != 0:
                    text = FONT.render(str(value), True, (119, 110, 101))
                    text_rect = text.get_rect(center=target_rect.center)
                    screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(ANIMATION_DELAY)  # Delay to control animation speed

# Main game loop
running = True
game_over = False

while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_score()
    retry_button_rect = draw_retry_button()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            moved = False
            if event.key == pygame.K_LEFT:
                moved = game.move_left()
            elif event.key == pygame.K_RIGHT:
                moved = game.move_right()
            elif event.key == pygame.K_UP:
                moved = game.move_up()
            elif event.key == pygame.K_DOWN:
                moved = game.move_down()
            
            if moved:
                animate_movement()
                if game.is_game_over():
                    game_over = True
                    print("Game Over!")
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if retry_button_rect.collidepoint(event.pos):
                game.reset_game()
                game_over = False

pygame.quit()
sys.exit()

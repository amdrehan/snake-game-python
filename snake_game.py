import pygame
import random
import sys

# --- Basic settings ---
WIDTH, HEIGHT = 600, 400
CELL = 20  # size of each snake block
FPS = 10   # speed of game

# Colors (simple)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)


def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont("arial", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def random_food_position(snake):
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            return (x, y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game (Python + pygame)")
    clock = pygame.time.Clock()

    # Snake starts in the middle
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL, 0)  # moving right
    score = 0

    food = random_food_position(snake)
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    # Prevent reverse direction
                    if event.key == pygame.K_UP and direction != (0, CELL):
                        direction = (0, -CELL)
                    elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                        direction = (0, CELL)
                    elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                        direction = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                        direction = (CELL, 0)
                else:
                    # Restart on Enter
                    if event.key == pygame.K_RETURN:
                        snake = [(WIDTH // 2, HEIGHT // 2)]
                        direction = (CELL, 0)
                        score = 0
                        food = random_food_position(snake)
                        game_over = False

        if not game_over:
            # --- Move snake ---
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # --- Collisions (wall) ---
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
                game_over = True
            # --- Collisions (self) ---
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)

                # --- Food eaten ---
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                else:
                    snake.pop()  # keep same length

        # --- Draw ---
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

        # Draw snake
        for (x, y) in snake:
            pygame.draw.rect(screen, GREEN, (x, y, CELL, CELL))

        # Score
        draw_text(screen, f"Score: {score}", 22, WHITE, 70, 20)

        if game_over:
            draw_text(screen, "GAME OVER", 48, WHITE, WIDTH // 2, HEIGHT // 2 - 20)
            draw_text(screen, "Press Enter to Restart", 22, WHITE, WIDTH // 2, HEIGHT // 2 + 25)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

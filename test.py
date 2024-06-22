import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Snake initial position and speed
snake_pos = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
snake_speed = CELL_SIZE
snake_direction = 'RIGHT'

# Food initial position
food_pos = (random.randrange(1, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(1, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # Move the snake
    head_x, head_y = snake_pos[0]
    if snake_direction == 'UP':
        head_y -= snake_speed
    elif snake_direction == 'DOWN':
        head_y += snake_speed
    elif snake_direction == 'LEFT':
        head_x -= snake_speed
    elif snake_direction == 'RIGHT':
        head_x += snake_speed

    # Check for collision with food
    if head_x == food_pos[0] and head_y == food_pos[1]:
        # Increase snake length and spawn new food
        snake_pos.insert(0, (head_x, head_y))
        food_pos = (random.randrange(1, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(1, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)
    else:
        # Move the snake by adding a new head and removing the tail
        snake_pos.insert(0, (head_x, head_y))
        snake_pos.pop()

    # Check for collision with walls or itself
    if (head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT or
            len(snake_pos) != len(set(snake_pos))):
        running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw snake
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(10)

font = pygame.font.SysFont(None, 36)

# Inside the game loop, after drawing the snake and food
score_text = font.render("Score: {}".format(len(snake_pos) - 1), True, (0, 0, 0))
screen.blit(score_text, (10, 10))

# Inside the game loop, after checking for food collision
snake_speed = CELL_SIZE + (len(snake_pos) // 5)

# After the game loop (when running is set to False)
game_over_font = pygame.font.SysFont(None, 72)
game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
score_text = font.render("Final Score: {}".format(len(snake_pos) - 1), True, (0, 0, 0))

screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height()))
screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + score_text.get_height()))
pygame.display.flip()

pygame.time.wait(2000)  # Wait for 2 seconds before quitting
running = False

# After updating the snake's position
head_x %= SCREEN_WIDTH
head_y %= SCREEN_HEIGHT

# Define obstacle class and create obstacle instances
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

obstacles = [Obstacle(random.randrange(1, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                     random.randrange(1, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE)
             for _ in range(10)]  # Create 10 obstacles

# Inside the game loop, after checking for collisions with food
for obstacle in obstacles:
    pygame.draw.rect(screen, (0, 0, 255), (obstacle.x, obstacle.y, CELL_SIZE, CELL_SIZE))

# Check for collisions with obstacles
if any(obstacle.x == head_x and obstacle.y == head_y for obstacle in obstacles):
    running = False


# Quit the game 
pygame.quit()
  
"""
Ping-Pong Game
A two-player game with paddles, ball physics, and score keeping.
Controls: Player 1 (left) - W/S, Player 2 (right) - Up/Down arrows
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8
BALL_SIZE = 15
BALL_SPEED_INITIAL = 6
WINNING_SCORE = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MIDLINE_COLOR = (80, 80, 80)


def main():
    # Game environment setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ping-Pong")
    clock = pygame.time.Clock()

    # Paddles (rects: x, y, width, height)
    paddle_left = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_right = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Ball state
    ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
    ball_dx = BALL_SPEED_INITIAL * random.choice((1, -1))
    ball_dy = BALL_SPEED_INITIAL * random.choice((1, -1)) * 0.6

    # Score keeping
    score_left = 0
    score_right = 0
    font = pygame.font.Font(None, 72)
    game_over = False
    winner = None

    def reset_ball(serve_left=True):
        """Place ball at center and set direction."""
        nonlocal ball_x, ball_y, ball_dx, ball_dy
        ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        speed = BALL_SPEED_INITIAL
        ball_dx = -speed if serve_left else speed
        ball_dy = speed * random.uniform(-0.6, 0.6)

    def draw_midline():
        """Draw dashed center line."""
        segment_height = 20
        gap = 15
        x = SCREEN_WIDTH // 2 - 2
        y = 0
        while y < SCREEN_HEIGHT:
            pygame.draw.rect(screen, MIDLINE_COLOR, (x, y, 4, segment_height))
            y += segment_height + gap

    def draw_all():
        """Draw playing field, paddles, ball, and score."""
        screen.fill(BLACK)
        draw_midline()
        pygame.draw.rect(screen, WHITE, paddle_left)
        pygame.draw.rect(screen, WHITE, paddle_right)
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        score_text_left = font.render(str(score_left), True, WHITE)
        score_text_right = font.render(str(score_right), True, WHITE)
        screen.blit(score_text_left, (SCREEN_WIDTH // 4 - score_text_left.get_width() // 2, 30))
        screen.blit(score_text_right, (3 * SCREEN_WIDTH // 4 - score_text_right.get_width() // 2, 30))

        if game_over and winner is not None:
            msg = f"Player {winner} wins! Press R to restart, Q to quit."
            msg_surface = pygame.font.Font(None, 36).render(msg, True, WHITE)
            screen.blit(msg_surface, (SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        pygame.display.flip()

    # Main game loop
    reset_ball(serve_left=True)
    while True:
        # Event handling (player input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if game_over and event.key == pygame.K_r:
                    game_over = False
                    winner = None
                    score_left = 0
                    score_right = 0
                    reset_ball(True)

        if not game_over:
            # Player input: paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and paddle_left.top > 0:
                paddle_left.y -= PADDLE_SPEED
            if keys[pygame.K_s] and paddle_left.bottom < SCREEN_HEIGHT:
                paddle_left.y += PADDLE_SPEED
            if keys[pygame.K_UP] and paddle_right.top > 0:
                paddle_right.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and paddle_right.bottom < SCREEN_HEIGHT:
                paddle_right.y += PADDLE_SPEED

            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            # Collisions: walls (top and bottom)
            if ball_y <= 0:
                ball_y = 0
                ball_dy = -ball_dy
            if ball_y >= SCREEN_HEIGHT - BALL_SIZE:
                ball_y = SCREEN_HEIGHT - BALL_SIZE
                ball_dy = -ball_dy

            # Collisions: paddles
            ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
            if ball_rect.colliderect(paddle_left):
                ball_dx = abs(ball_dx)  # Send right
                ball_x = paddle_left.right + 1
                # Slight angle based on where ball hit paddle
                hit_pos = (ball_rect.centery - paddle_left.centery) / (PADDLE_HEIGHT / 2)
                ball_dy += hit_pos * 2
            if ball_rect.colliderect(paddle_right):
                ball_dx = -abs(ball_dx)  # Send left
                ball_x = paddle_right.left - BALL_SIZE - 1
                hit_pos = (ball_rect.centery - paddle_right.centery) / (PADDLE_HEIGHT / 2)
                ball_dy += hit_pos * 2

            # Cap vertical speed
            max_dy = 10
            ball_dy = max(-max_dy, min(max_dy, ball_dy))

            # Score: ball past paddles
            if ball_x + BALL_SIZE < 0:
                score_right += 1
                if score_right >= WINNING_SCORE:
                    game_over = True
                    winner = 2
                else:
                    reset_ball(serve_left=False)
            if ball_x > SCREEN_WIDTH:
                score_left += 1
                if score_left >= WINNING_SCORE:
                    game_over = True
                    winner = 1
                else:
                    reset_ball(serve_left=True)

        draw_all()
        clock.tick(60)


if __name__ == "__main__":
    main()

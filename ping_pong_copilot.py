# ping_pong_copilot.py
import pygame
import sys

# Game settings
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Paddle and ball setup
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH-40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_vel = [BALL_SPEED_X, BALL_SPEED_Y]

score_left, score_right = 0, 0

def reset_ball():
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_vel[0] *= -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Ball movement
    ball.x += ball_vel[0]
    ball.y += ball_vel[1]

    # Collisions with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1

    # Collisions with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_vel[0] *= -1

    # Score keeping
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()

    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255,255,255), left_paddle)
    pygame.draw.rect(screen, (255,255,255), right_paddle)
    pygame.draw.ellipse(screen, (255,255,255), ball)
    pygame.draw.aaline(screen, (255,255,255), (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    score_text = font.render(f"{score_left}   {score_right}", True, (255,255,255))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()
    clock.tick(60)
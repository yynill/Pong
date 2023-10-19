import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 600

WHITE = (255, 255, 255)
SCORE_COL = (100, 100, 100)
BLACK = (0, 0, 0)

BAR_WIDTH = 8
BAR_HEIGHT = 60

BALL_WIDTH = 10
BALL_HEIGHT = 10

FPS = 60
VEL = 10

BORDER_WIDTH = 2
BORDER_TILE_HEIGHT = 10

player_1_score = 0
player_2_score = 0


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong!')


def player_1_movement(keys_pressed, player_1):
    if keys_pressed[pygame.K_w] and player_1.y > 0:
        player_1.y -= VEL
    if keys_pressed[pygame.K_s] and player_1.y < HEIGHT - BAR_HEIGHT:
        player_1.y += VEL


def player2_movement(keys_pressed, player_2):
    if keys_pressed[pygame.K_UP] and player_2.y > 0:
        player_2.y -= VEL
    if keys_pressed[pygame.K_DOWN] and player_2.y < HEIGHT - BAR_HEIGHT:
        player_2.y += VEL


def handle_ball(ball, ball_vel, player_1, player_2):
    global player_1_score
    global player_2_score

    ball.x += ball_vel[0]
    ball.y += ball_vel[1]

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1

    if ball.left <= 0:
        player_2_score += 1

        ball.x = WIDTH/2 - BALL_WIDTH
        ball.y = random.randint(0, HEIGHT - BALL_HEIGHT)
        ball_vel[0] *= -1

    if ball.right >= WIDTH:
        player_1_score += 1

        ball.x = WIDTH/2 - BALL_WIDTH
        ball.y = random.randint(0, HEIGHT - BALL_HEIGHT)
        ball_vel[0] *= -1

    if ball.colliderect(player_1) or ball.colliderect(player_2):
        ball_vel[0] *= -1

    return ball_vel


def draw_window(player_1, player_1_score, player_2, player_2_score, ball):
    window.fill(BLACK)

    num_tiles = ((HEIGHT // BORDER_TILE_HEIGHT)//2)+1

    for t in range(num_tiles):
        tile = pygame.Rect(WIDTH // 2 - BORDER_WIDTH // 2,
                           t*num_tiles, BORDER_WIDTH, BORDER_TILE_HEIGHT)

        pygame.draw.rect(window, WHITE, tile)

    pygame.draw.rect(window, WHITE, player_1)
    pygame.draw.rect(window, WHITE, player_2)

    font = pygame.font.Font('./Assets/pixel_font.ttf', 100)

    center_x_left = WIDTH // 4
    center_x_right = WIDTH * 3 // 4

    center_y = HEIGHT // 2

    player_1_score_txt = font.render(
        str(player_1_score), 1, SCORE_COL)
    player_1_rect = player_1_score_txt.get_rect(
        center=(center_x_left, center_y))
    window.blit(player_1_score_txt, player_1_rect)

    player_2_score_txt = font.render(
        str(player_2_score), 1, SCORE_COL)
    player_2_rect = player_2_score_txt.get_rect(
        center=(center_x_right, center_y))
    window.blit(player_2_score_txt, player_2_rect)

    pygame.draw.rect(window, WHITE, ball)

    pygame.display.update()


def main():
    player_1 = pygame.Rect(30, HEIGHT/2, BAR_WIDTH, BAR_HEIGHT)
    player_2 = pygame.Rect(WIDTH - 30, HEIGHT/2, BAR_WIDTH, BAR_HEIGHT)

    ball = pygame.Rect(WIDTH/2 - BALL_WIDTH, HEIGHT/2 -
                       BALL_HEIGHT, BALL_WIDTH, BALL_HEIGHT)

    ball_vel = [6, 6]

    clock = pygame.time.Clock()
    # gameloop
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        player_1_movement(keys_pressed, player_1)
        player2_movement(keys_pressed, player_2)

        handle_ball(ball, ball_vel, player_1, player_2)

        draw_window(player_1, player_1_score,  player_2,
                    player_2_score,  ball)

    pygame.quit()


if __name__ == '__main__':
    main()

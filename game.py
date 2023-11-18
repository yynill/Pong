import pygame
import random


class PongGame:
    def __init__(self):
        pygame.init()

        self.WIDTH = 900
        self.HEIGHT = 600

        self.WHITE = (255, 255, 255)
        self.SCORE_COL = (100, 100, 100)
        self.BLACK = (0, 0, 0)

        self.BAR_WIDTH = 8
        self.BAR_HEIGHT = 60

        self.BALL_WIDTH = 10
        self.BALL_HEIGHT = 10

        self.FPS = 60
        self.VEL = 10

        self.BORDER_WIDTH = 2
        self.BORDER_TILE_HEIGHT = 10

        self.player_1_score = 0
        self.player_2_score = 0

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Pong!')

        self.player_1 = pygame.Rect(
            30, self.HEIGHT / 2, self.BAR_WIDTH, self.BAR_HEIGHT)
        self.player_2 = pygame.Rect(
            self.WIDTH - 30, self.HEIGHT / 2, self.BAR_WIDTH, self.BAR_HEIGHT)

        self.ball = pygame.Rect(self.WIDTH / 2 - self.BALL_WIDTH, self.HEIGHT / 2 - self.BALL_HEIGHT,
                                self.BALL_WIDTH, self.BALL_HEIGHT)

        self.ball_vel = [6, 6]

    def player_1_movement(self, keys_pressed):
        if keys_pressed[pygame.K_w] and self.player_1.y > 0:
            self.player_1.y -= self.VEL
        if keys_pressed[pygame.K_s] and self.player_1.y < self.HEIGHT - self.BAR_HEIGHT:
            self.player_1.y += self.VEL

    def player_2_movement(self, keys_pressed):
        if keys_pressed[pygame.K_UP] and self.player_2.y > 0:
            self.player_2.y -= self.VEL
        if keys_pressed[pygame.K_DOWN] and self.player_2.y < self.HEIGHT - self.BAR_HEIGHT:
            self.player_2.y += self.VEL

    def handle_ball(self):
        self.ball.x += self.ball_vel[0]
        self.ball.y += self.ball_vel[1]

        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.ball_vel[1] *= -1

        if self.ball.left <= 0:
            self.player_2_score += 1
            self.ball.x = self.WIDTH / 2 - self.BALL_WIDTH
            self.ball.y = random.randint(0, self.HEIGHT - self.BALL_HEIGHT)
            self.ball_vel[0] *= -1

        if self.ball.right >= self.WIDTH:
            self.player_1_score += 1
            self.ball.x = self.WIDTH / 2 - self.BALL_WIDTH
            self.ball.y = random.randint(0, self.HEIGHT - self.BALL_HEIGHT)
            self.ball_vel[0] *= -1

        if self.ball.colliderect(self.player_1) or self.ball.colliderect(self.player_2):
            self.ball_vel[0] *= -1

    def draw_window(self):
        self.window.fill(self.BLACK)

        num_tiles = ((self.HEIGHT // self.BORDER_TILE_HEIGHT) // 2) + 1

        for t in range(num_tiles):
            tile = pygame.Rect(self.WIDTH // 2 - self.BORDER_WIDTH // 2,
                               t * num_tiles, self.BORDER_WIDTH, self.BORDER_TILE_HEIGHT)
            pygame.draw.rect(self.window, self.WHITE, tile)

        pygame.draw.rect(self.window, self.WHITE, self.player_1)
        pygame.draw.rect(self.window, self.WHITE, self.player_2)

        font = pygame.font.Font('./Assets/pixel_font.ttf', 100)

        center_x_left = self.WIDTH // 4
        center_x_right = self.WIDTH * 3 // 4
        center_y = self.HEIGHT // 2

        player_1_score_txt = font.render(
            str(self.player_1_score), 1, self.SCORE_COL)
        player_1_rect = player_1_score_txt.get_rect(
            center=(center_x_left, center_y))
        self.window.blit(player_1_score_txt, player_1_rect)

        player_2_score_txt = font.render(
            str(self.player_2_score), 1, self.SCORE_COL)
        player_2_rect = player_2_score_txt.get_rect(
            center=(center_x_right, center_y))
        self.window.blit(player_2_score_txt, player_2_rect)

        pygame.draw.rect(self.window, self.WHITE, self.ball)

        pygame.display.update()

    def run_game(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys_pressed = pygame.key.get_pressed()
            self.player_1_movement(keys_pressed)
            self.player_2_movement(keys_pressed)
            self.handle_ball()
            self.draw_window()

        pygame.quit()


if __name__ == '__main__':
    game = PongGame()
    game.run_game()

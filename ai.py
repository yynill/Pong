import pygame
from game import PongGame
import neat
import os
import visualize
import time

pygame.init()


class PongAi:
    def __init__(self, genome, config) -> None:
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)
        self.game = PongGame(True)
        self.score_before = 0

    def calculate_fitness(self):
        self.genome.fitness += self.game.aiHits * 10
        self.genome.fitness -= self.game.player_1_score * 5

    def train_ai(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.player_2_y = self.game.player_2.y
            self.ball_y = self.game.ball.y
            self.ball_x = self.game.ball.x
            self.player_2_x = self.game.player_2.x

            output = self.net.activate(
                (self.player_2_y,
                 self.ball_y,
                 abs(self.ball_x - self.player_2_x)))

            decision = output.index(max(output))

            if decision == 0:
                if self.game.player_2.y < self.game.HEIGHT - self.game.BAR_HEIGHT:
                    self.game.player_2.y += self.game.VEL
            elif decision == 1:
                if self.game.player_2.y > 0:
                    self.game.player_2.y -= self.game.VEL
            else:
                pass

            self.game.handle_ball()
            self.game.draw_window()
            pygame.display.update()

            clock.tick(self.game.FPS)
            time.sleep(0.01)

            if self.genome.fitness >= 100 or self.game.player_1_score >= 5:
                self.calculate_fitness()
                break


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0.0

        pong_ai = PongAi(genome, config)
        pong_ai.train_ai()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def run(config_path):
    # Load configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5, filename_prefix='pong_checkpoint_'))
    winner = p.run(eval_genomes, 1)  # Run for one generation
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    config_path = os.path.join(os.getcwd(), "config.txt")

    run(config_path)

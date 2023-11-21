import pygame
from game import PongGame
import neat
import os
import visualize
import pickle

pygame.init()


class PongAi:
    def __init__(self, genome, config) -> None:
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)
        self.game = PongGame(True)

    def train_ai(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

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

            if self.game.aiHits >= 100 or self.game.player_1_score >= 10:
                self.calculate_fitness()
                self.game.aiHits = 0
                break

    def calculate_fitness(self):
        self.genome.fitness += self.game.aiHits * 2
        self.genome.fitness -= self.game.player_1_score


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0.0

        pong_ai = PongAi(genome, config)
        pong_ai.train_ai()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break


def run(config_path):
    # Load configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Checkpointer.restore_checkpoint('new_checkpoint_20')
    # p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, filename_prefix='new_checkpoint_'))
    winner = p.run(eval_genomes, 20)
    # save best genome obj

    with open('best_pong_ai.pkl', 'wb') as f:
        pickle.dump(winner, f)


def test_ai_against_human(config_path, checkpoint_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    try:
        winner = pickle.load(open(checkpoint_file, 'rb'))
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
        game = PongGame(False)

    except Exception as e:
        print(f"Error loading checkpoint file: {e}")
        return

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        player_2_y = game.player_2.y
        ball_y = game.ball.y
        ball_x = game.ball.x
        player_2_x = game.player_2.x

        output = winner_net.activate(
            (player_2_y,
             ball_y,
             abs(ball_x - player_2_x)))

        decision = output.index(max(output))

        if decision == 0:
            if game.player_2.y < game.HEIGHT - game.BAR_HEIGHT:
                game.player_2.y += game.VEL
        elif decision == 1:
            if game.player_2.y > 0:
                game.player_2.y -= game.VEL
        else:
            pass

        game.handle_ball()

        keys_pressed = pygame.key.get_pressed()
        game.player_1_movement(keys_pressed)
        game.draw_window()
        pygame.display.update()


if __name__ == "__main__":
    config_path = os.path.join(os.getcwd(), "config.txt")

    # train ai #

    # run(config_path)

    # play against ai #

    checkpoint_file = 'best_pong_ai.pkl'
    test_ai_against_human(config_path, checkpoint_file)

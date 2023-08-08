import os
import neat
# import visualize
import resources
# import matplotlib as plt

X_train = resources.X_train
y_train = resources.y_train
X_test = resources.X_test
y_test = resources.y_test

bf = 0
bg = 0
def training(genomes, config):
    nets = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)

    for j in range(0, len(nets)):
        correct_time = 0
        for i in range(0, len(X_train)):
            output = nets[j].activate(X_train[i])
            expected = y_train[i]
            distance = abs(expected - output[0])
            if distance < 0.5:
                correct_time += 1

        ge[j].fitness += correct_time / len(X_train)
            # if output[0] < 0 and y_train[i] == 0\
            #         or output[0] > 0 and y_train[i] == 1:
            #     # have correct answer
            #     ge[j].fitness = ge[j].fitness + 1
            # else:
            #     # have incorrect answer
            #     ge[j].fitness = ge[j].fitness - 2

            # output = abs(o[0])
            # # if 0.1 < output < 0.3:
            # #     print(str(output) + "\n")
            # decrease = abs(y_train[i] - output)
            # # y = y_train[i]
            # # fg = ge[j].fitness
            # ge[j].fitness = ge[j].fitness - decrease
            # if output > 1 or output < -1:
            #     exit()


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run for up to 300 generations.
    best_genome = population.run(training, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(best_genome))
    # Show output of the most fit genome against training data.
    print('\nStarting with data test:')
    clone_best_genome = neat.nn.FeedForwardNetwork.create(best_genome, config)
    for xi, xo in zip(X_test, y_test):
        output = clone_best_genome.activate(xi)
        print("input {!r}, expected output {!r}, got {}".format(xi, xo, output[0]))

    # node_names = {-1: 'A', -2: 'B', 0: 'A : Bx3'}
    # visualize.draw_net(config, best_genome, True, node_names=node_names)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)
    # print(stats)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)

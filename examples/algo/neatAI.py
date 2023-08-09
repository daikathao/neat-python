import os
import pickle
import neat
import pandas as pd


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for ind in train_data.index:
            xi = (train_data['SMA_5_2'][ind], train_data['SMA_5_1'][ind], train_data['SMA_5'][ind], train_data['SMA_20_2'][ind], train_data['SMA_20_1'][ind], train_data['SMA_20'][ind])
            output = net.activate(xi)
            xo = int(train_data['Sell'][ind])
            genome.fitness -= (output[0] - xo) ** 2


def runTrainning(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)
    with open(pickleFile, 'wb') as f:
        pickle.dump(winner, f)

def runTesting(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    if os.path.isfile(pickleFile):
        # load the winner
        with open(pickleFile, 'rb') as f:
            winner = pickle.load(f)
    else:
        exit()
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    for ind in test_data.index:
        xi = (
        test_data['SMA_5_2'][ind], test_data['SMA_5_1'][ind], test_data['SMA_5'][ind], test_data['SMA_20_2'][ind],
        test_data['SMA_20_1'][ind], test_data['SMA_20'][ind])
        output = winner_net.activate(xi)
        xo = int(test_data['Sell'][ind])
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-299')
    # p.run(eval_genomes, 10)

if __name__ == '__main__':
    pickleFileName = 'neatAI.pkl'
    local_dir = os.path.dirname(__file__)
    train_data = pd.read_csv(local_dir + '/result_VN30.csv')
    test_data = ai_data = pd.read_csv(local_dir + '/result_POW.csv')

    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    config_path = os.path.join(local_dir, 'neatAI_config')
    pickleFile = os.path.join(local_dir, pickleFileName)
    runTrainning(config_path)
    runTesting()

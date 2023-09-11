import pandas as pd
import neat
import os
import pickle
import constants
import math
from bookmaker import Bookmaker


def training(genomes, config):
    # We have x number of genomes. X is specified in the configuration file
    # for ever genome we will create one object of Bookmaker class, this object will simulate behaviour of the person
    # which buys and sells stocks
    # Also for each genome we create a neural network
    bookmakers = []
    nets = []
    ge = []
    # Creating individual data for every object in this generation
    for _, genome in genomes:
        bookmaker = Bookmaker(constants.STARTING_CAPITAL)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        bookmakers.append(bookmaker)
        nets.append(net)
        ge.append(genome)

    # getting data for this generation
    savedFile = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA, ticker + '.csv')
    data = pd.read_csv(savedFile)
    data_set = data[constants.CSV_OPEN_COLUMN]
    macd = data['MACD']
    signal = data['MACDs']
    rows_number = len(data.index)

    # starting simulation, from 35 because we need to omit all of the zeroes that appears during calculating MACD
    for i in range(35, rows_number):
        for j in range(0, len(bookmakers)):
            try:
                decision = nets[j].activate((macd[i], signal[i]))  # decision can be a real number form 0 to 1
            except (IndexError, ValueError):
                continue

            # if there is a missing data cell, then substitute it with the latest stock value
            index = i
            while pd.isnull(data_set[index]):
                index -= 1
            if decision[0] > 0.9:
                if bookmakers[j].canBuyMore(data_set[index]):
                    bookmakers[j].buy_all_stocks(data_set[index])
            elif decision[0] < 0.1:
                if bookmakers[j].canSellStock():
                    bookmakers[j].sell_all_stocks(data_set[index])

                    # Increase fitness when bookmaker sold stock with profit
                    # Decrease fitness when bookmaker sold stock with loss
                    if len(bookmakers[j].incomes_list) > 0:
                        index = len(bookmakers[j].incomes_list) - 1
                        difference = bookmakers[j].incomes_list[index] - bookmakers[j].expenses_list[index]
                        if difference > 0:
                            ge[j].fitness += difference
                        if difference <= 0:
                            ge[j].fitness += difference

                        ge[j].fitness = ge[j].fitness + difference
                        bookmakers[j].incomes_list.pop()
                        bookmakers[j].expenses_list.pop()

                    # bookmaker is bankrupt, so delete it from further trading
                    if bookmakers[j].capital < constants.STARTING_CAPITAL * 0.3 and bookmakers[j].number_of_stocks == 0:
                        nets.pop(bookmakers.index(bookmakers[j]))
                        ge.pop(bookmakers.index(bookmakers[j]))
                        bookmakers.pop(bookmakers.index(bookmakers[j]))

def run(config_path):
    # creating configuration basing on our configuration file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # creating population basing on our configuration
    population = neat.Population(config)

    # creating reporter that will print crucial data in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # saving the best genome after completing the training
    winner = population.run(training, constants.NUMBER_OF_GENERATIONS)


    # statistics of the best genome
    print('\nBest genome:\n{!s}'.format(winner))

    # save the best genome to a file
    save_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME)
    with open(save_path, 'wb') as fp:
        pickle.dump(winner, fp)


def main():
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    run(config_path)


if __name__ == '__main__':
    ticker = "MBB"
    main()

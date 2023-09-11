import pandas as pd
import pickle
import os
import neat
import constants
from bookmaker import Bookmaker


def simulate_stock_market(best_genome, config, current_capital):
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    bookmaker = Bookmaker(current_capital)

    savedFile = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA, ticker + '.csv')
    data = pd.read_csv(savedFile)
    data_set = data[constants.CSV_OPEN_COLUMN]
    macd = data['MACD']
    signal = data['MACDs']
    rows_number = len(data.index)

    for i in range(0, rows_number):
        decision = net.activate((macd[i], signal[i]))  # decision can be a real number form 0 to 1

        # if there is a missing data cell, then substitute it with the latest stock value
        index = i
        while pd.isnull(data_set[index]):
            index -= 1
        if decision[0] > 0.9:
            bookmaker.buy_all_stocks(data_set[index], data['Date'][index])
        elif decision[0] < 0.1:
            bookmaker.sell_all_stocks(data_set[index], data['Date'][index])

    # On the last day we sell all of our stocks
    bookmaker.sell_all_stocks(data_set[rows_number - 1], data['Date'][rows_number - 1])
    return bookmaker.capital



def main():
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # load best genome
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME)
    best_genome = None
    try:
        with open(best_genome_path, 'rb') as fp:
            best_genome = pickle.load(fp)
    except FileNotFoundError:
        print('You need to train a network first')
        return


    start_capital = constants.STARTING_CAPITAL
    result_capital = simulate_stock_market(best_genome, config, start_capital)
    print('{}: we have earned {}'.format(ticker, result_capital - start_capital))


if __name__ == '__main__':
    ticker = "VCB"
    main()

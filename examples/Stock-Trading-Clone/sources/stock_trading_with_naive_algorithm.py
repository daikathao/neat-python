import pandas as pd
import pickle
import os
import constants
from bookmaker import Bookmaker


def simulate_stock_market(full_data, macd, signal, start_index, current_capital):
    data = full_data[constants.CSV_OPEN_COLUMN]
    bookmaker = Bookmaker(current_capital)
    last_index = len(data.index)

    last_macd_value = macd[start_index]
    last_signal_value = signal[start_index]

    # start from start_index + 1, because we treat start_index as a point of reference
    for i in range(start_index + 1, last_index):
        # if MACD crosses SIGNAL from top, then sell stocks
        if last_macd_value > last_signal_value and signal[i] > macd[i]:
            if bookmaker.canSellStock():
                bookmaker.sell_all_stocks(data[i], full_data['Date'][i])
        # else if MACD crosses SIGNAL from bottom, then buy stocks
        elif last_macd_value < last_signal_value and signal[i] < macd[i]:
            if bookmaker.canBuyMore(data[i]):
                bookmaker.buy_all_stocks(data[i], full_data['Date'][i])

        last_macd_value = macd[i]
        last_signal_value = signal[i]

    # On the last day we sell all of our stocks
    if bookmaker.canSellStock():
        bookmaker.sell_all_stocks(data[last_index - 1], full_data['Date'][last_index - 1])
    return bookmaker.capital


def main():
    savedFile = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA, ticker + '.csv')
    data = pd.read_csv(savedFile)
    macd = data['MACD']
    signal = data['MACDs']
    start_capital = constants.STARTING_CAPITAL
    result_capital = simulate_stock_market(data, macd, signal, 0, start_capital)
    print('{}: we have earned {}'.format(ticker, result_capital - start_capital))

if __name__ == '__main__':
    ticker = "SAM_2023"
    main()

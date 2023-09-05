import math


class Bookmaker:

    def __init__(self, start_capital):
        self.capital = start_capital
        self.number_of_stocks = 0
        self.incomes_list = []
        self.expenses_list = []

    # buy all stocks that bookmaker can afford
    def buy_all_stocks(self, stock_price, date=''):
        how_many_stocks = math.floor(self.capital / stock_price)
        if self.canBuyMore(stock_price):
            self.capital -= stock_price * how_many_stocks
            self.expenses_list.extend([stock_price] * how_many_stocks)
            self.number_of_stocks += how_many_stocks
            if date:
                print('Buy with price {} in {}'.format(stock_price, date))
        # else:
        #     print('------------------ Request a long with price {} in {}'.format(stock_price, date))

    def sell_all_stocks(self, stock_price, date=''):
        if self.number_of_stocks > 0:
            if date:
                print('Sell with price {} in {}'.format(stock_price, date))
            self.capital += stock_price * self.number_of_stocks
            self.incomes_list.extend([stock_price] * self.number_of_stocks)
            self.number_of_stocks = 0
        # else:
        #     print('------------------ Request a short with price {} in {}'.format(stock_price, date))

    def canBuyMore(self, stock_price):
        how_many_stocks = math.floor(self.capital / stock_price)
        if how_many_stocks > 0:
            return True
        else:
            return False

    def canSellStock(self):
        if self.number_of_stocks > 0:
            return True
        else:
            return False

""" Module for fetching stock data """

from yfinance import Ticker
import logging

class Stock:
    """ Accesses current values of a stock from its ticker """
    def __init__(self, ticker):
        self.ticker = ticker
        try:
            stock_history = Ticker(ticker).history()
            self.yesterday_closing_price = stock_history.iat[-2, -4]
            self.current_price = stock_history.iat[-1, -4]
        except Exception as e:
            logging.info("error loading stock data: %s", e)

    def get_day_over_day_percent_change(self):
        """ Calculates the percent change of the stock between yesterday and today """
        return round(100 * (self.current_price - self.yesterday_closing_price) \
               / self.yesterday_closing_price, 2)

    def get_stock_data(self):
        """ Gets formatted stock data: ticker, price, % change """
        percent_change = self.get_day_over_day_percent_change()
        return f"{self.ticker.upper()} ${round(self.current_price,1)}" + \
               f"{'-' if percent_change < 0 else '+'}{round(abs(percent_change),1)}%"

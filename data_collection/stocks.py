from yfinance import Ticker

class Stock:
    """ Accesses current values of a stock from its ticker """    
    def __init__(self, ticker):
        self.ticker = ticker
        stock_history = Ticker(ticker).history()
        self.yesterday_closing_price = stock_history.iat[-2, -4]
        self.current_price = stock_history.iat[-1, -4]
    
    def get_day_over_day_percent_change(self):
        """ Calculates the percent change of the stock between yesterday and today """
        return round(100 * (self.current_price - self.yesterday_closing_price) / self.yesterday_closing_price, 2)
    
    # NOTE: May have to change format to compress into <= 16 chars for screen to fit
    def get_stock_data(self):
        """ Gets formatted stock data: ticker, price, % change """
        percent_change = self.get_day_over_day_percent_change()
        return f"{self.ticker.upper()} ${round(self.current_price,1)} {'-' if percent_change < 0 else '+'}{round(abs(percent_change),1)}%"

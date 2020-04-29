# Libraries
import pandas as pd
from pandas_datareader import data as pdr
from pandas_datareader._utils import RemoteDataError
import statsmodels.api as sm


# Class which analyze a stock based on historical data
class Analysis:
    # Constructor
    def __init__(self, stock_name, index_name, start_date, end_date):
        self.__stock_name = stock_name
        self.__index_name = index_name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__stock_data = pd.DataFrame()
        self.__index_data = pd.DataFrame()
        self.__stock_returns = pd.DataFrame()

        self.__download_hist_data()

    # Download historical data
    def __download_hist_data(self):
        # Download data from Yahoo Finance
        try:
            self.__stock_data = pdr.get_data_yahoo(self.__stock_name,
                                                   start=self.__start_date,
                                                   end=self.__end_date)
        except RemoteDataError:
            # handle error
            print 'Stock symbol "{}" is not valid'.format(self.__stock_name)

        try:
            self.__index_data = pdr.get_data_yahoo(self.__index_name,
                                                   start=self.__start_date,
                                                   end=self.__end_date)
        except RemoteDataError:
            # handle error
            print 'Stock symbol "{}" is not valid'.format(self.__index_name)

        self.__stock_data = self.__stock_data[['Close', 'Adj Close']]

        self.__stock_data.dropna(inplace=True)

        self.__index_data = self.__index_data['Close']

        self.__index_data.dropna(inplace=True)

    def get_stock_data(self):
        return self.__stock_data

    def get_index_data(self):
        return self.__index_data

    def get_price_mean(self):
        return self.__stock_data['Adj Close'].mean()

    def get_price_sd(self):
        return self.__stock_data['Adj Close'].std()

    def calculate_daily_return_mean(self):
        self.__stock_returns = self.__stock_data['Adj Close'].pct_change(1)
        # Drop first line with NA
        self.__stock_returns.dropna(inplace=True)
        return self.__stock_returns.mean()

    def get_return_sd(self):
        return self.__stock_returns.std()

    def implement_regression(self):
        explanatory_variable = sm.add_constant(self.__index_data)
        model = sm.OLS(self.__stock_data['Close'], explanatory_variable)
        results = model.fit()
        return results.summary()

    def main(self):
        average_stock_value = self.get_price_mean()
        print "\nAverage Stock Value:", average_stock_value
        stock_volatility = self.get_price_sd()
        print "\nStock Volatility:", stock_volatility
        daily_average_stock_return = self.calculate_daily_return_mean()
        print "\nAverage Daily Stock return:", daily_average_stock_return
        daily_return_volatility = self.get_return_sd()
        print "\nDaily Return Volatility:", daily_return_volatility
        regression_results = self.implement_regression()
        print '\n', regression_results


stock_name = 'JPM'
index_name = '^GSPC'
start_date = '2015-04-02'
end_date = '2015-06-25'

analysis = Analysis(stock_name, index_name, start_date, end_date)
analysis.main()

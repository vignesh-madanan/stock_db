from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
from nsepy import get_history
from datetime import date
from nsetools import Nse
import json
from itertools import starmap
import yfinance as yf

class Mongo:
    def __init__(self,):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.stocks
        self.all_collections = self.db.list_collection_names()

class StockData(Mongo):
    def __init__(self):
        super().__init__()
        ALL_SYMBOLS = ['SBIN']
        with open(r"nse_symbols.json", "r") as read_file:
            self.all_data = json.load(read_file)


    def get_data_nse(self, symbol, start_date, end_date):
        print(f'Getting Data for {symbol}')
        data = get_history(data = get_history(symbol=symbol, start=start_date, end=end_date), index = True)
        if not data.shape[0]:
            print('[WARNING]: No data found for {symbol}')
            return 
        data.reset_index(inplace = True)
        data.columns = map(str.lower, data.columns)
        return data
    
    def get_data_yahoo(self,symbol, start_date, end_date):
        
        #Bank Niftt ^NSEBANK
        print(f'Using Online, getting data for {symbol} from yahoo finance')
        ticker_info = yf.Ticker(symbol)
        data = ticker_info.history(period="max")

        data.reset_index(inplace = True)
        data.columns = map(str.lower, data.columns)
        
        return data

    @staticmethod
    def intepret_data(symbol):
        with open(r"nse_symbols.json", "r") as read_file:
            all_data = json.load(read_file)
        print(all_data[symbol])
        

    def is_valid_symbol(self, symbol):
        return True if self.all_data[symbol] else False

    def store_data(self, symbol, start_date, end_date):

        # if not self.is_valid_symbol(symbol):
        #     print(f'{symbol} not a valid data')
        #     return
        symbol = "^NSEBANK"

        data = self.get_data_yahoo(symbol = symbol , start_date = None, end_date = None)
        
        data = data.to_dict(orient = 'record')

        if symbol.upper() in self.all_collections:
            print('Data Already Found')
            return
        sb = symbol.upper()
        print(list(self.db[sb].insert_many(data)))

if __name__ == '__main__':
    stock_data = StockData()
    arguments = [('SBIN', date(2020,5,25), date(2020,5,28))]
    list(starmap(stock_data.store_data, arguments))
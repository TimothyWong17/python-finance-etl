import requests
import json
import config

class FetchStockAPIData:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.stock_profile_api_url = f'{config.stock_profile_url}?symbol={self.stock_symbol}&token={config.API_KEY}'
        self.stock_price_api_url = f'{config.stock_price_url}?symbol={self.stock_symbol}&token={config.API_KEY}'
        self.stock_data = {}
        
    
    def get_stock_profile_data(self):
        stock_profile_res = requests.get(self.stock_profile_api_url)
        return json.loads(stock_profile_res.text)
    
    def get_stock_price_data(self):
        stock_price_res = requests.get(self.stock_price_api_url)
        return json.loads(stock_price_res.text)
    
    def get_stock_details(self):
        stock_profile_data = self.get_stock_profile_data()
        stock_price_data = self.get_stock_price_data()
        self.stock_data['stock_profile'] = stock_profile_data
        self.stock_data['stock_price'] = stock_price_data
        return self.stock_data
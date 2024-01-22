from fetch_stock_api import FetchStockAPIData
from top_stocks_scrapper import TopStocksScrapper
import pandas as pd
import csv
from datetime import datetime
import sqlite3


class StockETL:
    def __init__(self):
        self.topStocks = TopStocksScrapper().get_top_stocks()
        self.stock_data = {}
    
    
    def extract(self):
        for symbol, stock_name in self.topStocks.items():
            print(f'Fetching Data for {stock_name}({symbol})')
            FetchStockData = FetchStockAPIData(symbol)
            self.stock_data[stock_name] = FetchStockData.get_stock_details()

        return self.stock_data
    
    def transform(self):
        df = pd.DataFrame.from_dict({(i,j): self.stock_data[i][j] 
                           for i in self.stock_data.keys() 
                           for j in self.stock_data[i].keys()},
                       orient='index')
        df = df.reset_index()
        
        df_columns = {c: 'first' if c != 'level_1' else ', '.join for c in df.columns.tolist() if c != 'level_0'}
        df = df.groupby('level_0').agg(df_columns).reset_index()
        
        df.drop('level_1', axis=1, inplace=True)
        df.rename(columns={'level_0': 'stock_name', 'c':'current_price', 'd':'delta_change', 'dp': 'delta_change_percentage', 'h': 'high_price', 'l': 'low_price', 'o':'open_price', 'pc':'prev_close_price', 't': 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.to_csv('stock_data.csv')
        return df

        
    def load(self, data):
        conn = sqlite3.connect('db/db_stock')
        data.to_sql('stocks', con=conn, if_exists='append')
        conn.commit()
        conn.close()
        
        
    def query(self,query):
        conn = sqlite3.connect('db/db_stock')
        cursor = conn.cursor()
        cursor.execute(query)
        
        for row in cursor.fetchall():
            print(row)

    
    def run(self):
        self.extract()
        df = self.transform()
        self.load(df)
        self.query(
            """
            SELECT 
                stock_name, 
                timestamp, 
                current_price,
                row_number() over (partition by stock_name order by timestamp desc) as stock_price_history_order
            FROM 
                stocks
            """
        )

if __name__ == "__main__":
    stockETL = StockETL()
    stockETL.run()
    



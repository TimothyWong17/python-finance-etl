# python-finance-etl
* Utilized: https://finnhub.io/docs/api/library and https://finance.yahoo.com/gainers/ in project
* This ETL pipeline will
  * Scrape the Top 20 Stocks from Yahoo Finance Daily Gainers Report
  * Pull Data Stock data of the Top 20 Stocks from Finnhub API
  * Clean the data to standardized view and load copy as csv
  * Create Table in SQLite DB
  * Each time ETL Scripts run it will load the daily stock data into SQLite Table
  * ETL Script has the class method option to write custom sql queries against SQLite DB
 
  

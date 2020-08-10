from Database.DB import DB_object
from Crawl_data.Crawler import datacrawler
from Finance.Stocks import Stock


from pathlib2 import Path
import argparse
import datetime
import pandas as pd


# To Do:
# decorator for Trading date: Consistent Datetime concept, implemented via decorator
# Decorator in Utils for loging time
# Decorator in Utils for error logging on Database
# prarser Concept
# Delta Load
# load COT data
# No Data redudance on Databases
# function calc_to_database() not dynamically -> see index and Stocks
# Create Database Tables dynamically from Attributes
# write to database dynamically
# create better connection between index data and stock data
# calcualtions for same dates
# implement Class Machine learning

# Load in Fundamentals:
# - Get fundamental data in Google sheet
# - Create Database Table
# - Load in Fundamentals

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--Initialize", help="Initialize the project - create database, initial tables and load data", action="store_true")

    parser.add_argument("-C", "--Calculate", help="Calculate Financial Key Figures for all stocks that are loaded", action="store_true")
    args = parser.parse_args()

    #if args.Initialize:
    if 1==2:

        # Initialie Database
        DB_DIR = Path('__file__').resolve().parent.joinpath('Database/stocks.db')
        DB = DB_object(str(DB_DIR))
        conn = DB.create_connection()
        print(DB)


        # drop table
        DB.drop_table('Stocks_Stage')
        DB.drop_table('Index_Stage')

        # Create landing tables
        stock_table = DB.create_stock_stage()
        index_table = DB.create_index_stage()

        # Initial Load
        index, datasource, start_date, end_date = 'DAX', 'yahoo', '2019-01-01', '2019-12-30'
        datacrawler(conn, stock_table, index, datasource, start_date, end_date).crawl_prices_to_db()

        index_tickers = 'ECON'
        datacrawler(conn, index_table, index_tickers, datasource, start_date, end_date).crawl_prices_to_db()

    # if args.calculation:
    if 1==1:
        DB_DIR = Path('__file__').resolve().parent.joinpath('Database/stocks.db')
        DB = DB_object(str(DB_DIR))
        conn = DB.create_connection()
        print(DB)

        # read in data from Database
        Index_frame = pd.read_sql_query("""select * from Index_Stage where 1=1 ;""", conn)
        Stock_frame = pd.read_sql_query("""select * from Stocks_Stage where 1=1 ;""", conn)

        # -> block gets relevant for multiple indexes
        #for index_name in Index_frame['Symbol'].unique():

            #Index_calc_table = DB.create_index_calc()
            #index_object = Index_(Index_frame, index_name)

            # write in Database
            #index_object.calc_to_database(Index_calc_table, conn)

        # Calculate Stock Attributes and Keyfigures for all Stocks:
        for stock_name in Stock_frame['Symbol'].unique():

            dates_MOM = [14, 21, 28]
            dates_SMA = [14, 21, 28]
            dates_OBV = [14, 21, 28]
            vol_window = 30

            # To Do: maybe create Stock Object dynamically
            stock_object = Stock(Stock_frame, stock_name, Index_frame, vol_window, dates_MOM, dates_SMA, dates_OBV)
            
            print('##################################################')
            print('calculating financial key figures for ', stock_name)

            Stock_calc_table = DB.create_stock_calc()
            stock_object.calc_to_database(Stock_calc_table, conn)


# test predictions




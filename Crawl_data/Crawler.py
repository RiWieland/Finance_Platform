
from Crawl_data.Tickers_Yahoo import SP500, DAX, ETF, ECON

import datetime
import pandas as pd
from pandas.io import sql
import csv
from pandas_datareader import data
import sqlite3
import time
import datetime
import pickle
from datetime import datetime


class datacrawler():  # getting attributes from praser

    def __init__(self, db_connection, db_staging_table,index, datasource, start_date, end_date):
        self.db_connection = db_connection
        self.db_staging_table = db_staging_table
        self.index = index
        self.datasource = datasource
        self.start = start_date
        self.end = end_date

    def __select_index(self):

        if self.index == 'SP500':

            return SP500

        if self.index == 'DAX':

            return DAX

        if self.index == 'ECON':

            return ECON

        else:
            print('Index not found - datacrawl stoped')

    def crawl_prices_to_db(self):

        tickers_list = self.__select_index()
        complete_dataframe = pd.DataFrame()

        for stock in tickers_list:

            try:

                df = data.DataReader(stock, self.datasource, self.start, self.end)
                df['Symbol'] = stock
                df['Index_'] = self.index

                df.index.names = ['Trading_Date']
                df.reset_index(inplace=True)

                df.rename(columns={'Adj Close': 'Adj_Close', }, inplace=True)

                complete_dataframe = complete_dataframe.append(df, ignore_index=True)#.reset_index(inplace=True,drop=False)

                
                print('prices drawn for', stock)

            except Exception as e:
                print(e)
                #print("Yahoo Finance connection not robust, not successful for:", stock)
        complete_dataframe.drop_duplicates(inplace=True, ignore_index=True) 
        complete_dataframe.to_sql(self.db_staging_table, self.db_connection, if_exists="append", index=False)
        print("prices written to table ", self.db_staging_table)

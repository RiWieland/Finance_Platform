import pandas as pd


def Label_Best_Return(Stock_Frame, Num=3, Period = 'Month'):
        '''
        Label the Num of Stocks with best preformance among the index per month
        '''
        portfolio = dict()
        for _, mon in enumerate(Stock_Frame[Period].unique()):
            print(mon)
            df = Stock_Frame.loc[Stock_Frame['Month']==mon]
            df['RETURNS'] = df['RETURNS'].astype(float)

            portfolio[mon] = df.groupby('Symbol')['RETURNS'].sum().sort_values(ascending=False)[:Num].index


            # Calc returns for each Symbol with group by

            #return_month = df['Close'][-1] - df['Close'][0]

            # find best preforming
        return portfolio

import pandas as pd


def Create_Return_Matrix(Stock_Frame, Period = None):
        '''
        Create Returns for monthly-base for labeling
        '''
        return_matrix = dict()
        tmp_matrix = dict()
        if Period is None: # for extending in future for weekly returns
            year_list = Stock_Frame['Year'].unique()
            
            for year in year_list:
            
                for _, per in enumerate(Stock_Frame.loc[(Stock_Frame['Year']==year)].Month.unique()):

                    df = Stock_Frame.loc[(Stock_Frame['Year']==year) & (Stock_Frame['Month']==per)]

                    tmp = df.groupby('Symbol')['Adj_Close'].agg(['first', 'last'])
                    tmp_matrix[per] = tmp['last']- tmp['first']
                    
                return_matrix[year] = tmp_matrix
            
        return return_matrix

def Portfolio_Best_Return(Return_Matrix, Num=3, Period='Month'):
    Portfolio = dict()
    temp = dict()
    for year in Return_Matrix.keys():
        for month in Return_Matrix[year].keys():
                 
            temp[month] = Return_Matrix[year][month].sort_values(ascending=False)[:Num]
            
        Portfolio[year] = temp
        
    return Portfolio


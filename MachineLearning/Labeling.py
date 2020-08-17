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


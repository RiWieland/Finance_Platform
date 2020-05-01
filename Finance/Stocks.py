import pandas as pd
import numpy as np

from Utils.Utils import to_numeric_


# Write Decorator for numeric values!
# to learn:
# - getters/setters
# @property, @ classmethod
# Underscores in current setting
# Is this correct pattern to assign attributes via functions?

class Stock:          # Design own class for Stock?

    def __init__(self, stock_frame, stock_name, index_frame, vol_n, MOM_n, SMA_n, OBV_N):
        self.stock_frame = stock_frame
        self.stock_name = stock_name
        self.index_frame = index_frame
        self.vol_window = vol_n
        self.risk_free = 0
        self.MOM_n = MOM_n
        self.SMA_n = SMA_n
        self.OBV_n = OBV_N

        self.stock_df = self.__get_stock_df()
        
    @to_numeric_('stock_frame')
    def __get_stock_df(self):          # use double underscore in beginning here?

        self.df_stock = self.stock_frame.loc[self.stock_frame['Symbol'] == self.stock_name]
        self.df_stock.reset_index(inplace=True)

        return self.df_stock

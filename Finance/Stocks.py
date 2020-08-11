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
        self.Dates = self.get_dates()
        self.returns = self.calc_return()
        self.calc_return_index = self.calc_return_index()
        self.log_return = self.calc_log_return()
        self.vol = self.calc_volatility()
        self.sharpe_ration = self.calc_sharpe()
        self.vol_chg = self.calc_vol_change()
        self.Will_R = self.calc_wil_r()
        self.calc_sto_osc = self.calc_sto_osc()
        self.calc_rsi = self.calc_rsi()
        self.calc_mom = self.calc_mom()
        self.sma = self.calc_sma()
        self.beta = self.calc_beta()
        self.obv = self.calc_obv()
        self.bollinger_lower = self.bollinger_lower()
        self.bollinger_upper = self.bollinger_upper()
        self.macd, self.macd_signal = self.macd()


    @to_numeric_('stock_frame')
    def __get_stock_df(self):          # use double underscore in beginning here?

        self.df_stock = self.stock_frame.loc[self.stock_frame['Symbol'] == self.stock_name]
        self.df_stock.reset_index(inplace=True)

        return self.df_stock

    # Do this with @property
    def get_dates(self):
        # Add Month/Year
        self.df_stock['Year'] = pd.DatetimeIndex(self.df_stock['Trading_Date']).year
        self.df_stock['Month'] = pd.DatetimeIndex(self.df_stock['Trading_Date']).month
        self.df_stock['Week'] = pd.DatetimeIndex(self.df_stock['Trading_Date']).week
        self.df_stock['Day'] = pd.DatetimeIndex(self.df_stock['Trading_Date']).day

        return self.df_stock

    def calc_return(self):
        self.df_stock['RETURNS'] = self.df_stock['Close'].pct_change()
        # adjust nan values:
        self.df_stock['RETURNS'].interpolate('nearest', inplace=True)
        self.df_stock['RETURNS'].iloc[0] = self.df_stock['RETURNS'].iloc[1]

        return self.df_stock
   
    def calc_return_index(self):
        self.index_frame['RETURNS'] = self.index_frame['Close'].astype(float).pct_change()
        # adjust nan values:
        self.index_frame['RETURNS'].interpolate('nearest', inplace=True)
        self.index_frame['RETURNS'].iloc[0] = self.index_frame['RETURNS'].iloc[1]
        
        return self.index_frame


    def calc_log_return(self):
        self.df_stock['LOG_RETURN'] = np.log(self.df_stock['Close'] / self.df_stock['Close'].shift(1))

        return self.df_stock['LOG_RETURN']

    def calc_volatility(self):
        self.df_stock['VOL'] = pd.Series(self.df_stock['LOG_RETURN']).rolling(self.vol_window).std()
        #pd.rolling_std(self.df_stock['LOG_RETURN'], window=self.vol_window) * np.sqrt(self.vol_window)
        return self.df_stock['VOL']

    def calc_sharpe(self):

        volatility = self.returns.std() * np.sqrt(self.vol_window)
        self.df_stock['SHARPE_RATIO'] = (self.returns.mean() - self.risk_free) / volatility
        return self.df_stock['SHARPE_RATIO']

    def calc_vol_change(self):
            self.df_stock['VOL_CHG'] = self.df_stock['Volume'].pct_change()

            return self.df_stock

    def calc_wil_r(self):                   # For all Attribute-Functions: Use no, single, or double underscore?
        df_store2 = pd.DataFrame()
        # Create the "L14" column in the DataFrame
        df_store2['L'] = pd.to_numeric(self.df_stock['Low']).rolling(window=14).min()

        # Create the "H14" column in the DataFrame
        df_store2['H'] = self.df_stock['High'].rolling(window=14).max()

        # Create WIL_R:
        self.df_stock['WIL_R'] = (df_store2['H'].subtract(pd.to_numeric(self.df_stock['Close']))) * (-100) / (df_store2['H'].subtract(df_store2['L']))

        return self.df_stock

    def calc_sto_osc(self):
        '''
        Stochastic Oscillator
        '''
        df_store = pd.DataFrame()
        # Create the "L14" column in the DataFrame
        df_store['L'] = self.df_stock['Low'].rolling(window=14).min()

        # Create the "H14" column in the DataFrame
        df_store['H'] = self.df_stock['High'].rolling(window=14).max()

        # Create the "%K" column in the DataFrame
        self.df_stock['STO_OSC'] = 100 * ((self.df_stock['Close'] - df_store['L']) / (df_store['H'] - df_store['L']))

        return self.df_stock

    def calc_rsi(self):
        '''
        Calculate Relative Strenght Index
        RSI is a popular momentum indicator which determines whether the stock is overbought
        or oversold
        '''
        delta = self.df_stock.Close.diff()
        window = 15
        up_days = delta.copy()
        up_days[delta <= 0] = 0.0
        down_days = abs(delta.copy())
        down_days[delta > 0] = 0.0
        RS_up = up_days.rolling(window).mean()
        RS_down = down_days.rolling(window).mean()
        self.df_stock['RSI'] = 100 - 100 / (1 + RS_up / RS_down)

        return self.df_stock

    # Momentum
    def calc_mom(self):

        for n in self.MOM_n:

            M = pd.Series(self.df_stock['Close'].diff(n), name='MOM_' + str(n))
            self.df_stock = self.df_stock.join(M)

        return self.df_stock

    def calc_sma(self):

        for n in self.SMA_n:

            #self.df_stock['SMA'] = pd.Series(pd.rolling_mean(self.df_stock['Close'], self.SMA_n), name='SMA_' + str(self.SMA_n))
            S = pd.Series(self.df_stock['Close'], name='SMA_' + str(n)).rolling(n).mean()
            self.df_stock = self.df_stock.join(S)

        return self.df_stock


    # rolling Beta of Stock:
    def calc_beta(self):
        # input_df['BETA'] = input_df.rolling(30).cov().unstack()['RETURN']['RETURN_INDICES']/ input_df.rolling(30).var().unstack()['RETURN_INDICES']

        window_ = 30
        # join indice Data for available stock data:
        df_merge = pd.merge(self.df_stock, self.index_frame, on=['Trading_Date'],
                            how='left', suffixes=('_Stock', '_Index'))

        df_merge.interpolate(method='linear', inplace=True)

        cov_ = pd.Series(df_merge['RETURNS_Stock'] ).rolling(window=window_).cov(df_merge['RETURNS_Index'])
        var_Index = pd.Series(df_merge['RETURNS_Index']).rolling(window=window_).var()

        self.df_stock['BETA'] = cov_ / var_Index
        #self.df_stock['BETA'] = cov_ / var_Index

        return self.df_stock['BETA']

    def calc_vol_ema(self):
        '''
        Calculate Volatility Expotential-Moving-Average
        '''
        prev_index = 0
        index_list = self.df_stock.index.values.tolist()
        self.df_stock.iloc[0, self.df_stock.columns.get_loc('VOL_EMA')] = abs(self.df_stock.iloc[0]['RETURN'])

        for i in range(1, len(index_list)):
            # Volatility EAM:
            alpha = 2 / (180 + 1)
            LAG_VOLATILITY_EMA = self.df_stock.iloc[prev_index, self.df_stock.columns.get_loc('VOL_EMA')]

            self.df_stock.loc[i, 'VOL_EMA'] = alpha * np.absolute(self.df_stock.loc[i, 'RETURN']) + (1 - alpha) * LAG_VOLATILITY_EMA

            prev_index = prev_index + 1

        return self.df_stock['VOL_EMA']

    # On-balance Volume
    def calc_obv(self):
        """
        Calculate On-Balance Volume for given data.
        """

        for n in self.OBV_n:
            i = 0
            OBV = [0]
            while i < self.df_stock.index[-1]:
                if self.df_stock.loc[i + 1, 'Close'] - self.df_stock.loc[i, 'Close'] > 0:
                    OBV.append(self.df_stock.loc[i + 1, 'Volume'])
                if self.df_stock.loc[i + 1, 'Close'] - self.df_stock.loc[i, 'Close'] == 0:
                    OBV.append(0)
                if self.df_stock.loc[i + 1, 'Close'] - self.df_stock.loc[i, 'Close'] < 0:
                    OBV.append(-self.df_stock.loc[i + 1, 'Volume'])
                i = i + 1
            OBV = pd.Series(OBV)
            OBV_ma = pd.Series(OBV.rolling(n, min_periods=n).mean(), name='OBV_' + str(n))
            self.df_stock = self.df_stock.join(OBV_ma)

        return self.df_stock
    
    def bollinger_upper(self, window=21):
        rolling_mean = self.df_stock.Close.rolling(window).mean()
        rolling_std = self.df_stock.Close.rolling(window).std()
        self.df_stock['BOLLING_UPPER'] = rolling_mean + (rolling_std*2)
        return self.df_stock['BOLLING_UPPER']
    
    
    def bollinger_lower(self, window=21):
        rolling_mean = self.df_stock.Close.rolling(window).mean()
        rolling_std = self.df_stock.Close.rolling(window).std()
        self.df_stock['BOLLING_LOWER'] = rolling_mean - (rolling_std*2)
        return self.df_stock['BOLLING_LOWER']

    def macd(self):
        exp1 = self.df_stock.Close.ewm(span=12, adjust=False).mean()
        exp2 = self.df_stock.Close.ewm(span=26, adjust=False).mean()
        self.df_stock['MACD'] = exp1-exp2
        self.df_stock['MACD_SIGNAL'] = self.df_stock.MACD.ewm(span=9, adjust=False).mean()
        return self.df_stock[['MACD', 'MACD_SIGNAL']]


    def calc_to_database(self, target_table, db_connection):

        self.df_stock[['Trading_Date', 'Symbol', 'Year', 'Month', 'Week', 'Day', 'RETURNS', 'VOL_CHG', 'WIL_R',
                           'STO_OSC', 'RSI', 'MOM_14', 'MOM_21',
                        'MOM_28', 'SMA_14', 'SMA_21', 'SMA_28', 'OBV_14', 'OBV_21', 'OBV_28', 'BETA']].to_sql(
                target_table, db_connection, if_exists="append", index=False)




import sqlite3
from sqlite3 import Error



class DB_object():

    def __init__(self, path):
        self.path = path
        self.create_connection()

    def __str__(self):
        return "running sqlite3 version :{0}, " \
               "Connection to Database on: {1})".format(sqlite3.version, self.path)

    def create_connection(self):
        """ create a database connection to a SQLite database """

        try:
            self.conn = sqlite3.connect(self.path)
            print("Create Connection to SQL Lite")

            return self.conn

        except Error as e:
            print(e)

    def close_connection(self):
        try:

            self.conn.close()
            print("Closed Connection to SQL-LITE")

        except Error as e:
            print(e)

    def create_stock_stage(self):

        sql_command = """
            CREATE TABLE IF NOT EXISTS Stocks_Stage ( 
            Trading_Date DATE, 
            High VARCHAR(20), 
            Low VARCHAR(30), 
            Open VARCHAR(30),
            Close VARCHAR(30), 
            Volume VARCHAR(30),
            Adj_Close VARCHAR(30),
            Symbol VARCHAR(30),
            Index_ VARCHAR(30));"""

        self.conn.cursor().execute(sql_command)
        print("Staging_table created")

        return 'Stocks_Stage'

    def create_stock_calc(self):

        sql_command = """
            CREATE TABLE IF NOT EXISTS Stock_Calc ( 
            Trading_Date DATE, 
            Symbol VARCHAR(30),
            Index_ VARCHAR(30),
            Year VARCHAR(30),
            Month VARCHAR(30),
            Week VARCHAR(30),
            Day VARCHAR(30),
            Close VARCHAR(30),
            Adj_Close VARCHAR(30),
            RETURNS VARCHAR(30),
            LOG_RETURN VARCHAR(30),
            VOL VARCHAR(30),
            SHARPE_RATIO VARCHAR(30),
            VOL_CHG VARCHAR(30),
            WIL_R VARCHAR(30),
            STO_OSC VARCHAR(30),
            RSI VARCHAR(30),
            MOM_14 VARCHAR(30),
            MOM_21 VARCHAR(30), 
            MOM_28 VARCHAR(30), 
            OBV_14 VARCHAR(30),
            OBV_21 VARCHAR(30), 
            OBV_28 VARCHAR(30),  
            SMA_14 VARCHAR(30),
            SMA_21 VARCHAR(30),
            SMA_28 VARCHAR(30),
            BETA VARCHAR(30),
            BOLLING_LOWER VARCHAR(30),
            BOLLING_UPPER VARCHAR(30),
            MACD VARCHAR(30),
            MACD_SIGNAL VARCHAR(30)
            );"""

        self.conn.cursor().execute(sql_command)
        print("Table Stock Calc created")

        return 'Stock_Calc'

    def create_index_stage(self):

        sql_command = """
            CREATE TABLE IF NOT EXISTS Index_Stage ( 
            Trading_Date DATE, 
            High VARCHAR(20), 
            Low VARCHAR(30), 
            Open VARCHAR(30),
            Close VARCHAR(30), 
            Volume VARCHAR(30),
            Adj_Close VARCHAR(30),
            Symbol VARCHAR(30),
            Index_ VARCHAR(30));"""

        self.conn.cursor().execute(sql_command)
        print("Index_table created")

        return 'Index_Stage'

    def create_index_calc(self):

        sql_command = """
            CREATE TABLE IF NOT EXISTS Index_Calc ( 
            Trading_Date DATE, 
            Symbol VARCHAR(30),
            Index_ VARCHAR(30),
            Year VARCHAR(30),
            Month VARCHAR(30),
            Week VARCHAR(30),
            Day VARCHAR(30),
            Returns VARCHAR(30),
            Vol_Chg VARCHAR(30)   
            );"""

        self.conn.cursor().execute(sql_command)
        print("Table Index_Calc created")

        return 'Index_Calc'

    def create_COT_staging(self):

        sql_command = """
        CREATE TABLE COT_Stage ( 
        Date DATE PRIMARY KEY, 
        High VARCHAR(20), 
        Low VARCHAR(30), 
        Open VARCHAR(30), 
        Close VARCHAR(30), 
        Volune VARCHAR(30), 
        Adj Close VARCHAR(30)
        );"""

        self.cursor.execute(sql_command)
        print("COT Table created")

    def drop_table(self, table_name):

        sql_command = """
        DROP TABLE IF EXISTS """ + table_name + """;"""

        self.conn.cursor().execute(sql_command)

        print("Droped Table:", table_name)


def query(conn, TABLE, YEAR=None, SYMBOL=None):
    '''
    # Condition as List to be implemented
    # Export table as pandas DF
    '''
    sql = 'select * from {} where 1=1 '.format(TABLE)
    if YEAR:
        
        sql += 'and YEAR = {} '.format(str(YEAR))

    if SYMBOL:
        SYMBOL = "'" + SYMBOL + "'"
        sql += 'and SYMBOL = {} '.format(str(SYMBOL))
    
    
    Stock_frame = pd.read_sql_query(sql, conn)
    Stock_frame['Trading_Date'] = pd.to_datetime(Stock_frame['Trading_Date'])

    return Stock_frame




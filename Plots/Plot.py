
import pandas as pd
import matplotlib.pyplot as plt

def dynamic_ploting(stock, *args, path=None):#), path=None): #, path=None):

    # Bollinger band plot with EMA and original historical data
    plt.figure(figsize=(16,5))
    plt.style.use('seaborn-whitegrid')
    color_index=5
    colors = "bgrcmykw"

    plt.plot(stock.Trading_Date, stock.Close, color='#3388cf' ,label='Close')
    #plt.plot(stock.index, stock.MA21, color='#ad6eff', label='Moving Average (21 days)')

    for arg in args:

        if arg =='Bollinger_Band':
            plt.plot(stock.Trading_Date, stock.BOLLING_UPPER, color='#ffbd74', alpha=0.15)
            plt.plot(stock.Trading_Date, stock.BOLLING_LOWER, color='#ffa33f', alpha=0.15)
            plt.fill_between(stock.Trading_Date, stock.BOLLING_UPPER, stock.BOLLING_LOWER, color='#ffa33f', alpha=0.05, label='Bollinger Band')

        else:

            plt.plot(stock.Trading_Date, stock[arg], c=colors[color_index], label=arg, alpha=0.4)
            color_index = color_index + 1

    plt.legend(frameon=True, loc=1, ncol=1, fontsize=10, borderpad=.6)
    plt.title('Bollinger Bands', fontSize=15)
    plt.ylabel('Price', fontSize=12)
    plt.xlim([stock.Trading_Date.min(), stock.Trading_Date.max()])

    if path != None:
        plt.savefig(path)
    else:
        plt.show()

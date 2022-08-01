import pandas as pd
import pandas_ta as ta
import finplot as fplt

if __name__ == "__main__":
    df = pd.DataFrame()
    df = pd.read_csv("csv/ibov2016-2022.csv", sep=",")    
    df.set_index(pd.DatetimeIndex(df["Date"]), inplace=True)    
    
    # Padrões de candle
    df['doji'] = df.ta.cdl_pattern(name="doji")
    df['dragonflydoji'] = df.ta.cdl_pattern(name="dragonflydoji")
    df['hammer'] = df.ta.cdl_pattern(name="hammer")
    
    # Plotagem da figura com Finplot
    ax = fplt.create_plot('IBOV')
    fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
    # overlay de volume
    fplt.volume_ocv(df[['Open', 'Close', 'Volume']], ax=ax.overlay())
    
    # dumb markers do doji
    df.loc[(df['doji'] != 0), 'doji-marker'] = df['Low'] - 100
    fplt.plot(df['doji-marker'], ax=ax, color='#114ba8', style='^', legend='Doji', size=12)
    # dumb markers do dragonfly
    df.loc[(df['dragonflydoji'] != 0), 'dragonfly-marker'] = df['Low'] - 200
    fplt.plot(df['dragonfly-marker'], ax=ax, color='#31b302', style='v', legend='Dragonfly', size=12)
    # dumb markers do hammer
    df.loc[(df['hammer'] != 0), 'hammer-marker'] = df['High'] + 100
    fplt.plot(df['hammer-marker'], ax=ax, color='#31b302', style='+', legend='Hammer', size=12)
    
    fplt.show()
    # print(df)


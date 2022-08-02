from operator import length_hint
import pandas as pd
import pandas_ta as ta
import finplot as fplt

if __name__ == "__main__":
    df = pd.DataFrame()
    df = pd.read_csv("csv/ibov2016-2022.csv", sep=",")    
    # Torna o campo Date o índice do vetor
    df.set_index(pd.DatetimeIndex(df["Date"]), inplace=True)    
    
    # Padrões de candle
    df['doji'] = df.ta.cdl_pattern(name="doji")
    df['dragonflydoji'] = df.ta.cdl_pattern(name="dragonflydoji")
    df['hammer'] = df.ta.cdl_pattern(name="hammer")
    df['invertedhammer'] = df.ta.cdl_pattern(name="invertedhammer")
    df['engulfing'] = df.ta.cdl_pattern(name="engulfing")
    df['harami'] = df.ta.cdl_pattern(name="harami")
    df['rsi'] = df.ta.rsi(length=14)
    df['sma'] = df.ta.sma(length=21)
    df['ema'] = df.ta.ema(length=21)
    
    # Plotagem da figura com Finplot
    ax, ax2 = fplt.create_plot('IBOV', rows=2)
    fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
    # overlay de volume
    fplt.volume_ocv(df[['Open', 'Close', 'Volume']], ax=ax.overlay())
    
    # dumb markers do doji
    df.loc[(df['doji'] != 0), 'doji-marker'] = df['Low'] - 100
    fplt.plot(df['doji-marker'], ax=ax, color='#114ba8', style='^', legend='Doji', size=20)
    # dumb markers do dragonfly
    df.loc[(df['dragonflydoji'] != 0), 'dragonfly-marker'] = df['Low'] - 200
    fplt.plot(df['dragonfly-marker'], ax=ax, color='#31b302', style='v', legend='Dragonfly', size=20)
    # dumb markers do hammer
    df.loc[(df['hammer'] != 0), 'hammer-marker'] = df['High'] + 100
    fplt.plot(df['hammer-marker'], ax=ax, color='#31b302', style='+', legend='Hammer', size=20)
    # dumb markers do inverted hammer
    df.loc[(df['invertedhammer'] != 0), 'invertedhammer-marker'] = df['High'] + 100
    fplt.plot(df['invertedhammer-marker'], ax=ax, color='#31b302', style='o', legend='Inverted Hammer', size=20)
    # dumb markers do engulfing
    df.loc[(df['engulfing'] != 0), 'engulfing-marker'] = df['High'] + 200
    fplt.plot(df['engulfing-marker'], ax=ax, color='#114ba8', style='o', legend='Engulfing', size=20)
    # dumb markers do harami
    df.loc[(df['harami'] != 0), 'harami-marker'] = df['Low'] - 200
    fplt.plot(df['harami-marker'], ax=ax, color='#114ba8', style='+', legend='Engulfing', size=20)
    
    # plotar médias
    fplt.plot(df['sma'], ax=ax, legend='SMA 21', color='#31b302')
    fplt.plot(df['ema'], ax=ax, legend='EMA 21', color='#114ba8')
    
    # plotar RSI
    fplt.plot(df['rsi'], ax=ax2, legend='RSI')
    fplt.add_band(30, 70, ax=ax2)
    
    print(df)
    fplt.show()


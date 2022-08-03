import pandas as pd
import finplot as fplt

def normalize_fuzzy_indicators(df, key):
    normalized_df=(df[key]-df[key].min())/(df[key].max()-df[key].min())*100
    return normalized_df

def normalize_crispy_indicators(df, key):
    normalized_df=(df[key]-df[key].min())/(df[key].max()-df[key].min())
    return normalized_df

def plot_financial_data(df, advise_point):
        df = df.set_index(pd.DatetimeIndex(df["Date"]))
        # Plotagem da figura com Finplot
        ax, ax2, ax3 = fplt.create_plot('IBOV', rows=3)
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
        fplt.plot(abs(df['engulfing-marker']), ax=ax, color='#114ba8', style='o', legend='Engulfing', size=20)
        # dumb markers do harami
        df.loc[(df['harami'] != 0), 'harami-marker'] = df['Low'] - 200
        fplt.plot(abs(df['harami-marker']), ax=ax, color='#114ba8', style='+', legend='Harami', size=20)
        
        # plotar médias
        fplt.plot(df['sma'], ax=ax, legend='SMA 21', color='#31b302')
        fplt.plot(df['ema'], ax=ax, legend='EMA 21', color='#114ba8')
        
        # plotar RSI
        fplt.plot(df['rsi'], ax=ax2, legend='RSI')
        fplt.add_band(30, 70, ax=ax2)
        
        # plotar Williams %R
        fplt.plot(df['posicao'], ax=ax3, legend='Williams %R')
        fplt.add_band(20, 80, ax=ax3)
        
        # plotar ponto de interesse
        dt_time = pd.to_datetime(df['Date'][advise_point])
        fplt.plot(dt_time, (df['Low'][dt_time] - 500), ax=ax, color='#fc050d', style='o', legend='Advise Point', size=100)
        
        # print(df)
        # print('Ponto de análise: ' + df['Date'][advise_point])
        fplt.show()
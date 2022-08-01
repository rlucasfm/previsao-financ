import pandas as pd
import pandas_ta as ta
import finplot as fplt
# import plotly.graph_objects as go

if __name__ == "__main__":
    df = pd.DataFrame()
    df = pd.read_csv("csv/ibov2016-2022.csv", sep=",")    
    df.set_index(pd.DatetimeIndex(df["Date"]), inplace=True)
    # df.sort_values(by="unix", inplace=True)
    # df["date"] = pd.to_datetime(df["unix"], unit="s")
    
    # Padrões de candle
    df['doji'] = df.ta.cdl_pattern(name="doji")
    
    # Plotagem da figura com Finplot
    ax = fplt.create_plot('IBOV')
    fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
    # overlay de volume
    fplt.volume_ocv(df[['Open', 'Close', 'Volume']], ax=ax.overlay())
    # dumb markers do doji
    df.loc[(df['doji'] != 0), 'marker'] = df['Low'] - 100
    fplt.plot(df['marker'], ax=ax, color='#114ba8', style='^', legend='Doji', size=12)
    fplt.show()
    
    # Plotagem da figura com Plotly
    # fig = go.Figure(data = [go.Candlestick(x = df.Date,
    #     open = df.Open,
    #     high = df.High,
    #     close = df.Close,
    #     low = df.Low
    #     )])

    # Marker do doji
    # fig.add_trace(go.Scatter(x = df.Date,
    #     y = (df.High + 600) * (df.doji/100),
    #     mode = 'markers',
    #     marker = dict(color='Blue', size=12),
    #     hoverinfo = 'skip'
    #     ))
    # fig.update_yaxes(range=[40000, 140000])
    # fig.show()

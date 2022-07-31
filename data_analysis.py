import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

if __name__ == "__main__":
    df = pd.DataFrame() # Empty DataFrame
    df = pd.read_csv("btcusd.csv", sep=",")    
    # df.set_index(pd.DatetimeIndex(df["datetime"]), inplace=True)
    df.sort_values(by="unix", inplace=True)
    df["date"] = pd.to_datetime(df["unix"], unit="s")
    
    fig = go.Figure(data = [go.Candlestick(x = df.date,
        open = df.open,
        high = df.high,
        close = df.close,
        low = df.low)])
    
    fig.show()

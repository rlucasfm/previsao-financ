import pandas as pd
import pandas_ta as ta

class SymbolData:
    def __init__(self, symbol_name):        
        self.df = pd.DataFrame()
        self.df = pd.read_csv(symbol_name, sep=",")            

    def proccess_indicators(self):
        self.df['doji'] = self.df.ta.cdl_pattern(name="doji")
        self.df['dragonflydoji'] = self.df.ta.cdl_pattern(name="dragonflydoji")
        self.df['hammer'] = self.df.ta.cdl_pattern(name="hammer")
        self.df['invertedhammer'] = self.df.ta.cdl_pattern(name="invertedhammer")
        self.df['engulfing'] = self.df.ta.cdl_pattern(name="engulfing")
        self.df['harami'] = self.df.ta.cdl_pattern(name="harami")
        self.df['rsi'] = self.df.ta.rsi(length=14)
        self.df['sma'] = self.df.ta.sma(length=21)
        self.df['ema'] = self.df.ta.ema(length=21)
        
        return self.df
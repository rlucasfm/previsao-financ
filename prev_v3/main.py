from signal_processing import SymbolData
from technical_analysis import FuzzyObject
from utils import normalize_fuzzy_indicators, normalize_crispy_indicators, plot_financial_data

class Consts:
    WINDOW_SIZE = 30
    FIRST_DATE = '2022-02-01'


if __name__ == "__main__":
    # Load data and normalize
    symbol_data = SymbolData('csv/ibov2016-2022.csv')
    sd_copy = symbol_data.proccess_indicators().copy()
    symbol_data.df['engulfing'] = normalize_crispy_indicators(symbol_data.df, 'engulfing')
    symbol_data.df['dragonflydoji'] = normalize_crispy_indicators(symbol_data.df, 'dragonflydoji')
    symbol_data.df['doji'] = normalize_crispy_indicators(symbol_data.df, 'doji')
    symbol_data.df['harami'] = normalize_crispy_indicators(symbol_data.df, 'harami')
    symbol_data.df['hammer'] = normalize_crispy_indicators(symbol_data.df, 'hammer')
    symbol_data.df['invertedhammer'] = normalize_crispy_indicators(symbol_data.df, 'invertedhammer')
    symbol_data.df['sma'] = normalize_fuzzy_indicators(symbol_data.df, 'sma')
    symbol_data.df['ema'] = normalize_fuzzy_indicators(symbol_data.df, 'ema')
    
    # Select Symbol Data window
    index_first_date = symbol_data.df.index[symbol_data.df['Date'] == Consts.FIRST_DATE].tolist()[0]
    index_last_date = index_first_date + Consts.WINDOW_SIZE
    symbol_data_windowed = symbol_data.df.iloc[index_first_date:index_last_date, :].copy()
    
    # Window data for plot
    sb_copy_data_windowed = sd_copy.iloc[index_first_date:index_last_date, :]    
    
    # Select analysis point
    indicators = sb_copy_data_windowed[['doji', 'dragonflydoji', 'hammer', 'invertedhammer', 'engulfing', 'harami']]
    indicators['engulfing'] = indicators['engulfing'].abs()
    indicators['harami'] = indicators['harami'].abs()
    advise_point = indicators.sum(axis=1).argmax() + indicators.first_valid_index()   
       
    # Criação do Objeto Fuzzy 
    print(symbol_data_windowed)
    fuzzy_forecast = FuzzyObject(
        symbol_data_windowed['engulfing'][advise_point],
        symbol_data_windowed['dragonflydoji'][advise_point],
        symbol_data_windowed['doji'][advise_point],
        symbol_data_windowed['harami'][advise_point],
        symbol_data_windowed['hammer'][advise_point],
        symbol_data_windowed['invertedhammer'][advise_point],
        symbol_data_windowed['sma'][advise_point],
        symbol_data_windowed['rsi'][advise_point],
        symbol_data_windowed['ema'][advise_point],
        20
    )
    # fuzzy_forecast.print_dataset()

    # Computação dos resultados e exibição    
    fuzzy_forecast.compute_results()
    fuzzy_forecast.print_results()
    plot_financial_data(sb_copy_data_windowed)
    
    
        
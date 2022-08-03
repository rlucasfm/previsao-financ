from signal_processing import SymbolData
from technical_analysis import FuzzyObject
from utils import normalize_fuzzy_indicators, normalize_crispy_indicators, plot_financial_data
# Ignorar warnings
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

class Consts:
    WINDOW_SIZE = 60
    FIRST_DATE = '2018-02-05'

def main(first_date='2018-02-05', window=60, test=False):
    # ---- Load data and normalize
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
    
    # ---- Select Symbol Data window
    index_first_date = symbol_data.df.index[symbol_data.df['Date'] == first_date].tolist()[0]
    index_last_date = index_first_date + window
    symbol_data_windowed = symbol_data.df.iloc[index_first_date:index_last_date, :].copy()
    
    # ---- Window data for plot
    sb_copy_data_windowed = sd_copy.iloc[index_first_date:index_last_date, :]
    
    # ---- Select analysis point
    indicators = sb_copy_data_windowed[['doji', 'dragonflydoji', 'hammer', 'invertedhammer', 'engulfing', 'harami']]
    indicators['engulfing'] = indicators['engulfing'].abs()
    indicators['harami'] = indicators['harami'].abs()
    adv_pt = indicators.sum(axis=1).argmax()
    advise_point = adv_pt + indicators.first_valid_index()   
       
    # ---- Criação do Objeto Fuzzy 
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
        symbol_data_windowed['posicao'][advise_point],
    )

    # ---- Computação dos resultados  
    results = fuzzy_forecast.compute_results()
    
    if(not test):
        # Exibição dos resultados no gráfico com pertinencias
        fuzzy_forecast.print_results()    
        # ---- Exibir as funções de pertinencia
        # fuzzy_forecast.print_dataset()
        # ---- Printar dados de indicadores no ponto de análise
        print(symbol_data_windowed.loc[advise_point, :])
        # Exibe os candles na janela escolhida, assim como o ponto de interesse escolhido
        plot_financial_data(sb_copy_data_windowed, adv_pt)
    
    return {
        "resultados": results,
        "dados_selecionados": symbol_data_windowed,
        "ponto_analise": advise_point
    }
    
if __name__ == "__main__":
    main(Consts.FIRST_DATE, Consts.WINDOW_SIZE)
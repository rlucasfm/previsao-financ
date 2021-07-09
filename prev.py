import matplotlib.pyplot as plt
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl


if __name__ == "__main__":
    universe = np.arange(0, 11, 1)

    print('Definindo os antecedentes...')
    sinal_candle = ctrl.Antecedent(universe, 'sinal_candle')
    mediamovel = ctrl.Antecedent(universe, 'media_movel')
    posicao = ctrl.Antecedent(universe, 'posicao')
    print('Definindo o consequente...')
    previsao = ctrl.Consequent(np.arange(0, 101, 1), 'previsao')    

    print('Definindo as funcoes de pertinencia...')
    sinal_candle.automf(names=['Engolfo Alta', 'Doji', 'Martelo', 'Dragonfly Gravestone', 'Pinca', 'Engolfo Baixa', 'Dragonfly'])
    mediamovel.automf(names=['Alta', 'Baixa'])
    posicao.automf(names=['Fundo', 'Topo'])

    previsao['venda'] = fuzz.sigmf(previsao.universe, 20, -0.2)
    previsao['manter'] = fuzz.gaussmf(previsao.universe, 50, 15)
    previsao['compra'] = fuzz.sigmf(previsao.universe, 80, 0.2)    
    
    sinal_candle.view()
    mediamovel.view()
    posicao.view()   
    previsao.view()     

    print('Definindo as regras...')
    regra1 = ctrl.Rule(sinal_candle['Engolfo Alta']         & mediamovel['Alta']                        , previsao['compra'])
    regra2 = ctrl.Rule(sinal_candle['Engolfo Baixa']        & mediamovel['Baixa']                       , previsao['venda'])
    regra3 = ctrl.Rule(sinal_candle['Doji']                 & posicao['Fundo']                          , previsao['compra'])
    regra4 = ctrl.Rule(sinal_candle['Doji']                 & posicao['Topo']                           , previsao['venda'])
    regra5 = ctrl.Rule(sinal_candle['Dragonfly']            & posicao['Fundo']                          , previsao['compra'])
    regra6 = ctrl.Rule(sinal_candle['Dragonfly Gravestone'] & posicao['Topo']                           , previsao['venda'])
    regra7 = ctrl.Rule(sinal_candle['Martelo']              & mediamovel['Alta']    & posicao['Fundo']  , previsao['compra'])
    regra8 = ctrl.Rule(sinal_candle['Martelo']              & mediamovel['Baixa']   & posicao['Topo']   , previsao['venda'])
    regra9 = ctrl.Rule(sinal_candle['Pinca']                & posicao['Fundo']                          , previsao['venda'])
    regra10= ctrl.Rule(sinal_candle['Pinca']                & posicao['Topo']                           , previsao['compra'])
    

    sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9, regra10])
    sistema = ctrl.ControlSystemSimulation(sistema_controle)

    # # Inputs aceita um array numpy ou um valor inteiro
    sistema.input['sinal_candle'] = 5
    sistema.input['media_movel'] = 7
    sistema.input['posicao'] = 2
    sistema.compute()

    print(sistema.output['previsao'])
    previsao.view(sim=sistema)
    plt.show()
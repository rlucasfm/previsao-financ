import sys
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl


if __name__ == "__main__":
    universe = np.arange(0, 10.01, 0.01)
    uni3 = np.arange(0, 2.1, 0.01)
    uni2 = np.arange(0, 1.1, 0.01)

    # -------------- DEFINIÇÃO DE ANTECEDENTES --------------
    print('Definindo os antecedentes...')        
    engulfing = ctrl.Antecedent(uni2, 'engulfing')
    dragonfly = ctrl.Antecedent(uni2, 'dragonfly')    
    doji = ctrl.Antecedent(uni2, 'doji')    
    harami = ctrl.Antecedent(uni2, 'harami')    
    martelo = ctrl.Antecedent(uni2, 'martelo')
    martelo_invertido = ctrl.Antecedent(uni2, 'martelo_invertido')

    mediamovel = ctrl.Antecedent(universe, 'media_movel')
    rsi = ctrl.Antecedent(universe, 'rsi')
    ema = ctrl.Antecedent(universe, 'ema')
    posicao = ctrl.Antecedent(universe, 'posicao')

    # -------------- DEFINIÇÃO DO CONSEQUENTE --------------
    print('Definindo o consequente...')
    previsao = ctrl.Consequent(np.arange(0, 101, 1), 'previsao')
    
    # ------ DEFINIÇÃO DO THRESHOLD DE AGRESSIVIDADE -------
    threshold = 3

    # -------------- DEFINIÇÃO DAS FUNÇÕES DE PERTINÊNCIA --------------
    print('Definindo as funcoes de pertinencia...')
    engulfing['baixa'] = fuzz.trimf(engulfing.universe, [-0.01, 0, 0.01])
    engulfing['nao'] = fuzz.trimf(engulfing.universe, [0.49, 0.5, 0.51])   
    engulfing['alta'] = fuzz.trimf(engulfing.universe, [0.99, 1, 1.01]) 

    dragonfly['nao'] = fuzz.trimf(dragonfly.universe, [-0.01, 0, 0.01])
    dragonfly['sim'] = fuzz.trimf(dragonfly.universe, [0.99, 1, 1.01]) 

    doji['nao'] = fuzz.trimf(doji.universe, [-0.01, 0, 0.01])
    doji['sim'] = fuzz.trimf(doji.universe, [0.99, 1, 1.01]) 

    harami['baixa'] = fuzz.trimf(harami.universe, [-0.01, 0, 0.01])
    harami['nao'] = fuzz.trimf(harami.universe, [0.49, 0.5, 0.51])
    harami['alta'] = fuzz.trimf(harami.universe, [0.99, 1, 1.01])

    martelo['nao'] = fuzz.trimf(martelo.universe, [-0.01, 0, 0.01])
    martelo['sim'] = fuzz.trimf(martelo.universe, [0.99, 1, 1.01]) 
    
    martelo_invertido['nao'] = fuzz.trimf(martelo_invertido.universe, [-0.01, 0, 0.01])
    martelo_invertido['sim'] = fuzz.trimf(martelo_invertido.universe, [0.99, 1, 1.01]) 
    
    mediamovel['Baixa'] = fuzz.trimf(mediamovel.universe, [-0.01, 0, 5])
    mediamovel['Alta'] = fuzz.trimf(mediamovel.universe, [5, 10, 11])
    
    rsi['sobrevenda'] = fuzz.trimf(rsi.universe, [-0.01, 0, 5])
    rsi['sobrecompra'] = fuzz.trimf(rsi.universe, [5, 10, 11])

    ema['Baixa'] = fuzz.trimf(ema.universe, [-0.01, 0, 5])
    ema['Alta'] = fuzz.trimf(ema.universe, [5, 10, 11])

    posicao['Fundo'] = fuzz.trimf(posicao.universe, [-0.01, 0, 5])
    posicao['Topo'] = fuzz.trimf(posicao.universe, [5, 10, 11])    

    previsao['venda'] = fuzz.sigmf(previsao.universe, (35 + threshold), -0.2)
    previsao['manter'] = fuzz.gaussmf(previsao.universe, 50, (15 - threshold))
    previsao['compra'] = fuzz.sigmf(previsao.universe, (65 - threshold), 0.2)   
    
    # -------------- Descomente isto caso queira observar as funções de pertinência --------------
    engulfing.view()
    # dragonfly.view()
    # doji.view()
    # harami.view()
    # martelo.view()
    # martelo_invertido.view()
    # mediamovel.view()
    # rsi.view()
    # ema.view()
    # posicao.view()   
    # previsao.view()     

    # -------------- DEFINIÇÃO DAS REGRAS --------------
    print('Definindo as regras...')
    regra1 = ctrl.Rule(engulfing['alta']             & mediamovel['Alta']                               , previsao['compra'])
    regra2 = ctrl.Rule(engulfing['baixa']            & mediamovel['Baixa']                              , previsao['venda'])
    regra3 = ctrl.Rule(doji['sim']                                           & posicao['Fundo']         , previsao['compra'])
    regra4 = ctrl.Rule(doji['sim']                                           & posicao['Topo']          , previsao['venda'])
    regra5 = ctrl.Rule(dragonfly['sim']                                      & posicao['Fundo']         , previsao['compra'])    
    regra6 = ctrl.Rule(martelo_invertido['sim']      & mediamovel['Alta']    & posicao['Fundo']         , previsao['compra'])
    regra7 = ctrl.Rule(martelo['sim']                & mediamovel['Baixa']   & posicao['Topo']          , previsao['venda'])
    regra8 = ctrl.Rule(harami['alta']                                        & posicao['Fundo']         , previsao['compra'])
    regra9 = ctrl.Rule(harami['baixa']                                       & posicao['Topo']          , previsao['venda'])
    regra10= ctrl.Rule(                                                      posicao['Topo']            , previsao['venda'])
    regra11= ctrl.Rule(                                                      posicao['Fundo']           , previsao['compra'])
    regra12= ctrl.Rule(                              mediamovel['Alta']                                 , previsao['compra'])
    regra13= ctrl.Rule(                              mediamovel['Baixa']                                , previsao['venda'])
    # Regras com Média Móvel
    regra14= ctrl.Rule(                              ~posicao['Topo']        & ~posicao['Fundo']        , previsao['manter'])
    regra15= ctrl.Rule(                              ~mediamovel['Alta']     & ~mediamovel['Baixa']     , previsao['manter'])
    regra16= ctrl.Rule(                              mediamovel['Alta']      & posicao['Topo']          , previsao['manter'])
    regra17= ctrl.Rule(                              mediamovel['Baixa']     & posicao['Fundo']         , previsao['manter'])
    regra18 = ctrl.Rule(engulfing['alta']            & mediamovel['Alta']    & posicao['Fundo']         , previsao['compra'])
    regra19 = ctrl.Rule(engulfing['baixa']           & mediamovel['Baixa']   & posicao['Topo']          , previsao['venda'])
    regra20 = ctrl.Rule(doji['sim']                  & posicao['Fundo']      & mediamovel['Alta']       , previsao['compra'])
    regra21 = ctrl.Rule(doji['sim']                  & posicao['Topo']       & mediamovel['Baixa']      , previsao['venda'])
    regra22 = ctrl.Rule(dragonfly['sim']             & posicao['Fundo']      & mediamovel['Alta']       , previsao['compra'])
    regra23 = ctrl.Rule(harami['alta']               & posicao['Fundo']      & mediamovel['Alta']       , previsao['compra'])
    regra24 = ctrl.Rule(harami['baixa']              & posicao['Topo']       & mediamovel['Baixa']      , previsao['venda'])
    # Regras com EMA
    regra25= ctrl.Rule(                              ~ema['Alta']            & ~ema['Baixa']            , previsao['manter'])
    regra26= ctrl.Rule(                              ema['Alta']             & posicao['Topo']          , previsao['manter'])
    regra27= ctrl.Rule(                              ema['Baixa']            & posicao['Fundo']         , previsao['manter'])
    regra28 = ctrl.Rule(engulfing['alta']            & ema['Alta']           & posicao['Fundo']         , previsao['compra'])
    regra29 = ctrl.Rule(engulfing['baixa']           & ema['Baixa']          & posicao['Topo']          , previsao['venda'])
    regra30 = ctrl.Rule(doji['sim']                  & posicao['Fundo']      & ema['Alta']              , previsao['compra'])
    regra31 = ctrl.Rule(doji['sim']                  & posicao['Topo']       & ema['Baixa']             , previsao['venda'])
    regra32 = ctrl.Rule(dragonfly['sim']             & posicao['Fundo']      & ema['Alta']              , previsao['compra'])
    regra33 = ctrl.Rule(harami['alta']               & posicao['Fundo']      & ema['Alta']              , previsao['compra'])
    regra34 = ctrl.Rule(harami['baixa']              & posicao['Topo']       & ema['Baixa']             , previsao['venda'])
    # Regras com RSI
    regra35= ctrl.Rule(                              ~rsi['sobrevenda']      & ~rsi['sobrecompra']      , previsao['manter'])
    regra36= ctrl.Rule(                              rsi['sobrecompra']      & posicao['Topo']          , previsao['venda'])
    regra37= ctrl.Rule(                              rsi['sobrevenda']       & posicao['Fundo']         , previsao['compra'])
    regra38 = ctrl.Rule(engulfing['alta']            & rsi['sobrevenda']     & posicao['Fundo']         , previsao['compra'])
    regra39 = ctrl.Rule(engulfing['baixa']           & rsi['sobrecompra']    & posicao['Topo']          , previsao['venda'])
    regra40 = ctrl.Rule(doji['sim']                  & posicao['Fundo']      & rsi['sobrevenda']        , previsao['compra'])
    regra41 = ctrl.Rule(doji['sim']                  & posicao['Topo']       & rsi['sobrecompra']       , previsao['venda'])
    regra42 = ctrl.Rule(dragonfly['sim']             & posicao['Fundo']      & rsi['sobrevenda']        , previsao['compra'])
    regra43 = ctrl.Rule(harami['alta']               & posicao['Fundo']      & rsi['sobrevenda']        , previsao['compra'])
    regra44 = ctrl.Rule(harami['baixa']              & posicao['Topo']       & rsi['sobrecompra']       , previsao['venda'])


    sistema_controle = ctrl.ControlSystem([
                                       regra1, 
                                       regra2, 
                                       regra3, 
                                       regra4, 
                                       regra5, 
                                       regra6, 
                                       regra7, 
                                       regra8, 
                                       regra9, 
                                       regra10, 
                                       regra11, 
                                       regra12, 
                                       regra13, 
                                       regra14, 
                                       regra15,
                                       regra16, 
                                       regra17,
                                       regra18,
                                       regra19,
                                       regra20,
                                       regra21,
                                       regra22,
                                       regra23,
                                       regra24,
                                       regra25,
                                       regra26,
                                       regra27,
                                       regra28,
                                       regra29,
                                       regra30,
                                       regra31,
                                       regra32,
                                       regra33,
                                       regra34,
                                       regra35,
                                       regra36,
                                       regra37,
                                       regra38,
                                       regra39,
                                       regra40,
                                       regra41,
                                       regra42,
                                       regra43,
                                       regra44
                                       ])
    sistema = ctrl.ControlSystemSimulation(sistema_controle)

    # 0 - Não há, 1 - Há
    sistema.input['engulfing'] = 1
    # 0 - Não há, 1 - Há
    sistema.input['dragonfly'] = 0
    # 0 - Não há, 1 - Há
    sistema.input['doji'] = 0
    # 0 - Não há, 1 - Há
    sistema.input['harami'] = 0
    # 0 - Não há, 1 - Há
    sistema.input['martelo'] = 0
    # 0 - Não há, 1 - Há
    sistema.input['martelo_invertido'] = 0
    # Qualquer valor entre 0 a 10, sendo 0 uma média totalmente para baixo, e 10 totalmente para cima
    sistema.input['media_movel'] = 6
    # Qualquer valor entre 0 a 10, sendo 0 uma média totalmente para baixo, e 10 totalmente para cima
    sistema.input['ema'] = 6
    # Qualquer valor entre 0 a 10, sendo 0 totalmente em sobrevenda, e 10 totalmente em sobrecompra
    sistema.input['rsi'] = 6
    # Qualquer valor entre 0 e 10, sendo 0 um fundo absoluto e 10 um topo absoluto
    sistema.input['posicao'] = 2

    try:
        sistema.compute()
        result = sistema.output['previsao']
        res = {}
        res['venda'] = fuzz.interp_membership(previsao.universe, previsao['venda'].mf, result)
        res['manter'] = fuzz.interp_membership(previsao.universe, previsao['manter'].mf, result)
        res['compra'] = fuzz.interp_membership(previsao.universe, previsao['compra'].mf, result)

        print("Valor da previsão: \t" + str(result))
        print("Pertinencia Venda: \t" + str(res['venda']))
        print("Pertinencia Manter: \t" + str(res['manter']))
        print("Pertinencia Compra: \t" + str(res['compra']))    
        print("Indicação: \t\t" + max(res, key=res.get))

        previsao.view(sim=sistema)
        plt.show()
    except ValueError:
        print('O sistema é esparso demais. Não nenhuma regra que possa relacionar os inputs dados')
        print('Indicação: \t\t manter')
        sys.exit()
    

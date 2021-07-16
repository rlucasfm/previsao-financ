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
    engolfo = ctrl.Antecedent(uni3, 'engolfo')    
    dragonfly = ctrl.Antecedent(uni3, 'dragonfly')    
    doji = ctrl.Antecedent(uni2, 'doji')    
    pinca = ctrl.Antecedent(uni2, 'pinca')    
    martelo = ctrl.Antecedent(uni3, 'martelo')

    mediamovel = ctrl.Antecedent(universe, 'media_movel')
    posicao = ctrl.Antecedent(universe, 'posicao')

    # -------------- DEFINIÇÃO DO CONSEQUENTE --------------
    print('Definindo o consequente...')
    previsao = ctrl.Consequent(np.arange(0, 101, 1), 'previsao')    

    # -------------- DEFINIÇÃO DAS FUNÇÕES DE PERTINÊNCIA --------------
    print('Definindo as funcoes de pertinencia...')
    engolfo['nao'] = fuzz.trimf(engolfo.universe, [-0.01, 0, 0.01])
    engolfo['baixa'] = fuzz.trimf(engolfo.universe, [0.99, 1, 1.01]) 
    engolfo['alta'] = fuzz.trimf(engolfo.universe, [1.99, 2, 2.01])

    dragonfly['nao'] = fuzz.trimf(dragonfly.universe, [-0.01, 0, 0.01])
    dragonfly['comum'] = fuzz.trimf(dragonfly.universe, [0.99, 1, 1.01]) 
    dragonfly['gravestone'] = fuzz.trimf(dragonfly.universe, [1.99, 2, 2.01])

    doji['nao'] = fuzz.trimf(doji.universe, [-0.01, 0, 0.01])
    doji['sim'] = fuzz.trimf(doji.universe, [0.99, 1, 1.01]) 

    pinca['nao'] = fuzz.trimf(pinca.universe, [-0.01, 0, 0.01])
    pinca['sim'] = fuzz.trimf(pinca.universe, [0.99, 1, 1.01]) 

    martelo['nao'] = fuzz.trimf(martelo.universe, [-0.01, 0, 0.01])
    martelo['comum'] = fuzz.trimf(martelo.universe, [0.99, 1, 1.01]) 
    martelo['invertido'] = fuzz.trimf(martelo.universe, [1.99, 2, 2.01])
    
    mediamovel['Baixa'] = fuzz.trimf(mediamovel.universe, [-0.01, 0, 5])
    mediamovel['Alta'] = fuzz.trimf(mediamovel.universe, [5, 10, 11])

    posicao['Fundo'] = fuzz.trimf(posicao.universe, [-0.01, 0, 5])
    posicao['Topo'] = fuzz.trimf(posicao.universe, [5, 10, 11])    

    previsao['venda'] = fuzz.sigmf(previsao.universe, 20, -0.2)
    previsao['manter'] = fuzz.gaussmf(previsao.universe, 50, 15)
    previsao['compra'] = fuzz.sigmf(previsao.universe, 80, 0.2)    
    
    # -------------- Descomente isto caso queira observar as funções de pertinência --------------
    # engolfo.view()
    # dragonfly.view()
    # doji.view()
    # pinca.view()
    # martelo.view()
    # mediamovel.view()
    # posicao.view()   
    # previsao.view()     

    # -------------- DEFINIÇÃO DAS REGRAS --------------
    print('Definindo as regras...')
    regra1 = ctrl.Rule(engolfo['alta']                      & mediamovel['Alta']                        , previsao['compra'])
    regra2 = ctrl.Rule(engolfo['baixa']                     & mediamovel['Baixa']                       , previsao['venda'])
    regra3 = ctrl.Rule(doji['sim']                          & posicao['Fundo']                          , previsao['compra'])
    regra4 = ctrl.Rule(doji['sim']                          & posicao['Topo']                           , previsao['venda'])
    regra5 = ctrl.Rule(dragonfly['comum']                   & posicao['Fundo']                          , previsao['compra'])
    regra6 = ctrl.Rule(dragonfly['gravestone']              & posicao['Topo']                           , previsao['venda'])
    regra7 = ctrl.Rule(martelo['invertido']                 & mediamovel['Alta']    & posicao['Fundo']  , previsao['compra'])
    regra8 = ctrl.Rule(martelo['comum']                     & mediamovel['Baixa']   & posicao['Topo']   , previsao['venda'])
    regra9 = ctrl.Rule(pinca['sim']                         & posicao['Fundo']                          , previsao['venda'])
    regra10= ctrl.Rule(pinca['sim']                         & posicao['Topo']                           , previsao['compra'])
    

    sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9, regra10])
    sistema = ctrl.ControlSystemSimulation(sistema_controle)

    # Inputs aceita um array numpy ou um valor inteiro
    sistema.input['engolfo'] = 0
    sistema.input['dragonfly'] = 0
    sistema.input['doji'] = 0
    sistema.input['pinca'] = 0
    sistema.input['martelo'] = 2
    sistema.input['media_movel'] = 7
    sistema.input['posicao'] = 2

    try:
        sistema.compute()        
    except ValueError:
        print('O sistema é esparso demais. Não há nenhuma regra que possa relacionar os inputs dados')
        sys.exit()

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

    # previsao.view(sim=sistema)
    # plt.show()
    

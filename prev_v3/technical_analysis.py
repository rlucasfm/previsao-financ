import sys
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

class FuzzyObject:
    def __init__(self, engulfing, dragonflydoji, doji, harami, hammer, invertedhammer, sma, rsi, ema, posicao):
        self.input = {}
        self.input['engulfing'] = engulfing
        self.input['dragonflydoji'] = dragonflydoji
        self.input['doji'] = doji
        self.input['harami'] = harami
        self.input['hammer'] = hammer
        self.input['invertedhammer'] = invertedhammer
        self.input['sma'] = sma
        self.input['rsi'] = rsi
        self.input['ema'] = ema
        self.input['posicao'] = posicao
        
        self.define_dataset()
        self.define_rules()

    def define_dataset(self):
        universe = np.arange(0, 100.01, 0.01)
        # uni3 = np.arange(0, 2.1, 0.01)
        uni2 = np.arange(0, 1.1, 0.01)

        # -------------- DEFINIÇÃO DE ANTECEDENTES --------------
        print('Definindo os antecedentes...')        
        self.engulfing = ctrl.Antecedent(uni2, 'engulfing')
        self.dragonflydoji = ctrl.Antecedent(uni2, 'dragonflydoji')    
        self.doji = ctrl.Antecedent(uni2, 'doji')    
        self.harami = ctrl.Antecedent(uni2, 'harami')    
        self.hammer = ctrl.Antecedent(uni2, 'hammer')
        self.invertedhammer = ctrl.Antecedent(uni2, 'invertedhammer')

        self.sma = ctrl.Antecedent(universe, 'sma')
        self.rsi = ctrl.Antecedent(universe, 'rsi')
        self.ema = ctrl.Antecedent(universe, 'ema')
        self.posicao = ctrl.Antecedent(universe, 'posicao')

        # -------------- DEFINIÇÃO DO CONSEQUENTE --------------
        print('Definindo o consequente...')
        self.previsao = ctrl.Consequent(np.arange(0, 101, 1), 'previsao')
        
        # ------ DEFINIÇÃO DO THRESHOLD DE AGRESSIVIDADE -------
        threshold = 3

        # -------------- DEFINIÇÃO DAS FUNÇÕES DE PERTINÊNCIA --------------
        print('Definindo as funcoes de pertinencia...')
        self.engulfing['baixa'] = fuzz.trimf(self.engulfing.universe, [-0.01, 0, 0.01])
        self.engulfing['nao'] = fuzz.trimf(self.engulfing.universe, [0.49, 0.5, 0.51])   
        self.engulfing['alta'] = fuzz.trimf(self.engulfing.universe, [0.99, 1, 1.01])   

        self.dragonflydoji['nao'] = fuzz.trimf(self.dragonflydoji.universe, [-0.01, 0, 0.01])
        self.dragonflydoji['sim'] = fuzz.trimf(self.dragonflydoji.universe, [0.99, 1, 1.01]) 

        self.doji['nao'] = fuzz.trimf(self.doji.universe, [-0.01, 0, 0.01])
        self.doji['sim'] = fuzz.trimf(self.doji.universe, [0.99, 1, 1.01]) 

        self.harami['baixa'] = fuzz.trimf(self.harami.universe, [-0.01, 0, 0.01])
        self.harami['nao'] = fuzz.trimf(self.harami.universe, [0.49, 0.5, 0.51])
        self.harami['alta'] = fuzz.trimf(self.harami.universe, [0.99, 1, 1.01])

        self.hammer['nao'] = fuzz.trimf(self.hammer.universe, [-0.01, 0, 0.01])
        self.hammer['sim'] = fuzz.trimf(self.hammer.universe, [0.99, 1, 1.01]) 
        
        self.invertedhammer['nao'] = fuzz.trimf(self.invertedhammer.universe, [-0.01, 0, 0.01])
        self.invertedhammer['sim'] = fuzz.trimf(self.invertedhammer.universe, [0.99, 1, 1.01]) 
        
        self.sma['Baixa'] = fuzz.trimf(self.sma.universe, [-0.01, 0, 50])
        self.sma['Alta'] = fuzz.trimf(self.sma.universe, [50, 100, 101])
        
        self.rsi['sobrevenda'] = fuzz.trimf(self.rsi.universe, [-0.01, 0, 50])
        self.rsi['sobrecompra'] = fuzz.trimf(self.rsi.universe, [50, 100, 101])

        self.ema['Baixa'] = fuzz.trimf(self.ema.universe, [-0.01, 0, 50])
        self.ema['Alta'] = fuzz.trimf(self.ema.universe, [50, 100, 101])

        self.posicao['Fundo'] = fuzz.trimf(self.posicao.universe, [-0.01, 0, 50])
        self.posicao['Topo'] = fuzz.trimf(self.posicao.universe, [50, 100, 101])    

        self.previsao['venda'] = fuzz.sigmf(self.previsao.universe, (35 + threshold), -0.2)
        self.previsao['manter'] = fuzz.gaussmf(self.previsao.universe, 50, (15 - threshold))
        self.previsao['compra'] = fuzz.sigmf(self.previsao.universe, (65 - threshold), 0.2)
    
    
    def print_dataset(self):
    #    self.engulfing.view()
    #    self.dragonflydoji.view()
    #    self.doji.view()
    #    self.harami.view()
    #    self.hammer.view()
    #    self.invertedhammer.view()
       self.sma.view()
       self.rsi.view()
       self.ema.view()
       self.posicao.view()   
    #    self.previsao.view()
    
       plt.show()
       
    def define_rules(self):
        # -------------- DEFINIÇÃO DAS REGRAS --------------
        print('Definindo as regras...')
        regra1 = ctrl.Rule(self.engulfing['alta']           & self.sma['Alta']                                      , self.previsao['compra'])
        regra2 = ctrl.Rule(self.engulfing['baixa']          & self.sma['Baixa']                                     , self.previsao['venda'])
        regra3 = ctrl.Rule(self.doji['sim']                                             & self.posicao['Fundo']     , self.previsao['compra'])
        regra4 = ctrl.Rule(self.doji['sim']                                             & self.posicao['Topo']      , self.previsao['venda'])
        regra5 = ctrl.Rule(self.dragonflydoji['sim']                                    & self.posicao['Fundo']     , self.previsao['compra'])    
        regra6 = ctrl.Rule(self.invertedhammer['sim']       & self.sma['Alta']          & self.posicao['Fundo']     , self.previsao['compra'])
        regra7 = ctrl.Rule(self.hammer['sim']               & self.sma['Baixa']         & self.posicao['Topo']      , self.previsao['venda'])
        regra8 = ctrl.Rule(self.harami['alta']                                           & self.posicao['Fundo']     , self.previsao['compra'])
        regra9 = ctrl.Rule(self.harami['baixa']                                           & self.posicao['Topo']      , self.previsao['venda'])
        regra10= ctrl.Rule(                                                             self.posicao['Topo']        , self.previsao['venda'])
        regra11= ctrl.Rule(                                                             self.posicao['Fundo']       , self.previsao['compra'])
        regra12= ctrl.Rule(                                 self.sma['Alta']                                        , self.previsao['compra'])
        regra13= ctrl.Rule(                                 self.sma['Baixa']                                       , self.previsao['venda'])
        # Regras com SMA        
        regra14= ctrl.Rule(                                 ~self.posicao['Topo']       & ~self.posicao['Fundo']    , self.previsao['manter'])
        regra15= ctrl.Rule(                                 ~self.sma['Alta']           & ~self.sma['Baixa']        , self.previsao['manter'])
        regra16= ctrl.Rule(                                 self.sma['Alta']            & self.posicao['Topo']      , self.previsao['manter'])
        regra17= ctrl.Rule(                                 self.sma['Baixa']           & self.posicao['Fundo']     , self.previsao['manter'])
        regra18 = ctrl.Rule(self.engulfing['alta']          & self.sma['Alta']          & self.posicao['Fundo']     , self.previsao['compra'])
        regra19 = ctrl.Rule(self.engulfing['baixa']         & self.sma['Baixa']         & self.posicao['Topo']      , self.previsao['venda'])
        regra20 = ctrl.Rule(self.doji['sim']                & self.posicao['Fundo']     & self.sma['Alta']          , self.previsao['compra'])
        regra21 = ctrl.Rule(self.doji['sim']                & self.posicao['Topo']      & self.sma['Baixa']         , self.previsao['venda'])
        regra22 = ctrl.Rule(self.dragonflydoji['sim']       & self.posicao['Fundo']     & self.sma['Alta']          , self.previsao['compra'])
        regra23 = ctrl.Rule(self.harami['alta']             & self.posicao['Fundo']     & self.sma['Alta']          , self.previsao['compra'])
        regra24 = ctrl.Rule(self.harami['baixa']            & self.posicao['Topo']      & self.sma['Baixa']         , self.previsao['venda'])
        # Regras com EMA
        regra25= ctrl.Rule(                                 ~self.ema['Alta']           & ~self.ema['Baixa']        , self.previsao['manter'])
        regra26= ctrl.Rule(                                 self.ema['Alta']            & self.posicao['Topo']      , self.previsao['manter'])
        regra27= ctrl.Rule(                                 self.ema['Baixa']           & self.posicao['Fundo']     , self.previsao['manter'])
        regra28 = ctrl.Rule(self.engulfing['alta']          & self.ema['Alta']          & self.posicao['Fundo']     , self.previsao['compra'])
        regra29 = ctrl.Rule(self.engulfing['baixa']         & self.ema['Baixa']         & self.posicao['Topo']      , self.previsao['venda'])
        regra30 = ctrl.Rule(self.doji['sim']                & self.posicao['Fundo']     & self.ema['Alta']          , self.previsao['compra'])
        regra31 = ctrl.Rule(self.doji['sim']                & self.posicao['Topo']      & self.ema['Baixa']         , self.previsao['venda'])
        regra32 = ctrl.Rule(self.dragonflydoji['sim']       & self.posicao['Fundo']     & self.ema['Alta']          , self.previsao['compra'])
        regra33 = ctrl.Rule(self.harami['alta']             & self.posicao['Fundo']     & self.ema['Alta']          , self.previsao['compra'])
        regra34 = ctrl.Rule(self.harami['baixa']            & self.posicao['Topo']      & self.ema['Baixa']         , self.previsao['venda'])
        # Regras com RSI
        regra35= ctrl.Rule(                                 ~self.rsi['sobrevenda']     & ~self.rsi['sobrecompra']  , self.previsao['manter'])
        regra36= ctrl.Rule(                                 self.rsi['sobrecompra']     & self.posicao['Topo']      , self.previsao['venda'])
        regra37= ctrl.Rule(                                 self.rsi['sobrevenda']      & self.posicao['Fundo']     , self.previsao['compra'])
        regra38 = ctrl.Rule(self.engulfing['alta']          & self.rsi['sobrevenda']    & self.posicao['Fundo']     , self.previsao['compra'])
        regra39 = ctrl.Rule(self.engulfing['baixa']         & self.rsi['sobrecompra']   & self.posicao['Topo']      , self.previsao['venda'])
        regra40 = ctrl.Rule(self.doji['sim']                & self.posicao['Fundo']     & self.rsi['sobrevenda']    , self.previsao['compra'])
        regra41 = ctrl.Rule(self.doji['sim']                & self.posicao['Topo']      & self.rsi['sobrecompra']   , self.previsao['venda'])
        regra42 = ctrl.Rule(self.dragonflydoji['sim']       & self.posicao['Fundo']     & self.rsi['sobrevenda']    , self.previsao['compra'])
        regra43 = ctrl.Rule(self.harami['alta']             & self.posicao['Fundo']     & self.rsi['sobrevenda']    , self.previsao['compra'])
        regra44 = ctrl.Rule(self.harami['baixa']            & self.posicao['Topo']      & self.rsi['sobrecompra']   , self.previsao['venda'])


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
        self.sistema = ctrl.ControlSystemSimulation(sistema_controle)
        
    def compute_results(self):
        # 0 - Baixa, 0.5 - Não há, 1 - Alta 
        self.sistema.input['engulfing'] = self.input['engulfing']
        # 0 - Não há, 1 - Há
        self.sistema.input['dragonflydoji'] = self.input['dragonflydoji']
        # 0 - Não há, 1 - Há
        self.sistema.input['doji'] = self.input['doji']
        # 0 - Baixa, 0.5 - Não há, 1 - Alta 
        self.sistema.input['harami'] = self.input['harami']
        # 0 - Não há, 1 - Há
        self.sistema.input['hammer'] = self.input['hammer']
        # 0 - Não há, 1 - Há
        self.sistema.input['invertedhammer'] = self.input['invertedhammer']
        # Qualquer valor entre 0 a 10, sendo 0 uma média totalmente para baixo, e 10 totalmente para cima
        self.sistema.input['sma'] = self.input['sma']
        # Qualquer valor entre 0 a 10, sendo 0 uma média totalmente para baixo, e 10 totalmente para cima
        self.sistema.input['ema'] = self.input['ema']
        # Qualquer valor entre 0 a 10, sendo 0 totalmente em sobrevenda, e 10 totalmente em sobrecompra
        self.sistema.input['rsi'] = self.input['rsi']
        # Qualquer valor entre 0 e 10, sendo 0 um fundo absoluto e 10 um topo absoluto
        self.sistema.input['posicao'] = self.input['posicao']

        try:
            self.sistema.compute()
            result = self.sistema.output['previsao']
            res = {}
            res['venda'] = fuzz.interp_membership(self.previsao.universe, self.previsao['venda'].mf, result)
            res['manter'] = fuzz.interp_membership(self.previsao.universe, self.previsao['manter'].mf, result)
            res['compra'] = fuzz.interp_membership(self.previsao.universe, self.previsao['compra'].mf, result)

            print("Valor da previsão: \t" + str(result))
            print("Pertinencia Venda: \t" + str(res['venda']))
            print("Pertinencia Manter: \t" + str(res['manter']))
            print("Pertinencia Compra: \t" + str(res['compra']))    
            print("Indicação: \t\t" + max(res, key=res.get))
            
        except ValueError:
            print('O sistema é esparso demais. Não nenhuma regra que possa relacionar os inputs dados')
            print('Indicação: \t\t manter')
            sys.exit()
    
    def print_results(self):
        self.previsao.view(sim=self.sistema)
        plt.show()
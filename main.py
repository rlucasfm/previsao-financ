import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl


if __name__ == "__main__":
    universe = np.arange(0, 11, 1)

    print('Definindo os antecedentes...')
    qualidade = ctrl.Antecedent(universe, 'qualidade')
    servico = ctrl.Antecedent(universe, 'servico')
    print('Definindo o consequente...')
    gorjeta = ctrl.Consequent(np.arange(0, 21, 1), 'gorjeta')

    print('Definindo as variáveis linguísticas...')
    qualidade.automf(number=3, names=['ruim', 'boa', 'saborosa'])
    servico.automf(number=3, names=['ruim', 'aceitável', 'ótimo'])

    print('Definindo as funções de pertinência...')
    gorjeta['baixa'] = fuzz.sigmf(gorjeta.universe, 5, -1)
    gorjeta['media'] = fuzz.gaussmf(gorjeta.universe, 10, 3)
    gorjeta['alta'] = fuzz.pimf(gorjeta.universe, 10, 20, 25, 50)    

    # gorjeta.view()
    # input('Enter')

    print('Definindo as regras...')
    regra1 = ctrl.Rule(qualidade['ruim'] | servico['ruim'], gorjeta['baixa'])
    regra2 = ctrl.Rule(servico['aceitável'], gorjeta['media'])
    regra3 = ctrl.Rule(qualidade['saborosa'] | servico['ótimo'], gorjeta['alta'])

    sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])
    sistema = ctrl.ControlSystemSimulation(sistema_controle)

    sistema.input['qualidade'] = 9
    sistema.input['servico'] = 8
    sistema.compute()

    print(sistema.output['gorjeta'])
    gorjeta.view(sim=sistema)
    input('Enter')
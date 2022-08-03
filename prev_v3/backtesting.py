from main import main
from utils import random_date
from datetime import datetime

class Backtester:
    def __init__(self):
        self.sucessos = 0
        self.fracassos = 0 
        self.indiferente = 0      
    
    def check_result(self, data, point, indication):
        if(indication == 'compra'):
            if(data['Close'][point] < data['Close'][point+1] or data['Close'][point] < data['Close'][point+2]):
                self.sucessos += 1
                return 'Sucesso!'
            else:
                self.fracassos += 1
                return 'Fracasso!'
        elif(indication == 'venda'):
            if(data['Close'][point] > data['Close'][point+1] or data['Close'][point] > data['Close'][point+2]):
                self.sucessos += 1
                return 'Sucesso!'
            else:
                self.fracassos += 1
                return 'Fracasso!'
        else:
            self.indiferente += 1
            return 'Indiferente...'

if __name__ == "__main__":
    backtester = Backtester()
    attempts = 500
    for i in range(attempts):
        while True:
            try:
                rnd_date = random_date('2016-07-29', '2022-07-29')
                results = main(rnd_date, 60, True)
                # print(results['resultados']['indicacao'])
                print(backtester.check_result(results['dados_selecionados'], results['ponto_analise'], results['resultados']['indicacao']))                
                break                
            except Exception as err:
                # print(err)
                continue
            
    print('Sucessos: '+str(backtester.sucessos))
    print('Fracassos: '+str(backtester.fracassos))
    print('Indiferente: '+str(backtester.indiferente))
    
    f = open('log.txt', 'a')
    hoje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sucesso_percent = backtester.sucessos/attempts*100
    fracassos_percent = backtester.fracassos/attempts*100
    indiferente_percent = backtester.indiferente/attempts*100    
    positivos_percent = sucesso_percent + indiferente_percent
    
    f.write(f' \n--------- TESTE {hoje} ---------\n \
                Tentativas: {attempts}\n \
                Sucessos: {backtester.sucessos}\n \
                Fracassos: {backtester.fracassos}\n \
                Indiferente: {backtester.indiferente}\n \
                Sucesso %: {sucesso_percent}\n \
                Fracassos %: {fracassos_percent}\n \
                Indiferente %: {indiferente_percent}\n \
                Positivos %: {positivos_percent}\n \
            ')
    f.close()
    

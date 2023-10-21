from flask import Flask, request, jsonify
from requests import get
from re import findall
from itertools import permutations
from time import sleep as sl, strftime as time
from math import pi, sqrt
import os

hora = time('%H')
app = Flask(__name__)
jogos = {'mega sena': {'sequencias': [], 'tamanho': 6, 'maior_numero': 60, 'download': 'https://asloterias.com.br/lista-de-resultados-da-mega-sena'},
         'lotofacil': {'sequencias': [], 'tamanho': 15, 'maior_numero': 25,'download': 'https://asloterias.com.br/lista-de-resultados-da-lotofacil'},
         'dupla sena': {'sequencias': [], 'tamanho': 6, 'maior_numero': 50,'download': 'https://asloterias.com.br/lista-de-resultados-da-dupla-sena'},
         'quina': {'sequencias': [], 'tamanho': 5, 'maior_numero': 80,'download': 'https://asloterias.com.br/lista-de-resultados-da-quina'},
         'dia de sorte': {'sequencias': [], 'tamanho': 7, 'maior_numero': 31,'download': 'https://asloterias.com.br/lista-de-resultados-da-dia-de-sorte'},
         'lotomania': {'sequencias': [], 'tamanho': 20, 'maior_numero': 99,'download': 'https://asloterias.com.br/lista-de-resultados-da-lotomania'},
         'timemania': {'sequencias': [], 'tamanho': 7, 'maior_numero': 80,'download': 'https://asloterias.com.br/lista-de-resultados-da-timemania'},}

def atualizar_jogos():
    try:
        global jogos

        print('iniciando a atualização dos jogos')
        for sequencia, var in jogos.items():
            while True:
                try:
                    r = get(var['download']).text
                    break
                except:
                    pass

            regex = '\d\d'
            for x in range(1, var['tamanho']):
                regex += ' \d\d'

            sequencias = list(map(lambda string: [int(n) for n in string.split(' ')], findall(f'({regex})', r)))
            jogos[sequencia]['sequencias'] = sequencias
        print('atualização dos jogos feita')
    except:
        return True # retornando erro como True

def somaunidades(seq):
    try:
        soma = 0

        for num in seq:
            if len(str(num)) == 2:
                soma += int(str(num)[0])
                soma += int(str(num)[1])
            else:
                soma += int(num)

        return soma
    except:
        try:
            return soma
        except:
            return 0

def resultadonumeros(sequencia, jogo):
    try:
        global jogos
        
        lista1 = list(range(1, jogos[jogo]['maior_numero']+1))
        lista2 = []
        texto = ''

        for seq in sequencia:
            for num in seq:
                if num in lista1:
                    lista1.pop(lista1.index(num))
                    lista2.append(num)
        
        lista2 = sorted(lista2)

        if lista1 != []:
            texto += f'\nos numeros que não apareceram foram:\n{str(lista1)[1:-1]}'
        else:
            texto += f'todos os numeros apareceram'
        if lista2 != []:
            texto += f'\n\nos numeros que apareceram foram:\n{str(lista2)[1:-1]}'
        else:
            texto += f'todos os numeros não apareceram'
        
        return texto
    except:
        try:
            return texto
        except:
            return ''

def numerointeiro(seq): # verifica se a entrada esta correta
    try:
        int(seq)
        if len(seq.split(' ')) != 1:
            return 'coloque um numero inteiro para a verificação.\nex:\n25\n45\n32'
        else:
            return False # retorna false como tudo certo
    except:
        return 'coloque um numero inteiro para a verificação.\nex:\n25\n45\n32'
    
def numerosequencia(seq, jogo): # verifica se a entrada esta correta
    global jogos
    try:
        try:
            seq = [int(x) for x in seq.split(', ')]
        except:
            try:
                seq = [int(x) for x in seq.split(' ')]
            except:
                return 'coloque uma sequencia para a verificação.\nex:\n01 02 03 04 05 06\n01 10 15 20 25 30'
        if len(seq) < 3:
            return 'coloque uma sequencia para a verificação.\nex:\n01 02 03 04 05 06\n01 10 15 20 25 30'
        else:
            return False # retorna false como tudo certo
    except:
        return 'coloque uma sequencia para a verificação.\nex:\n01 02 03 04 05 06\n01 10 15 20 25 30'

def num_sequencia(seq, jogo):
    jogos[jogo]['sequencias'].reverse()
    num = jogos[jogo]['sequencias'].index(seq) + 1
    jogos[jogo]['sequencias'].reverse()
    return num

@app.route("/", methods=['GET'])
def teste():
    return 'funcionando!'

@app.route('/concursos', methods=['GET'])
def concursos():
    global jogos

    concurso = request.args.get('concurso')

    return jsonify(jogos[concurso]['sequencias'])

@app.route('/primeiro_concurso', methods=['GET'])
def primeiro_concurso():
    global jogos

    concurso = request.args.get('concurso')

    return jsonify(jogos[concurso]['sequencias'][0])

@app.route("/ferramenta", methods=['GET'])
def main():
    try:
        global hora
        global jogos

        if hora != time('%H'):
            hora = time('%H')
            r = atualizar_jogos()
            if r:
                return 'erro na atualização dos dados. Chame o desenvolvedor!'

        jogo = request.args.get('jogo')
        ferramenta = request.args.get('ferramenta')
        sequencia = request.args.get('sequencia')

        if jogo == '':
            return 'escolha um jogo para que a verificação possa ser feita'
        elif ferramenta == '':
            return 'escolha uma ferramenta para que a verificação possa ser feita'
        elif sequencia == '':
            return 'escolha uma sequencia para que a verificação possa ser feita'

        # return f'o jogo escolhido foi {jogo}, a ferramenta foi: {ferramenta} e a sequencia digitada foi: {sequencia}'
    except:
        return 'ouve um erro inesperado no recebimento dos dados. Por favor. Contate o dono do site.'

    try:
        if ferramenta == 'soma de unidades iguais':
            try:
                r = numerointeiro(sequencia)
                if r:
                    return r

                listaiguais = [] # criando as variaveis
                texto = 'as sequencias com soma das unidades iguais foram:\n[hr]\n'
                
                sequencias = jogos[jogo]['sequencias'] # verificando o jogo

                for seq in sequencias:
                    if somaunidades(seq) == int(sequencia):
                        listaiguais.append(seq)
                
                if len(listaiguais) != 0:
                    for igual in listaiguais: # criando a resposta
                        for num in igual:
                            texto += f'{num} '
                        texto+='\n[hr]\n'

                    texto += resultadonumeros(listaiguais, jogo)

                else:
                    return 'nenhuma sequencia deu a mesma soma das unidades!' # caso não aja nenhuma

                return texto # retornando a resposta
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'
            
        elif ferramenta == 'soma de dezenas iguais':
            try:
                r = numerointeiro(sequencia)
                if r:
                    return r

                listaiguais = [] # criando as variaveis
                texto = 'as sequencias com soma das dezenas iguais foram:\n[hr]\n'
                
                sequencias = jogos[jogo]['sequencias'] # verificando o jogo

                for seq in sequencias:
                    if sum(seq) == int(sequencia):
                        listaiguais.append(seq)
                
                if len(listaiguais) != 0:
                    for igual in listaiguais: # criando a resposta
                        for num in igual:
                            texto += f'{num} '
                        texto+='\n[hr]\n'

                    texto += resultadonumeros(listaiguais, jogo)

                else:
                    return 'nenhuma sequencia deu a mesma soma das unidades!' # caso não aja nenhuma

                return texto # retornando a resposta
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'

        elif ferramenta == '3 numeros ou mais':
            try:
                r = numerosequencia(sequencia, jogo)
                if r:
                    return r
                
                try:
                    sequencia = [int(x) for x in sequencia.split(', ')]
                except:
                    try:
                        sequencia = [int(x) for x in sequencia.split(' ')]
                    except:
                        return 'erro na sequencia inserida'

                if len(sequencia) < 3:
                    return 'coloque uma sequencia maior que 3 numeros'

                listinha = []
                texto = 'as sequencias que tiveram numeros iguais foram:\n[hr]\n' # [color=#ff0000] aaaaaa [/color]

                for seq in jogos[jogo]['sequencias']:
                    cont = 0
                    for n in seq:
                        if n in sequencia:
                            cont += 1
                        if cont == 3:
                            listinha.append(seq)
                            break
                
                if listinha != []:
                    for seq in listinha:
                        texto += f'concurso: {num_sequencia(seq, jogo)} - '
                        for n in seq:
                            if n in sequencia:
                                texto += f'[color=#ff0000]{n}[/color] '
                            else:
                                texto += f'{n} '
                        texto += '\n[hr]\n'

                    texto += resultadonumeros(listinha, jogo)

                    return texto
                else:
                    return 'nenhuma sequencia teve seus numeros aparecendo mais que 3 vezes sobre os numeros escolhidos.'

            except Exception as error:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'

        elif ferramenta == 'numeros anteriores':
            try:
                r = numerointeiro(sequencia)
                if r:
                    return r

                texto = f'os numeros que vieram antes do numero {sequencia} foram:\n'
                lista = []
                dic = {}

                for seq in jogos[jogo]['sequencias']:
                    if int(sequencia) in seq:
                        if seq.index(int(sequencia)) != 0:

                            if seq[seq.index(int(sequencia)) -1] not in dic:
                                dic[seq[seq.index(int(sequencia)) -1]] = 1
                            else:
                                dic[seq[seq.index(int(sequencia)) -1]] += 1

                            if seq[seq.index(int(sequencia)) -1] not in lista:
                                lista.append(seq[seq.index(int(sequencia)) -1])

                for n, r in dic.items():
                    texto += f'{n} apareceu {r} vezes;\n'
                texto = texto[:-2]+'.\n'

                texto += resultadonumeros([lista], jogo)

                return texto
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'

        elif ferramenta == 'proximos numeros':
            try:
                r = numerointeiro(sequencia)
                if r:
                    return r

                texto = f'os numeros que vieram depois do numero {sequencia} foram:\n'
                lista = []
                dic = {}

                for seq in jogos[jogo]['sequencias']:
                    if int(sequencia) in seq:
                        if seq.index(int(sequencia)) != jogos[jogo]['tamanho'] -1:

                            if seq[seq.index(int(sequencia)) +1] not in dic:
                                dic[seq[seq.index(int(sequencia)) +1]] = 1
                            else:
                                dic[seq[seq.index(int(sequencia)) +1]] += 1

                            if seq[seq.index(int(sequencia)) +1] not in lista:
                                lista.append(seq[seq.index(int(sequencia)) +1])

                for n, r in dic.items():
                    texto += f'{n} apareceu {r} vezes;\n'
                texto = texto[:-2]+'.\n'

                texto += resultadonumeros([lista], jogo)

                return texto
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'

        elif ferramenta == 'semelhantes':
            try:
                r = numerosequencia(sequencia, jogo)
                if r:
                    return r

                texto = 'os numeros que não tiveram semelhança foram:\n'
                lista = [*range(1, jogos[jogo]['maior_numero']+1)]

                [lista.remove(int(f'{x[0]}{x[1]}')) if int(f'{x[0]}{x[1]}') in lista else None for x in list(permutations([int(x) for x in sequencia.split(' ')], 2))]
                [lista.remove(int(x)) if int(x) in lista else None for x in sequencia.split(' ')]

                for n in lista:
                    texto += f'{n}, '
                
                texto = texto[:-2]+'\n'

                texto += resultadonumeros([lista], jogo)

                return texto
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'

        elif ferramenta == 'raio':
            try:
                r = numerointeiro(sequencia)
                if r:
                    return r
                
                num = str(pi * int(sequencia)).replace('.', '')
                n = 0
                lista_pi = []
                lista = list(range(1, 61))

                while True:
                    try:
                        lista_pi.append(int(f'{num[n]}{num[n+1]}'))
                        n+=2
                    except:
                        break

                for x in lista_pi:
                    y = x
                    while True:
                        if y > 60:
                            y -= 60
                            if y < 60:
                                lista_pi.append(y)
                                lista_pi.remove(x)
                                break
                        else:
                            break

                [lista.remove(x) if x in lista else None for x in lista_pi]

                texto = f'os numeros sem o raio do numero {sequencia} foram:\n'
                for n in lista:
                    texto+=f'{n}, '

                texto = texto[:-2]+'\n'
                texto += resultadonumeros([lista], jogo)

                return texto
            
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'

        elif ferramenta == 'raiz':
            try:
                r = numerointeiro(sequencia)
                if r:
                    return r
                
                num = str(sqrt(int(sequencia))).replace('.', '')

                n = 0
                lista_sqrt = []
                lista = list(range(1, 61))

                while True:
                    try:
                        lista_sqrt.append(int(f'{num[n]}{num[n+1]}'))
                        n+=2
                    except:
                        break

                for x in lista_sqrt:
                    y = x
                    while True:
                        if y > 60:
                            y -= 60
                            if y < 60:
                                lista_sqrt.append(y)
                                lista_sqrt.remove(x)
                                break
                        else:
                            break

                [lista.remove(x) if x in lista else None for x in lista_sqrt]

                texto = f'os numeros sem a raiz do numero {sequencia} foram:\n'
                for n in lista:
                    texto+=f'{n}, '

                texto = texto[:-2]+'\n'
                texto += resultadonumeros([lista], jogo)

                return texto
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'

        elif ferramenta == 'intervalos':
            try:
                r = numerointeiro(sequencia)
                if r:
                    return r
                
                sequencia = int(sequencia)

                primeiro = 0
                contagem = False
                intervalos = {}
                intervalo = 0

                for seq in jogos[jogo]['sequencias']:
                    if contagem == False:
                        if sequencia in seq:
                            contagem = True
                            continue
                        else:
                            primeiro += 1
                    else:
                        intervalo += 1
                        if sequencia in seq:
                            if intervalo in intervalos:
                                intervalos[intervalo] += 1
                            else:
                                intervalos[intervalo] = 1
                            intervalo = 0
                
                intervalos_ord = dict(sorted(intervalos.items(), key=lambda item: item[1], reverse=True))
                texto = f'os intervalos de jogos em que o numero {sequencia} apareceu foram:\nultima aparição a {primeiro} jogos\n'
                for chave, valor in intervalos_ord.items():
                    texto+=f'intervalo de {chave} - {valor} vezes.\n'
                return texto
            except:
                return 'ouve um erro inesperado na ferramenta. Contate o dono do site'
    
    except:
        return 'ouve um erro inesperado no processamento dos dados. Contate o criador do site'
    
    return 'algo deu errado, por favor, tente mais tarde.'

if __name__ == "__main__":
    atualizar_jogos()
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))

# https://patrick-siotti-animated-rotary-phone-r6vpvqvgg6jfpq54-5000.preview.app.github.dev/?jogo=[jogo]&ferramenta=[ferramenta]&sequencia=[sequencia]

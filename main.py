import csv
import math
import os


transporteAplicacao = []
# Criar dicionario de produtos
produtos = { 
    1: {
        'nome': 'Celular',
        'peso': 0.5
    },
    2: {
        'nome': 'Geladeira',
        'peso': 60
    },
    3: {
        'nome': 'Freezer',
        'peso': 100
    },
    4: {
        'nome': 'Cadeira',
        'peso': 5.0
    },
    5: {
        'nome': 'Luminária',
        'peso': 0.8
    },
    6: {
        'nome': 'Lavadora de roupa',
        'peso': 120
    },
}

# Ler arquivo csv para ter as distancias
distancias = {}
with open('distancias.csv', newline='') as csvfile:
    arquivo = csv.reader(csvfile, delimiter=';')
    cidades = next(arquivo)  # pula para a primeira célula pegando a lista de cidades
    for cidade in cidades:
        distancias[cidade] = {}  # cria um dicionário para cada cidade
    for i, linha in enumerate(arquivo): # cada linha no arquivo
        for j, coluna in enumerate(linha): # cada coluna na linha
            distancias[cidades[i]][cidades[j]] = int(coluna)

def menu_principal():
    os.system("cls")
    opcao = ''
    while(True):
        print('1 - Consultar trechos e modalidades')
        print("2 - Cadastrar transporte")
        print("3 - Dados estatíticos")
        print("0 - Finalizar programa")
        try:
            opcao = int(input("Digite o número da operação que deseja realizar: "))
        except:
            print('Resposta inválida, digite um numero válido: 0-3')
        if opcao == 1 or opcao == 2:
            menu_cidades(opcao)
        if opcao == 3:
            estatisticas()
        if opcao == 0:
            exit()
        
def menu_cidades(opcao):
    os.system("cls")
    for i, cidade in enumerate(cidades):
        print(f'{i} - {cidade}')
        
    while (True):
        try:
            localPartida = int(input('Digite o número da cidade de partida: '))
        except:
            print('Digite, lembrando que deve ser digitado um número de 1 a 23.')
            continue
        if localPartida < 0 or localPartida > 23:
            print('Digite novamente, os números devem ser de 1 a 23!')
            continue
        
        localParada = 0
        parada = str(input('Alguma cidade de parada? Digite S ou N: '))
        if (parada == 'S' or parada == 's'):
            try:
                localParada = int(input('Digite a numeração da cidade de parada: '))
            except:
                print(f'Tente novamente!')
                continue
            if localParada < 0 or localParada > 23:
                print('Digite novamente, o número precisa ser de 1-23!')
                continue
            
        try:
            localDestino = int(input('Digite o número da cidade de destino: '))
        except:
            print(f'Digite novamente.')
        if localDestino < 0 or localDestino > 23:
            print(f'Digite novamente.')
            continue
        else:
            break
            
        if (localParada != 0):
            distanciaTotal = distancias[cidades[localPartida]][cidades[localParada]] + distancias[cidades[localParada]][cidades[localDestino]]
        else:
            distanciaTotal = distancias[cidades[localPartida]][cidades[localDestino]]

    if opcao == 1:
        modalidade = menu_modalidades()
        trechos(localPartida, localDestino, localParada, distanciaTotal, modalidade)
    if opcao == 2:
        itensDescarregar = 0
        itens = menu_itens('carregar')
        if (localParada != 0):
            descarga = str(input('Será descarregado algo na parada ? Digite S ou N: '))
            if (descarga == 'S' or descarga == 's'):
                itensDescarregar = menu_itens('descarregar', itens)
        cadastroTransporte(localPartida, localDestino, localParada, distanciaTotal, itens, itensDescarregar)
    
def menu_modalidades():
    modalidade = 0
    while (modalidade < 1 or modalidade > 3):
        print('1 - Pequeno porte')
        print('2 - Médio porte')
        print('3 - Grande Porte')
        
        try: 
            modalidade = int(input('Selecione a modalidade: '))
        except:
            print('Resposta inválida, digite um número de 1-3')
        
    return modalidade
    
def trechos(localPartida, localDestino, localParada, distanciaTotal, modalidade):
    if modalidade == 1:
        valorKm = 4.87
        modalidadeTransporte = "Pequeno porte"
    if modalidade == 2:
        valorKm = 11.92
        modalidadeTransporte = "Médio porte"
    if modalidade == 3:
        valorKm = 27.44
        modalidadeTransporte = "Grande porte"
    precoTrecho = distanciaTotal * valorKm
    print(f'Cidade partida: {cidades[localPartida]}')
    print(f'Cidade de parada: {cidades[localParada]}')
    print(f'Cidade destino: {cidades[localDestino]}')
    print(f'Distância entre as cidades: {distanciaTotal}')
    print(f'Modalidade: {modalidadeTransporte}')
    print(f'Preço por km: R$ {valorKm}')
    print(f'Custo total do transporte: R$ {precoTrecho} ')
    input("Aperta qualquer tecla para continuar: ")
    menu_principal()

def cadastroTransporte(localPartida, localDestino, localParada, distanciaTotal, itens, itensDescarregar):
    os.system("cls")
    pesoTotal = 0
    pesoDescarga = 0
    caminhoesParada = 0
    totalItens = 0
    produtosStr = ''
    produtosDescargaStr = ''
    
    for item in itens:
        pesoTotal += item['peso'] * item['quantidade']
        totalItens += item['quantidade']
        produtosStr = produtosStr + f'{item["nome"]} | {item["quantidade"]}, '
    if (localParada != 0):
        caminhoesParada = calcular_caminhao(pesoTotal, distancias[cidades[localPartida]][cidades[localParada]])

        if itensDescarregar != 0:
            for produto in itensDescarregar:
                pesoDescarga += produto['peso'] * produto['quantidade']
                pesoTotal = pesoTotal - pesoDescarga
                totalItens += produto['quantidade']
                produtosDescargaStr = produtosDescargaStr + f'{produto["nome"]} | {produto["quantidade"]}, '
        caminhoesFinal = calcular_caminhao(pesoTotal, distancias[cidades[localParada]][cidades[localDestino]])
    else:
        caminhoesFinal = calcular_caminhao(pesoTotal, distanciaTotal)

    caminhoesNecessariosParada = ''
    caminhoesNecessariosFinal = ''
    valorTrechoParada = 0
    if (caminhoesParada != 0):
        valorTotal = caminhoesParada[1] + caminhoesFinal[1]
        valorTrechoParada = caminhoesParada[1]
        valorTrecho = caminhoesFinal[1]
        caminhaoParada, quantidadeCaminhaoParada = caminhoesParada[0]
        caminhaoFinal, quantidadeCaminhaoFinal = caminhoesFinal[0]

        caminhoesNecessariosParada = caminhoesNecessariosParada + f'{caminhaoParada} | {quantidadeCaminhaoParada}, '
        caminhoesNecessariosFinal = caminhoesNecessariosFinal + f'{caminhaoFinal} | {quantidadeCaminhaoFinal}, '
    else:
        valorTotal = caminhoesFinal[1]
        valorTrecho = caminhoesFinal[1]
        caminhaoFinal, quantidadeCaminhaoFinal = caminhoesFinal[0]
        caminhoesNecessariosFinal = caminhoesNecessariosFinal + f'{caminhaoFinal} | {quantidadeCaminhaoFinal}, '
    print(f'Local partida: {cidades[localPartida]}')
    print(f'Local destino: {cidades[localDestino]}')
    print(f'Local parada: {cidades[localParada]}')
    print(f'Distância a ser percorrida: {distanciaTotal} km')
    print(f'Produtos: {produtosStr}')
    print(f'Produtos descarga: {produtosDescargaStr}')
    print(f'Peso da carga: {pesoTotal}')
    print(f'Peso da descarga: {pesoDescarga}')
    print(f'Caminhões necessários até a parada: {caminhoesNecessariosParada}')
    print(f'Caminhões necessários até o final: {caminhoesNecessariosFinal}')
    print(f'Custo total da viagem: R$ {valorTotal}')
    print(f'Valor total dos itens: {totalItens}')
    print(f'Custo unitário: {valorTotal/totalItens}')
    dadosTransporte = {
        "custoTotal": valorTotal,
        "custoTrecho": valorTrecho,
        "custoTrechoParada": valorTrechoParada,
        "distancia": distanciaTotal,
        "totalItens": totalItens,
        "caminhoesParada": caminhoesParada, 
        "caminhoesFinal":  caminhoesFinal
    }
    transporteAplicacao.append(dadosTransporte)
    input("Aperta qualquer tecla para continuar: ")
    menu_principal()

def menu_itens(tipo, itens = 0):
    produtosTransporte = []
    outroItem = 'S'
    while(outroItem != 'N' and outroItem != 'n'):
        for i, produto in enumerate(produtos):
            i += 1
            print(f"{i} - {produtos[i].get('nome')}")
        item = int(input(f'Escolha o item para {tipo}: '))

        if (tipo == 'descarregar'):
            counter = 0
            for produto in itens:
                if (produto['nome'] == produtos[item].get('nome')):
                    counter = 1
            if (counter == 0):
                print('Item não foi encontrado no transporte')
                continue
        produtos[item]['quantidade'] = int(input('Digite a quantidade do produto: '))
        produtosTransporte.append(produtos[item])
        outroItem = str(input('Deseja inserir outro item? Digite S ou N: '))
        
    return produtosTransporte


def estatisticas():
    if (len(transporteAplicacao) == 0):
        print("Nenhum transporte encontrado.")
    for transporte in transporteAplicacao:
        if (transporte["caminhoesParada"] != 0):
            valorTrechoParada = transporte["caminhoesParada"][1]
            caminhaoParada, quantidadeCaminhaoParada = transporte["caminhoesParada"][0]
            valorTrecho = transporte["caminhoesFinal"][1]
            caminhaoFinal, quantidadeCaminhaoFinal = transporte["caminhoesFinal"][0]
            totalCaminhoes = quantidadeCaminhaoFinal + quantidadeCaminhaoParada
            custoModalidade = f'{caminhaoFinal} | R$ {valorTrecho / quantidadeCaminhaoFinal}, {caminhaoParada} | R$ {valorTrechoParada / quantidadeCaminhaoFinal}'
        else:
            valorTrecho = transporte["caminhoesFinal"][1]
            caminhaoFinal, quantidadeCaminhaoFinal = transporte["caminhoesFinal"][0]
            totalCaminhoes = quantidadeCaminhaoFinal + quantidadeCaminhaoParada
            custoModalidade = f'{caminhaoFinal} | R$ {valorTrecho / quantidadeCaminhaoFinal}'

        print(f'Custo total: {transporte["valorTotal"]}')
        if (transporte["valorTrechoParada"] != 0):
            print(f'Custo trecho parada: {transporte["valorTrechoParada"]}')
        print(f'Custo trecho final: {transporte["valorTrecho"]}')
        print(f'Custo médio por tipo de produto: {transporte["custoTotal"] / transporte["totalItens"]}')
        print(f'Custo total para cada modalidade de transporte: {custoModalidade}')
        print(f'Número total de veículos deslocados: {totalCaminhoes}')
        print(f'Total de itens transportados: {transporte["totalItens"]}')
        input("Aperta qualquer tecla para continuar: ")
        menu_principal()

def calcular_caminhao(peso, distancia):
    caminhoes = {
        'pequeno': {'capacidade': 1000, 'custo': 4.87},
        'medio': {'capacidade': 4000, 'custo': 11.92},
        'grande': {'capacidade': 10000, 'custo': 27.44}
    }

    custos = []
    solucao = []

    for k, v in caminhoes.items():
        qtde_caminhoes = math.ceil(peso / v['capacidade'])
        custo_total = qtde_caminhoes * v['custo'] * distancia

        if custo_total != float('inf'):
            custos.append(custo_total)
            solucao.append((k, qtde_caminhoes))

    if not custos:
        return [], float('inf')

    melhor = min(custos)
    indice = custos.index(melhor)

    return solucao[indice], melhor

menu_principal()

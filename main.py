import os
import re
from itertools import combinations
import csv
import time
import matplotlib.pyplot as plt

# classe base de grafos que as diferentes representações seguem
class Grafo:
    def __init__(self):
        pass
    def adicionarAresta(self, i: int, j: int):
        pass
    def getArestas(self, vertice: int) -> list[int]:
        return []
    # Essa função retorna se a aresta (vertice, verticeQueConecta) existe
    # O algoritmo 1 necessita dessa checagem para evitar arestas multiplas
    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        return False
    def getTermo(self, vertice: int) -> str:
        return ""
    def getQuantidadeDeVertices(self) -> int:
        return 0


# classe derivada da classe base Grafo que representa um grafo usando uma lista de adjacência
class GrafoLista(Grafo):
    def __init__(self, n: int, termos: list[str]):
        self.vertices: list[list[int]] = [[] for x in range(n)]
        self.termos = termos.copy()
        self.n = n
    def adicionarAresta(self, i: int, j: int):
        # eu checo antes de adicionar para evitar copias
        # a implementação não permite arestas multiplas
        if j not in self.vertices[i]:
            self.vertices[i].append(j)
        # eu adiciono o vizinho no vertice oposto também já que a natureza da representação em lista de adjacência obriga isso
        # inicialmente isso era feito na funcao que gerava o grafo, porém não é correto fazer isso, dado
        # que esse é um detalhe de implementação. Eu checo se a aresta ja não existe antes para evitar criar novamente.
        if i not in self.vertices[j]:
            self.vertices[j].append(i)
    def getArestas(self, vertice: int) -> list[int]:
        return self.vertices[vertice]
    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        return verticeQueConecta in self.vertices[vertice]
    def getTermo(self, vertice: int) -> str:
        return self.termos[vertice]
    def getQuantidadeDeVertices(self) -> int:
        return self.n


# classe derivada da classe base Grafo que representa um grafo usando uma matriz de adjacência
class GrafoMatriz(Grafo):
    def __init__(self, n: int, termos: list[str]):
        # cria a matriz nxn e inicia todos os valores dela para zero
        self.matriz = [[0 for _ in range(n)] for _ in range(n)]
        self.termos = termos.copy()
        self.n = n
    def adicionarAresta(self, i: int, j: int):
        self.matriz[i][j] = 1
        # o oposto também deve ocorrer se a aresta (i,j) existe na representação a aresta (j,i) também existe
        # lembrando que são grafos não direcionados
        self.matriz[j][i] = 1
    def getArestas(self, vertice: int) -> list[int]:
        return [idx for idx, valor in enumerate(self.matriz[vertice]) if valor == 1]
    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        return self.matriz[vertice][verticeQueConecta] == 1
    def getTermo(self, vertice: int) -> str:
        return self.termos[vertice]
    def getQuantidadeDeVertices(self) -> int:
        return self.n

# extrai todos as termos de um texto -
def extrairTermos(text: str) -> list[str]:
    # retorna apenas as palavras, ignorando numeros e pontuações, mas incluindo palavras acentuadas, tambem coloca as palavras em minusculo
    return [p.lower() for p in re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text)]

# extrair todos os termos da base de dados -
# cada texto da base de dados vai virar uma lista com todos os termos
def extrairTextosBaseDeDados(caminho: str) -> list[list[str]]:
    textos: list[list[str]] = []
    # percorre todos os arquivos na pasta caminho
    for nomeArquivo in os.listdir(caminho):
        caminhoArquivo = os.path.join(caminho, nomeArquivo)
        if os.path.isfile(caminhoArquivo):
            try:
                with open(caminhoArquivo, 'r') as arquivo:
                    textos.append(extrairTermos(arquivo.read()))
            except Exception as err:
                print(f"Erro lendo arquivo {nomeArquivo}: {err}")
    return textos

# retorna os n termos mais frequentes que aparecem em todos os textos -
def coletarNTermosMaisFrequentes(n: int, textos: list[list[str]]) -> list[str]:
    # cria um dicionario em que a chave é o termo e o valor é a quantidade de vezes que a palavra aparece
    termos: dict[str, int] = {}
    for text in textos:
        for palavra in text:
            if palavra not in termos:
                termos[palavra] = 0
            termos[palavra] += 1
    # Ordena os termos em ordem reversa a partir do valor
    termosOrdenados = sorted(termos.items(), key=lambda item: item[1], reverse=True)
    # Vetor dos n termos mais frequentes
    return [termo for termo,_ in termosOrdenados[:n]]

# Função que gera o grafo de coocorrencia baseado no pseudocodigo
# o parametro grafoRepresentação é para dizer se a função irar usar a representação de grafo do tipo matriz ou lista
def GerarGrafoCoocorrencia(grafoRepresentacao: str, texts: list[list[str]], n: int, w: int = 5) -> Grafo:
    Voc = coletarNTermosMaisFrequentes(n, texts)
    # grafo com n vertices, que também armazena o termo relativo ao i-nesimo vertice
    if grafoRepresentacao == "lista":
        grafo = GrafoLista(n, Voc)
    else:
        grafo = GrafoMatriz(n, Voc)

    for T in texts:
        # filtra apenas as palavras do texto que esteja nos n termos mais frequentes
        palavras = [p for p in T if p in Voc]
        for i in range(len(palavras) - w + 1):
            # cria um conjunto com as palavra que estão dentro da janela de palavras
            janela = set(palavras[i:i+w])
            # retorna todos os pares distintos possiveis na janela de palavras
            paresDistintos = combinations(janela, 2)
            for ta, tb in paresDistintos:
                # obtem os indices de ta e tb no Voc, lembrando que existe uma copia de Voc no grafo, 
                # então essa informação poderá ser posteriormente consultada.
                u = Voc.index(ta)
                v = Voc.index(tb)
                # adiciono a aresta não direcionada no grafo, 
                # a função concreta em cada tipo de representação de grafo cuida do detalhe de como isso é feito
                # os detalhes podem ser lidos nos comentários de cada função
                if not grafo.arestaExiste(u, v):
                    grafo.adicionarAresta(u, v)
    return grafo


# Função gera um CSV do grafo para ser lido pelo gephi e gerar a visualização
# o gephi suporta uma serie de formatos essa função retorna um CSV como Adjacency List https://gephi.org/users/supported-graph-formats/csv-format/
def exportToCSV(grafo: Grafo):
    with open("output.csv", 'w',newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=';')
        for i in range(500):
            row = []
            row.append(grafo.getTermo(i))
            for vertice in grafo.getArestas(i):
                row.append(grafo.getTermo(vertice))
            csvWriter.writerow(row)

# Função para fazer os benchmarks esperados
def medirDesempenho(quantidadeExecucoes: int = 1000000):
    # Conjunto de 500, 1000 e 2000 termos
    nTermos = [500, 1000, 2000]
    texts = extrairTextosBaseDeDados("./textos")
    # Salva os tempos medios para criar os grafos, segue essa ordem de tempos
    # Força Bruta/Lista, Força Bruta/Matriz, Tarjan/Lista, Tarjan/Matriz
    dadosParaGrafico = {500: [], 1000: [], 2000: []}
    for n in nTermos:
        # Função que gera o grafo de coocorrencia, é pedido para gerar o vocabulario de n termos
        # isso é feito dentro da propria função seguindo o pseudocodigo
        # Apesar da função retornar o tipo generico Grafo,o codigo ira gerar um grafo em lista ou matriz baseado no parametro
        grafoEmLista = GerarGrafoCoocorrencia("lista", texts, n)
        grafoEmMatriz = GerarGrafoCoocorrencia("matriz", texts, n)

        # Cada uma das 4 combinações são exectuadas abaixo
        print(f"Para um conjunto de {n} termos:")

        # Combinação Força bruta/Lista
        inicioFL = time.perf_counter()
        for i in range(quantidadeExecucoes):
            algoritmoForcaBruta(grafoEmLista)
        fimFL = time.perf_counter()
        tempoMedioForcaBrutaLista = ((fimFL-inicioFL)/quantidadeExecucoes)*1000
        print(f"    A combinação Força Bruta/Lista tomou um tempo médio de: {tempoMedioForcaBrutaLista} milisegundos")

        # Combinação Força bruta/Matriz
        inicioFM = time.perf_counter()
        for i in range(quantidadeExecucoes):
            algoritmoForcaBruta(grafoEmMatriz)
        fimFM = time.perf_counter()
        tempoMedioForcaBrutaMatriz = ((fimFM-inicioFM)/quantidadeExecucoes)*1000
        print(f"    A combinação Força Bruta/Matriz tomou um tempo médio de: {tempoMedioForcaBrutaMatriz} milisegundos")

        # Combinação Tarjan/Lista
        inicioTL = time.perf_counter()
        for i in range(quantidadeExecucoes):
            algoritmoTarjan(grafoEmLista)
        fimTL = time.perf_counter()
        tempoMedioTarjanLista = ((fimTL-inicioTL)/quantidadeExecucoes)*1000
        print(f"    A combinação Tarjan/Lista tomou um tempo médio de: {tempoMedioTarjanLista} milisegundos")

        # Combinação Tarjan/Matriz
        inicioTM = time.perf_counter()
        for i in range(quantidadeExecucoes):
            algoritmoTarjan(grafoEmMatriz)
        fimTM = time.perf_counter()
        tempoMedioTarjanMatriz = ((fimTM-inicioTM)/quantidadeExecucoes)*1000
        print(f"    A combinação Tarjan/Matriz tomou um tempo médio de: {tempoMedioTarjanMatriz} milisegundos\n")

        # Salva os dados para posteriormente criar o grafico
        dadosParaGrafico[n]= [tempoMedioForcaBrutaLista, tempoMedioForcaBrutaMatriz, tempoMedioTarjanLista, tempoMedioTarjanMatriz]

    plotarGrafico(dadosParaGrafico)

def plotarGrafico(dados: dict[int, list[int]]):
    tamanhos = [500,1000, 2000]
    # Inicializar as listas para cada combinação de execução
    fb_lista = []    # Força Bruta / Lista
    fb_matriz = []   # Força Bruta / Matriz
    tarjan_lista = []  # Tarjan / Lista
    tarjan_matriz = [] # Tarjan / Matriz
    # Popular os tempos médios correspondentes
    for tamanho in tamanhos:
        tempos = dados[tamanho]
        fb_lista.append(tempos[0])
        fb_matriz.append(tempos[1])
        tarjan_lista.append(tempos[2])
        tarjan_matriz.append(tempos[3])

    # Plotar as curvas
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, fb_lista, marker='o', label='Força Bruta / Lista')
    plt.plot(tamanhos, fb_matriz, marker='s', label='Força Bruta / Matriz')
    plt.plot(tamanhos, tarjan_lista, marker='^', label='Tarjan / Lista')
    plt.plot(tamanhos, tarjan_matriz, marker='x', label='Tarjan / Matriz')
    plt.xticks(tamanhos)
    # Adiciona título e rótulos
    plt.title('Comparação de Tempo Médio de Execução')
    plt.xlabel('Tamanho do Vocabulário (n)')
    plt.ylabel('Tempo Médio de Execução (ms)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # Mostra o gráfico
    plt.show()

# Algoritmo de tarjan. A funcao retorna uma lista de lista com as componentes fortemente conexas 
# ou no caso do grafos não direcionados do exemplo as componentes biconexas
def algoritmoTarjan(grafo: Grafo):
    stack = []
    lo = [0 for _ in range(grafo.getQuantidadeDeVertices())]
    pre = [-1 for _ in range(grafo.getQuantidadeDeVertices())]
    sc = [-1 for _ in range(grafo.getQuantidadeDeVertices())]
    cnt = 0
    k = 0

    # Implementacao da funcao dfs
    # sera criada aqui dentro para evitar ter que usar variavel global
    def dfsRstrongCompsT(grafo: Grafo, vertice: int, sc: list[int], pai: int = -1):
        nonlocal cnt, pre, k, stack, lo
        pre[vertice] = cnt
        cnt+=1
        stack.append(vertice)
        lo[vertice] = pre[vertice]

        for w in grafo.getArestas(vertice):
            if w == pai:
                continue
            if pre[w] == -1:
                dfsRstrongCompsT(grafo, w, sc, vertice)
                lo[vertice] = min(lo[vertice], lo[w])
            elif pre[w] < pre[vertice] and sc[w] == -1:
                lo[vertice] = min(lo[vertice], pre[w])

        if lo[vertice] == pre[vertice]:
            while True:
                u = stack.pop()
                sc[u] = k
                if u == vertice:
                    break
            k+=1



    for vertice in range(grafo.getQuantidadeDeVertices()):
        if pre[vertice] == -1:
            dfsRstrongCompsT(grafo, vertice, sc)

    componentes = [[] for _ in range(k)]
    for vertice in range(grafo.getQuantidadeDeVertices()):
        componentes[sc[vertice]].append(vertice)

    return componentes

def algoritmoForcaBruta(grafo: Grafo) -> list[list[int]]:
    # vetor que marca se um vertice ja foi visitado, inicio todos como falso
    visitado = [False for _ in range(grafo.getQuantidadeDeVertices())]
    componentes = []

    def dfs(vertice: int, component: list[int]):
        # Marca o vertice atual como visitado
        visitado[vertice] = True
        component.append(vertice)
        # percorre todos os vizinhos do vertice atual
        for vizinho in grafo.getArestas(vertice):
            if not visitado[vizinho]:
                dfs(vizinho, component)


    for vertice in range(grafo.getQuantidadeDeVertices()):
        if not visitado[vertice]:
            componente = []
            dfs(vertice, componente)
            componentes.append(componente)
    
    return componentes

#componentes = algoritmoTarjan(grafoTeste)
#componentes2 = algoritmoForcaBruta(grafoTeste)
#print(componentes)
#print(componentes2)


grafoTeste = GrafoLista(9, ['1','2','3','4','5','6','7','8','9'])
# componente biconexa 1
grafoTeste.adicionarAresta(0,1)
grafoTeste.adicionarAresta(0,2)
grafoTeste.adicionarAresta(1,0)
grafoTeste.adicionarAresta(1,2)
grafoTeste.adicionarAresta(1,4)
grafoTeste.adicionarAresta(2,0)
grafoTeste.adicionarAresta(2,1)
# componente biconexa 2
grafoTeste.adicionarAresta(4,1)
grafoTeste.adicionarAresta(4,3)
grafoTeste.adicionarAresta(4,5)
grafoTeste.adicionarAresta(3,4)
grafoTeste.adicionarAresta(3,5)
grafoTeste.adicionarAresta(5,4)
grafoTeste.adicionarAresta(5,3)
grafoTeste.adicionarAresta(5,6)
# componente biconexa
grafoTeste.adicionarAresta(6,5)
grafoTeste.adicionarAresta(6,8)
grafoTeste.adicionarAresta(6,7)
grafoTeste.adicionarAresta(7,6)
grafoTeste.adicionarAresta(7,8)
grafoTeste.adicionarAresta(8,6)
grafoTeste.adicionarAresta(8,7)

#texts = extrairTextosBaseDeDados("./textos")
#graph = GerarGrafoCoocorrencia("matriz", texts, 500)
#exportToCSV(graph)
medirDesempenho(10)
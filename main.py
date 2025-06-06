import os
import re
from itertools import combinations
import csv

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
    def getTermo(self, vertice: int) -> str :
        return ""


# classe derivada da classe base Grafo que representa um grafo usando uma lista de adjacência
class GrafoLista(Grafo):
    def __init__(self, n: int, termos: list[str]):
        self.vertices: list[list[int]] = [[] for x in range(n)]
        self.termos = termos.copy()
    def adicionarAresta(self, i: int, j: int):
        self.vertices[i].append(j)
        # eu adiciono o vizinho no vertice oposto também já que a natureza da representação em lista de adjacência obriga isso
        # inicialmente isso era feito na funcao que gerava o grafo, porém não é correto fazer isso, dado
        # que esse é um detalhe de implementação.
        self.vertices[j].append(i)
    def getArestas(self, vertice: int) -> list[int]:
        return self.vertices[vertice]
    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        return verticeQueConecta in self.vertices[vertice]
    def getTermo(self, vertice: int) -> str:
        return self.termos[vertice]


# classe derivada da classe base Grafo que representa um grafo usando uma matriz de adjacência
class GrafoMatriz(Grafo):
    def __init__(self, n: int, termos: list[str]):
        # cria a matriz nxn e inicia todos os valores dela para zero
        self.matriz = [[0 for _ in range(n)] for _ in range(n)]
        self.termos = termos.copy()
    def adicionarAresta(self, i: int, j: int):
        self.matriz[i][j] = 1
        # o oposto também deve ocorrer se a aresta (i,j) existe na representação a aresta (j,i) também existe
        # lembrando que são grafos não direcionados
        self.matriz[j][i] = 1
    def getArestas(self, vertice: int) -> list[int]:
        return [idx for idx, valor in enumerate(self.matriz) if valor == 1]
    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        return self.matriz[vertice][verticeQueConecta] == 1
    def getTermo(self, vertice: int) -> str:
        return self.termos[vertice]

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

def GerarGrafoCoocorrencia(texts: list[list[str]], n: int, w: int = 5):
    Voc = coletarNTermosMaisFrequentes(n, texts)
    # grafo com n vertices, que também armazena o termo relativo ao i-nesimo vertice
    grafo = GrafoLista(n, Voc)
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

from .base import Grafo
#classe grafo na implementação com matriz de adjacência derivada da classe Grafo

class GrafoMatriz(Grafo):
    def __init__(self, termos: list[str]):
        # Inicializa o grafo como uma matriz de adjacência (n x n)
        # Cada posição (i, j) da matriz indica se existe uma aresta entre os vértices i e j (1 existe 0 não existe)
        self.matriz = [[0 for _ in range(len(termos))] for _ in range(len(termos))]
        self.termos = termos.copy()  # armazena os termos associados aos vértices
        self.n = len(termos)  # número total de vértices

    def adicionarAresta(self, i: int, j: int):
        # Adiciona uma aresta não-direcionada entre os vértices i e j
        # Atualiza as duas posições da matriz para representar a conexão
        self.matriz[i][j] = 1
        self.matriz[j][i] = 1

    def getArestas(self, vertice: int) -> list[int]:
        # Retorna a lista de vértices conectados ao vértice informado
        # Faz isso verificando quais posições na linha correspondente da matriz possuem valor 1
        return [idx for idx, valor in enumerate(self.matriz[vertice]) if valor == 1]

    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        # Verifica se há uma aresta entre os dois vértices na matriz
        return self.matriz[vertice][verticeQueConecta] == 1

    def getTermo(self, vertice: int) -> str:
        # Retorna o termo (palavra) associado ao vértice
        return self.termos[vertice]

    def getQuantidadeDeVertices(self) -> int:
        # Retorna o número total de vértices no grafo
        return self.n

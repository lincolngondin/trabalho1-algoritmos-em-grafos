from .base import Grafo
#classe do grado na implementação com lista de adjacência derivada da classe Grafo

class GrafoLista(Grafo):
    def __init__(self, termos: list[str]):
        # Inicializa o grafo como uma lista de adjacência
        # Cada vértice corresponde a um termo, e a lista em cada posição representa seus vizinhos
        self.vertices: list[list[int]] = [[] for _ in range(len(termos))]
        self.termos = termos.copy()  # guarda uma cópia dos termos associados aos vértices
        self.n = len(termos)  # número total de vértices

    def adicionarAresta(self, i: int, j: int):
        # Adiciona uma aresta não-direcionada entre os vértices i e j
        # Garante que a conexão só seja feita uma vez (sem duplicatas)
        if j not in self.vertices[i]:
            self.vertices[i].append(j)
        if i not in self.vertices[j]:
            self.vertices[j].append(i)

    def getArestas(self, vertice: int) -> list[int]:
        # Retorna a lista de vizinhos (arestas) do vértice informado
        return self.vertices[vertice]

    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        # Verifica se há uma aresta entre os dois vértices
        return verticeQueConecta in self.vertices[vertice]

    def getTermo(self, vertice: int) -> str:
        # Retorna o termo (palavra) associado ao vértice
        return self.termos[vertice]

    def getQuantidadeDeVertices(self) -> int:
        # Retorna o número total de vértices no grafo
        return self.n

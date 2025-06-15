#classe basse grafo que sera usada como modelo pelos grafos em lista e matriz de adjacencia
class Grafo:
    def __init__(self):
        pass
    def adicionarAresta(self, i: int, j: int):
        pass
    def getArestas(self, vertice: int) -> list[int]:
        return []
    def arestaExiste(self, vertice: int, verticeQueConecta: int) -> bool:
        return False
    def getTermo(self, vertice: int) -> str:
        return ""
    def getQuantidadeDeVertices(self) -> int:
        return 0

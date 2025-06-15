# versao adaptada do algoritimo de tarjan usado para identificar componentes conexas em grafos direcionado
# adaptação feita pois usar o algoritimo original em grafos nao direcionados causam resultados não condizentes com o esperado

def algoritmoTarjan(grafo) -> list[list[int]]:
    visitado = [False] * grafo.getQuantidadeDeVertices()  # vetor para marcar vértices já visitados
    componentes = []  # lista que armazenará todas as componentes conexas encontradas

    def dfs(vertice_inicial: int) -> list[int]:
        # Implementação iterativa da busca em profundidade (DFS) usando pilha
        # Coleta todos os vértices conectados ao vértice inicial, formando uma componente conexa
        pilha = [vertice_inicial]
        componente = []
        visitado[vertice_inicial] = True
        while pilha:
            v = pilha.pop()
            componente.append(v)
            for vizinho in grafo.getArestas(v):
                if not visitado[vizinho]:
                    visitado[vizinho] = True
                    pilha.append(vizinho)
        return componente

    for v in range(grafo.getQuantidadeDeVertices()):
        # Para cada vértice ainda não visitado, aplica a DFS e agrupa os vértices alcançados
        componentes.append(dfs(v)) if not visitado[v] else None

    return componentes  # retorna a lista de componentes conexas identificadas

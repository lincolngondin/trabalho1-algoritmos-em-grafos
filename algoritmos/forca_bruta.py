#algoritimo para detecção de componentes conexas implementado na "força bruta"
#aplica dfs em um vertice, agrupa todos os vertices alcançados na execução da dfs em uma componente so
#passa para o proximo vertice(nao alcançado na primeira busca) e faz o mesmo processo

def algoritmoForcaBruta(grafo) -> list[list[int]]:
    visitado = [False] * grafo.getQuantidadeDeVertices() #inicialmente setamos todos os vertices como nao visitados
    componentes = []  #componentes inicialmente vazias

    def dfs(v: int, componente: list[int]):  #definição de busca em profundidade
        visitado[v] = True #vertice atual é setado como visitado
        componente.append(v)  #vertice atual é adcionado a componente atual
        for vizinho in grafo.getArestas(v): 
            if not visitado[vizinho]: #se nao visitado, aplica dfs no vertice
                dfs(vizinho, componente)

    for v in range(grafo.getQuantidadeDeVertices()):
        if not visitado[v]:
            componente = []
            dfs(v, componente)
            componentes.append(componente) #para cada "quebra" na sequencia dos vertices, cria uma componente nova contendo os vertices que foram 
                                           #alcançados a partir do vertice inicial
    return componentes

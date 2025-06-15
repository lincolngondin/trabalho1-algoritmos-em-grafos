import matplotlib.pyplot as plt

def plotarGrafico(dados: dict[int, list[float]]):
    tamanhos = [500, 1000, 2000]  # tamanhos de vocabulário utilizados para os testes

    # Inicializa listas que irão armazenar os tempos médios para cada combinação algoritmo/representação
    fb_lista, fb_matriz, tarjan_lista, tarjan_matriz = [], [], [], []

    # Separa os tempos médios de execução por tipo de algoritmo e tipo de grafo
    for tamanho in tamanhos:
        tempos = dados[tamanho]
        fb_lista.append(tempos[0])      # Força Bruta / Lista de Adjacência
        fb_matriz.append(tempos[1])     # Força Bruta / Matriz de Adjacência
        tarjan_lista.append(tempos[2])  # Tarjan / Lista de Adjacência
        tarjan_matriz.append(tempos[3]) # Tarjan / Matriz de Adjacência

    # Configura e plota os dados em um gráfico de linha
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, fb_lista, marker='o', label='Força Bruta / Lista')
    plt.plot(tamanhos, fb_matriz, marker='s', label='Força Bruta / Matriz')
    plt.plot(tamanhos, tarjan_lista, marker='^', label='Tarjan / Lista')
    plt.plot(tamanhos, tarjan_matriz, marker='x', label='Tarjan / Matriz')
    plt.xticks(tamanhos)
    plt.title('Comparação de Tempo Médio de Execução')
    plt.xlabel('Tamanho do Vocabulário (n)')
    plt.ylabel('Tempo Médio de Execução (ms)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

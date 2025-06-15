import time
from algoritmos.tarjan import algoritmoTarjan
from algoritmos.forca_bruta import algoritmoForcaBruta
from utils.exportacao import exportToCSV
from utils.gerarGrafo import inicializarGrafos
from visualizacao.grafico import plotarGrafico

def medir_tempo_algoritmo(nome_algoritmo: str, representacao: str, funcao, grafo, quantidade_execucoes: int) -> float:
    # Mede o tempo médio de execução de um algoritmo sobre um grafo, repetindo várias vezes
    # Exibe o tempo médio em milissegundos
    inicio = time.perf_counter()
    for _ in range(quantidade_execucoes):
        funcao(grafo)
    fim = time.perf_counter()
    tempo_medio = ((fim - inicio) / quantidade_execucoes) * 1000
    print(f"    A combinação {nome_algoritmo}/{representacao} tomou um tempo médio de: {tempo_medio:.6f} milissegundos")
    return tempo_medio

def medirDesempenho(quantidadeExecucoes: int = 1000000):
    # Função principal para medir o desempenho de algoritmos em diferentes representações de grafos
    # Executa os testes com 3 tamanhos diferentes e armazena os resultados para gerar gráfico comparativo

    dadosParaGrafico = {500: [], 1000: [], 2000: []}  # dicionário para armazenar os tempos para o gráfico
    nTermos = [500, 1000, 2000]  # diferentes tamanhos do grafo a serem testados

    for n in nTermos:
        grafoEmLista, grafoEmMatriz = inicializarGrafos(n)  # inicializa grafos nas duas representações (lista e matriz)

        print(f"Para um conjunto de {n} termos:")

        # Mede o tempo médio de execução para cada combinação de algoritmo e representação
        tempoMedioForcaBrutaLista  = medir_tempo_algoritmo("Força Bruta", "Lista", algoritmoForcaBruta, grafoEmLista, quantidadeExecucoes)
        tempoMedioForcaBrutaMatriz = medir_tempo_algoritmo("Força Bruta", "Matriz", algoritmoForcaBruta, grafoEmMatriz, quantidadeExecucoes)
        tempoMedioTarjanLista      = medir_tempo_algoritmo("Tarjan", "Lista", algoritmoTarjan, grafoEmLista, quantidadeExecucoes)
        tempoMedioTarjanMatriz     = medir_tempo_algoritmo("Tarjan", "Matriz", algoritmoTarjan, grafoEmMatriz, quantidadeExecucoes)
        print()

        if n == 500:
            exportToCSV(grafoEmLista)  # exporta a estrutura do grafo de 500 termos para CSV

        # Armazena os tempos coletados no dicionário para futura plotagem
        dadosParaGrafico[n] = [
            tempoMedioForcaBrutaLista,
            tempoMedioForcaBrutaMatriz,
            tempoMedioTarjanLista,
            tempoMedioTarjanMatriz
        ]

    plotarGrafico(dadosParaGrafico)  # gera o gráfico com os dados de desempenho

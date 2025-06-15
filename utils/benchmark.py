import time
from algoritmos.tarjan import algoritmoTarjan
from algoritmos.forca_bruta import algoritmoForcaBruta
from utils.exportacao import exportToCSV
from utils.gerarGrafo import inicializarGrafos
from visualizacao.grafico import plotarGrafico
import datetime
from utils.exportacao import gerar_relatorio_pdf_completo  # ajuste o import conforme seu projeto

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
    dadosParaGrafico = {500: [], 1000: [], 2000: []}
    nTermos = [500, 1000, 2000]

    for n in nTermos:
        grafoEmLista, grafoEmMatriz = inicializarGrafos(n)

        print(f"Para um conjunto de {n} termos:")

        tempoMedioForcaBrutaLista  = medir_tempo_algoritmo("Força Bruta", "Lista", algoritmoForcaBruta, grafoEmLista, quantidadeExecucoes)
        tempoMedioForcaBrutaMatriz = medir_tempo_algoritmo("Força Bruta", "Matriz", algoritmoForcaBruta, grafoEmMatriz, quantidadeExecucoes)
        tempoMedioTarjanLista      = medir_tempo_algoritmo("Tarjan", "Lista", algoritmoTarjan, grafoEmLista, quantidadeExecucoes)
        tempoMedioTarjanMatriz     = medir_tempo_algoritmo("Tarjan", "Matriz", algoritmoTarjan, grafoEmMatriz, quantidadeExecucoes)
        print()
        
        if n == 500:
            exportToCSV(grafoEmLista)

        dadosParaGrafico[n] = [
            tempoMedioForcaBrutaLista,
            tempoMedioForcaBrutaMatriz,
            tempoMedioTarjanLista,
            tempoMedioTarjanMatriz
        ]

    # Criar nome do arquivo com timestamp pra salvar vários relatórios
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"relatorios/relatorio_desempenho_{timestamp}.pdf"

    # Certifique-se que a pasta "relatorios" existe
    import os
    os.makedirs("relatorios", exist_ok=True)

    # Gerar o relatório PDF com os dados coletados
    gerar_relatorio_pdf_completo(dadosParaGrafico, quantidadeExecucoes, nome_arquivo)

    # Mostrar gráfico (opcional)
    plotarGrafico(dadosParaGrafico)


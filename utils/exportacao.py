import csv
import os
from grafo.base import Grafo
from datetime import datetime

# gera um CSV do grafo para ser lido pelo gephi e gerar a visualização
# o gephi suporta uma serie de formatos essa função retorna um CSV como Adjacency List https://gephi.org/users/supported-graph-formats/csv-format/
def exportToCSV(grafo: Grafo, caminho='output.csv'):
    with open(caminho, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=';')
        for i in range(grafo.getQuantidadeDeVertices()):
            row = [grafo.getTermo(i)] + [grafo.getTermo(v) for v in grafo.getArestas(i)]
            csvWriter.writerow(row)

# gera um realtorio de execução contendo os dados da rodada e como se sai cada algoritimo com cada abordagem
def gerarRelatorioDesempenho(dados: dict[int, list[float]], pasta: str = "relatorios"):
    # Cria a pasta caso não exista
    os.makedirs(pasta, exist_ok=True)

    # Gera um nome de arquivo com base no horário atual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"relatorio_{timestamp}.txt"
    caminho_completo = os.path.join(pasta, nome_arquivo)

    # Escreve o conteúdo do relatório
    with open(caminho_completo, "w", encoding="utf-8") as arquivo:
        arquivo.write("Relatório de Desempenho dos Algoritmos de Componentes Conexas\n")
        arquivo.write("--------------------------------------------------------------\n\n")
        for n in sorted(dados.keys()):
            tempos = dados[n]
            arquivo.write(f"Tamanho do vocabulário: {n}\n")
            arquivo.write(f"  Força Bruta / Lista  : {tempos[0]:.6f} ms\n")
            arquivo.write(f"  Força Bruta / Matriz : {tempos[1]:.6f} ms\n")
            arquivo.write(f"  Tarjan / Lista       : {tempos[2]:.6f} ms\n")
            arquivo.write(f"  Tarjan / Matriz      : {tempos[3]:.6f} ms\n\n")

    print(f"Relatório salvo em: {caminho_completo}")

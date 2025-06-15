import csv
from grafo.base import Grafo

# Função gera um CSV do grafo para ser lido pelo gephi e gerar a visualização
# o gephi suporta uma serie de formatos essa função retorna um CSV como Adjacency List https://gephi.org/users/supported-graph-formats/csv-format/
def exportToCSV(grafo: Grafo, caminho='output.csv'):
    with open(caminho, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=';')
        for i in range(grafo.getQuantidadeDeVertices()):
            row = [grafo.getTermo(i)] + [grafo.getTermo(v) for v in grafo.getArestas(i)]
            csvWriter.writerow(row)

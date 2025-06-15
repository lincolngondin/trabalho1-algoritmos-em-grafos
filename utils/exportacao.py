import csv
from grafo.base import Grafo
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

# gera um CSV do grafo para ser lido pelo gephi e gerar a visualização
# o gephi suporta uma serie de formatos essa função retorna um CSV como Adjacency List https://gephi.org/users/supported-graph-formats/csv-format/
def exportToCSV(grafo: Grafo, caminho='output.csv'):
    with open(caminho, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=';')
        for i in range(grafo.getQuantidadeDeVertices()):
            row = [grafo.getTermo(i)] + [grafo.getTermo(v) for v in grafo.getArestas(i)]
            csvWriter.writerow(row)

def gerar_relatorio_pdf_completo(dados_tempos: dict[int, list[float]], quantidade_execucoes: int, caminho_saida: str):
    doc = SimpleDocTemplate(caminho_saida, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elementos = []
    styles = getSampleStyleSheet()

    # Título
    titulo = Paragraph("Relatório de Desempenho dos Algoritmos", styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    # Quantidade de execuções
    exec_texto = Paragraph(f"<b>Quantidade de Execuções por teste:</b> {quantidade_execucoes}", styles['Normal'])
    elementos.append(exec_texto)
    elementos.append(Spacer(1, 20))

    # Cabeçalhos com quebra de linha
    cabecalhos = [
        "Tamanho do<br/>Vocabulário (n)", 
        "Força Bruta<br/>Lista (ms)", 
        "Força Bruta<br/>Matriz (ms)", 
        "Tarjan<br/>Lista (ms)", 
        "Tarjan<br/>Matriz (ms)"
    ]
    cabecalho_paragraphs = [Paragraph(h, styles['BodyText']) for h in cabecalhos]

    tabela_dados = [cabecalho_paragraphs]

    # Dados da tabela
    for n, tempos in sorted(dados_tempos.items()):
        linha = [str(n)] + [f"{tempo:.6f}" for tempo in tempos]
        tabela_dados.append(linha)

    # Criação da tabela com largura ajustada
    tabela = Table(tabela_dados, colWidths=[90, 90, 90, 90, 90])

    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),

        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f0f0f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    tabela.setStyle(estilo)
    elementos.append(tabela)
    elementos.append(Spacer(1, 30))

    # Criar gráfico matplotlib embutido
    fig, ax = plt.subplots(figsize=(8, 4.5))
    tamanhos = sorted(dados_tempos.keys())
    fb_lista = [dados_tempos[t][0] for t in tamanhos]
    fb_matriz = [dados_tempos[t][1] for t in tamanhos]
    tarjan_lista = [dados_tempos[t][2] for t in tamanhos]
    tarjan_matriz = [dados_tempos[t][3] for t in tamanhos]

    ax.plot(tamanhos, fb_lista, marker='o', label='Força Bruta / Lista')
    ax.plot(tamanhos, fb_matriz, marker='s', label='Força Bruta / Matriz')
    ax.plot(tamanhos, tarjan_lista, marker='^', label='Tarjan / Lista')
    ax.plot(tamanhos, tarjan_matriz, marker='x', label='Tarjan / Matriz')

    ax.set_xticks(tamanhos)
    ax.set_title('Comparação de Tempo Médio de Execução')
    ax.set_xlabel('Tamanho do Vocabulário (n)')
    ax.set_ylabel('Tempo Médio de Execução (ms)')
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='PNG')
    plt.close(fig)
    img_buffer.seek(0)

    imagem = Image(img_buffer)
    imagem._restrictSize(500, 300)
    elementos.append(imagem)

    # Gerar PDF
    doc.build(elementos)

    print(f"Relatório PDF salvo em: {caminho_saida}")

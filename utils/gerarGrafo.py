from utils.processamento_texto import extrairTextosBaseDeDados, TextosOriginaisParaComparar, coletarNTermosMaisFrequentes
from grafo.lista import GrafoLista
from grafo.matriz import GrafoMatriz
from itertools import combinations

def GerarGrafoCoocorrencia(grafoRepresentacao: str, texts: list[list[str]], originalTexts: list[list[str]], n: int, w: int):
    # Gera um grafo de coocorrência a partir dos textos, conectando termos frequentes que aparecem próximos (janela deslizante)
    
    Voc = coletarNTermosMaisFrequentes(n, texts)  # seleciona os n termos mais frequentes como vocabulário
    mapa_indices = {termo: idx for idx, termo in enumerate(Voc)}  # mapeia cada termo a um índice

    # Inicializa o grafo na representação desejada (lista ou matriz)
    if grafoRepresentacao == "lista":
        grafo = GrafoLista(Voc)
    else:
        grafo = GrafoMatriz(Voc)

    # Varre os textos originais, criando janelas de tamanho w
    for T in originalTexts:
        for i in range(len(T) - w + 1):
            janela = T[i:i+w]
            termosNaJanela = [p for p in janela if p in mapa_indices]  # considera apenas os termos do vocabulário
            paresDistintos = combinations(set(termosNaJanela), 2)  # gera pares únicos de coocorrência na janela
            for ta, tb in paresDistintos:
                u = mapa_indices[ta]
                v = mapa_indices[tb]
                # Adiciona aresta entre os termos se ainda não existir
                if not grafo.arestaExiste(u, v):
                    grafo.adicionarAresta(u, v)

    return grafo  # retorna o grafo gerado com as conexões de coocorrência

def inicializarGrafos(QuantidadeDeTermosPgeracaoDosGrafos: int = 50, TamanhoDaJanela: int = 5):
    # Função auxiliar para preparar os dois grafos (lista e matriz) com base nos textos extraídos

    texts = extrairTextosBaseDeDados("resumos_arxiv_salvar")  # textos pré-processados para frequência. use ./textosDeTeste para usar os textos de teste
    textosOriginais = TextosOriginaisParaComparar("resumos_arxiv_salvar")  # textos completos para análise de coocorrência. use ./textosDeTeste para usar os textos de teste

    # Gera os grafos de coocorrência em ambas as representações
    grafoEmLista  = GerarGrafoCoocorrencia("lista", texts, textosOriginais, QuantidadeDeTermosPgeracaoDosGrafos, TamanhoDaJanela)
    grafoEmMatriz = GerarGrafoCoocorrencia("matriz", texts, textosOriginais, QuantidadeDeTermosPgeracaoDosGrafos, TamanhoDaJanela)

    return grafoEmLista, grafoEmMatriz  # retorna os dois grafos gerados

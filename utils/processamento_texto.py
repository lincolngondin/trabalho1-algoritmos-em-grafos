import os
import re
from collections import Counter
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))  # conjunto de stopwords em inglês para filtrar palavras irrelevantes

def extrairTermos(text: str) -> list[str]:
    # Extrai palavras do texto (convertidas para minúsculas), removendo stopwords e palavras com caracteres inválidos
    palavras = [p.lower() for p in re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text)]
    return [p for p in palavras if p not in stop_words and '�' not in p]

def extrairTermosOriginais(text: str) -> list[str]:
    # Extrai palavras do texto (minúsculas), sem remover stopwords — usado para preservar sequência original dos textos
    palavras = [p.lower() for p in re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text)]
    return [p for p in palavras]

def extrairTextosBaseDeDados(caminho: str) -> list[list[str]]:
    # Percorre os arquivos em um diretório, aplicando `extrairTermos` para filtrar e normalizar os textos
    textos: list[list[str]] = []
    for nomeArquivo in os.listdir(caminho):
        caminhoArquivo = os.path.join(caminho, nomeArquivo)
        if os.path.isfile(caminhoArquivo):
            try:
                with open(caminhoArquivo, 'r', encoding='utf-8', errors='replace') as arquivo:
                    conteudo = arquivo.read()
                    textos.append(extrairTermos(conteudo))
            except Exception as err:
                print(f"Erro lendo arquivo {nomeArquivo}: {err}")
    return textos

def TextosOriginaisParaComparar(caminho: str) -> list[list[str]]:
    # Similar à função anterior, mas aplica `extrairTermosOriginais` — serve para manter os textos completos para coocorrência
    textos: list[list[str]] = []
    for nomeArquivo in os.listdir(caminho):
        caminhoArquivo = os.path.join(caminho, nomeArquivo)
        if os.path.isfile(caminhoArquivo):
            try:
                with open(caminhoArquivo, 'r', encoding='utf-8', errors='replace') as arquivo:
                    conteudo = arquivo.read()
                    textos.append(extrairTermosOriginais(conteudo))
            except Exception as err:
                print(f"Erro lendo arquivo {nomeArquivo}: {err}")
    return textos

def coletarNTermosMaisFrequentes(n: int, textos: list[list[str]]) -> list[str]:
    # Conta a frequência de todos os termos e retorna os `n` mais frequentes — usado para compor o vocabulário do grafo
    todos_termos = [palavra for texto in textos for palavra in texto]
    contagem = Counter(todos_termos)
    return [termo for termo, _ in contagem.most_common(n)]

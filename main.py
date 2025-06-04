import os
import re

# classe base de grafos que as diferentes representações seguem
class Grafo:
    def __init__(self):
        pass
    def adicionarVertice(self, termo: str):
        pass


# classe derivada da classe base Grafo que representa um grafo usando uma lista de adjacência
class GrafoLista(Grafo):
    def __init__(self, n: int =1):
        self.vertices = [0 for x in range(n)]
        pass
    def adicionarVertice(self, termo: str):
        pass
        

gl = GrafoLista()
print(gl.vertices)

# classe derivada da classe base Grafo que representa um grafo usando uma matriz de adjacência
class GrafoMatriz(Grafo):
    def __init__(self):
        super().__init__()

# extrai todos as termos de um texto -
def extrairTermos(text: str) -> list[str]:
    # retorna apenas as palavras, ignorando numeros e pontuações, mas incluindo palavras acentuadas
    return re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text)

# extrair todas os termos da base de dados -
# cada texto da base de dados vai virar uma lista com todos os termos
def extrairTextosBaseDeDados(caminho: str) -> list[list[str]]:
    textos: list[list[str]] = []
    # percorre todos os arquivos na pasta caminho
    for nomeArquivo in os.listdir(caminho):
        caminhoArquivo = os.path.join(caminho, nomeArquivo)
        if os.path.isfile(caminhoArquivo):
            try:
                with open(caminhoArquivo, 'r') as arquivo:
                    textos.append(extrairTermos(arquivo.read()))
            except Exception as err:
                print(f"Erro lendo arquivo {nomeArquivo}: {err}")
    return textos

# retorna os n termos mais frequentes que aparecem em todos os textos -
def coletarNTermosMaisFrequentes(n: int, textos: list[list[str]]) -> list[str]:
    termos: dict[str, int] = {}
    for text in textos:
        for palavra in text:
            print(text)
            if palavra not in termos:
                termos[palavra] = 0
            termos[palavra] += 1
    termosOrdenados = sorted(termos.items(), key=lambda item: item[1], reverse=True)
    return [termo for termo,_ in termosOrdenados[:n]]
    

def GerarGrafoCoocorrencia(Texts, n, w):
    pass

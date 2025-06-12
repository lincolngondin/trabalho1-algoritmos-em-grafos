import os
import requests
from bs4 import BeautifulSoup
import re
import time

# Lista de categorias desejadas
categorias = [
    # Computer Science
    "cs.AI", "cs.AR", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR", "cs.CV",
    "cs.CY", "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.FL", "cs.GL", "cs.GR",
    "cs.GT", "cs.HC", "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM",
    "cs.MS", "cs.NA", "cs.NE", "cs.NI", "cs.OH", "cs.OS", "cs.PF", "cs.PL",
    "cs.RO", "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY",

    # Physics
    "physics.acc-ph", "physics.ao-ph", "physics.atm-clus", "physics.atom-ph",
    "physics.bio-ph", "physics.chem-ph", "physics.class-ph", "physics.comp-ph",
    "physics.data-an", "physics.ed-ph", "physics.flu-dyn", "physics.gen-ph",
    "physics.geo-ph", "physics.hist-ph", "physics.ins-det",
    "physics.med-ph", "physics.optics", "physics.soc-ph", "physics.plasm-ph",
    "physics.pop-ph", "physics.space-ph",

    # Math
    "math.AG", "math.AT", "math.AP", "math.CT", "math.CA", "math.CO",
    "math.AC", "math.CV", "math.DG", "math.DS", "math.FA", "math.GM",
    "math.GN", "math.GT", "math.GR", "math.HO", "math.IT", "math.KT",
    "math.LO", "math.MP", "math.MG", "math.NT", "math.NA", "math.OA",
    "math.OC", "math.PR", "math.QA", "math.RT", "math.RA", "math.SP",
    "math.ST",

    # Quantitative Biology
    "q-bio.BM", "q-bio.CB", "q-bio.GN", "q-bio.MN", "q-bio.NC",
    "q-bio.OT", "q-bio.PE", "q-bio.QM", "q-bio.SC",

    # Quantitative Finance
    "q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF", "q-fin.PM",
    "q-fin.PR", "q-fin.RM", "q-fin.ST",

    # Statistics
    "stat.AP", "stat.CO", "stat.ME", "stat.ML",

    # Electrical Engineering and Systems Science
    "eess.AS", "eess.IV", "eess.SP", "eess.SY",

    # Economics
    "econ.EM"
]

# Limpa nomes de arquivos
def limpar_nome(texto):
    return re.sub(r'[\\/*?:"<>|\n]', "_", texto).strip()

# Pasta onde salvar os resumos
os.makedirs("resumos_arxiv", exist_ok=True)

# Quantos artigos por categoria?
max_artigos = 40

for categoria in categorias:
    print(f"\n📚 Coletando artigos de: {categoria}")
    url = f"https://arxiv.org/list/{categoria}/new"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Captura todos os blocos de título + abstract
        summaries = soup.find_all("dd")

        for i, summary in enumerate(summaries[:max_artigos]):
            # Extrai título
            title_tag = summary.find("div", class_="list-title")
            title = title_tag.text.replace("Title:", "").strip() if title_tag else f"artigo_{i+1}"
            title_limpo = limpar_nome(title)

            # Extrai resumo
            abstract_tag = summary.find("p", class_="mathjax")
            abstract = abstract_tag.text.strip() if abstract_tag else "Resumo não encontrado."

            # Extrai link (via <a href>)
            link_tag = summary.find_previous_sibling("dt").find("a", title="Abstract")
            link = f"https://arxiv.org{link_tag['href']}" if link_tag else "Link indisponível"

            # Salva em arquivo .txt
            filename = f"resumos_arxiv/{categoria}_{i+1}_{title_limpo[:50]}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(abstract)

            print(f"✅ Salvo: {filename}")
            time.sleep(0.5)  # pequena pausa para boa prática

    except Exception as e:
        print(f"⚠️ Erro ao processar {categoria}: {e}")

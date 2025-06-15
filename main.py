import sys
import nltk
from utils.benchmark import medirDesempenho

nltk.download('stopwords')
sys.setrecursionlimit(2000)

if __name__ == "__main__":
    medirDesempenho(10)

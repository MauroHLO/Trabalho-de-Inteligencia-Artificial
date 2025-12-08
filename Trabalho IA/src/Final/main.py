import os
import sys
from parste import Parste     # seu ambiente STRIPS
from busca import Busca

PASTA = r"Trabalho IA\src\instancias"


def escolher_arquivo():
    print("\nInstâncias disponíveis:\n")

    if not os.path.isdir(PASTA):
        print(f"ERRO: pasta '{PASTA}' não encontrada.")
        sys.exit(1)

    arquivos = [f for f in os.listdir(PASTA) if f.endswith(".strips")]

    if not arquivos:
        print("Nenhum arquivo .strips encontrado.")
        sys.exit(1)

    for i, arq in enumerate(arquivos, 1):
        print(f"{i}. {arq}")

    print()
    op = int(input("Escolha o número da instância: "))

    # devolve o caminho COMPLETO
    return os.path.join(PASTA, arquivos[op - 1])

def escolher_algoritmo():
    print("\nAlgoritmos Disponiveis:\n")
    limite = None

    algoritmos = ["BFS", "DLS", "IDS", "A*", "Bidirecional"]

    for i, algoritmo in enumerate(algoritmos, 1):
        print(f"{i}. {algoritmo}")
    
    print()

    op = int(input("Escolha um Algoritmo: "))

    if op == 2:
        limite = int(input("Defnina um Limite para a Busca: "))
    return algoritmos[op-1], limite


def main():
    for _ in range(4):
        if len(sys.argv) == 1:
            caminho = escolher_arquivo()
        else:
            caminho = sys.argv[1]

        print(f"\nLendo instância: {caminho}")
        print("=" * 70)

        amb = Parste()      
        busca = Busca(amb)
        amb.lerArquivo(caminho)   
        alg, lim = escolher_algoritmo()
        
        busca.executar_busca(alg, lim)


if __name__ == "__main__":
    main()

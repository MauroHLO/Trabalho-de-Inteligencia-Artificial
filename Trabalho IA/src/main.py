import os
import sys
import time

from planner.parser import carregar_instancia
from planner.busca import bfs, dfs_limited, ids, astar
from planner.bidirecional import bidirecional

PASTA = "Trabalho IA\src\instancias"   # coloque o nome da pasta onde ficam os arquivos .strips

def escolher_arquivo():
    print("\nInstâncias disponíveis:\n")

    arquivos = [f for f in os.listdir(PASTA) if f.endswith(".strips")]

    if not arquivos:
        print("Nenhum arquivo .strips encontrado.")
        sys.exit(1)

    for i, arq in enumerate(arquivos, 1):
        print(f"{i}. {arq}")

    print()
    op = int(input("Escolha o número da instância: "))

    return os.path.join(PASTA, arquivos[op - 1])


def rodar_algoritmo(nome, func, INI, OBJ, ACOES):
    inicio = time.time()
    custo, caminho, nos = func(INI, OBJ, ACOES)
    tempo = time.time() - inicio

    print(f"{nome:15} | Custo: {str(custo):>4} | Nós: {nos:>7} | Tempo: {tempo*1000:7.2f} ms")

    if custo is not None and custo <= 25:
        for i, ac in enumerate(caminho, 1):
            print(f"   {i:3}. {ac}")

    print("-" * 70)


def main():

    # Se o usuário *não* passou arquivo, mostramos menu
    if len(sys.argv) == 1:
        caminho = escolher_arquivo()
    else:
        caminho = sys.argv[1]

    print(f"\nLendo instância: {caminho}")
    print("=" * 70)

    INI, OBJ, ACOES = carregar_instancia(caminho)

    print(f"Total de ações        : {len(ACOES)}")
    print("=" * 70)

    rodar_algoritmo("BFS", bfs, INI, OBJ, ACOES)
    rodar_algoritmo("DFS limitada", dfs_limited, INI, OBJ, ACOES)
    rodar_algoritmo("IDS", ids, INI, OBJ, ACOES)
    rodar_algoritmo("A*", astar, INI, OBJ, ACOES)
    rodar_algoritmo("Bidirecional", bidirecional, INI, OBJ, ACOES)


if __name__ == "__main__":
    main()

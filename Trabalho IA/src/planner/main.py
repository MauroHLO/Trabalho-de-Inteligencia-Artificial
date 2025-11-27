# main.py
# -------------------------------------------------------------------------
# Executa um planejador STRIPS para o Mundo dos Blocos
# usando várias buscas: BFS, DFS, IDS, A*, Bidirecional.
# -------------------------------------------------------------------------

import sys
import time

from planner.parser import carregar_strips
from planner.busca import bfs, dfs_limited, ids, astar
from planner.bidirecional import bidirecional


# -------------------------------------------------------------------------
def rodar_algoritmo(nome, func, INI, OBJ, ACOES):
    inicio = time.time()
    custo, caminho, nos = func(INI, OBJ, ACOES)
    tempo = time.time() - inicio

    print(f"{nome:15} | Custo: {str(custo):>4} | Nós: {nos:>7} | Tempo: {tempo*1000:7.2f} ms")

    # Mostra caminho se não for gigantesco
    if custo is not None and custo <= 25:
        for i, ac in enumerate(caminho, 1):
            print(f"   {i:3}. {ac}")

    print("-" * 70)


# -------------------------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Uso correto:")
        print("   python main.py <arquivo.strips>")
        sys.exit(1)

    caminho = sys.argv[1]

    print(f"\nLendo instância: {caminho}")
    print("=" * 70)

    # ---------------------------------------------------------------------
    # Carregar a instância completa
    # ---------------------------------------------------------------------
    INI, OBJ, ACOES, mapa = carregar_strips(caminho)

    print(f"Total de proposições : {len(mapa.proposicoes)}")
    print(f"Total de ações        : {len(ACOES)}")
    print("=" * 70)

    # ---------------------------------------------------------------------
    # Rodar algoritmos de busca
    # ---------------------------------------------------------------------
    rodar_algoritmo("BFS", bfs, INI, OBJ, ACOES)
    rodar_algoritmo("DFS limitada", dfs_limited, INI, OBJ, ACOES)
    rodar_algoritmo("IDS", ids, INI, OBJ, ACOES)
    rodar_algoritmo("A*", astar, INI, OBJ, ACOES)
    rodar_algoritmo("Bidirecional", bidirecional, INI, OBJ, ACOES)


# -------------------------------------------------------------------------
if __name__ == "__main__":
    main()

# search.py
# -------------------------------------------------------------------------
# Implementação dos algoritmos de busca sobre estados STRIPS:
#   - sucessores
#   - BFS
#   - DFS limitada
#   - IDS
#   - A*
#
# Cada estado é representado como uma tupla ordenada de ints positivos.
# Cada ação é um objeto Acao contendo pré-condições e efeitos.
#
# OBJ (objetivo) é uma lista de ints assinados:
#   +p -> proposição p deve ser verdadeira
#   -p -> proposição p deve ser falsa
#
# -------------------------------------------------------------------------

from collections import deque
import heapq

from planner.heuristica import heuristica


# -------------------------------------------------------------------------
# Gera sucessores aplicando TODAS as ações possíveis
# -------------------------------------------------------------------------
def sucessores(estado, acoes):
    """
    estado: tuple[int] com proposições verdadeiras
    acoes: List[Acao]

    Retorna uma lista:
        [(novo_estado, nome_da_acao), ...]
    """
    est_set = set(estado)
    suc = []

    for ac in acoes:
        if ac.aplicavel(est_set):
            novo = ac.aplicar(est_set)
            suc.append((novo, ac.nome))

    return suc


# -------------------------------------------------------------------------
# Verifica se um estado satisfaz o objetivo parcial
# -------------------------------------------------------------------------
def satisfaz_objetivo(estado, OBJ):
    """
    estado = tuple de proposições verdadeiras
    OBJ    = lista de ints assinados

    +p → p deve estar no estado
    -p → p não deve estar no estado
    """
    est_set = set(estado)

    for g in OBJ:
        if g > 0:
            if g not in est_set:
                return False
        else:
            if -g in est_set:
                return False

    return True


# -------------------------------------------------------------------------
# BFS
# -------------------------------------------------------------------------
def bfs(INI, OBJ, acoes):
    fila = deque([(INI, 0, [])])
    visit = {INI}
    nos = 0

    while fila:
        estado, custo, caminho = fila.popleft()
        nos += 1

        if satisfaz_objetivo(estado, OBJ):
            return custo, caminho, nos

        for prox, mov in sucessores(estado, acoes):
            if prox not in visit:
                visit.add(prox)
                fila.append((prox, custo + 1, caminho + [mov]))

    return None, [], nos


# -------------------------------------------------------------------------
# DFS com limite de profundidade
# -------------------------------------------------------------------------
def dfs_limited(INI, OBJ, acoes, limite=30):
    pilha = [(INI, 0, [])]
    visit = set()
    nos = 0

    while pilha:
        estado, custo, caminho = pilha.pop()
        nos += 1

        if estado in visit:
            continue
        visit.add(estado)

        if satisfaz_objetivo(estado, OBJ):
            return custo, caminho, nos

        if custo >= limite:
            continue

        for prox, mov in sucessores(estado, acoes):
            pilha.append((prox, custo + 1, caminho + [mov]))

    return None, [], nos


# -------------------------------------------------------------------------
# Busca em profundidade iterativa
# -------------------------------------------------------------------------
def ids(INI, OBJ, acoes, max_lim=50):
    total = 0

    for L in range(max_lim):
        pilha = [(INI, 0, [])]
        visit = set()
        nos = 0

        while pilha:
            estado, custo, caminho = pilha.pop()
            nos += 1

            if estado in visit:
                continue
            visit.add(estado)

            if satisfaz_objetivo(estado, OBJ):
                return custo, caminho, total + nos

            if custo < L:
                for prox, mov in sucessores(estado, acoes):
                    pilha.append((prox, custo + 1, caminho + [mov]))

        total += nos

    return None, [], total


# -------------------------------------------------------------------------
# A* usando heurística definida em heuristics.py
# -------------------------------------------------------------------------
def astar(INI, OBJ, acoes):
    aberta = [(heuristica(INI, OBJ), 0, INI, [])]  # (f=g+h, g, estado, caminho)
    visit = {}
    nos = 0

    while aberta:
        f, g, estado, caminho = heapq.heappop(aberta)
        nos += 1

        if satisfaz_objetivo(estado, OBJ):
            return g, caminho, nos

        if estado in visit and visit[estado] <= g:
            continue

        visit[estado] = g

        for prox, mov in sucessores(estado, acoes):
            ng = g + 1

            if prox not in visit or visit[prox] > ng:
                nf = ng + heuristica(prox, OBJ)
                heapq.heappush(aberta, (nf, ng, prox, caminho + [mov]))

    return None, [], nos

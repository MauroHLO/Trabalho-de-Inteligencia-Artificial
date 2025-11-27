# bidirectional.py
# -----------------------------------------------------------------------
# Implementação de BUSCA BIDIRECIONAL para STRIPS (Mundo dos Blocos)
#
# Estados são tuples de ints representando proposições verdadeiras.
# Ações são objetos planner.actions.Acao.
#
# Objetivo OBJ é a lista de ints assinados:
#   +p → p deve ser verdadeiro
#   -p → p deve ser falso
#
# A busca ocorre simultaneamente:
#   - BFS a partir do INÍCIO
#   - BFS reversa a partir do OBJETIVO
#
# Quando as fronteiras se encontram, o caminho é reconstruído.
# -----------------------------------------------------------------------

from collections import deque
from planner.busca import satisfaz_objetivo, sucessores


# -----------------------------------------------------------------------
# Gera sucessores reversos (para BFS do lado do OBJETIVO)
# 
# Isso significa: ações que "desfazem" efeitos.
#
# Tecnicamente, um sucessor reverso é um estado anterior no qual
# aplicar a ação leva ao estado atual.
#
# Para isso, se ac.aplicar(X)=estado então X é um predecessor.
# -----------------------------------------------------------------------
def predecessores(estado, acoes):
    preds = []
    est_set = set(estado)

    for ac in acoes:
        # Para a ação ser "desfazível":
        # estado deve conter todos os efeitos positivos dela
        # e não conter os efeitos negativos
        ok = True

        for p in ac.add:
            if p not in est_set:
                ok = False
                break

        for p in ac.delete:
            if p in est_set:
                ok = False
                break

        if not ok:
            continue

        # Para obter o predecessor X, precisamos "remover add" e "adicionar delete"
        prev = set(est_set)
        for p in ac.add:
            prev.remove(p)
        for p in ac.delete:
            prev.add(p)

        preds.append((tuple(sorted(prev)), ac.nome))

    return preds


# -----------------------------------------------------------------------
# Reconstrói o caminho total quando as fronteiras se encontram.
# 
# pai_f : dict estado → (pai, nome_da_ação)
# pai_t : dict estado → (pai, nome_da_ação)
# encontro : estado onde as buscas se tocaram
# -----------------------------------------------------------------------
def reconstruir_caminho(encontro, pai_f, pai_t):
    caminho = []

    # ---- Do início até o nó de encontro
    atual = encontro
    seq_f = []
    while pai_f[atual] is not None:
        pai, acao = pai_f[atual]
        seq_f.append(acao)
        atual = pai
    seq_f.reverse()

    # ---- Do encontro até o objetivo (ações reversas)
    atual = encontro
    seq_t = []
    while pai_t[atual] is not None:
        pai, acao = pai_t[atual]
        seq_t.append(acao)
        atual = pai

    # Ações do lado "trás" precisam ser invertidas semanticamente.
    # Aqui mantemos o nome original mas é possível refinar se necessário.
    seq_total = seq_f + [f"(rev) {a}" for a in seq_t]

    return seq_total


# -----------------------------------------------------------------------
# Busca Bidirecional
# -----------------------------------------------------------------------
def bidirecional(INI, OBJ, acoes):
    """
    Retorna: (custo, caminho, nos_expandidos)
    """

    # Caso trivial
    if satisfaz_objetivo(INI, OBJ):
        return 0, [], 0

    # FRONT (da esquerda)
    frente = {INI}
    fila_f = deque([INI])
    pai_f = {INI: (None, None)}

    # BACK (meta →)
    # Para o lado do objetivo, precisamos de um ESTADO-OBJETIVO REAL
    # OBJ é parcial, então geramos um estado mínimo satisfatório
    objetivo = gerar_estado_objetivo_parcial(OBJ)
    tras = {objetivo}
    fila_t = deque([objetivo])
    pai_t = {objetivo: (None, None)}

    nos = 0

    while fila_f and fila_t:
        # ------------------------------------------------------
        # Expansão da frente
        # ------------------------------------------------------
        atual = fila_f.popleft()
        nos += 1

        for prox, acao in sucessores(atual, acoes):
            if prox not in frente:
                frente.add(prox)
                pai_f[prox] = (atual, acao)
                fila_f.append(prox)

                # Se encontrou o lado de trás
                if prox in tras:
                    caminho = reconstruir_caminho(prox, pai_f, pai_t)
                    return len(caminho), caminho, nos

        # ------------------------------------------------------
        # Expansão de trás (predecessores)
        # ------------------------------------------------------
        atual = fila_t.popleft()

        for prev, acao in predecessores(atual, acoes):
            if prev not in tras:
                tras.add(prev)
                pai_t[prev] = (atual, acao)
                fila_t.append(prev)

                if prev in frente:
                    caminho = reconstruir_caminho(prev, pai_f, pai_t)
                    return len(caminho), caminho, nos

    return None, [], nos


# -----------------------------------------------------------------------
# Gera um estado mínimo que satisfaz OBJ
#
# OBJ contém predicados +p e -p. Para construir um estado válido:
#   - inclua apenas os +p
#   - nunca inclua os -p
# -----------------------------------------------------------------------
def gerar_estado_objetivo_parcial(OBJ):
    est = []

    for g in OBJ:
        if g > 0:
            est.append(g)

    return tuple(sorted(est))

# heuristics.py
# -------------------------------------------------------------------
# Heurísticas para o planejador STRIPS do problema Block World
# -------------------------------------------------------------------
#
# Cada heurística recebe:
#   estado : tuple[int]
#   OBJ    : lista de ints assinados (positivo = deve ser verdadeiro,
#                                      negativo = deve ser falso)
#
# Retorna:
#   h(estado) : valor heurístico inteiro
#
# -------------------------------------------------------------------

def heuristica(estado, OBJ):
    """
    Heurística admissível simples:
    Conta quantos predicados do objetivo ainda NÃO estão satisfeitos.

    OBJ contém ints positivos e negativos:
        +p -> proposição p deve estar no estado
        -p -> proposição p deve NÃO estar no estado

    Isso é sempre admissível porque nunca superestima a distância.
    """
    est_set = set(estado)
    faltando = 0

    for g in OBJ:
        if g > 0:
            # objetivo positivo: precisa estar no estado
            if g not in est_set:
                faltando += 1
        else:
            # objetivo negativo: proposição -g deve estar ausente
            if -g in est_set:
                faltando += 1

    return faltando


# -------------------------------------------------------------------
# Se quiser adicionar mais heurísticas no futuro, coloque aqui:
#
# def h_max(...):
# def h_add(...):
# def h_relaxed(...):
#
# E no search.py basta trocar a heurística usada no A*.
# -------------------------------------------------------------------

# mapping.py
# -----------------------------------------------
# Mapeamento de proposições STRIPS para inteiros
# -----------------------------------------------
#
# Cada proposição (ex: "on_a_b") recebe um ID inteiro positivo.
# Estados são representados como tuplas ordenadas desses inteiros.
#
# Exemplo:
#   on_a_b    -> 1
#   clear_a   -> 2
#   ~clear_b  -> -3
#
# Esse arquivo é importado pelos módulos:
#   - parser.py
#   - actions.py
#   - search.py
#   - bidirectional.py
#
# -----------------------------------------------

propos_map = {}   # str -> int
propos_rev = {}   # int -> str
_next_pid = 1     # contador global de proposições


def get_pid(prop: str) -> int:
    """
    Retorna um ID inteiro único para a proposição 'prop'.
    Se a proposição ainda não existir no mapeamento, cria uma nova entrada.

    Parameters
    ----------
    prop : str
        Nome da proposição (sem "~")

    Returns
    -------
    int
        ID inteiro positivo associado à proposição.
    """
    global _next_pid

    if prop not in propos_map:
        propos_map[prop] = _next_pid
        propos_rev[_next_pid] = prop
        _next_pid += 1

    return propos_map[prop]

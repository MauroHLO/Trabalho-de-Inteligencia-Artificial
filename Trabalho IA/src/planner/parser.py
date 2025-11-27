# parser.py
# ---------------------------------------------------------------------
# Leitor de instâncias STRIPS no formato usado pelo problema Block World
# ---------------------------------------------------------------------
#
# Este arquivo contém:
#   - parse_token_list
#   - carregar_instancia
#
# Ele converte um arquivo .strips em:
#   INI  = estado inicial (tuple de ints positivos)
#   OBJ  = lista de ints assinados (predicados que devem ser verdadeiros ou falsos)
#   ações = lista de objetos Acao
#
# Formato esperado do arquivo (já validado nas instâncias enviadas):
#
#   nome_acao_1
#   precondicoes_1
#   efeitos_1
#   nome_acao_2
#   precondicoes_2
#   efeitos_2
#   ...
#   <estado_inicial>
#   <estado_objetivo>
#
# Últimas duas linhas SEMPRE são:
#   - estado inicial (somente verdadeiros)
#   - estado objetivo (verdadeiros e/ou negativos como "~prop")
#
# ---------------------------------------------------------------------

from planner.acoes import Acao
from planner.mapeamento import get_pid


# ---------------------------------------------------------------------
# Função auxiliar: quebra tokens separados por ';'
# ---------------------------------------------------------------------
def parse_token_list(line: str):
    """
    Recebe string 'a;b;~c' e retorna ['a', 'b', '~c'].
    Remove espaços e ignora strings vazias.
    """
    if not line:
        return []
    parts = [t.strip() for t in line.split(';') if t.strip() != ""]
    return parts


# ---------------------------------------------------------------------
# PARSER PRINCIPAL
# ---------------------------------------------------------------------
def carregar_instancia(path: str):
    """
    Lê uma instância STRIPS e retorna:
        (estado_inicial, objetivo, lista_de_acoes)

    Estado inicial:
        apenas proposições verdadeiras → ints positivos ordenados

    Objetivo:
        lista de ints assinados
            p   → proposição deve ser verdadeira
            -p  → proposição deve ser falsa

    Ações:
        criadas como objetos Acao
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw_lines = [l.rstrip("\n").strip() for l in f.readlines()]

    # Remove linhas vazias
    lines = [l for l in raw_lines if l != ""]

    if len(lines) < 3:
        raise ValueError("Arquivo STRIPS muito curto.")

    # As DUAS ÚLTIMAS LINHAS são sempre:
    # penúltima: estado inicial
    # última:    objetivo
    estado_inicial_line = lines[-2]
    objetivo_line = lines[-1]

    # Todas as linhas anteriores são ações (agrupadas de 3 em 3)
    action_lines = lines[:-2]

    if len(action_lines) % 3 != 0:
        raise ValueError(
            "Erro no arquivo STRIPS: ações deveriam vir em blocos de 3 linhas "
            "(nome / pre / post)."
        )

    acoes = []
    i = 0

    # ----------------------------------------------------------
    # PARSE DAS AÇÕES
    # ----------------------------------------------------------
    while i + 2 < len(action_lines):
        nome = action_lines[i]
        preline = action_lines[i + 1]
        postline = action_lines[i + 2]
        i += 3

        pre_tokens = parse_token_list(preline)
        post_tokens = parse_token_list(postline)

        pre_signed = []
        add = []
        delete = []

        # ---- pré-condições ----
        for tok in pre_tokens:
            if tok.startswith("~"):
                pid = get_pid(tok[1:])
                pre_signed.append(-pid)
            else:
                pid = get_pid(tok)
                pre_signed.append(pid)

        # ---- efeitos ----
        for tok in post_tokens:
            if tok.startswith("~"):
                pid = get_pid(tok[1:])
                delete.append(pid)
            else:
                pid = get_pid(tok)
                add.append(pid)

        acoes.append(Acao(nome, pre_signed, add, delete))

    # ----------------------------------------------------------
    # PARSE DO ESTADO INICIAL
    # ----------------------------------------------------------
    init_tokens = parse_token_list(estado_inicial_line)
    ini_set = set()

    for tok in init_tokens:
        if tok.startswith("~"):
            # geralmente não aparecem negativos no estado inicial,
            # mas tratamos caso exista.
            pid = get_pid(tok[1:])
            ini_set.discard(pid)
        else:
            pid = get_pid(tok)
            ini_set.add(pid)

    INI = tuple(sorted(ini_set))

    # ----------------------------------------------------------
    # PARSE DO OBJETIVO
    # ----------------------------------------------------------
    goal_tokens = parse_token_list(objetivo_line)
    OBJ = []

    for tok in goal_tokens:
        if tok.startswith("~"):
            pid = get_pid(tok[1:])
            OBJ.append(-pid)
        else:
            pid = get_pid(tok)
            OBJ.append(pid)

    return INI, tuple(OBJ), acoes

def carregar_strips(path):
    INI, OBJ, ACOES = carregar_instancia(path)
    return INI, OBJ, ACOES, None  # para manter 4 valores

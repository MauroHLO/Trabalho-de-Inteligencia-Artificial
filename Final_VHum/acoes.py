from dataclasses import dataclass
from typing import Set, Optional

# Representa uma ação do problema (nome, precondições e efeitos)
@dataclass
class Acao:
    acao: str
    precondicao: Set[int]
    poscondicao: Set[int]

# Nó usado na busca: guarda o estado, o pai e qual ação gerou o nó
@dataclass
class No:
    estado: Set[int]
    pai: Optional['No']
    acao: Optional[int]
    profundidade: Optional[int]

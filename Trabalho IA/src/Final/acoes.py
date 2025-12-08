from dataclasses import dataclass
from typing import Set, Optional

@dataclass
class Acao:
    acao: str
    precondicao: Set[int]
    poscondicao: Set[int]   

@dataclass
class No:
    estado: Set[int]
    pai: Optional['No']
    acao: Optional[int]
    profundidade: Optional[int]
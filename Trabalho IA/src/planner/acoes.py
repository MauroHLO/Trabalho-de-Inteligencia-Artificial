# actions.py
# --------------------------------------------------------
# Implementação da classe Acao para o planejador STRIPS
# --------------------------------------------------------
#
# Uma ação STRIPS possui:
#   - nome
#   - pré-condições (lista de ints: positivos = deve ser verdadeiro,
#                                     negativos = deve ser falso)
#   - efeitos: lista add (positivos) e delete (positivos)
#
# O estado é representado como uma tupla de inteiros positivos,
# contendo apenas proposições verdadeiras.
#
# Métodos principais:
#   - aplicavel(estado_set)
#   - aplicar(estado_set)
#
# --------------------------------------------------------

from typing import List, Set, Tuple


class Acao:
    """
    Representa uma ação STRIPS.

    Atributos:
    ----------
    nome : str
        Nome da ação STRIPS
    pre : List[int]
        Pré-condições assinadas:
            +p → proposição p deve estar no estado
            -p → proposição p deve NÃO estar no estado
    add : List[int]
        Proposições que se tornam verdadeiras após a ação
    delete : List[int]
        Proposições que se tornam falsas após a ação
    """

    def __init__(self, nome: str, pre_signed: List[int], add: List[int], delete: List[int]):
        self.nome = nome
        self.pre = pre_signed
        self.add = add
        self.delete = delete

    # ----------------------------------------------------

    def aplicavel(self, estado_set: Set[int]) -> bool:
        """
        Verifica se a ação pode ser aplicada no estado atual.

        estado_set : conjunto de proposições verdadeiras (positivas)
        """
        for p in self.pre:
            if p > 0:
                if p not in estado_set:
                    return False
            else:
                if -p in estado_set:
                    return False
        return True

    # ----------------------------------------------------

    def aplicar(self, estado_set: Set[int]) -> Tuple[int]:
        """
        Aplica a ação ao estado e retorna um novo estado.

        Regras:
          - adicionar proposições do add
          - remover proposições do delete
          - estado final retornado como tupla ordenada (imutável e hashable)
        """
        novo = set(estado_set)  # copia

        # remove efeitos negativos (delete)
        for d in self.delete:
            novo.discard(d)

        # adiciona efeitos positivos (add)
        for a in self.add:
            novo.add(a)

        return tuple(sorted(novo))

    # ----------------------------------------------------

    def __repr__(self):
        return f"Acao({self.nome})"

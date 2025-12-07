from collections import deque
from acoes import No, Acao


class Busca:
    def __init__(self, parste):
        self.parste = parste

    def verificarFinalizacao(self, estadoFinal, estadoAtual):
        return estadoFinal.issubset(estadoAtual)

    def verificaPreCondicao(self, acao: Acao, no: No):
        return acao.precondicao.issubset(no.estado)

    def verificaAntepassados(self, no: No, estadoAtual):
        while no is not None:
            if no.estado == estadoAtual:
                return False
            no = no.pai
        return True

    def imprimeEstado(self, no: No):
        nomes = [self.parste.mapeamentoReverso[i] for i in no.estado]
        print(", ".join(nomes))

    def imprimeArvore(self, no: No, n=0):
        if no.pai:
            n = self.imprimeArvore(no.pai)
            print("Ação:", self.parste.acoes[no.acao].acao)

        print(f"Estado {n}: ", end="")
        self.imprimeEstado(no)
        return n + 1

    def realizarAcao(self, acao, no):
        novoEstado = set(no.estado)

        for efeito in acao.poscondicao:
            if efeito > 0:
                novoEstado.add(efeito)
            else:
                novoEstado.discard(-efeito)

        return No(
            novoEstado,
            no,
            self.parste.get_pid(acao.acao),
            no.profundidade + 1
        )

    def buscaEmLargura(self):
        fila = deque([self.parste.noInicial])
        visitados = {frozenset(self.parste.noInicial.estado)}

        while fila:
            noAtual = fila.popleft()

            if self.verificarFinalizacao(self.parste.estadoFinal, noAtual.estado):
                return noAtual  # <-- NÃO imprime aqui

            for aid, acao in self.parste.acoes.items():
                if self.verificaPreCondicao(acao, noAtual):
                    novo = self.realizarAcao(acao, noAtual)
                    ef = frozenset(novo.estado)

                    if ef not in visitados:
                        visitados.add(ef)
                        fila.append(novo)

        return None

    def buscaEmProfundidadeLimitada(self, noAtual, limite):

        if self.verificarFinalizacao(self.parste.estadoFinal, noAtual.estado):
            return noAtual

        if noAtual.profundidade >= limite:
            return None

        for aid, acao in self.parste.acoes.items():
            if self.verificaPreCondicao(acao, noAtual):
                novo = self.realizarAcao(acao, noAtual)

                if not self.verificaAntepassados(noAtual, novo.estado):
                    continue

                resultado = self.buscaEmProfundidadeLimitada(novo, limite)
                if resultado is not None:
                    return resultado

        return None

    # -------------------------------
    # IDDFS
    # -------------------------------
    def iddfs(self, noInicial):

        limite = 1
        while True:
            resultado = self.buscaEmProfundidadeLimitada(noInicial, limite)

            if resultado is not None:
                return resultado 

            limite += 1

    def executar_busca(self, tipo="BFS", limite=None):

        if tipo == "BFS":
            resultado = self.buscaEmLargura()

        elif tipo == "DFS Limitada":
            if limite is None:
                raise ValueError("Para DLS (Busca em Profundidade Limitada), informe um limite.")
            resultado = self.buscaEmProfundidadeLimitada(self.parste.noInicial, limite)

        elif tipo == "IDS":
            resultado = self.iddfs(self.parste.noInicial)

        else:
            raise ValueError(f"Tipo de busca desconhecido: {tipo}")

        if resultado is not None:
            print("\n=== SOLUÇÃO ENCONTRADA ===")
            self.imprimeArvore(resultado)
        else:
            print("\nNenhuma solução encontrada.")

        return resultado

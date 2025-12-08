from collections import deque
from heapq import heappush, heappop
from itertools import count
from acoes import No, Acao
from typing import Set
import time


class Busca:
    def __init__(self, parser):
        self.parser = parser
        self.relevantes = set()

        if hasattr(self.parser, "estadoFinal") and hasattr(self.parser, "acoes"):
            self._build_relevantes()

    def _build_relevantes(self):
        self.relevantes = set()

        for p in self.parser.estadoFinal:
            self.relevantes.add(abs(p))

        for _, acao in self.parser.acoes.items():
            for p in acao.precondicao:
                self.relevantes.add(abs(p))
            for p in acao.poscondicao:
                self.relevantes.add(abs(p))

    # -------------------------
    # Funções utilitárias
    # -------------------------

    def verificarFinalizacao(self, objetivo: Set[int], estadoAtual: Set[int]):
        return objetivo.issubset(estadoAtual)

    def verificaPreCondicao(self, acao: Acao, no: No):
        return acao.precondicao.issubset(no.estado)

    # -------------------------
    # Impressão da solução
    # -------------------------

    def imprimeEstado(self, no: No):
        nomes = [self.parser.mapeamentoReverso[i] for i in no.estado]
        print(", ".join(nomes))

    def imprimeArvore(self, no: No, n=0):
        if no.pai:
            n = self.imprimeArvore(no.pai)
            if no.acao in self.parser.acoes:
                print("Ação:", self.parser.acoes[no.acao].acao)
            else:
                print("Ação PID:", no.acao)

        print(f"Estado {n}: ", end="")
        self.imprimeEstado(no)
        return n + 1

    # -------------------------
    # Aplicar ação
    # -------------------------

    def realizarAcao(self, acao: Acao, no: No):
        novoEstado = set(no.estado)

        for efeito in acao.poscondicao:
            if efeito > 0:
                novoEstado.add(efeito)
            else:
                novoEstado.discard(-efeito)

        return No(
            estado=novoEstado,
            pai=no,
            acao=self.parser.get_pid(acao.acao),
            profundidade=no.profundidade + 1
        )

    # --------------------------------------------
    # Filtrar ações relevantes (reduz a expansão)
    # --------------------------------------------

    def acao_relevante(self, acao: Acao):
        if not self.relevantes:
            self._build_relevantes()

        for e in acao.poscondicao:
            if e > 0 and e in self.relevantes:
                return True

        for p in acao.precondicao:
            if abs(p) in self.relevantes:
                return True

        return False

    # -------------------------
    # Busca em Largura (BFS)
    # -------------------------

    def buscaEmLargura(self):
        fila = deque([self.parser.noInicial])
        visitados = {frozenset(self.parser.noInicial.estado)}

        while fila:
            noAtual = fila.popleft()

            if self.verificarFinalizacao(self.parser.estadoFinal, noAtual.estado):
                return noAtual

            for _, acao in self.parser.acoes.items():
                if not self.acao_relevante(acao):
                    continue

                if self.verificaPreCondicao(acao, noAtual):
                    novo = self.realizarAcao(acao, noAtual)
                    est = frozenset(novo.estado)

                    if est not in visitados:
                        visitados.add(est)
                        fila.append(novo)

        return None

    # -------------------------
    # Heurística H_ADD (simples)
    # -------------------------

    def heuristica(self, estado, objetivo):
        custos = {lit: 0 for lit in estado}
        usadas = set()
        mudou = True

        while mudou:
            mudou = False

            if all(g in custos for g in objetivo):
                break

            for aid, acao in self.parser.acoes.items():
                if aid in usadas:
                    continue

                if acao.precondicao.issubset(custos.keys()):
                    custo_pre = [custos[p] for p in acao.precondicao]
                    novo_custo = 1 + sum(custo_pre) if custo_pre else 1

                    for efeito in acao.poscondicao:
                        if efeito not in custos or novo_custo < custos[efeito]:
                            custos[efeito] = novo_custo
                            mudou = True

                    usadas.add(aid)

        if not all(g in custos for g in objetivo):
            return float("inf")

        return sum(custos[g] for g in objetivo)

    # -------------------------
    # Busca A*
    # -------------------------

    def buscaAEstrela(self):
        self._build_relevantes()

        inicial = self.parser.noInicial
        objetivo = self.parser.estadoFinal

        g_ini = inicial.profundidade or 0
        h_ini = self.heuristica(inicial.estado, objetivo)
        f_ini = g_ini + h_ini

        heap = []
        contador = count()
        heappush(heap, (f_ini, h_ini, next(contador), inicial))

        visitados = {frozenset(inicial.estado & self.relevantes): g_ini}

        while heap:
            _, _, _, noAtual = heappop(heap)
            red = frozenset(noAtual.estado & self.relevantes)

            if self.verificarFinalizacao(objetivo, noAtual.estado):
                return noAtual

            for _, acao in self.parser.acoes.items():
                if not self.acao_relevante(acao):
                    continue
                if not self.verificaPreCondicao(acao, noAtual):
                    continue

                novo = self.realizarAcao(acao, noAtual)

                if self.verificarFinalizacao(objetivo, novo.estado):
                    return novo

                g = novo.profundidade
                h = self.heuristica(novo.estado, objetivo)
                f = g + h

                red_novo = frozenset(novo.estado & self.relevantes)

                if red_novo not in visitados or g < visitados[red_novo]:
                    visitados[red_novo] = g
                    heappush(heap, (f, h, next(contador), novo))

        return None

    # -------------------------
    # Dispatcher
    # -------------------------

    def executar_busca(self, tipo="BFS", limite=None):
        import tracemalloc

        tracemalloc.start()
        inicio_tempo = time.time()

        # --------------------
        # Seleção da busca
        # --------------------
        if tipo == "BFS":
            resultado = self.buscaEmLargura()
        elif tipo =="DLS":
            if limite is None:
                raise ValueError("Para DLS (Busca em Profundidade Limitada), informe um limite.")
            resultado = self.buscaEmProfundidadeLimitada(self.parste.noInicial, limite, {})
        elif tipo == "IDS":
            resultado = self.iddfs(self.parste.noInicial)
        elif tipo == "A*":
            resultado = self.buscaAEstrela()
        else:
            raise ValueError(f"Tipo de busca desconhecido: {tipo}")

        fim_tempo = time.time()
        tempo_total = fim_tempo - inicio_tempo

        # --------------------
        # Capturar memória usada
        # --------------------
        mem_atual, mem_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --------------------
        # Impressão
        # --------------------
        if resultado is not None:
            print("\n=== SOLUÇÃO ENCONTRADA ===")
            self.imprimeArvore(resultado)
            print(f"\nTempo de Execução: {tempo_total:.3f} segundos")
            print(f"Memória atual: {mem_atual / 1024:.2f} KB")
            print(f"Memória pico: {mem_pico / 1024:.2f} KB")
        else:
            print("\nNenhuma solução encontrada.")
            print(f"Tempo de Execução: {tempo_total:.3f} segundos")
            print(f"Memória atual: {mem_atual / 1024:.2f} KB")
            print(f"Memória pico: {mem_pico / 1024:.2f} KB")

        # --------------------
        # Retornar dados
        # --------------------
        return {
            "solucao": resultado,
            "tempo": tempo_total,
            "memoria_atual": mem_atual,
            "memoria_pico": mem_pico
        }
        
    # ----------------------------------------------------
    # Busca em Profundidade Limitada (usada por DLS/IDS)
    # ----------------------------------------------------

    def buscaEmProfundidadeLimitada(self, noAtual, limite, visitados):
        red = frozenset(noAtual.estado & self.relevantes)

        if red in visitados and visitados[red] <= noAtual.profundidade:
            return None

        visitados[red] = noAtual.profundidade

        if self.verificarFinalizacao(self.parser.estadoFinal, noAtual.estado):
            return noAtual

        if noAtual.profundidade >= limite:
            return None

        for _, acao in self.parser.acoes.items():
            if not self.acao_relevante(acao):
                continue
            if not self.verificaPreCondicao(acao, noAtual):
                continue

            novo = self.realizarAcao(acao, noAtual)
            r = self.buscaEmProfundidadeLimitada(novo, limite, visitados)

            if r is not None:
                return r

        return None

    # -------------------------
    # IDS
    # -------------------------

    def iddfs(self, noInicial):
        limite = 0
        while True:
            resultado = self.buscaEmProfundidadeLimitada(noInicial, limite, {})
            if resultado is not None:
                return resultado
            limite += 1

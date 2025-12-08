from collections import deque
from heapq import heappush, heappop
from itertools import count
from acoes import No, Acao
from typing import Set
import time


class Busca:
    def __init__(self, parste):
        self.parste = parste
        # Precompute conjunto de predicados "relevantes" para reduzir estados
        # Relevantes = todos os predicados que aparecem no objetivo OU em qualquer ação
        self.relevantes = set()
        # populate relevantes if parste already loaded (else refresh later)
        if hasattr(self.parste, "estadoFinal") and hasattr(self.parste, "acoes"):
            self._build_relevantes()

    def _build_relevantes(self):
        self.relevantes = set()
        # objetivo pode conter negativos (no seu modelo objetivo tinha ints assinados)
        for p in self.parste.estadoFinal:
            if p > 0:
                self.relevantes.add(p)
            else:
                # se objetivos negativos, considere a versão positiva como relevante também
                self.relevantes.add(-p)
        # incluir predicados de ações (pré e pos)
        for _, a in self.parste.acoes.items():
            for p in a.precondicao:
                if p > 0:
                    self.relevantes.add(p)
                else:
                    self.relevantes.add(-p)
            for p in a.poscondicao:
                if p > 0:
                    self.relevantes.add(p)
                else:
                    self.relevantes.add(-p)

    # -------------------------
    # Utilitários básicos
    # -------------------------
    def verificarFinalizacao(self, estadoFinal: Set[int], estadoAtual: Set[int]):
        # estadoFinal pode conter ints negativos (dependendo do parser),
        # mas no seu caso objetivo é subconjunto de estado positivo.
        return estadoFinal.issubset(estadoAtual)

    def verificaPreCondicao(self, acao: Acao, no: No):
        return acao.precondicao.issubset(no.estado)

    # -------------------------
    # Impressão
    # -------------------------
    def imprimeEstado(self, no: No):
        nomes = [self.parste.mapeamentoReverso[i] for i in no.estado]
        print(", ".join(nomes))

    def imprimeArvore(self, no: No, n=0):
        if no.pai:
            n = self.imprimeArvore(no.pai)
            # no.acao é o pid da ação; usamos parste.acoes para mapear
            if no.acao in self.parste.acoes:
                print("Ação:", self.parste.acoes[no.acao].acao)
            else:
                # fallback se acoes chave for diferente (caso raro)
                print("Ação PID:", no.acao)

        print(f"Estado {n}: ", end="")
        self.imprimeEstado(no)
        return n + 1

    # -------------------------
    # Aplica ação (gera novo nó)
    # -------------------------
    def realizarAcao(self, acao: Acao, no: No):
        # Criar novo estado de forma eficiente:
        # Partimos de uma cópia (necessário porque estados mudam)
        novoEstado = set(no.estado)

        for efeito in acao.poscondicao:
            if efeito > 0:
                novoEstado.add(efeito)
            else:
                novoEstado.discard(-efeito)

        # profundidade = no.profundidade + 1 (assumimos custo unitário)
        return No(
            novoEstado,
            no,
            self.parste.get_pid(acao.acao),
            no.profundidade + 1
        )

    # -------------------------
    # Filtro de relevância de ação (rápido)
    # ação é considerada relevante se:
    # - algum efeito positivo adiciona algo do objetivo OR
    # - alguma pré-condição é relevante (ajuda a conectar)
    # -------------------------
    def acao_relevante(self, acao: Acao):
        # Rápido check: se não construímos 'relevantes' ainda, construir agora
        if not self.relevantes:
            self._build_relevantes()
        # checar efeitos positivos
        for e in acao.poscondicao:
            if e > 0 and e in self.relevantes:
                return True
        # checar pré-condições (se pré é relevante)
        for p in acao.precondicao:
            if (p > 0 and p in self.relevantes) or (p < 0 and -p in self.relevantes):
                return True
        return False

    # -------------------------
    # Busca em largura (mantida sem mudanças importantes)
    # -------------------------
    def buscaEmLargura(self):
        fila = deque([self.parste.noInicial])
        visitados = {frozenset(self.parste.noInicial.estado)}

        while fila:
            noAtual = fila.popleft()

            if self.verificarFinalizacao(self.parste.estadoFinal, noAtual.estado):
                return noAtual

            for aid, acao in self.parste.acoes.items():
                # opcional: ainda é vantajoso filtrar ações irrelevantes
                if not self.acao_relevante(acao):
                    continue

                if self.verificaPreCondicao(acao, noAtual):
                    novo = self.realizarAcao(acao, noAtual)
                    ef = frozenset(novo.estado)

                    if ef not in visitados:
                        visitados.add(ef)
                        fila.append(novo)

        return None

    # -------------------------
    # Heurística simples admissível
    # -------------------------
    def heuristica(self, estado, objetivo):
        # Dicionário de custos para alcançar cada literal.
        # Inicializa fatos do estado atual com custo 0, outros com infinito.
        custos = {lit: 0 for lit in estado}

        # Conjunto de ações que já aplicamos "mentalmente"
        acoes_aplicadas = set()

        mudou = True
        while mudou:
            mudou = False

            # Verifica se já alcançamos todos os objetivos
            if all(g in custos for g in objetivo):
                break

            # Itera sobre ações
            for aid, acao in self.parste.acoes.items():
                if aid in acoes_aplicadas:
                    continue

                # Verifica se pré-condições são alcançáveis com o conhecimento atual
                if acao.precondicao.issubset(custos.keys()):

                    # Custo das precondições
                    custo_pre = [custos[p] for p in acao.precondicao]

                    # --- H_ADD: soma de custos das precondições ---
                    if not custo_pre:  # Sem precondições
                        novo_custo = 1
                    else:
                        novo_custo = 1 + sum(custo_pre)

                    # Aplica efeitos
                    for efeito in acao.poscondicao:
                        if efeito not in custos or novo_custo < custos[efeito]:
                            custos[efeito] = novo_custo
                            mudou = True

                    acoes_aplicadas.add(aid)

        # Se saiu do loop e ainda não tem os objetivos, é impossível
        if not all(g in custos for g in objetivo):
            return float('inf')

        # --- H_ADD: soma dos custos para alcançar cada meta ---
        return sum(custos[g] for g in objetivo)


    # -------------------------
    # A* otimizado
    # -------------------------
    def buscaAEstrela(self):
        # garantir relevantes atualizados
        self._build_relevantes()

        inicial = self.parste.noInicial
        objetivo = self.parste.estadoFinal

        # g_inicial = profundidade do inicial (assumimos 0)
        g_inicial = inicial.profundidade if inicial.profundidade is not None else 0
        h_inicial = self.heuristica(inicial.estado, objetivo)
        f_inicial = g_inicial + h_inicial

        heap = []
        contador = count()  # desempate estável

        heappush(heap, (f_inicial, h_inicial, next(contador), inicial))

        # visitados armazena g mínimo conhecido para o estado reduzido
        reduzido = frozenset(inicial.estado & self.relevantes)
        visitados = { reduzido: g_inicial }

        while heap:
            f_atual, h_atual, _, noAtual = heappop(heap)

            # Se este nó já foi expandido por um caminho melhor, pule
            reduzido_atual = frozenset(noAtual.estado & self.relevantes)
            g_atual = noAtual.profundidade
            if reduzido_atual in visitados and g_atual > visitados[reduzido_atual]:
                # já existe caminho melhor conhecido para esse estado reduzido
                continue

            # objetivo?
            if self.verificarFinalizacao(objetivo, noAtual.estado):
                return noAtual

            # expandir ações (filtrando irrelevantes)
            for aid, acao in self.parste.acoes.items():
                if not self.acao_relevante(acao):
                    continue
                if not self.verificaPreCondicao(acao, noAtual):
                    continue

                novo = self.realizarAcao(acao, noAtual)

                # early goal check para poupar trabalho
                if self.verificarFinalizacao(objetivo, novo.estado):
                    return novo

                g_novo = novo.profundidade  # custo acumulado (ações unitárias)
                h_novo = self.heuristica(novo.estado, objetivo)
                f_novo = g_novo + h_novo

                reduzido_novo = frozenset(novo.estado & self.relevantes)

                # se encontramos um caminho melhor para o estado reduzido, atualize e empurre
                if reduzido_novo not in visitados or g_novo < visitados[reduzido_novo]:
                    visitados[reduzido_novo] = g_novo
                    heappush(heap, (f_novo, h_novo, next(contador), novo))

        return None

    # -------------------------
    # Dispatcher (mantém compatibilidade)
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


    # ---------- Mantive DLS/IDDFS (sem mudanças adicionais) ----------
    def buscaEmProfundidadeLimitada(self, noAtual, limite, visitados):
        estado_red = frozenset(noAtual.estado & self.relevantes)

        # Se já visitado neste nível, não expandir
        if estado_red in visitados and visitados[estado_red] <= noAtual.profundidade:
            return None
        visitados[estado_red] = noAtual.profundidade

        # objetivo?
        if self.verificarFinalizacao(self.parste.estadoFinal, noAtual.estado):
            return noAtual

        if noAtual.profundidade >= limite:
            return None

        for aid, acao in self.parste.acoes.items():
            if not self.acao_relevante(acao):
                continue
            if not self.verificaPreCondicao(acao, noAtual):
                continue

            novo = self.realizarAcao(acao, noAtual)

            resultado = self.buscaEmProfundidadeLimitada(novo, limite, visitados)
            if resultado is not None:
                return resultado

        return None


    def iddfs(self, noInicial):
        limite = 0
        while True:
            visitados = {}
            resultado = self.buscaEmProfundidadeLimitada(noInicial, limite, visitados)
            if resultado is not None:
                return resultado
            limite += 1


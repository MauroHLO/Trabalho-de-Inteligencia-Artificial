from acoes import No, Acao
from collections import deque


class Parste:
    def __init__(self):
        self.mapeamento = {}
        self.mapeamentoReverso = {}
        self.acoes = {}
        self.contMap = 1

        self.estadoFinal = set()
        self.noInicial = No(estado=set(), pai=None, acao=None, profundidade=0)

        # 🔥 Novo: conjuntos pré-computados para otimização da busca
        self.predicados_relevantes = set()

    # ------------------------------------------------------
    # Otimização 1: evitar chamada dupla a mapeamentos
    # ------------------------------------------------------
    def get_pid(self, name):
        pid = self.mapeamento.get(name)
        if pid is None:
            pid = self.contMap
            self.mapeamento[name] = pid
            self.mapeamentoReverso[pid] = name
            self.contMap += 1
        return pid

    # ------------------------------------------------------
    # Otimização 2: split eficiente
    # ------------------------------------------------------
    @staticmethod
    def parse_token_list(line):
        if not line:
            return []
        return [t for t in line.split(";") if t]

    # ------------------------------------------------------
    # LEITURA DO ARQUIVO STRIPS
    # ------------------------------------------------------
    def lerArquivo(self, path: str):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            # 👇 Otimização: strip apenas 1x e ignorar vazios diretamente
            lines = [l.strip() for l in f if l.strip()]

        if len(lines) < 3:
            raise ValueError("Arquivo STRIPS muito curto.")

        # Últimas duas linhas sempre são EI e Objetivo
        action_lines = lines[:-2]
        init_line = lines[-2]
        goal_line = lines[-1]

        # Ações sempre vêm em blocos de 3
        if len(action_lines) % 3 != 0:
            raise ValueError("Erro: ações devem vir em blocos de 3 linhas.")

        # Limpar estruturas
        self.acoes.clear()
        self.estadoFinal.clear()
        self.noInicial.estado = set()
        self.predicados_relevantes.clear()

        # ------------------------------------------------------
        # PARSE DAS AÇÕES
        # ------------------------------------------------------
        for i in range(0, len(action_lines), 3):
            nome = action_lines[i]
            preline = action_lines[i + 1]
            postline = action_lines[i + 2]

            pre_toks = self.parse_token_list(preline)
            post_toks = self.parse_token_list(postline)

            pre = set()
            pos = set()

            # 🔥 Otimização: repetir menos chamadas a string.startswith
            for tk in pre_toks:
                if tk[0] == "~":
                    pid = self.get_pid(tk[1:])
                    pre.add(-pid)
                    self.predicados_relevantes.add(pid)
                else:
                    pid = self.get_pid(tk)
                    pre.add(pid)
                    self.predicados_relevantes.add(pid)

            for tk in post_toks:
                if tk[0] == "~":
                    pid = self.get_pid(tk[1:])
                    pos.add(-pid)
                    self.predicados_relevantes.add(pid)
                else:
                    pid = self.get_pid(tk)
                    pos.add(pid)
                    self.predicados_relevantes.add(pid)

            oid = self.get_pid(nome)
            self.acoes[oid] = Acao(nome, pre, pos)

        # ------------------------------------------------------
        # PARSE ESTADO INICIAL
        # ------------------------------------------------------
        for tk in self.parse_token_list(init_line):
            if tk[0] == "~":
                pid = self.get_pid(tk[1:])
                self.noInicial.estado.discard(pid)
            else:
                pid = self.get_pid(tk)
                self.noInicial.estado.add(pid)

        # ------------------------------------------------------
        # PARSE OBJETIVO
        # ------------------------------------------------------
        for tk in self.parse_token_list(goal_line):
            if tk[0] == "~":
                pid = self.get_pid(tk[1:])
                self.estadoFinal.add(-pid)
                self.predicados_relevantes.add(pid)
            else:
                pid = self.get_pid(tk)
                self.estadoFinal.add(pid)
                self.predicados_relevantes.add(pid)

    # ------------------------------------------------------
    # Funções utilitárias (inalteradas)
    # ------------------------------------------------------
    def verificarFinalizacao(self, estado):
        return self.estadoFinal.issubset(estado)

    def realizarAcao(self, acao: Acao, no: No):
        novoEstado = set(no.estado)
        for efeito in acao.poscondicao:
            if efeito > 0:
                novoEstado.add(efeito)
            else:
                novoEstado.discard(-efeito)

        return No(
            novoEstado,
            no,
            self.get_pid(acao.acao),
            no.profundidade + 1
        )

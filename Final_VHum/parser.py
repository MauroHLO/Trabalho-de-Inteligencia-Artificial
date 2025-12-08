from acoes import No, Acao


class Parser:
    def __init__(self):
        self.mapeamento = {}
        self.mapeamentoReverso = {}
        self.contMap = 1

        self.acoes = {}

        self.estadoFinal = set()
        self.noInicial = No(estado=set(), pai=None, acao=None, profundidade=0)

        self.predicados_relevantes = set()

    def get_pid(self, nome):
        pid = self.mapeamento.get(nome)
        if pid is None:
            pid = self.contMap
            self.mapeamento[nome] = pid
            self.mapeamentoReverso[pid] = nome
            self.contMap += 1
        return pid

    @staticmethod
    def parse_token_list(line):
        if not line:
            return []
        return [t for t in line.split(";") if t]

    # ------------------------------------------------------
    # Leitura do arquivo STRIPS
    # ------------------------------------------------------
    def lerArquivo(self, path: str):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            linhas = [l.strip() for l in f if l.strip()]

        if len(linhas) < 3:
            raise ValueError("Arquivo STRIPS muito curto.")

        action_lines = linhas[:-2]
        init_line = linhas[-2]
        goal_line = linhas[-1]

        # Blocos de ação sempre têm 3 linhas (nome, pré, pós)
        if len(action_lines) % 3 != 0:
            raise ValueError("As ações devem vir em blocos de 3 linhas.")

        self.acoes.clear()
        self.estadoFinal.clear()
        self.noInicial.estado = set()
        self.predicados_relevantes.clear()

        # ------------------------------------------------------
        # Leitura das ações
        # ------------------------------------------------------
        for i in range(0, len(action_lines), 3):
            nome = action_lines[i]
            pre_raw = self.parse_token_list(action_lines[i + 1])
            pos_raw = self.parse_token_list(action_lines[i + 2])

            pre = set()
            pos = set()

            # Lê pré-condições
            for tk in pre_raw:
                if tk.startswith("~"):
                    pid = self.get_pid(tk[1:])
                    pre.add(-pid)
                else:
                    pid = self.get_pid(tk)
                    pre.add(pid)

                self.predicados_relevantes.add(abs(pid))

            # Lê efeitos
            for tk in pos_raw:
                if tk.startswith("~"):
                    pid = self.get_pid(tk[1:])
                    pos.add(-pid)
                else:
                    pid = self.get_pid(tk)
                    pos.add(pid)

                self.predicados_relevantes.add(abs(pid))

            # ID da ação
            aid = self.get_pid(nome)
            self.acoes[aid] = Acao(nome, pre, pos)

        # ------------------------------------------------------
        # Estado inicial
        # ------------------------------------------------------
        for tk in self.parse_token_list(init_line):
            if tk.startswith("~"):
                pid = self.get_pid(tk[1:])
                self.noInicial.estado.discard(pid)
            else:
                pid = self.get_pid(tk)
                self.noInicial.estado.add(pid)

        # ------------------------------------------------------
        # Objetivo
        # ------------------------------------------------------
        for tk in self.parse_token_list(goal_line):
            if tk.startswith("~"):
                pid = self.get_pid(tk[1:])
                self.estadoFinal.add(-pid)
            else:
                pid = self.get_pid(tk)
                self.estadoFinal.add(pid)

            self.predicados_relevantes.add(abs(pid))

    # ------------------------------------------------------
    # Funções utilitárias
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

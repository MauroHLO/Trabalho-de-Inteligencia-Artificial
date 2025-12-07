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

    def get_pid(self, name):
        if name not in self.mapeamento:
            self.mapeamento[name] = self.contMap
            self.mapeamentoReverso[self.contMap] = name
            self.contMap += 1
        return self.mapeamento[name]

    def parse_token_list(self, line):
        if not line:
            return []
        return [t.strip() for t in line.split(";") if t.strip() != ""]

    def lerArquivo(self, path: str):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw_lines = [l.rstrip("\n").strip() for l in f.readlines()]

        lines = [l for l in raw_lines if l != ""]

        if len(lines) < 3:
            raise ValueError("Arquivo STRIPS muito curto.")

        estado_inicial_line = lines[-2]
        objetivo_line = lines[-1]
        action_lines = lines[:-2]

        if len(action_lines) % 3 != 0:
            raise ValueError("Erro: ações devem vir em blocos de 3 linhas.")

        self.acoes.clear()
        self.estadoFinal.clear()
        self.noInicial.estado = set()

        i = 0
        while i + 2 < len(action_lines):
            nome = action_lines[i]
            preline = action_lines[i + 1]
            postline = action_lines[i + 2]
            i += 3

            pre_toks = self.parse_token_list(preline)
            post_toks = self.parse_token_list(postline)

            pre = set()
            pos = set()

            for tk in pre_toks:
                if tk.startswith("~"):
                    pid = self.get_pid(tk[1:])
                    pre.add(-pid)
                else:
                    pid = self.get_pid(tk)
                    pre.add(pid)

            for tk in post_toks:
                if tk.startswith("~"):
                    pid = self.get_pid(tk[1:])
                    pos.add(-pid)
                else:
                    pid = self.get_pid(tk)
                    pos.add(pid)

            oid = self.get_pid(nome)
            self.acoes[oid] = Acao(nome, pre, pos)

        init_toks = self.parse_token_list(estado_inicial_line)

        for tk in init_toks:
            if tk.startswith("~"):
                pid = self.get_pid(tk[1:])
                self.noInicial.estado.discard(pid)
            else:
                pid = self.get_pid(tk)
                self.noInicial.estado.add(pid)
                
        goal_toks = self.parse_token_list(objetivo_line)

        for tk in goal_toks:
            if tk.startswith("~"):
                pid = self.get_pid(tk[1:])
                self.estadoFinal.add(-pid)
            else:
                pid = self.get_pid(tk)
                self.estadoFinal.add(pid)

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

    def verificaPreCondicao(self, acao: Acao, no: No):
        return acao.precondicao.issubset(no.estado)

    def imprimeEstado(self, no: No):
        print(", ".join(self.mapeamentoReverso[i] for i in no.estado))

    def imprimeArvore(self, no: No, n=0):
        if no.pai:
            n = self.imprimeArvore(no.pai)
            print("Ação:", self.acoes[no.acao].acao)
        print(f"Estado {n}: ", end="")
        self.imprimeEstado(no)
        return n + 1

    def buscaEmLargura(self):
        fila = deque([self.noInicial])
        visitados = {frozenset(self.noInicial.estado)}

        while fila:
            noAtual = fila.popleft()

            if self.verificarFinalizacao(noAtual.estado):
                print("\n=== SOLUÇÃO ENCONTRADA ===")
                self.imprimeArvore(noAtual)
                return noAtual

            for aid, acao in self.acoes.items():
                if self.verificaPreCondicao(acao, noAtual):
                    novo = self.realizarAcao(acao, noAtual)
                    ef = frozenset(novo.estado)
                    if ef not in visitados:
                        visitados.add(ef)
                        fila.append(novo)

        print("Nenhuma solução encontrada.")
        return None

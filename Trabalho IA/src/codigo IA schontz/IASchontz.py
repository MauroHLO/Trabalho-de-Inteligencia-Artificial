from dataclasses import dataclass
from typing import Set, Optional
from collections import deque

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

mapeamento = {}
mapeamentoReverso = {}
acoes = {}
contMap = 1
setVazio = set()
noInicial = No(estado=setVazio, pai=None, acao=None, profundidade=0)
estadoFinal = set()

def mapear(representacao):
    if representacao not in mapeamento:
        global contMap
        mapeamento[representacao] = contMap
        mapeamentoReverso[contMap] = representacao
        contMap += 1



def lerArquivo(caminho):
    global estadoFinal
    global noInicial
    global acoes
    with open(caminho, "r") as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    i = 0
    for linha in linhas:
        for representacao in linha.split(";"):
            if "~" in representacao:
                mapear(representacao[1:])
            else:
                mapear(representacao)
            if linha == linhas[-2]:
                noInicial.estado.add(mapeamento[representacao])
            elif linha == linhas[-1]:
                estadoFinal.add(mapeamento[representacao])
    for linha in linhas:
        if linha == linhas[-2]:
            break
        if i % 3 == 0:
            pre = set()
            pos = set()
            for representacao in linhas[i+1].split(";"):
                pre.add(mapeamento[representacao])
            for representacao in linhas[i+2].split(";"):
                if "~" in representacao:
                    pos.add(-mapeamento[representacao[1:]])
                else:
                    pos.add(mapeamento[representacao])
            acao = Acao(acao=linha, precondicao=pre, poscondicao=pos)
            acoes[mapeamento[acao.acao]] = acao
        i += 1


def verificarFinalizacao(estado):
    if estadoFinal.issubset(estado):
        return True
    return False


def realizarAcao(acao:Acao, no:No):
    novoEstado = set(no.estado)
    for i in acao.poscondicao:
        i = int(i)
        if i > 0:
            novoEstado.add(i)
        else:
            novoEstado.remove(i*-1)
    return No(estado=novoEstado, pai=no, acao=mapeamento[acao.acao], profundidade=no.profundidade +1)

def verificaPreCondicao(acao:Acao, no:No):
    if acao.precondicao.issubset(no.estado):
        return True
    else:
        return False

def imprimeArvore(no:No, numero = 0):
    if no.pai != None:
        numero = imprimeArvore(no.pai)
        print(f"Acao realizada: {acoes[mapeamento[mapeamentoReverso[no.acao]]].acao}")
    print(f'Estado {numero}', end=': ')
    imprimeEstado(no)
    return numero + 1

def imprimeEstado(no: No):
    for i in no.estado:
        print(mapeamentoReverso[i], end=', ')
    print()


def buscaEmLargura(): # maior valor encondrado com 9 blocos
    fila = deque()
    visitados = set()
    fila.append(noInicial)
    visitados.add(frozenset(noInicial.estado))
    while len(fila) > 0:
        noAtual = fila.popleft()
        if verificarFinalizacao(noAtual.estado):
            print("\n=== SOLUÇÃO ENCONTRADA ===")
            imprimeArvore(noAtual)
            return noAtual
        for inteiro, acao in acoes.items():
            if verificaPreCondicao(acao, noAtual):
                novoNo = realizarAcao(acao, noAtual)
                estadoCongelado = frozenset(novoNo.estado)
                if estadoCongelado not in visitados:
                    visitados.add(estadoCongelado)
                    fila.append(novoNo)
    print("Nenhuma solução encontrada.")
    return None


def buscaEmProfundidadeLimitada(limite):
    # Pilha normal
    pilha = [noInicial]

    while pilha:
        noAtual = pilha.pop()

        # Achou objetivo?
        if verificarFinalizacao(noAtual.estado):
            print("\n=== SOLUÇÃO ENCONTRADA ===")
            imprimeArvore(noAtual)
            return True

        # Verifica limite
        if noAtual.profundidade >= limite:
            continue

        # Expande ações
        for inteiro, acao in acoes.items():
            if verificaPreCondicao(acao, noAtual):
                novoNo = realizarAcao(acao, noAtual)
                pilha.append(novoNo)

    return False


def buscaEmProfundidadeIterativa():
    limite = 1
    resultado = buscaEmProfundidadeLimitada(limite)
    while not resultado:
        limite += 1
        resultado = buscaEmProfundidadeLimitada(limite)







lerArquivo("blocks-9-0.strips")
buscaEmLargura()


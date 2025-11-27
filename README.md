# Trabalho-de-Inteligencia-Artificial
📦 Mundo dos Blocos STRIPS Planner

Este repositório contém um planejador STRIPS completo para o problema clássico Mundo dos Blocos, implementado como trabalho da disciplina de Inteligência Artificial.

O planejador suporta:

✔ Interpretador de STRIPS

✔ Estados representados como proposições inteiras

✔ Todas as ações definidas via parsing

✔ Objetivos parciais

✔ Várias técnicas de busca computacional:

BFS

DFS limitada

IDS

A* (com heurística admissível)

Bidirecional avançada

✔ Execução via CLI

📁 Estrutura do projeto
src/
  planner/
    parser.py        → lê e interpreta arquivos .strips
    mapeamento.py       → gerencia proposições e mapeamento string ↔ int
    acoes.py       → classe Acao (pré-condições e efeitos)
    heuristicas.py    → heurísticas admissíveis para A*
    busca.py        → BFS, DFS, IDS, A*
    bidirecional.py → busca bidirecional
  main.py            → ponto de entrada do programa

instancias/
  blocks-4-0.strips
  blocks-4-1.strips
  blocks-4-2.strips
  ...

▶ Como executar

Na raiz do projeto:

python src/main.py instancias/blocks-10-0.strips

Saída típica:

Lendo instância: blocks-10-0.strips
Proposições: 120
Ações: 650
====================================================================
BFS             | Custo:  14 | Nós:   87453 | Tempo:  531.22 ms
DFS limitada    | Custo: None | Nós:  300000 | Tempo:  411.12 ms
IDS             | Custo:  14 | Nós:  210434 | Tempo: 1212.88 ms
A*              | Custo:  14 | Nós:   46291 | Tempo:  178.65 ms
Bidirecional    | Custo:  14 | Nós:    8012 | Tempo:   55.22 ms

📘 Formato das instâncias

As instâncias seguem o padrão STRIPS:

# Comentários

Proposicoes:
On(A,B)
OnTable(A)
Clear(A)
...

Inicio:
On(C,A)
Clear(C)
...

Objetivo:
On(A,B)
Clear(A)
...

Acoes:
Action Move(A,Table,B)
Pre: Clear(A) ^ On(A,Table) ^ Clear(B)
Add: On(A,B) ^ Clear(Table)
Del: On(A,Table) ^ Clear(B)

...

Tudo é processado automaticamente.


🧠 Heurísticas

Atualmente o sistema inclui:

🟦 heurística básica (admissível)

Conta quantas metas ainda não foram satisfeitas.


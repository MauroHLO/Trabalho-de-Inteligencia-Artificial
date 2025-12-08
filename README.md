🧠 Planejador STRIPS – Mundo dos Blocos

Trabalho da disciplina de Inteligência Artificial

Este repositório contém um planejador STRIPS funcional para o clássico Mundo dos Blocos, incluindo:

interpretação completa de instâncias em formato .strips

representação interna usando proposições inteiras

pré-condições e efeitos de ações

estado inicial e objetivo lidos diretamente do arquivo

várias estratégias de busca

A implementação combina ideia estrutural original com otimizações e melhorias feitas ao longo do desenvolvimento da equipe.

🚀 Funcionalidades principais
✔ Leitura completa de arquivos STRIPS

O parser identifica automaticamente:

ações (nome, pré-condições e efeitos)

estado inicial

estado objetivo

Tudo é convertido para IDs inteiros para facilitar a busca.

✔ Suporte a várias técnicas de busca

Implementamos:

BFS (amplitude)

DLS – Busca em profundidade limitada

IDS – Iterative Deepening Search

A* (com heurística H_ADD simplificada)

Bidirecional (opção listada, mas não integrada na versão atual)

✔ Caminho da solução mostrado passo a passo

A saída imprime a sequência de ações realizadas e todos os estados intermediários.

📁 Estrutura do Projeto
Trabalho IA/
│
├── instancias/
│     ├── blocks-4-0.strips
│     ├── blocks-10-0.strips
│     └── ...
│
└── src/
      ├── main.py          → interface CLI e fluxo de execução
      ├── parser.py        → leitura e interpretação dos arquivos .strips
      ├── busca.py         → algoritmos de busca + heurística
      └── acoes.py         → definição das classes Acao e No

▶ Como executar

No terminal, dentro da pasta Trabalho IA:

python src/main.py


O programa irá:

listar os arquivos .strips na pasta instancias/

pedir para você escolher uma instância

pedir para escolher o algoritmo de busca

executar e mostrar a solução (quando houver)

Alternativamente, você pode passar o caminho direto:
python src/main.py instancias/blocks-4-0.strips

📝 Formato das instâncias STRIPS

Cada arquivo .strips segue o padrão:

Linha 1: nome da ação

Linha 2: pré-condições (separadas por ;)

Linha 3: efeitos (separados por ;)

(repete para todas as ações)

Penúltima linha: estado inicial

Última linha: objetivo

Exemplo simplificado:

unstack_c_d
clear_c;on_c_d
clear_d;holding_c;~on_c_d

putdown_c
holding_c
on_c_table;clear_c

clear_a;on_b_a
...

clear_c
on_a_b


Observação:
~predicado significa negação (efeito de remoção).

O parser converte tudo para inteiros, tratando:

positivos → fatos verdadeiros

negativos → fatos removidos durante a aplicação da ação

🔍 Heurística

O algoritmo A* utiliza uma versão simplificada da H_ADD, baseada na soma dos custos para alcançar os literais do objetivo:

custo do estado atual é 0

aplicar ação tem custo 1

efeitos vão se acumulando até possibilitar alcançar todos os objetivos

É leve o suficiente para instâncias pequenas e médias.

👥 Equipe

Implementação desenvolvida por um grupo de alunos da disciplina de IA, combinando:

parsing manual otimizado

representação por proposições inteiras

estratégias tradicionais de busca

melhorias sugeridas durante o processo

O código foi retrabalhado para ficar claro, consistente e legível para qualquer membro da equipe ou avaliador.

📌 Observação importante

Pastas devem manter a seguinte estrutura para evitar erros de caminho:

Trabalho IA/
    src/
        main.py
        parser.py
        busca.py
        acoes.py
    instancias/
        *.strips


A execução deve ser feita a partir da raiz do projeto.

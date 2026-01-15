import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from codigo.parser import Parser
from codigo.busca import Busca

PASTA_INSTANCIAS = r"C:\Users\Bernardo\Downloads\Trabalho-de-Inteligencia-Artificial-main(1)\Trabalho-de-Inteligencia-Artificial-main\Trabalho IA_Final\src\instancias"

def escolher_arquivo():
    print("\nInstâncias disponíveis:\n")
    if not os.path.isdir(PASTA_INSTANCIAS):
        print(f"Erro: pasta '{PASTA_INSTANCIAS}' não encontrada.")
        sys.exit(1)

    arquivos = [f for f in os.listdir(PASTA_INSTANCIAS) if f.endswith(".strips")]
    if not arquivos:
        print("Nenhum arquivo .strips encontrado.")
        sys.exit(1)

    for i, nome in enumerate(arquivos, 1):
        print(f"{i}. {nome}")

    escolha = int(input("\nEscolha o número da instância: "))
    return os.path.join(PASTA_INSTANCIAS, arquivos[escolha - 1])

def gerar_graficos(resultados):
    algos = [r['algo'] for r in resultados]
    nos = [r['nos_expandidos'] for r in resultados]
    tempos = [r['tempo'] for r in resultados]

    # Cores neutras e profissionais (Hexadecimal)
    # Azul acinzentado, Bege acinzentado, Verde sálvia, Ardósia
    cores_neutras = ['#778899', '#B0C4DE', '#A3B18A', '#95A5A6']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # --- Gráfico 1: Nós Expandidos ---
    ax1.bar(algos, nos, color=cores_neutras, edgecolor='#4D4D4D', linewidth=1)
    ax1.set_title('Nós Expandidos', fontsize=12, color='#2C3E50', fontweight='bold')
    ax1.set_ylabel('Quantidade de Nós', color='#2C3E50')
    ax1.tick_params(colors='#2C3E50') # Cor dos números nos eixos
    ax1.grid(axis='y', linestyle='-', alpha=0.3) # Grade bem sutil
    ax1.spines['top'].set_visible(False) # Remove borda de cima
    ax1.spines['right'].set_visible(False) # Remove borda da direita

    # --- Gráfico 2: Tempo Decorrido ---
    ax2.bar(algos, tempos, color=cores_neutras, edgecolor='#4D4D4D', linewidth=1)
    ax2.set_title('Tempo de Execução (s)', fontsize=12, color='#2C3E50', fontweight='bold')
    ax2.set_ylabel('Segundos', color='#2C3E50')
    ax2.tick_params(colors='#2C3E50')
    ax2.grid(axis='y', linestyle='-', alpha=0.3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()

def main():
    # 1. Escolha do arquivo (uma única vez)
    caminho = escolher_arquivo()
    
    ambiente = Parser()
    ambiente.lerArquivo(caminho)
    busca = Busca(ambiente)

    # 2. Definição dos algoritmos a serem testados
    # Removi "Bidirecional" pois ele não estava implementado no seu snippet anterior
    testes = [
        {"nome": "BFS", "limite": None},
        {"nome": "DLS", "limite": 100},
        {"nome": "IDS", "limite": None},
        {"nome": "A*",  "limite": None}
    ]

    lista_resultados = []

    print(f"\nIniciando Benchmark na instância: {os.path.basename(caminho)}")
    print("=" * 70)

    # 3. Execução em loop
    for teste in testes:
        print(f"\n>>> Executando {teste['nome']}...")
        dados = busca.executar_busca(teste['nome'], teste['limite'])
        
        # Armazena apenas o necessário para o gráfico
        lista_resultados.append({
            "algo": teste['nome'],
            "nos_expandidos": dados["nos_expandidos"],
            "tempo": dados["tempo"]
        })

    # 4. Exibição dos gráficos comparativos
    import numpy as np # Import necessário para as cores
    gerar_graficos(lista_resultados)

if __name__ == "__main__":
    main()
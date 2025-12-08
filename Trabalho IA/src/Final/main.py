import os
import sys
from parser import Parser
from busca import Busca

PASTA_INSTANCIAS = r"Trabalho IA\src\instancias"


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

    print()
    escolha = int(input("Escolha o número da instância: "))

    return os.path.join(PASTA_INSTANCIAS, arquivos[escolha - 1])


def escolher_algoritmo():
    print("\nAlgoritmos disponíveis:\n")
    algoritmos = ["BFS", "DLS", "IDS", "A*", "Bidirecional"]

    for i, nome in enumerate(algoritmos, 1):
        print(f"{i}. {nome}")

    print()
    escolha = int(input("Escolha um algoritmo: "))

    limite = None
    if escolha == 2:  # DLS
        limite = int(input("Defina o limite para a busca: "))

    return algoritmos[escolha - 1], limite


def main():
    for _ in range(4):
        if len(sys.argv) == 1:
            caminho = escolher_arquivo()
        else:
            caminho = sys.argv[1]

        print(f"\nLendo instância: {caminho}")
        print("=" * 70)

        ambiente = Parser()
        ambiente.lerArquivo(caminho)

        busca = Busca(ambiente)

        alg, limite = escolher_algoritmo()
        busca.executar_busca(alg, limite)


if __name__ == "__main__":
    main()

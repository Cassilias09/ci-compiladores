import sys
from lexical_analysis.lexical_analyzer import LexicalAnalyzer
from syntatic_analysis.syntactical_analyzer import SyntacticalAnalyzer
from exceptions.exception_list import ExceptionList


def main():
    if len(sys.argv) != 2:
        print("Erro: Número incorreto de argumentos.")
        print("Uso correto: python compiler.py <source_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)

    try:
        print("Iniciando análise léxica do arquivo:", file_path)

        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(source_code)

        print("Análise léxica concluída. Tokens gerados:\n")

        for token in tokens:
            print(token)

        print("\nIniciando análise sintática do arquivo:", file_path)
        analyzer = SyntacticalAnalyzer(tokens)
        trees = analyzer.parse()
    except ExceptionList as e:
        print(e)
        sys.exit(1)

    print("Análise sintática concluída. Árvores sintáticas geradas:\n")
    for i, tree in enumerate(trees):
        print(f"Árvore sintática linha {i + 1}:\n")
        tree.display()
        print("\n")


if __name__ == "__main__":
    main()

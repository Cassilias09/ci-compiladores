import sys
from exceptions.lexical_exception import LexicalException
from lexical_analysis.lexical_analyzer import LexicalAnalyzer
from exceptions.syntactical_exception import SyntacticalException
from syntatic_analysis.syntactical_analyzer import SyntacticalAnalyzer


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

    print("Iniciando análise léxica do arquivo:", file_path)

    analyzer = LexicalAnalyzer()
    try:
        tokens = analyzer.analyze(source_code)
    except LexicalException as e:
        print(f"Erro durante a análise léxica: {e}")
        sys.exit(1)

    print("Análise léxica concluída. Tokens gerados:\n")

    for token in tokens:
        print(token)

    print("\nIniciando análise sintática do arquivo:", file_path)
    analyzer = SyntacticalAnalyzer(tokens)
    try:
        tree = analyzer.parse()
    except SyntacticalException as e:
        print(f"Erro durante a análise sintática: {e}")
        sys.exit(1)

    print("Análise sintática concluída. Árvore sintática gerada:\n")
    tree.display()


if __name__ == "__main__":
    main()

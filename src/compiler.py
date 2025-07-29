import sys
from lexical_analysis.lexical_analyzer import LexicalAnalyzer
from syntatic_analysis.syntactical_analyzer import SyntacticalAnalyzer
from exceptions.exception_list import ExceptionList
from arguments import Arguments


def main():
    args = Arguments().parse(sys.argv[1:])
    file_path = args.input_path
    output_path = args.output

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
        syntactic_tree = analyzer.parse()

        print("Análise sintática concluída. Árvores sintáticas geradas:\n")
        syntactic_tree.display()
        print("\n")

        print("Iniciando geração de código assembly...")
        code = syntactic_tree.generate_code()
        print(code)

        if output_path:
            with open(output_path, "w") as file:
                file.write(code)

    except ExceptionList as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

# ci-compiladores
Repositório para colocar os trabalhos realizados na disciplina de Construção de Compiladores, do curso de Ciência da Computação.

## Documentação de Uso

### Como utilizar o compilador

1. Execução do compilador

   - Para executar o compilador, usar o seguinte comando na raiz do projeto
   ```bash
   python3 src/compiler.py inputs/<arquivo_teste>.ci -o <arquivo_teste>.s
   ```
   - Para montar e linkar o arquivo assembly gerado pelo compilador, executar
   ```bash
   as --64 -o <arquivo_teste>.o <arquivo_teste>.s
   ld -o <arquivo_teste> <arquivo_teste>.o
   ```
   - Para verificar o resultado da compilação, executar o programa gerado com o comando
   ```bash
   inputs/<arquivo_teste>
   ```

2. Para validação no output da análise léxica, árvore sintática e código assembly gerado na compilação, executar o comando com a flag --verbose
   ```bash
   python3 src/compiler.py inputs/<arquivo_teste>.ci --verbose
   ```
   - O analisador irá:
      - Realizar a análise léxica do arquivo informado, exibindo os tokens gerados.
      - Realizar a análise sintática, exibindo as árvores sintáticas geradas para cada linha do programa.
      - Em caso de erro léxico ou sintático, o erro será reportado no terminal e a execução será interrompida.

3. Ainda, para evitar a execução de múltiplos comandos e a manipulação de vários arquivos, executar o comando
   ```bash
   ./compile_and_run.sh inputs/<arquivo_teste>.ci
   ```
   - Este comando executa o compilador, faz a montagem e linkagem do programa, retorna o resultado final e remove os arquivos .s e .o resultantes da execução


4. Para exemplo de funcionamento do compilador, seguem os seguintes arquivos de teste na pasta inputs:
   - cod.ci
   - fun.ci
   - fib.ci
   - programa.ci
   - novoTeste.ci
   - test_all_comparisons.ci
   - test_comparison.ci
   - test_false_comparisons.ci
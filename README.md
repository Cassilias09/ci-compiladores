# ci-compiladores
Repositório para colocar os trabalhos realizados na disciplina de Construção de Compiladores, do curso de Ciência da Computação.

## Especificações dos Testes

O projeto deve incluir um conjunto de testes que verifica:
- A produção correta da árvore sintática para um conjunto de programas válidos.
- O valor do programa obtido pela interpretação desses programas.
- Exemplos de programas com erros de sintaxe, onde o compilador deve ser capaz de detectar e reportar esses erros.

## Documentação de Uso

### Como utilizar o analisador léxico e sintático
1. Certifique-se de que todas as dependências estão instaladas (se houver).
2. Para analisar um programa, execute o comando abaixo na raiz do projeto:
   ```bash
   python3 src/compiler.py <caminho_para_o_arquivo.ci>
   ```
   Exemplo:
   ```bash
   python3 src/compiler.py programa.ci
   ```
   O analisador irá:
   - Realizar a análise léxica do arquivo informado, exibindo os tokens gerados.
   - Realizar a análise sintática, exibindo as árvores sintáticas geradas para cada linha do programa.
   - Em caso de erro léxico ou sintático, o erro será reportado no terminal e a execução será interrompida.

3. Temos os arquivos programa.ci (correto) e programa_errado.ci (errado) para fins de teste
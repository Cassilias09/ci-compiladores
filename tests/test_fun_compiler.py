import os
import subprocess
import pytest

INPUTS_DIR = os.path.join(os.path.dirname(__file__), '../inputs')
SRC_DIR = os.path.join(os.path.dirname(__file__), '../src')
COMPILER = os.path.join(SRC_DIR, 'compiler.py')

 # Lista de (arquivo de entrada, se deve compilar com sucesso)
TEST_CASES = [
    ("basico.ci", True),
    ("ev.ci", True),
    ("novoTeste.ci", True),
    ("programa.ci", True),
    ("programa_errado.ci", False),
]

def run_compiler(input_file):
    """
    Executa o compilador Fun para o arquivo de entrada especificado.
    Retorna o resultado do processo (stdout, stderr, código de saída).
    """
    input_path = os.path.join(INPUTS_DIR, input_file)
    result = subprocess.run([
        'python3', COMPILER, '--input', input_path, '--verbose'
    ], capture_output=True, text=True)
    return result


@pytest.mark.parametrize("input_file,should_succeed", TEST_CASES)
def test_fun_program(input_file, should_succeed):
    """
    Testa se o compilador Fun aceita ou rejeita corretamente cada programa de teste.
    """
    result = run_compiler(input_file)
    if should_succeed:
        assert result.returncode == 0, f"Esperado sucesso para {input_file}, mas ocorreu erro: {result.stderr}"
    else:
        assert result.returncode != 0, f"Esperado erro para {input_file}, mas compilou com sucesso."

# Teste automatizado do compilador Fun
# Executa o compilador para cada arquivo de entrada e verifica o sucesso ou erro esperado.

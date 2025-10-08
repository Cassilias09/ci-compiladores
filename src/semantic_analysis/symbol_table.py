class SymbolTableEntry:
    def __init__(self, name, kind, offset=None, params=None):
        self.name = name
        self.kind = kind  # 'global', 'param' (parâmetro), 'local' (variável local), 'function' (função)
        self.offset = offset  # Deslocamento (offset) para variáveis baseadas na pilha
        self.params = params  # Para funções: lista de nomes dos parâmetros

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent  # Referência ao escopo pai (para encadeamento/lookup)
        self.table = {}  # Dicionário para armazenar as entradas de símbolos neste escopo
        self.offset = 0  # Contador de offset para o próximo item local/parâmetro a ser declarado

    def declare(self, name, kind, offset=None, params=None):
        entry = SymbolTableEntry(name, kind, offset, params)
        self.table[name] = entry
        return entry

    def lookup(self, name):
        if name in self.table:
            return self.table[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            return None

    def push_scope(self):
        # Cria um novo escopo filho, cujo pai é o escopo atual
        return SymbolTable(parent=self)

    def pop_scope(self):
        # Retorna ao escopo pai (usado ao sair de um bloco/função)
        return self.parent

    def all_entries(self):
        # Retorna todos os valores (entradas) da tabela de símbolos deste escopo
        return self.table.values()
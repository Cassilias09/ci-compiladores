from syntatic_analysis.nodes import BaseNode


class CodeStartNode(BaseNode):
    def __init__(self):
        super().__init__()
        self._children: list[BaseNode] = []
        self._variables: list[str] = []

    def add_child(self, child: BaseNode):
        self._children.append(child)

    def display(self):
        for child in self._children:
            child.display()

    def generate_code(self):
        code = ""
        var_code = ""
        for child in self._children:
            code += child.generate_code()
            code += "call imprime_num\n\n"
        for var in self._variables:
            var_code += ".lcomm " + var + ", 8\n"
        program = (
            ".section .bss\n"
            + var_code + "\n"
            + ".section .text\n"
            + ".globl _start\n\n"
            + "_start:\n"
            + code
            + "call sair\n"
            + '.include "runtime.s"\n'
        )
        return program

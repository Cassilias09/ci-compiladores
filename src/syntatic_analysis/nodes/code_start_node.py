from syntatic_analysis.nodes import BaseNode


class CodeStartNode(BaseNode):
    def __init__(self):
        super().__init__()
        self._children: list[BaseNode] = []

    def add_child(self, child: BaseNode):
        self._children.append(child)

    def display(self):
        for child in self._children:
            child.display()

    def generate_code(self):
        code = ""
        for child in self._children:
            code += child.generate_code()
            code += "call imprime_num\n\n"
        program = (
            ".section .text\n"
            + ".globl _start\n"
            + "_start:\n"
            + code
            + "call sair\n"
            + '.include "runtime.s"'
        )
        return program

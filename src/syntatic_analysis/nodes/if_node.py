from syntatic_analysis.nodes import BaseNode
from syntatic_analysis.nodes.declaration_node import LocalVarDeclNode

class IfNode(BaseNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition  # Expression node
        self.then_body = then_body  # BlockNode
        self.else_body = else_body  # BlockNode ou None

    def display(self, identation=0):
        print((" " * identation) + "If")
        self.condition.display(identation + 1)
        print((" " * (identation + 1)) + "Then:")
        for cmd in self.then_body.statements:
            cmd.display(identation + 2)
        if self.else_body:
            print((" " * (identation + 1)) + "Else:")
            for cmd in self.else_body.statements:
                cmd.display(identation + 2)

    def generate_code(self):
        cond_code = self.condition.generate_code()

        def gen_cmd(cmd, local_offset=[-8]):
            if isinstance(cmd, LocalVarDeclNode):
                code = cmd.generate_code(local_offset[0])
                local_offset[0] -= 8
                return code
            else:
                return cmd.generate_code()

        then_code = "\n".join(gen_cmd(cmd) for cmd in self.then_body.statements)
        else_code = ""
        if self.else_body:
            else_code = "\n".join(gen_cmd(cmd) for cmd in self.else_body.statements)

        label_else = "Lelse"
        label_end = "Lend"

        code = (
            cond_code
            + f"\ncmp $0, %rax\n"
            + f"je {label_else}\n"
            + then_code
            + f"\njmp {label_end}\n"
            + f"{label_else}:\n"
            + else_code
            + f"\n{label_end}:\n"
        )
        return code

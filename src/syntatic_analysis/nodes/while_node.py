from syntatic_analysis.nodes import BaseNode
from syntatic_analysis.utils.label_generator import LabelGenerator

class WhileNode(BaseNode):
    def __init__(self, condition, body):
        self.condition = condition  # Expression node
        self.body = body  # list[BaseNode]

    def display(self, identation: int = 0):
        print((" " * identation) + "While")
        self.condition.display(identation + 1)
        for cmd in self.body:
            cmd.display(identation + 1)

    def generate_code(self):
        label_start = LabelGenerator.new("LstartLoop")
        label_end = LabelGenerator.new("LendLoop")

        cond_code = self.condition.generate_code()
        body_code = "\n".join(cmd.generate_code() for cmd in self.body)

        code = (
            f"{label_start}:\n"
            + cond_code
            + f"\ncmp $0, %rax\n"
            + f"je {label_end}\n"
            + body_code
            + f"\njmp {label_start}\n"
            + f"{label_end}:\n"
        )
        return code
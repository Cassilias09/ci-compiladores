from typing import override


class ExceptionList(Exception):
    def __init__(self, process: str, exceptions: list[Exception] = []):
        self.exceptions = exceptions
        super().__init__(
            f"Erros encotrados durante o processo {process}:"
            + "\n"
            + "\n".join([str(e) for e in self.exceptions])
        )

    @override
    def __repr__(self) -> str:
        return super().__repr__() + "\n" + "\n".join([str(e) for e in self.exceptions])

    @override
    def __str__(self) -> str:
        return super().__str__()

    def add_exception(self, exception: Exception):
        self.exceptions.append(exception)

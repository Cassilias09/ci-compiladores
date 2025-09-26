class LabelGenerator:
    _counter = 0

    @classmethod
    def new(cls, prefix: str = "L") -> str:
        """
        Generate a new unique label.
        Example: L1, L2, L3... or If1, While2, etc.
        """
        cls._counter += 1
        return f"{prefix}{cls._counter}"
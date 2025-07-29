import argparse


class Arguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("input_path", help="path to the input file")
        self.parser.add_argument("-o", "--output", help="output filename")

    def parse(self, args: list[str]) -> argparse.Namespace:
        return self.parser.parse_args(args)

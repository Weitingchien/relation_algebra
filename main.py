import os
from cli.main_cli import main_cli


class Main:
    def __init__(self) -> None:
        self.initialize()

    def initialize(self) -> None:
        main_cli()


if __name__ == "__main__":
    main = Main()

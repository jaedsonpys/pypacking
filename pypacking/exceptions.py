class ConfigFileNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PackageNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

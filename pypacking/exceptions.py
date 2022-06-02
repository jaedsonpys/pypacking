class ConfigFileNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PackageNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

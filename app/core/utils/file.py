def file_loader(path: str) -> str:
    with open(path, "r") as file:
        return file.read()
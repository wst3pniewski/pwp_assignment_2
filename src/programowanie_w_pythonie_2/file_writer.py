from pathlib import Path


class FileWriter:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def __enter__(self):
        self.f = open(self.file_path, "w", encoding="utf-8")
        return self.f

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.f.close()


if __name__ == "__main__":
    with FileWriter("data/example.txt") as f:
        f.write("Hello world!")

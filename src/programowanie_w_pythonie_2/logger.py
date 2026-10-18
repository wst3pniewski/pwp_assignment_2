class Logger:
    def __init__(self):
        pass

    def __enter__(self):
        print("Start sekcji logowania")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Koniec sekcji logowania")


if __name__ == "__main__":
    with Logger():
        print("Some heavy computing...")

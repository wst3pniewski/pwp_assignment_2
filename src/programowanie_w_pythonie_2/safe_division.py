class SafeDivision:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero")
            return True

    def divide(self, a, b):
        return a / b


if __name__ == "__main__":
    with SafeDivision() as sd:
        print(sd.divide(10, 2))
        sd.divide(10, 0)

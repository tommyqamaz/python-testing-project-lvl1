class Logger:
    def __init__(self):
        pass

    def log(self, value):
        print(value)

    def save(file, path):
        with open(path, "w") as f:
            f.write(file)

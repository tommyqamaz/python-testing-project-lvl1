class Logger:
    """log the events"""

    def __init__(self):
        pass

    def log(self, value):
        print(value)

    def save(self, content, path):
        with open(path, "w") as f:
            f.write(content)

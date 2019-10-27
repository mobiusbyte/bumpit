import os
import random
import string


def fixture_path(name):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "fixtures", name)


def tmp_folder():
    folder = f"/tmp/{random_string()}"
    os.makedirs(folder)
    return folder


def random_string():
    return "".join(random.choice(string.ascii_letters) for _ in range(6))


class LoggerSpy:
    def __init__(self):
        self.messages = []

    def log(self, message):
        self.messages.append(message)

    warn = log
    info = log
    error = log

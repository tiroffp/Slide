"""
Defines exceptions used by the model class to represent game-ending board states
"""


class AddBlockError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GamveOverWin(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

from .constants import ClarityType


class ListCV:
    def __init__(self, values):
        self.type = ClarityType.List
        self.list = values

    @property
    def list_length(self):
        return len(self.list)


def list_cv(values):
    return ListCV(values)

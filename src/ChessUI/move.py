from .const import *


class Move:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def __str__(self):
        return f'From {ROWS - self.initial.row, ROW_LABELS_WHITE[self.initial.col]} To {ROWS - self.final.row, ROW_LABELS_WHITE[self.final.col]}'

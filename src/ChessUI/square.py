
class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return self.piece is None

    def has_enemy_piece(self, color):
        if self.is_empty():
            return False
        return True if color != self.piece.color else False

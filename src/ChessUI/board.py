import numpy as np

from .const import *
from .square import Square
from .piece import *
from .helper import get_opposite_color


class Board:

    def __init__(self):
        self.squares = self.squares = np.empty((8, 8), dtype=object)

        self._create()
        self._add_piece('white')
        self._add_piece('black')

    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row, col] = Square(row, col)

    def _add_piece(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        color = color if PLAYER == 'white' else get_opposite_color(color)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn, col] = Square(row_pawn, col, Pawn(color))

        # Knights
        self.squares[row_other, 1] = Square(row_other, 1, Knight(color))
        self.squares[row_other, 6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other, 2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other, 5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other, 0] = Square(row_other, 0, Rook(color))
        self.squares[row_other, 7] = Square(row_other, 7, Rook(color))

        # Placement for king and queen
        q_spot, k_spot = (3, 4) if PLAYER == 'white' else (4, 3)

        # Queen
        self.squares[row_other, q_spot] = Square(row_other, q_spot, Queen(color))

        # King
        self.squares[row_other, k_spot] = Square(row_other, k_spot, King(color))

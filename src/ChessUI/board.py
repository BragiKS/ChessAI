import numpy as np

from .square import Square
from .piece import *
from .helper import get_opposite_color
from .move import Move


class Board:

    def __init__(self):
        self.squares = np.empty((8, 8), dtype=object)
        self.last_move = None
        self._create()
        self._add_piece('white')
        self._add_piece('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # move piece to new square
        self.squares[initial.row, initial.col].piece = None
        self.squares[final.row, final.col].piece = piece

        # piece has moved
        piece.moved = True

        # clear previous possible moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):

        def add_move(next_row, next_col):
            initial = Square(row, col)
            final = Square(next_row, next_col)
            move = Move(initial, final)
            piece.add_moves(move)

        def is_valid_position(*args):
            for arg in args:
                if arg < 0 or arg > 7:
                    return False
            return True

        def add_directional_moves(row_inc, col_inc):
            next_row = row + row_inc
            next_col = col + col_inc
            while is_valid_position(next_row, next_col):
                if self.squares[next_row, next_col].has_piece():
                    if self.squares[next_row, next_col].has_enemy_piece(piece.color):
                        add_move(next_row, next_col)
                    break
                add_move(next_row, next_col)
                next_row += row_inc
                next_col += col_inc

        match piece.name:
            case 'pawn':

                def add_forward_moves():
                    step = 1 if piece.moved else 2
                    square_one = self.squares[row + 1 * piece.dir, col]
                    square_two = self.squares[row + 2 * piece.dir, col]
                    if is_valid_position(row + 1 * piece.dir) and square_one.is_empty():
                        add_move(row + 1 * piece.dir, col)
                    if is_valid_position(row + 2 * piece.dir) and step == 2 and square_two.is_empty():
                        add_move(row + 2 * piece.dir, col)

                def add_capture_moves(next_row, next_col):
                    if is_valid_position(next_row, next_col) and self.squares[next_row, next_col].has_enemy_piece(piece.color):
                        add_move(next_row, next_col)

                # Add forward moves
                add_forward_moves()

                # Add piece capturing moves
                if col != 7:
                    right_capture = (row + 1 * piece.dir, col + 1)
                    add_capture_moves(*right_capture)

                if col != 0:
                    left_capture = (row + 1 * piece.dir, col - 1)
                    add_capture_moves(*left_capture)

            case 'knight':
                def add_knight_move(row_d, col_d):
                    next_row = row + row_d if is_valid_position(row + row_d) else None
                    next_col = col + col_d if is_valid_position(col + col_d) else None
                    if next_row is not None and next_col is not None:
                        target_square = self.squares[next_row, next_col]
                        if target_square.is_empty() or target_square.has_enemy_piece(piece.color):
                            add_move(next_row, next_col)

                knight_moves = [
                    (-2, 1), (-2, -1), (2, 1), (2, -1),
                    (-1, 2), (-1, -2), (1, 2), (1, -2)
                ]

                for row_delta, col_delta in knight_moves:
                    add_knight_move(row_delta, col_delta)

            case 'bishop':
                add_directional_moves(1, 1)
                add_directional_moves(1, -1)
                add_directional_moves(-1, 1)
                add_directional_moves(-1, -1)

            case 'rook':
                add_directional_moves(0, 1)
                add_directional_moves(0, -1)
                add_directional_moves(1, 0)
                add_directional_moves(-1, 0)

            case 'queen':
                add_directional_moves(1, 1)
                add_directional_moves(1, -1)
                add_directional_moves(-1, 1)
                add_directional_moves(-1, -1)
                add_directional_moves(0, 1)
                add_directional_moves(0, -1)
                add_directional_moves(1, 0)
                add_directional_moves(-1, 0)

            case 'king':
                king_moves = [
                    (1, 0), (1, 1), (0, 1), (-1, 1),
                    (-1, 0), (-1, -1), (0, -1), (1, -1)
                ]

                for row_delta, col_delta in king_moves:
                    new_row, new_col = row + row_delta, col + col_delta
                    if is_valid_position(new_row, new_col):
                        target_square = self.squares[new_row, new_col]
                        if target_square.is_empty() or target_square.has_enemy_piece(piece.color):
                            add_move(new_row, new_col)

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

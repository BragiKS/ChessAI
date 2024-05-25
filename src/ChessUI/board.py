import numpy as np

from .const import *
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

        def add_move(piece, start_row, start_col, next_row, next_col):
            initial = Square(start_row, start_col)
            final = Square(next_row, next_col)
            move = Move(initial, final)
            piece.add_moves(move)

        def is_valid_position(row, col):
            return 0 <= row <= 7 and 0 <= col <= 7

        def add_diagonal_moves(piece, start_row, start_col, row_increment, col_increment):
            row_i, col_i = start_row, start_col
            while is_valid_position(row_i, col_i):
                target_square = self.squares[row_i, col_i]
                if target_square.has_piece():
                    if target_square.piece.color != piece.color:
                        add_move(piece, row, col, row_i, col_i)
                    break
                add_move(piece, row, col, row_i, col_i)
                row_i += row_increment
                col_i += col_increment

        def add_vertical_moves(piece, start_row, start_col, row_increment):
            row_i = start_row
            while is_valid_position(row_i, start_col):
                target_square = self.squares[row_i, start_col]
                if target_square.has_piece():
                    if target_square.piece.color != piece.color:
                        add_move(piece, row, col, row_i, start_col)
                    break
                add_move(piece, row, col, row_i, col)
                row_i += row_increment

        def add_horizontal_moves(piece, start_row, start_col, col_increment):
            col_i = start_col
            while is_valid_position(start_row, col_i):
                target_square = self.squares[start_row, col_i]
                if target_square.has_piece():
                    if target_square.piece.color != piece.color:
                        add_move(piece, row, col, start_row, col_i)
                    break
                add_move(piece, row, col, start_row, col_i)
                col_i += col_increment

        match piece.name:
            case 'pawn':

                def add_move_if_valid(row, col, start_row):
                    if is_valid_position(row, col) and not self.squares[row, col].has_piece():
                        add_move(piece, start_row, col, row, col)

                def add_capture_move_if_valid(row, col, start_row, start_col):
                    if is_valid_position(row, col) and self.squares[row, col].has_piece():
                        if self.squares[row, col].piece.color != piece.color:
                            add_move(piece, start_row, start_col, row, col)

                # Add forward moves
                one_step_forward = (row + 1 * piece.dir, col, row)
                add_move_if_valid(*one_step_forward)

                if not piece.moved:
                    two_steps_forward = (row + 2 * piece.dir, col, row)
                    add_move_if_valid(*two_steps_forward)

                # Add piece capturing moves
                if col != 7:
                    right_capture = (row + 1 * piece.dir, col + 1, row, col)
                    add_capture_move_if_valid(*right_capture)

                if col != 0:
                    left_capture = (row + 1 * piece.dir, col - 1, row, col)
                    add_capture_move_if_valid(*left_capture)

            case 'knight':
                def get_valid_coord(coord, delta, limit):
                    return coord + delta if 0 <= coord + delta <= limit else None

                def add_knight_move(piece, start_row, start_col, row_delta, col_delta):
                    new_row = get_valid_coord(start_row, row_delta, 7)
                    new_col = get_valid_coord(start_col, col_delta, 7)
                    if new_row is not None and new_col is not None:
                        target_square = self.squares[new_row, new_col]
                        if not target_square.has_piece() or target_square.piece.color != piece.color:
                            add_move(piece, start_row, start_col, new_row, new_col)

                knight_moves = [
                    (-2, 1), (-2, -1), (2, 1), (2, -1),
                    (-1, 2), (-1, -2), (1, 2), (1, -2)
                ]

                for row_delta, col_delta in knight_moves:
                    add_knight_move(piece, row, col, row_delta, col_delta)

            case 'bishop':
                add_diagonal_moves(piece, row + 1, col + 1, 1, 1)
                add_diagonal_moves(piece, row + 1, col - 1, 1, -1)
                add_diagonal_moves(piece, row - 1, col - 1, -1, -1)
                add_diagonal_moves(piece, row - 1, col + 1, -1, 1)

            case 'rook':
                add_vertical_moves(piece, row + 1, col, 1)
                add_vertical_moves(piece, row - 1, col, -1)
                add_horizontal_moves(piece, row, col + 1, 1)
                add_horizontal_moves(piece, row, col - 1, -1)

            case 'queen':
                add_diagonal_moves(piece, row + 1, col + 1, 1, 1)
                add_diagonal_moves(piece, row + 1, col - 1, 1, -1)
                add_diagonal_moves(piece, row - 1, col - 1, -1, -1)
                add_diagonal_moves(piece, row - 1, col + 1, -1, 1)
                add_vertical_moves(piece, row + 1, col, 1)
                add_vertical_moves(piece, row - 1, col, -1)
                add_horizontal_moves(piece, row, col + 1, 1)
                add_horizontal_moves(piece, row, col - 1, -1)

            case 'king':
                king_moves = [
                    (1, 0), (1, 1), (0, 1), (-1, 1),
                    (-1, 0), (-1, -1), (0, -1), (1, -1)
                ]

                for row_delta, col_delta in king_moves:
                    new_row, new_col = row + row_delta, col + col_delta
                    if is_valid_position(new_row, new_col):
                        target_square = self.squares[new_row, new_col]
                        if not target_square.has_piece() or target_square.piece.color != piece.color:
                            add_move(piece, row, col, new_row, new_col)

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

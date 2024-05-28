import numpy as np
import copy

from .square import Square
from .piece import *
from .helper import get_opposite_color
from .move import Move
from .sound import *


class Board:

    def __init__(self):
        self.squares = np.empty((8, 8), dtype=object)
        self.last_move = None
        self.revert_move = None
        self.white_king = self.squares[7, 4] if PLAYER == 'white' else self.squares[0, 3]
        self.black_king = self.squares[0, 4] if PLAYER == 'white' else self.squares[7, 3]
        self.moved_piece = None
        self.captured_piece = None
        self._create()
        self._add_piece('white')
        self._add_piece('black')
        self.sound = Sound()

    def flip_board(self):
        # Maybe do later
        pass

    def get_king(self, color):
        return self.white_king if color == 'white' else self.black_king

    def set_king(self, square, color):
        if color == 'white':
            self.white_king = square
        else:
            self.black_king = square

    def move(self, piece, move, future=False):
        initial = move.initial
        final = move.final

        # thing that we don't want when checking the future
        if not future:

            # piece has moved
            piece.moved = True

            # set last move
            self.last_move = move

            # play sounds
            if self.squares[final.row, final.col].has_piece():
                self.sound.play_capture()
            else:
                self.sound.play_move()

        # set move for revert
        self.revert_move = Move(self.squares[initial.row, initial.col], self.squares[final.row, final.col])
        self.moved_piece = self.squares[initial.row, initial.col].piece
        self.captured_piece = self.squares[final.row, final.col].piece

        # move piece to new square
        self.squares[initial.row, initial.col].piece = None
        self.squares[final.row, final.col].piece = piece

        # setting the position for the kings if moved
        if piece.name == 'king':
            self.set_king(self.squares[final.row, final.col], piece.color)

        # clear all previous possible moves
        self.clear_all_moves()

    def revert_board(self):
        # fetch data
        initial_row = self.revert_move.initial.row
        initial_col = self.revert_move.initial.col
        initial_piece = self.moved_piece
        final_row = self.revert_move.final.row
        final_col = self.revert_move.final.col
        final_piece = self.captured_piece

        # if king revert king move
        if initial_piece.name == 'king':
            self.set_king(self.squares[initial_row, initial_col], initial_piece.color)

        # revert table
        self.squares[initial_row, initial_col].piece = initial_piece
        self.squares[final_row, final_col].piece = final_piece

        # clear all previous possible moves
        self.clear_all_moves()
        self.calc_all_moves()

    def clear_all_moves(self):
        for square in self.squares.flat:
            if square.has_piece():
                square.piece.clear_moves()

    def king_in_check(self, king):
        for square in self.squares.flat:
            if square.has_piece() and square.piece.color != king.piece.color:
                for move in square.piece.moves:
                    if move.final.row == king.row and move.final.col == king.col:
                        return True
        return False

    def checkmate(self, color):
        for square in self.squares.flat:
            if square.has_piece() and color != square.piece.color and square.piece.has_moves():
                return False
        return True

    def valid_move(self, piece, move):
        if move in piece.moves:
            self.move(piece, move, True)
            self.calc_all_moves()
            king_square = self.get_king(piece.color)
            if self.king_in_check(king_square):
                self.revert_board()
                return False
            self.revert_board()
            return True
        return False

    def calc_all_moves(self):
        for square in self.squares.flat:
            if square.has_piece():
                self.calc_moves(square.piece, square.row, square.col)

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
                    if is_valid_position(next_row, next_col) and self.squares[next_row, next_col].has_enemy_piece(
                            piece.color):
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
        if color == 'white':
            self.white_king = self.squares[row_other, k_spot]
        else:
            self.black_king = self.squares[row_other, k_spot]

import numpy as np
import copy

from .square import Square
from .piece import *
from .helper import get_opposite_color
from .move import Move
from .sound import *
from .promote import *


class Board:

    def __init__(self):

        self.squares = np.empty((8, 8), dtype=object)
        self.last_move = None
        self.white_king = self.squares[7, 4] if PLAYER == 'white' else self.squares[0, 3]
        self.black_king = self.squares[0, 4] if PLAYER == 'white' else self.squares[7, 3]
        self.moved_piece = None
        self.captured_piece = None
        self.en_passant = None
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
            # play sounds
            # I know this if statement is fucked it's because I need the capture sound for "en passant"
            if (self.squares[final.row, final.col].has_piece() or
                    (isinstance(piece, Pawn) and self.en_passant is not None and
                     self.squares[final.row, final.col] == self.en_passant)):
                self.sound.play_capture()
            else:
                self.sound.play_move()

        self.moved_piece = self.squares[initial.row, initial.col].piece
        self.captured_piece = self.squares[final.row, final.col].piece

        # Remove piece that was captured with en passant
        if isinstance(piece, Pawn) and self.en_passant is not None:
            if self.squares[final.row, final.col] == self.en_passant:
                self.squares[final.row - 1 * piece.dir, final.col].piece = None

        # move piece to new square
        self.squares[initial.row, initial.col].piece = None
        self.squares[final.row, final.col].piece = piece

        # remove en_passant if any
        self.en_passant = None

        # pawn promotion and en passant
        if isinstance(piece, Pawn):
            # set en_passant if piece moved 2 squares
            if abs(initial.row - final.row) == 2:
                self.en_passant = self.squares[initial.row + 1 * piece.dir, initial.col]

            if final.row == 0 or final.row == 7:
                if not future:
                    self.pawn_promote(piece, final)
                else:
                    piece = Queen(piece.color)

        # play check sound P.S needs to happen after moving piece
        if not future and self.check(self.get_king(get_opposite_color(piece.color))):
            self.sound.play_check()

        # piece has moved
        piece.moved = True

        # set last move
        self.last_move = move

        # clear all previous moves
        self.clear_all_moves()

        # setting the position for the kings if moved
        if piece.name == 'king':
            self.set_king(self.squares[final.row, final.col], piece.color)

    def pawn_promote(self, piece, final):
        promote = Promote(piece, final)
        promote.start()

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

    def check(self, king):
        temp_board = copy.deepcopy(self)
        temp_board.calc_all_moves(get_opposite_color(king.piece.color))
        return temp_board.king_in_check(king)

    def checkmate(self, color):
        for square in self.squares.flat:
            if square.has_piece() and color != square.piece.color and square.piece.has_moves():
                return False
        return True

    def valid_move(self, piece, move):
        return move in piece.moves

    def future_move_valid(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        # Perform the move temporarily
        temp_board.move(temp_piece, move, future=True)

        # Recalculate all moves for the opposite color
        temp_board.calc_all_moves(get_opposite_color(piece.color))

        # Check if the current player's king is in check
        king_square = temp_board.get_king(piece.color)
        return temp_board.king_in_check(king_square)

    def calc_all_moves(self, color):
        for square in self.squares.flat:
            if square.has_piece() and square.piece.color == color:
                self.calc_moves(square.piece, square.row, square.col, False)

    def calc_moves(self, piece, row, col, bool=True):

        def add_move(next_row, next_col):
            initial = Square(row, col)
            final = Square(next_row, next_col)
            move = Move(initial, final)
            if bool:
                if not self.future_move_valid(piece, move):
                    piece.add_moves(move)
            else:
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
                    square_one = self.squares[row + 1 * piece.dir, col]
                    square_two = self.squares[row + 2 * piece.dir, col] if not piece.moved else None
                    if is_valid_position(row + 1 * piece.dir) and square_one.is_empty():
                        add_move(row + 1 * piece.dir, col)
                        if not piece.moved and square_two.is_empty():
                            add_move(row + 2 * piece.dir, col)

                def add_capture_moves(next_row, next_col):
                    if (is_valid_position(next_row, next_col) and
                            self.squares[next_row, next_col].has_enemy_piece(piece.color)):
                        add_move(next_row, next_col)

                def add_en_passant_moves(next_row, next_col):
                    if self.en_passant is not None:
                        if (is_valid_position(next_row, next_col) and
                                self.en_passant == self.squares[next_row, next_col]):
                            add_move(next_row, next_col)

                # Add forward moves
                add_forward_moves()

                # Add piece capturing moves
                if col != 7:
                    right_capture = (row + 1 * piece.dir, col + 1)
                    add_capture_moves(*right_capture)
                    add_en_passant_moves(*right_capture)

                if col != 0:
                    left_capture = (row + 1 * piece.dir, col - 1)
                    add_capture_moves(*left_capture)
                    add_en_passant_moves(*left_capture)

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

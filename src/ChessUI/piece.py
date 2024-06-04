import os
from .const import *


class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if PLAYER == color else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self):
        self.texture = os.path.join(f'./assets/images/{self.color}_{self.name}.png')

    def add_moves(self, move):
        self.moves.append(move)

    def set_moves(self, moves):
        self.moves = moves

    def clear_moves(self):
        self.moves = []

    def has_moves(self):
        return self.moves == []


class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if PLAYER == color else 1
        super().__init__('pawn', color, 1.0)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)


class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 9999.0)

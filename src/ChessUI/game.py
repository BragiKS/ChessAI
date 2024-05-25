import pygame

from .const import *
from .board import Board
from .dragger import Dragger
from .helper import highlight_color


class Game:

    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)  # light green
                else:
                    color = (119, 154, 88)  # dark green

                if self.dragger.initial_col == col and self.dragger.initial_row == row:
                    color = highlight_color(color)

                rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row, col].has_piece():
                    piece = self.board.squares[row, col].piece

                    img = pygame.image.load(piece.texture)
                    img_center = col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    if not self.dragger.piece == piece:
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = (100, 100, 100, 128)  # Grey
                radius = 25
                col = move.final.col + 0.5
                row = move.final.row + 0.5
                center = (col * SQ_SIZE, row * SQ_SIZE)

                # Create a temporary surface with per-pixel alpha
                temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                temp_surface = temp_surface.convert_alpha()

                # Draw the circle on the temporary surface
                pygame.draw.circle(temp_surface, color, (radius, radius), radius)

                # Blit the temporary surface onto the main surface
                surface.blit(temp_surface, (center[0] - radius, center[1] - radius))

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

import pygame

from .const import *
from .board import Board
from .dragger import Dragger


class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
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
                color = GREY_COLOR
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

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = HIGHLIGHT_COLOR_LIGHT if (pos.row + pos.col) % 2 == 0 else HIGHLIGHT_COLOR_DARK
                rect = (pos.col * SQ_SIZE, pos.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            row = self.hovered_sqr.row
            col = self.hovered_sqr.col
            color = LIGHT_HOVER if (row + col) % 2 == 0 else DARK_HOVER
            rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(surface, color, rect, 5)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, pos):
        mouse_x, mouse_y = pos
        row = max(min(mouse_y // SQ_SIZE, 7), 0)
        col = max(min(mouse_x // SQ_SIZE, 7), 0)
        self.hovered_sqr = self.board.squares[row, col]

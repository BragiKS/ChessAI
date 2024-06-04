import pygame

from .const import *


class Promote:
    def __init__(self, piece, position):
        self.piece = piece
        self.pos = position
        self.surface = pygame.display.get_surface()

    def show_window(self):
        color = (255, 255, 255)
        rect = pygame.Rect((self.pos.col + 1) * SQ_SIZE, self.pos.row * SQ_SIZE, SQ_SIZE, SQ_SIZE * 4)
        pygame.draw.rect(self.surface, color, rect, 0, 5)

    def show_pieces(self):
        pass

    def start(self):
        while True:
            self.show_window()
            break

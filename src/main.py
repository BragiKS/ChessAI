import pygame
import sys

import ChessUI as UI


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((UI.WIDTH, UI.HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = UI.Game()

    def gameloop(self):

        screen = self.screen
        game = self.game
        board = game.board
        dragger = game.dragger

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)
            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // UI.SQ_SIZE
                    clicked_col = dragger.mouseX // UI.SQ_SIZE

                    print(dragger.mouseY, clicked_row)
                    print(dragger.mouseX, clicked_col)

                    if board.squares[clicked_row, clicked_col].has_piece():
                        piece = board.squares[clicked_row, clicked_col].piece
                        if UI.PVP_MODE or piece.color == UI.PLAYER:
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            print(piece.value)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.gameloop()

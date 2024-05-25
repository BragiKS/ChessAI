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
            game.show_moves(screen)
            game.show_pieces(screen)

            # piece follow mouse if dragging a piece
            if dragger.dragging:
                dragger.update_blit(screen)

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
                        # PVP mode
                        if piece.color == game.next_player and UI.PVP_MODE:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            print(piece.value)
                        # AI mode
                        elif not UI.PVP_MODE:
                            pass

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)  # update position if moving mouse

                # release mouse-button
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        released_row = dragger.mouseY // UI.SQ_SIZE
                        released_col = dragger.mouseX // UI.SQ_SIZE

                        # create possible move
                        initial = UI.Square(dragger.initial_row, dragger.initial_col)
                        final = UI.Square(released_row, released_col)
                        move = UI.Move(initial, final)

                        # valid move?
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.next_turn()

                    dragger.undrag_piece()

                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.gameloop()

import pygame

from components.Board import Board
from components.DrawBoard import DrawBoard
from components.DrawMenu import DrawMenu


class Game:
    def __init__(self, width, height, square_size, screen) -> None:
        self.width = width
        self.height = height
        self.square_size = square_size
        self.screen = screen

        self.boardScreen = pygame.Surface((height, height))
        self.menuScreen = pygame.Surface((width - height, height))

        self.light_square = (220, 208, 194)
        self.dark_square = (83, 100, 83)
        self.highlight_color = (100, 249, 83, 130)
        self.selected_color = (255, 0, 0)

    def display(self):
        drawBoard = DrawBoard(self.boardScreen)
        menu = DrawMenu(self.menuScreen)

        board = Board()
        boardGame = board.get_board()

        running = True
        selected_square = None
        legal_moves = []
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click chuột trái
                        col, row = self.get_coor(*event.pos)
                        if col < 0 or col > 7 or row < 0 or row > 7:
                            continue
                        clicked_square = row * 8 + col

                        if clicked_square == selected_square:  # Bỏ chọn ô
                            selected_square = None
                            legal_moves = []
                        else:
                            if selected_square is not None:
                                move = board.get_move(selected_square, clicked_square)

                                try:
                                    if move and board.can_promote(move):
                                        print("Promote")
                                except Exception as e:
                                    e

                                if board.move_piece(move):
                                    print(move.uci())
                                    selected_square = None
                                    legal_moves = []
                                else:
                                    selected_square = clicked_square
                                    legal_moves = board.get_legal_moves()
                            else:
                                selected_square = clicked_square
                                legal_moves = board.get_legal_moves()

                        print(board.is_checkmate())

            drawBoard.display(boardGame, selected_square, legal_moves)
            menu.display()

            self.screen.blit(self.boardScreen, (0, 0))
            self.screen.blit(self.menuScreen, (self.height, 0))

            # self.draw()

            pygame.display.flip()

    def get_coor(self, x, y):
        return x // self.square_size, 7 - y // self.square_size
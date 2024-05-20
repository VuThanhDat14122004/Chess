import chess
import pygame

from components.Board import Board
from components.DrawBoard import DrawBoard
from components.DrawMenu import DrawMenu
from Bot.engine2 import ChessAl2
from Bot.engine import ChessAl


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

        self.bot2 = ChessAl()

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

            is_check = board.is_check()
            drawBoard.display(boardGame, selected_square, legal_moves, is_check)
            menu.display()

            self.screen.blit(self.boardScreen, (0, 0))
            self.screen.blit(self.menuScreen, (self.height, 0))

            # self.draw()

            pygame.display.flip()

            # Thực hiện nước đi của bot nếu đến lượt bot
            if not boardGame.turn:
                bot_move = self.bot.Think(boardGame)
                board.move_piece(bot_move)
                print(f"Bot move: {bot_move.uci()}")

            """"
            # Thực hiện nước đi của bot nếu đến lượt bot
            if boardGame.turn:  # Trắng đi trước (bot1)
                bot_move = self.bot1.Think(boardGame)
                if bot_move is None:
                    self.display_end_screen("Bot2 wins!")
                    running = False
                    continue
                board.move_piece(bot_move)
                print(f"Bot1 move: {bot_move.uci()}")
            else:  # Đen đi sau (bot2)
                bot_move = self.bot2.Think(boardGame)
                if bot_move is None:
                    self.display_end_screen("Bot1 wins!")
                    running = False
                    continue
                board.move_piece(bot_move)
                print(f"Bot2 move: {bot_move.uci()}")
            """

    def get_coor(self, x, y):
        return x // self.square_size, 7 - y // self.square_size

    # Hiển thị màn hình kết thúc
    def display_end_screen(self, message):
        font = pygame.font.SysFont(None, 55)
        text = font.render(message, True, (255, 255, 255))
        self.screen.fill((0, 0, 0))  # Làm sạch màn hình và tô màu đen
        self.screen.blit(
            text,
            (
                self.width // 2 - text.get_width() // 2,
                self.height // 2 - text.get_height() // 2,
            ),
        )
        pygame.display.flip()
        pygame.time.wait(3000)  # Chờ 3 giây trước khi đóng cửa sổ

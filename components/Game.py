import pygame

from components.Board import Board
from components.DrawBoard import DrawBoard
from components.DrawMenu import DrawMenu
import chess


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
        self.is_promote = False
    def display(self):
        drawBoard = DrawBoard(self.boardScreen)
        menu = DrawMenu(self.menuScreen)

        board = Board()
        boardGame = board.get_board()

        running = True
        selected_square = None
        clicked_square = -1
        legal_moves = []
        while running:
            if menu.current_time == 0:
                print("time_over")
                break
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    return False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click chuột trái
                        col, row = self.get_coor(*event.pos)
                        if col < 0 or col > 11 or row < 0 or row > 7:
                            continue
                        if col <= 7:
                            clicked_square = row * 8 + col
                        if clicked_square == selected_square:  # Bỏ chọn ô
                            selected_square = None
                            legal_moves = []
                        else:
                            if selected_square is not None and clicked_square != -1:
                                
                                if board.can_promote(selected_square, clicked_square):
                                    self.is_promote = True
                                    menu.is_promote = True
                                    menu.color_promote = boardGame.turn
                                    
                                    if self.get_num_promote(*event.pos, menu) == 0:
                                        print("QUEEN")
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.QUEEN)
                                        menu.is_promote = False
                                        self.is_promote = False
                                        
                                    elif self.get_num_promote(*event.pos, menu) == 1:
                                        print("ROOK")
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.ROOK)
                                        menu.is_promote = False
                                        self.is_promote = False
                                        
                                        
                                    elif self.get_num_promote(*event.pos, menu) == 2:
                                        print("BISHOP")
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.BISHOP)
                                        menu.is_promote = False
                                        self.is_promote = False
                                        
                                        
                                    elif self.get_num_promote(*event.pos, menu) == 3:
                                        print("KNIGHT")
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.KNIGHT)
                                        menu.is_promote = False
                                        self.is_promote = False
                                    
                                if self.is_promote == False:
                                    move = board.get_move(selected_square, clicked_square)
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
                    if event.button == 3:
                        if board.board.move_stack:
                            board.board.pop()
            drawBoard.display(boardGame, selected_square, legal_moves)
            menu.display()

            self.screen.blit(self.boardScreen, (0, 0))
            self.screen.blit(self.menuScreen, (self.height, 0))

            # self.draw()

            pygame.display.flip()

    def get_coor(self, x, y):
        return x // self.square_size, 7 - y // self.square_size

    def get_num_promote(self, x, y, menu: DrawMenu):
        if (y > 40 and y < 120 and x > 640 and x < 720):
            menu.is_promote = False
            return 0
        elif (y > 40 and y < 120 and x > 720 and x < 800):
            menu.is_promote = False
            return 1
        elif (y > 40 and y < 120 and x > 800 and x < 880):
            menu.is_promote = False
            return 2
        elif (y > 40 and y < 120 and x > 880 and x < 960):
            menu.is_promote = False
            return 3
        return -1
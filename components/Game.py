import pygame

from components.Board import Board
from components.DrawBoard import DrawBoard
from components.DrawMenu import DrawMenu
import chess
import time
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
        self.is_promote = False
        self.bot = ChessAl()
        self.history = []

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
            if board.is_checkmate():
                print("White wins")
                running = False
            elif board.is_checkmate():
                print("Black wins")
                running = False
            if menu.current_time <= 0:
                print("time_over")
                break
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    print(self.history)
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
                                        if board.board.piece_at(selected_square) is not None:
                                            piece_name = board.board.piece_at(selected_square).symbol()
                                            piece_move = move.uci()
                                            self.history.append({piece_name: piece_move})
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.QUEEN)
                                        menu.is_promote = False
                                        self.is_promote = False
                                        
                                    elif self.get_num_promote(*event.pos, menu) == 1:
                                        print("ROOK")
                                        if board.board.piece_at(selected_square) is not None:
                                            piece_name = board.board.piece_at(selected_square).symbol()
                                            piece_move = move.uci()
                                            self.history.append({piece_name: piece_move})
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.ROOK)
                                        menu.is_promote = False
                                        self.is_promote = False
                                        
                                        
                                    elif self.get_num_promote(*event.pos, menu) == 2:
                                        print("BISHOP")
                                        if board.board.piece_at(selected_square) is not None:
                                            piece_name = board.board.piece_at(selected_square).symbol()
                                            piece_move = move.uci()
                                            self.history.append({piece_name: piece_move})
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.BISHOP)
                                        menu.is_promote = False
                                        self.is_promote = False
                                        
                                        
                                    elif self.get_num_promote(*event.pos, menu) == 3:
                                        print("KNIGHT")
                                        if board.board.piece_at(selected_square) is not None:
                                            piece_name = board.board.piece_at(selected_square).symbol()
                                            piece_move = move.uci()
                                            self.history.append({piece_name: piece_move})
                                        move = board.get_move(selected_square, clicked_square)
                                        board.promote(move, chess.KNIGHT)
                                        menu.is_promote = False
                                        self.is_promote = False
                                    
                                if self.is_promote == False:
                                    move = board.get_move(selected_square, clicked_square)
                                    if board.board.piece_at(selected_square) is not None:
                                        piece_name = board.board.piece_at(selected_square).symbol()
                                        piece_move = move.uci()
                                        self.history.append({piece_name: piece_move})
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
                            move_pop = self.history.pop()
                            move_pop = list(move_pop.keys())[0]
                            value_move = self.find_last_move(move_pop)
                            move_pop = {move_pop: value_move}
                            self.update_his(move_pop, menu)
                        # if board.board.move_stack:
                        #     board.board.pop()
                        #     move_pop = self.history.pop()
                        #     move_pop = list(move_pop.keys())[0]
                        #     move_pop = {move_pop: '0'}
                        #     self.update_his(move_pop, menu)
                        
            drawBoard.display(boardGame, selected_square, legal_moves)
            if len(self.history) > 0:
                his_move_piece = self.history[-1]
                self.update_his(his_move_piece, menu)
            
            menu.display()
            
            if boardGame.turn:
                #menu.start_time = pygame.time.get_ticks()
                menu.draw_count_down()
            else :
                
                menu.draw_time()
            self.screen.blit(self.boardScreen, (0, 0))
            self.screen.blit(self.menuScreen, (self.height, 0))

            # self.draw()
            
            pygame.display.flip()
            
            if not boardGame.turn:
                menu.current_time = 60
                start_time = time.time()  # Bắt đầu đo thời gian
                bot_move = self.bot.Think(boardGame)
                square = 0
                try:
                    square = chess.parse_square(bot_move.uci()[2::])
                except:
                    if bot_move is not None:
                        square = chess.parse_square(bot_move.uci()[0:2])
                    else :
                        print("Bot lose")
                        break
                board.move_piece(bot_move)
                if board.board.piece_at(square) is not None:
                    piece_name = board.board.piece_at(square).symbol()
                    self.history.append({piece_name: bot_move.uci()})   
                end_time = time.time()  # Kết thúc đo thời gian
                print(f"Bot move: {bot_move.uci()}")
                print(f"Time: {end_time - start_time}")
                menu.current_time = 60
            if not boardGame.turn:
                menu.current_time = 60
            if len(self.history) > 0:
                his_move_piece = self.history[-1]
                self.update_his(his_move_piece, menu)


    def find_last_move(self, key_move):
        rev = self.history[::-1]
        for move in rev:
            if list(move.keys())[0] == key_move:
                return list(move.values())[0]
        return "0"



    def update_his(self, his_move_piece, menu):
        if list(his_move_piece.keys())[0] == "K":
            menu.history_move[0] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "Q":
            menu.history_move[1] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "R":
            menu.history_move[2] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "B":
            menu.history_move[3] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "N":
            menu.history_move[4] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "P":
            menu.history_move[5] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "k":
            menu.history_move[6] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "q":
            menu.history_move[7] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "r":
            menu.history_move[8] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "b":
            menu.history_move[9] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "n":
            menu.history_move[10] = list(his_move_piece.values())[0]
        elif list(his_move_piece.keys())[0] == "p":
            menu.history_move[11] = list(his_move_piece.values())[0]


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

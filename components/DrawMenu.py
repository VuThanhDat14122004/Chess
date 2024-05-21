import pygame
import time
import chess

class DrawMenu:
    def __init__(self, canvas) -> None:
        self.piece_images = {}
        self.screen = canvas
        self.start_time = pygame.time.get_ticks() #minutes
        self.time_limit = 900 #seconds
        self.square_size = 80
        self.SQUARE_SIZE = 80
        self.BORDER_SIZE = 4
        self.HIGHTLIGHT_COLOR = (100, 249, 83, 130)
        self.SELECTED_COLOR = (255, 0, 0)
        self.is_promote = False
        self.color_promote = True
        self.current_time = 900
        self.history_move = ["0","0","0","0","0","0","0","0","0","0","0","0"]
        # self.piece_history = []

    def display(self):
        self.screen.fill((150,150,150))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 320, 40))

        self.draw_count_down()
        self.draw_board_not_promote()
        self.draw_board_promote()
        self.load_pieces()
        self.draw_promote_menu(self.color_promote)
        self.draw_board_history()

    def draw_count_down(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        second = int(elapsed_time // 1000)

        second = self.time_limit - second
        minutes = int(second // 60)
        second %= 60
        self.current_time = minutes*60 + second
        time_text = f"Time remaining {minutes:02}:{second:02}"
        font = pygame.font.Font(None, 36)
        text = font.render(time_text, True, (150,250, 100))
        text_rect = text.get_rect(topright=(self.screen.get_width() - 40 , self.screen.get_height()- 630))
        self.screen.blit(text, text_rect)
        pygame.display.flip()


    def load_pieces(self):
        list_piece = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        for piece in range(len(list_piece)):
            for color in chess.COLORS:
                piece_name = chess.piece_name(list_piece[piece]).upper()
                color_name = "W" if color else "B"
                image_path = f"./resources/imgs/{color_name}_{piece_name}.png"
                self.piece_images[(piece, color)] = pygame.image.load(image_path)  
    

    def draw_promote_menu(self, color_piece: bool):
        if self.is_promote:
            for square in range(4):
                image = self.piece_images[(square, color_piece)]
                rect = image.get_rect(
                    center=(
                        (square % 4 + 0.5) * self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                    )
                )
                self.screen.blit(image, rect)


    def draw_board_not_promote(self):
        for row in range(1):
            for col in range(4):
                color = (255,255,0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.SQUARE_SIZE,
                        (row+ 0.5) * self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                    ),
                )
        

    def draw_board_promote(self):
        if self.is_promote:
            for row in range(1):
                for col in range(4):  
                    pygame.draw.rect(
                    self.screen,
                    self.HIGHTLIGHT_COLOR,
                    (
                        col * self.SQUARE_SIZE,
                        (row+0.5) * self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                    ),
                    self.BORDER_SIZE,
                    )

    def draw_board_history(self):
        w_king = pygame.image.load("./resources/imgs/w_king.png")
        w_queen = pygame.image.load("./resources/imgs/w_queen.png")
        w_rook = pygame.image.load("./resources/imgs/w_rook.png")
        w_bishop = pygame.image.load("./resources/imgs/w_bishop.png")
        w_knight = pygame.image.load("./resources/imgs/w_knight.png")
        w_pawn = pygame.image.load("./resources/imgs/w_pawn.png")
        b_king = pygame.image.load("./resources/imgs/b_king.png")
        b_queen = pygame.image.load("./resources/imgs/b_queen.png")
        b_rook = pygame.image.load("./resources/imgs/b_rook.png")
        b_bishop = pygame.image.load("./resources/imgs/b_bishop.png")
        b_knight = pygame.image.load("./resources/imgs/b_knight.png")
        b_pawn = pygame.image.load("./resources/imgs/b_pawn.png")
        list_piece = [w_king, w_queen, w_rook, w_bishop, w_knight, w_pawn, b_king, b_queen, b_rook, b_bishop, b_knight, b_pawn]
        iter = 0
        iter_move = 0
        
        for col in range(4):
            for row in range(6):
                if col % 2 == 0:
                    image = list_piece[iter]
                    
                    rect = image.get_rect(
                        center=(
                            (col % 4 + 0.5) * self.SQUARE_SIZE,
                            (row+2) * self.SQUARE_SIZE,
                        )
                    )
                    self.screen.blit(image, rect)
                    iter += 1
                else:
                    move_his = self.history_move[iter_move]
                    font = pygame.font.Font(None, 36)
                    text = font.render(move_his, True, (0,0,0))
                    if col == 1:
                        text = font.render(move_his, True, (255,255,255))
                    text_rect = text.get_rect(center=(col * self.SQUARE_SIZE + 20, (row+2) * self.SQUARE_SIZE))
                    self.screen.blit(text, text_rect)
                    iter_move += 1
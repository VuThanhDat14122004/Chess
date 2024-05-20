import pygame

import chess
from components.Board import Board


class DrawBoard:
    def __init__(self, canvas):
        self.piece_images = {}
        self.screen = canvas
        self.load_pieces()

        self.SQUARE_SIZE = 80
        self.BORDER_SIZE = 4
        self.LIGHT_SQUARE = (220, 208, 194)
        self.DARK_SQUARE = (83, 100, 83)
        self.HIGHTLIGHT_COLOR = (100, 249, 83, 130)
        self.SELECTED_COLOR = (255, 0, 0)
        self.CHECK_COLOR = (255, 0, 0, 128)

    def load_pieces(self):
        for piece in chess.PIECE_TYPES:
            for color in chess.COLORS:
                piece_name = chess.piece_name(piece).upper()
                color_name = "W" if color else "B"
                image_path = f"./resources/imgs/{color_name}_{piece_name}.png"
                self.piece_images[(piece, color)] = pygame.image.load(image_path)

    def display(self, boardGame, selected_square, legal_moves, is_check):

        self.draw_board()
        self.draw_selected_square(selected_square)
        for move in legal_moves:
            if move.from_square == selected_square:
                self.draw_highlight_square(move.to_square)

        if is_check:
            self.draw_check_square(boardGame)

        self.draw_pieces(boardGame)

        return True

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.SQUARE_SIZE,
                        row * self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                    ),
                )

    def draw_pieces(self, board):
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                image = self.piece_images[(piece.piece_type, piece.color)]
                rect = image.get_rect(
                    center=(
                        (square % 8 + 0.5) * self.SQUARE_SIZE,
                        (7 - square // 8 + 0.5) * self.SQUARE_SIZE,
                    )
                )
                self.screen.blit(image, rect)

    def draw_selected_square(self, square):
        if square is None:
            return
        col, row = square % 8, 7 - square // 8
        pygame.draw.rect(
            self.screen,
            self.SELECTED_COLOR,
            (
                col * self.SQUARE_SIZE,
                row * self.SQUARE_SIZE,
                self.SQUARE_SIZE,
                self.SQUARE_SIZE,
            ),
            self.BORDER_SIZE,
        )

    def draw_highlight_square(self, square):
        if square is None:
            return
        col, row = square % 8, 7 - square // 8
        pygame.draw.rect(
            self.screen,
            self.HIGHTLIGHT_COLOR,
            (
                col * self.SQUARE_SIZE,
                row * self.SQUARE_SIZE,
                self.SQUARE_SIZE,
                self.SQUARE_SIZE,
            ),
            self.BORDER_SIZE,
        )

    def draw_check_square(self, board):
        king_square = board.king(board.turn)
        if king_square is not None:
            col, row = king_square % 8, 7 - king_square // 8
            pygame.draw.rect(
                self.screen,
                self.CHECK_COLOR,
                (
                    col * self.SQUARE_SIZE,
                    row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                ),
                self.BORDER_SIZE,
            )

    def get_coor(self, x, y):
        return x // self.SQUARE_SIZE, 7 - y // self.SQUARE_SIZE

    def get_board(self):
        return self.boardGame

import pygame

from game.Piece import Piece


class King(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = "resources/imgs/" + color[0] + "_king.png"
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(
            self.img, (board.tile_width - 20, board.tile_height - 20)
        )

        self.notation = "K"

    def get_possible_moves(self, board):
        return []

    def can_castle(self, board):
        pass

    def get_valid_moves(self, board):
        return []

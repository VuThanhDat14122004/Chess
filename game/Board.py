import chess
from components.Bishop import Bishop
from components.King import King
from components.Knight import Knight
from components.Pawn import Pawn
from components.Queen import Queen
from components.Rook import Rook
from game.Square import Square


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = "white"
        self.board = chess.Board()
        boardStrs = str(self.board).split("\n")
        self.config = [b.split(" ") for b in boardStrs]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        squares = []
        for y in range(8):
            row = []
            for x in range(8):
                row.append(Square(x, y, self.tile_width, self.tile_height))
            squares.extend(row)
        return squares

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != ".":
                    square = self.get_square_from_pos((x, y))
                    if piece == "r":
                        square.occupying_piece = Rook((x, y), "black", self)
                    elif piece == "n":
                        square.occupying_piece = Knight((x, y), "black", self)
                    elif piece == "b":
                        square.occupying_piece = Bishop((x, y), "black", self)
                    elif piece == "q":
                        square.occupying_piece = Queen((x, y), "black", self)
                    elif piece == "k":
                        square.occupying_piece = King((x, y), "black", self)
                    elif piece == "p":
                        square.occupying_piece = Pawn((x, y), "black", self)
                    elif piece == "R":
                        square.occupying_piece = Rook((x, y), "white", self)
                    elif piece == "N":
                        square.occupying_piece = Knight((x, y), "white", self)
                    elif piece == "B":
                        square.occupying_piece = Bishop((x, y), "white", self)
                    elif piece == "Q":
                        square.occupying_piece = Queen((x, y), "white", self)
                    elif piece == "K":
                        square.occupying_piece = King((x, y), "white", self)
                    elif piece == "P":
                        square.occupying_piece = Pawn((x, y), "white", self)

    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
        elif self.selected_piece.move(self, clicked_square):
            self.turn = "white" if self.turn == "black" else "black"
        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    def is_in_check(self, color, board_change=None):
        output = False
        king_pos = None

        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]

        if changing_piece is not None:
            if changing_piece.notation == "K":
                king_pos = new_square.pos

        if king_pos is None:
            for piece in pieces:
                if piece.color == color and piece.notation == "K":
                    king_pos = piece.pos

        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True

        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def is_in_checkmate(self, color):
        output = False

        for piece in [i.occupying_piece for i in self.squares]:
            if piece is not None:
                if piece.notation == "K" and piece.color == color:
                    king = piece

        if king.get_valid_moves(self) == []:
            if self.is_in_check(color):
                output = True

        return output

    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True

        for square in self.squares:
            square.draw(display)

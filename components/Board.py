import chess


class Board:
    def __init__(self) -> None:
        self.board = chess.Board()

    def get_board(self):
        return self.board

    def get_move(self, from_square, to_square):
        return chess.Move(from_square, to_square)

    def move_piece(self, move):
        if move in self.get_legal_moves():
            self.board.push(move)
            return True, [move.xboard()[:2], move.xboard()[2:4]]
        return False

    def get_legal_moves(self):
        return list(self.board.legal_moves)

    def can_promote(self, move):
        if self.board.piece_at(move.from_square).piece_type == chess.PAWN and (
            move.to_square // 8 == 0 or move.to_square // 8 == 7
        ):
            return True
        return False

    def promote(self, move, piece):
        move.promotion = piece
        self.board.push(move)

    def piece_at(self, square):
        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:
            return square

        return None

    def is_checkmate(self):
        return self.board.is_checkmate()

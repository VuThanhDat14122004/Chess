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

    def can_promote(self, from_square, to_square):
        if self.board.piece_at(from_square) is None:
            return False
        if (self.board.piece_at(from_square).piece_type == chess.PAWN and (
            ((to_square >= 0 and to_square <= 7)and(from_square >= 8 and from_square <= 15))
            or((to_square >= 56 and to_square <= 63))and(from_square >= 48 and from_square <= 55))):
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
'''
board = chess.Board()

# Lấy danh sách các nước đi hợp lệ
legal_moves = board.legal_moves

# Duyệt qua từng nước đi hợp lệ
for move in legal_moves:
    # In ra thông tin về quân cờ thực hiện nước đi
    print(f"Nước đi: {move.uci()}")
    print(f"Quân cờ: {move.piece}")
'''
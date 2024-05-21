from collections import defaultdict
import chess
import chess.polyglot
import math
from chess import Move, Board

MaxValue = 999999999
pieceValues = {None: 0, "p": 100, "n": 320, "b": 330, "r": 500, "q": 1500, "k": 20000}
TranspositionTable = {}

pawn_table = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    10,
    10,
    20,
    30,
    30,
    20,
    10,
    10,
    5,
    5,
    10,
    25,
    25,
    10,
    5,
    5,
    0,
    0,
    0,
    20,
    20,
    0,
    0,
    0,
    5,
    -5,
    -10,
    0,
    0,
    -10,
    -5,
    5,
    5,
    10,
    10,
    -20,
    -20,
    10,
    10,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

knight_table = [
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
    -40,
    -20,
    0,
    0,
    0,
    0,
    -20,
    -40,
    -30,
    0,
    10,
    15,
    15,
    10,
    0,
    -30,
    -30,
    5,
    15,
    20,
    20,
    15,
    5,
    -30,
    -30,
    0,
    15,
    20,
    20,
    15,
    0,
    -30,
    -30,
    5,
    10,
    15,
    15,
    10,
    5,
    -30,
    -40,
    -20,
    0,
    5,
    5,
    0,
    -20,
    -40,
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
]

bishop_table = [
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    5,
    10,
    10,
    5,
    0,
    -10,
    -10,
    5,
    5,
    10,
    10,
    5,
    5,
    -10,
    -10,
    0,
    10,
    10,
    10,
    10,
    0,
    -10,
    -10,
    10,
    10,
    10,
    10,
    10,
    10,
    -10,
    -10,
    5,
    0,
    0,
    0,
    0,
    5,
    -10,
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
]

rook_table = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    10,
    10,
    10,
    10,
    10,
    10,
    5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    0,
    0,
    0,
    5,
    5,
    0,
    0,
    0,
]

queen_table = [
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    5,
    5,
    5,
    5,
    0,
    -10,
    -5,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    -10,
    5,
    5,
    5,
    5,
    5,
    0,
    -10,
    -10,
    0,
    5,
    0,
    0,
    0,
    0,
    -10,
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
]

king_table = [
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -20,
    -30,
    -30,
    -40,
    -40,
    -30,
    -30,
    -20,
    -10,
    -20,
    -20,
    -20,
    -20,
    -20,
    -20,
    -10,
    20,
    20,
    0,
    0,
    0,
    0,
    20,
    20,
    20,
    30,
    10,
    0,
    0,
    10,
    30,
    20,
]


def EvaluatePiece(piece, square, is_white):
    if piece.piece_type == chess.PAWN:
        value = pieceValues["p"] + (
            pawn_table[square] if is_white else pawn_table[chess.square_mirror(square)]
        )
    elif piece.piece_type == chess.KNIGHT:
        value = pieceValues["n"] + (
            knight_table[square]
            if is_white
            else knight_table[chess.square_mirror(square)]
        )
    elif piece.piece_type == chess.BISHOP:
        value = pieceValues["b"] + (
            bishop_table[square]
            if is_white
            else bishop_table[chess.square_mirror(square)]
        )
    elif piece.piece_type == chess.ROOK:
        value = pieceValues["r"] + (
            rook_table[square] if is_white else rook_table[chess.square_mirror(square)]
        )
    elif piece.piece_type == chess.QUEEN:
        value = pieceValues["q"] + (
            queen_table[square]
            if is_white
            else queen_table[chess.square_mirror(square)]
        )
    elif piece.piece_type == chess.KING:
        value = pieceValues["k"] + (
            king_table[square] if is_white else king_table[chess.square_mirror(square)]
        )
    return value


def TrySkipTurn(board: Board) -> bool:
    if board.is_check():
        return False
    else:
        board.push(Move.null())
        return True


def UndoSkipTurn(board: Board) -> None:
    board.pop()


def ForceSkipTurn(board: Board) -> None:
    board.push(Move.null())


def IsDraw(board: Board) -> bool:
    return (
        board.is_fifty_moves()
        or board.is_insufficient_material()
        or board.is_stalemate()
        or board.is_repetition()
    )


def getLegalCapture(board: Board) -> list[Move]:
    captures = []
    for m in list(board.legal_moves):
        if board.is_capture(m):
            captures.append(m)
    return captures


class ChessAl2:
    def __init__(self):
        self.depth = 3
        self.startAlpha = -MaxValue
        self.startBeta = MaxValue
        self.numPrunes = []
        for i in range(self.depth + 1):
            self.numPrunes.append(0)
        self.evaluationCalls = None
        self.sign = float(1)
        self.bestMoveTotal = None
        self.board = None
        self.opening_book_path = "resources/Perfect2017.bin"

    def Think(self, board: Board) -> Move:
        self.board = board
        self.sign = 1 if board.turn else -1

        # Kiểm tra nước đi trong sách khai cuộc
        if self.opening_book_path:
            with chess.polyglot.open_reader(self.opening_book_path) as reader:
                try:
                    entry = reader.weighted_choice(board)
                    print(f"Opening move: {entry.move}")
                    return entry.move
                except IndexError:
                    print("No opening move found. Switching to regular search.")

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None  # Trả về None nếu không còn nước đi hợp lệ

        self.bestMoveTotal = legal_moves[0]
        for num in self.numPrunes:
            num = 0
        self.evaluationCalls = 0
        curEvaluation = self.IterativeDeepeningSearch(self.startAlpha, self.startBeta)
        return self.bestMoveTotal

    def MoveFilter(self):
        newMoves = getLegalCapture(self.board)
        attackedSquares = []
        if TrySkipTurn(self.board):
            for m in newMoves:
                atkSqr = m.to_square
                if atkSqr not in attackedSquares:
                    attackedSquares.append(atkSqr)
            UndoSkipTurn(self.board)
        else:
            return list(self.board.legal_moves)

        for m in list(self.board.legal_moves):
            if m.promotion:
                newMoves.append(m)
            self.board.push(m)
            if self.board.is_check:
                newMoves.append(m)
            self.board.pop()
            if m.from_square in attackedSquares:
                newMoves.append(m)
        return newMoves

    def IterativeDeepeningSearch(self, alpha, beta):
        for depth in range(1, self.depth + 1):
            eval = self.Search(depth, alpha, beta, True)
            if eval <= alpha or eval >= beta:
                eval = self.Search(depth, -MaxValue, MaxValue, True)
            alpha = max(alpha, eval - 50)
            beta = min(beta, eval + 50)
        return eval

    def Search(self, depth, alpha, beta, maxPlayer):
        board_key = self.board._transposition_key()
        if (
            board_key in TranspositionTable
            and TranspositionTable[board_key]["depth"] >= depth
        ):
            tt_entry = TranspositionTable[board_key]
            if tt_entry["flag"] == "exact":
                return tt_entry["value"]
            elif tt_entry["flag"] == "lowerbound":
                alpha = max(alpha, tt_entry["value"])
            elif tt_entry["flag"] == "upperbound":
                beta = min(beta, tt_entry["value"])
            if alpha >= beta:
                return tt_entry["value"]

        if self.board.is_checkmate():
            return MaxValue if maxPlayer else -MaxValue
        if IsDraw(self.board):
            return 0
        if depth == 0:
            self.evaluationCalls += 1
            return self.AnalyzePosition()

        moves = self.MoveFilter()
        bestEval = -MaxValue if maxPlayer else MaxValue
        bestMove = self.bestMoveTotal
        for m in moves:
            self.board.push(m)
            eval = self.Search(depth - 1, alpha, beta, not maxPlayer)
            self.board.pop()
            if maxPlayer:
                if eval > bestEval:
                    bestEval = eval
                    bestMove = m
                    alpha = max(alpha, eval)
            else:
                if eval < bestEval:
                    bestEval = eval
                    bestMove = m
                    beta = min(beta, eval)
            if alpha >= beta:
                break

        if depth == self.depth:
            self.bestMoveTotal = bestMove

        # Transposition Table
        tt_entry = {
            "value": bestEval,
            "depth": depth,
            "flag": (
                "exact"
                if alpha < bestEval < beta
                else "lowerbound" if bestEval <= alpha else "upperbound"
            ),
        }
        TranspositionTable[board_key] = tt_entry

        return bestEval

    def AnalyzePosition(self):
        return self.EvaluateAllFigure()

    def EvaluateFigure(self, curPiece: chess.Square, pieceTurn: bool) -> float:
        piece = self.board.piece_at(curPiece)
        if piece is None:
            return 0

        # pieceType = piece.symbol().lower()
        color = piece.color
        is_white = piece.color == chess.WHITE
        curPieceValue = EvaluatePiece(piece, curPiece, is_white)
        pieceEvaluation = float(curPieceValue)
        skipSuccess = False
        if pieceTurn:
            skipSuccess = True
            self.board.push(Move.null())
        isDefended = self.board.is_attacked_by(color, curPiece)
        WorseAttacker = 0
        for m in list(self.board.legal_moves):
            if (m.to_square == curPiece) and (
                pieceValues[
                    (
                        self.board.piece_at(m.from_square).symbol().lower()
                        if self.board.piece_at(m.from_square)
                        else None
                    )
                ]
                < pieceEvaluation
            ):
                WorseAttacker += 1
        attackedByWorsePiece = False
        if WorseAttacker > 0:
            attackedByWorsePiece = True
        ForceSkipTurn(self.board)
        numPossibleMoves = 0
        for m in list(self.board.legal_moves):
            if m.from_square == curPiece:
                numPossibleMoves += 1
        isAttacked = self.board.is_attacked_by(not color, curPiece)
        canCapture = []
        for m in list(self.board.legal_moves):
            if m.from_square == curPiece:
                canCapture.append(
                    pieceValues[
                        (
                            self.board.piece_at(m.to_square).symbol().lower()
                            if self.board.piece_at(m.to_square)
                            else None
                        )
                    ]
                    - pieceEvaluation
                    * (self.board.is_attacked_by(not color, m.to_square))
                )
        bestCapture = max(canCapture) if canCapture else 0
        bestCapture = max(bestCapture, 0)
        UndoSkipTurn(self.board)
        if skipSuccess:
            UndoSkipTurn(self.board)
        pieceEvaluation += float(numPossibleMoves - 1.25) / 10
        pieceEvaluation += (0.5 if attackedByWorsePiece else 0) * float(curPieceValue)
        pieceEvaluation += (0.5 if (isAttacked and not isDefended) else 0) * float(
            curPieceValue
        )
        return pieceEvaluation

    def EvaluateAllFigure(self):
        totalEval = float(0)
        for p in range(64):
            pieceEvaluation = self.EvaluateFigure(p, self.board.turn)
            if pieceEvaluation != 0:
                totalEval += pieceEvaluation
        return self.sign * totalEval

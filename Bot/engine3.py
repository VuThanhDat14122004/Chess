import chess
from chess import Move, Board
import chess.polyglot
MaxValue = 999999999
pieceValues = [0, 1, 3, 3, 5, 9, 10]


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


class ChessAl:
    def __init__(self):
        self.depth = 3
        self.startAlpha = -MaxValue
        self.startBeta = MaxValue
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

        self.bestMoveTotal = list(board.legal_moves)[0]

        self.evaluationCalls = 0
        curEvaluation = self.Search(self.depth, self.startAlpha, self.startBeta, True)
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

    def Search(self, depth, alpha, beta, maxPlayer):
        if self.board.is_checkmate():
            return -MaxValue if maxPlayer else MaxValue
        if IsDraw(self.board):
            return 0
        if depth == 0:
            self.evaluationCalls += 1
            return self.EvaluateAllFigure()
        moves = self.MoveFilter()
        if maxPlayer:
            maxEval = float(-MaxValue)
            bestMove = self.bestMoveTotal
            for m in moves:
                self.board.push(m)
                eval = float(self.Search(depth - 1, alpha, beta, not maxPlayer))
                self.board.pop()
                if eval > maxEval:
                    bestMove = m
                    maxEval = eval
                    alpha = eval
                if alpha >= beta:
                    break
            if depth == self.depth:
                self.bestMoveTotal = bestMove
            return maxEval
        else:
            minEval = float(MaxValue)
            for m in moves:
                self.board.push(m)
                eval = float(self.Search(depth - 1, alpha, beta, not maxPlayer))
                self.board.pop()
                if eval < minEval:
                    minEval = eval
                    beta = eval
                if alpha >= beta:
                    break
            return minEval

    def AnalyzePosition(self):
        if self.board.is_checkmate():
            return -MaxValue if self.board.turn else MaxValue
        return self.EvaluateAllFigure()

    def EvaluateFigure(self, curPiece: chess.Square, pieceTurn: bool) -> float:
        pieceType = self.board.piece_type_at(curPiece)
        color = self.board.piece_at(curPiece).color
        curPieceValue = pieceValues[pieceType if pieceType else 0]
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
                        self.board.piece_type_at(m.from_square)
                        if self.board.piece_type_at(m.from_square)
                        else 0
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
                            self.board.piece_type_at(m.to_square)
                            if self.board.piece_type_at(m.to_square)
                            else 0
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
            if self.board.piece_at(p):
                pieceTurn = self.board.piece_at(p).color == self.board.turn
                if self.board.piece_at(p).color:
                    totalEval += self.EvaluateFigure(p, pieceTurn)
                else:
                    totalEval -= self.EvaluateFigure(p, pieceTurn)
        return self.sign * totalEval

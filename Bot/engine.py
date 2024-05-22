from collections import defaultdict
import chess
import chess.polyglot
from chess import Move, Board

MaxValue = 999999999
pieceValues = {None: 0, "p": 100, "n": 320, "b": 330, "r": 500, "q": 1500, "k": 20000}
pieceRanks = {"p": 1, "n": 2, "b": 3, "r": 4, "q": 5, "k": 6}
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


killer_moves = [defaultdict(int) for _ in range(1000)]
history_heuristics = [defaultdict(int) for _ in range(2)]


class ChessAl:
    def __init__(self):
        self.depth = 2
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
        return sorted(newMoves, key=self.MVV_LVA_Score, reverse=True)

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
        transposition = TranspositionTable.get(
            board_key,
            {"depth": -1, "value": 0, "flag": "none", "best_move_raw_value": None},
        )
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
        if depth <= 0:
            self.evaluationCalls += 1
            return self.AnalyzePosition()

        # Null Move Pruning
        if depth >= 3 and not self.board.is_check() and not self.board.is_checkmate():
            self.board.push(chess.Move.null())
            eval = -self.Search(depth - 1 - 2, -beta, -beta + 1, not maxPlayer)
            self.board.pop()
            if eval >= beta:
                return eval

        moves = self.MoveFilter()

        # Sắp xếp các nước đi dựa trên lịch sử heuristic
        move_potential = []
        for move in moves:
            potential = -(
                (transposition["best_move_raw_value"] == move.uci()) * 2_000_000_000
                + self.board.is_capture(move)
                * 1_000_000
                * pieceValues.get(self.board.piece_type_at(move.to_square), 0)
                - pieceValues.get(self.board.piece_type_at(move.from_square), 0)
                + (move == killer_moves[depth].get(move.uci(), None)) * 900_000
                + history_heuristics[self.board.turn].get(move.uci(), 0)
            )
            move_potential.append((potential, move))

        move_potential.sort(key=lambda x: x[0])
        moves = [move for _, move in move_potential]

        move_potential.sort(key=lambda x: x[0])
        moves = [move for _, move in move_potential]

        bestEval = -MaxValue if maxPlayer else MaxValue
        bestMove = self.bestMoveTotal
        for m in moves:
            if not self.board.is_legal(m):
                continue
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
                # Killer Moves
                if depth < len(killer_moves):
                    killer_moves[depth][m.uci()] += 1
                break

        if depth == self.depth:
            self.bestMoveTotal = bestMove

        # Cập nhật lịch sử heuristic
        history_heuristics[self.board.turn][bestMove] += depth * depth

        # Transposition Table
        tt_entry = {
            "value": bestEval,
            "depth": depth,
            "flag": (
                "exact"
                if alpha < bestEval < beta
                else "lowerbound" if bestEval <= alpha else "upperbound"
            ),
            "best_move_raw_value": bestMove.uci(),  # Cập nhật khóa best_move_raw_value
        }
        TranspositionTable[board_key] = tt_entry

        return bestEval

    def AnalyzePosition(self):
        if self.board.is_checkmate():
            return -MaxValue if self.board.turn else MaxValue
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
        attacker_penalty = 0
        defender_bonus = 0
        for m in list(self.board.legal_moves):
            attacker_piece = self.board.piece_at(m.from_square)
            if attacker_piece:
                attacker_value = EvaluatePiece(
                    attacker_piece, m.from_square, attacker_piece.color == chess.WHITE
                )
                attacker_rank = pieceRanks[attacker_piece.symbol().lower()]
                cur_piece_rank = pieceRanks[piece.symbol().lower()]
                if attacker_rank < cur_piece_rank and attacker_value < curPieceValue:
                    WorseAttacker += 1
                    attacker_penalty += 10 * (
                        cur_piece_rank - attacker_rank
                    )  # Phạt nếu bị tấn công bởi quân yếu hơn

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
                target_piece = self.board.piece_at(m.to_square)
                if target_piece:
                    target_value = EvaluatePiece(
                        target_piece, m.to_square, target_piece.color == chess.WHITE
                    )
                    target_rank = pieceRanks[target_piece.symbol().lower()]
                    if target_rank > cur_piece_rank:
                        defender_bonus += (
                            target_rank - cur_piece_rank
                        ) * 10  # Thưởng nếu bảo vệ quân cờ có thể bị ăn bởi quân có rank cao hơn
                else:
                    target_value = 0
                canCapture.append(
                    target_value
                    - pieceEvaluation
                    * self.board.is_attacked_by(not color, m.to_square)
                )
        bestCapture = max(canCapture) if canCapture else 0
        bestCapture = max(bestCapture, 0)
        UndoSkipTurn(self.board)
        if skipSuccess:
            UndoSkipTurn(self.board)
        pieceEvaluation += float(numPossibleMoves - 1.25) * 10
        pieceEvaluation += (0.5 if attackedByWorsePiece else 0) * float(curPieceValue)
        pieceEvaluation += (0.5 if (isAttacked and not isDefended) else 0) * float(
            curPieceValue
        )
        pieceEvaluation -= attacker_penalty
        pieceEvaluation += defender_bonus
        return pieceEvaluation

    def EvaluateAllFigure(self):
        score = 0.0
        white_piece_count = 0
        black_piece_count = 0
        white_pawn_bonus = 0.0
        black_pawn_bonus = 0.0

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                is_white = piece.color == chess.WHITE
                if is_white:
                    white_piece_count += 1
                else:
                    black_piece_count += 1
                score += self.EvaluateFigure(square, self.board.turn) * (
                    1 if is_white else -1
                )

        # Điều chỉnh điểm số dựa trên số lượng quân cờ (endgame trọng số)
        total_pieces = white_piece_count + black_piece_count
        endgame_multiplier = (
            1.2
            if total_pieces <= 12 or white_piece_count <= 6 or black_piece_count <= 6
            else 1.0
        )

        if endgame_multiplier > 1.0:  # Điều kiện xác định cờ tàn
            for square in chess.SQUARES:
                piece = self.board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN:
                    rank = chess.square_rank(square)
                    if piece.color == chess.WHITE:
                        if rank == 6:
                            white_pawn_bonus += 50  # thưởng cho tốt ở rank 7
                        elif rank == 5:
                            white_pawn_bonus += 30  # thưởng cho tốt ở rank 6
                    else:
                        if rank == 1:
                            black_pawn_bonus += 50  # thưởng cho tốt ở rank 2
                        elif rank == 2:
                            black_pawn_bonus += 30  # thưởng cho tốt ở rank 3

        score += (white_pawn_bonus - black_pawn_bonus) * endgame_multiplier

        # Tính toán điểm số cho trạng thái chiếu và chiếu bí
        white_board_multiplier = -1 if self.board.turn == chess.WHITE else 1
        if self.board.is_check():
            score -= white_board_multiplier * (
                pieceValues["k"] // 10
            )  # Giảm điểm cho trạng thái chiếu
        if self.board.is_checkmate():
            score -= white_board_multiplier * (
                pieceValues["k"] // 4
            )  # Giảm điểm mạnh hơn cho trạng thái chiếu bí

        return score * self.sign

    def MVV_LVA_Score(self, move):
        victim = self.board.piece_at(move.to_square)
        attacker = self.board.piece_at(move.from_square)
        if victim and attacker:
            return (
                pieceValues[victim.symbol().lower()]
                - pieceValues[attacker.symbol().lower()]
            )
        return 0
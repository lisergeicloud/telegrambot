import math
import copy
from board import State, Board

class AlphaBetaPruning:

    def __init__(self, max_ply):
        self.max_ply = max_ply

    def run(self, player, board, max_ply):
        assert max_ply > 0, "Maximum depth must be greater than 0."

        self.max_ply = max_ply
        inf = math.inf
        self.alpha_beta_pruning(player, board, -inf, inf, 0)

    def alpha_beta_pruning(self, player, board, alpha, beta, current_ply):
        if current_ply == self.max_ply or board.game_over:
            return self.score(player, board, current_ply)

        current_ply += 1

        if board.get_turn() == player:
            return self.get_max(player, board, alpha, beta, current_ply)
        else:
            return self.get_min(player, board, alpha, beta, current_ply)

    def get_max(self, player, board, alpha, beta, current_ply):
        best_move_index = -1
        am = copy.deepcopy(board.get_available_moves())

        for the_move in am:
            modified_board = copy.deepcopy(board)
            modified_board.move(the_move)

            score = self.alpha_beta_pruning(player, modified_board, alpha, beta, current_ply)

            if score > alpha:
                alpha = score
                best_move_index = the_move

            if alpha >= beta:
                break
        if best_move_index != -1:
            board.move(best_move_index)

        return int(alpha)

    def get_min(self, player, board, alpha, beta, current_ply):
        best_move_index = -1
        am = copy.deepcopy(board.get_available_moves())

        for the_move in am:
            modified_board = copy.deepcopy(board)
            modified_board.move(the_move)

            score = self.alpha_beta_pruning(player, modified_board, alpha, beta, current_ply)

            if score < beta:
                beta = score
                best_move_index = the_move

            if alpha >= beta:
                break
        if best_move_index != -1:
            board.move(best_move_index)

        return int(beta)

    def score(self, player, board, current_ply):
        assert player in [State.X, State.O], "Player must be X or O."

        opponent = State.O if player == State.X else State.X

        if board.game_over and board.get_winner() == player:
            return 10 - current_ply
        elif board.game_over and board.get_winner() == opponent:
            return -10 + current_ply
        else:
            return 0

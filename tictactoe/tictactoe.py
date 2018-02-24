import telegram

from tictactoe import alphabeta, evaluation


def get_reply(board_size):
    buttons = []
    for i in range(0, board_size * board_size, board_size):
        row = [telegram.InlineKeyboardButton(' ', callback_data=str(i + x)) for x in range(board_size)]
        buttons.append(row)
    return buttons


def run_move(game):
    if game[3] == 3:
        abp = alphabeta.AlphaBetaPruning(game[0].board.board_width ** 2 - 1)
        if game[0].board.board_width > 3:
            m_p = 5
        else:
            m_p = game[0].board.board_width ** 2 - 1
        abp.run(player=game[0].board.get_turn(), board=game[0].board, max_ply=m_p)
    elif game[3] == 8:
        if game[0].board.move_count == 0:
            pl_mv = evaluation.firstmove(game[0].board)
        elif game[0].board.move_count == 1:
            pl_mv = evaluation.secondmove(game[0].board)
        else:
            pl_mv = evaluation.nextMove(game[0].board, 2, 3)
        game[0].board.move(pl_mv)
    else:
        raise ValueError

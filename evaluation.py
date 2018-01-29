import queue as q
import gomokuboard
import time
import random
import copy


def firstmove (board):
    x = board.board_width // 2
    return x * board.board_width + x

def secondmove (board):
    x, y = 0, 0
    for i in range(board.board_width):
        for j in range(board.board_width):
            if board.board[i][j] != gomokuboard.State.Blank:
                x, y = i, j

    if y <= board.board_width // 2:
        dy = 1
    else:
        dy = -1

    if x <= board.board_width // 2:
        dx = 1
    else:
        dx = -1

    return (x + dx) * board.board_width + (y + dy)


def randommove (board):
    t = True
    while t:
        index = random.randint(0, board.board_width ** 2 - 1)
        t = index in board.moves_available
    board.move(index)


def _eval_func(board, index, attack):
    x, y = index % board.board_width, index // board.board_width
    if attack:
        colour = gomokuboard.State.X if board.get_turn() == gomokuboard.State.X else gomokuboard.State.O
        opp = gomokuboard.State.O if board.get_turn() == gomokuboard.State.X else gomokuboard.State.X
    else:
        colour = gomokuboard.State.O if board.get_turn() == gomokuboard.State.X else gomokuboard.State.X
        opp = gomokuboard.State.X if board.get_turn() == gomokuboard.State.X else gomokuboard.State.O

    total_consec = 0
    for pair in ((1, 0), (0, 1), (1, 1), (1, -1)):
        dy, dx = pair
        pathlist = ["."]
        for s in (1, -1):
            for i in range(1, gomokuboard.WINNING):
                py = y + dy * i * s
                px = x + dx * i * s
                if ((not board.in_board(py, px) or board.board[py][px] == opp) or (i + 1 == gomokuboard.WINNING and board.in_board(py + dy * s, px + dx * s) and board.board[py + dy * s][px + dx * s] == colour)):
                    break
                elif s > 0:
                    pathlist.append(board.board[py][px])
                elif s < 0:
                    pathlist.insert(0, board.board[py][px])

        path_num = len(pathlist) - gomokuboard.WINNING + 1
        if path_num > 0:
            for i in range(path_num):
                consec = pathlist[i:i+gomokuboard.WINNING].count(colour)
                total_consec += consec ** 5 if consec != gomokuboard.WINNING - 1 else 100 ** (9 if attack else 8)

    return total_consec

def evaluate_position(board, p):
    pos = p[0] * board.board_width + p[1]

    if board.in_board(p[0], p[1]) and pos in board.moves_available:
        return _eval_func(board, pos, True) + _eval_func(board, pos, False)
    else:
        return 0


def attackArea(y, x):
    area = []

    for pair in ((1, 0), (0, 1), (1, 1), (1, -1)):
        dy, dx = pair

        for s in (-1, 1):
            for i in range(1, gomokuboard.WINNING):
                py = y + dy * i * s
                px = x + dx * i * s
                area.append((py, px))

    return area


def topAtoms(board, limit):
    topqueue = q.PriorityQueue()
    spots = set()

    for t in board.board_X + board.board_O:
        for m in attackArea(t[0], t[1]):
            if board.in_board(m[0], m[1]) and m[0] * board.board_width + m[1] in board.moves_available:
                spots.add(m)

    for r in spots:
        topqueue.put((evaluate_position(board, r)*(-1), r))

    toplist = []
    i = 0

    while i < limit and not topqueue.empty():
        toplist.append(topqueue.get())
        i += 1

    for i in range(len(toplist)):
        toplist[i] = (- toplist[i][0], toplist[i][1])

    return toplist


def dive3(board, dlimit, st_time, tlimit):
    bm = topAtoms(board, 1)[0][1]
    nextboard = copy.deepcopy(board)
    nextboard.move(bm[0] * nextboard.board_width + bm[1])

    if nextboard.game_over:
        return 1
    elif time.time() - st_time > tlimit or not dlimit:
        return 0
    else:
        return - dive3(nextboard, dlimit - 1, st_time, tlimit)


def nextMove(board, tlimit, dive = 3):
    check_top = 10
    check_depth = 20
    atomlist = topAtoms(board, check_top)
    mehlist = []
    bahlist = []

    tfract = (tlimit - ((0.1) * (tlimit / 10 + 1))) / float(len(atomlist))

    for atom in atomlist:
        (val, mv) = atom
        nextboard = copy.deepcopy(board)
        nextboard.move(mv[0] * nextboard.board_width + mv[1])

        if nextboard.game_over:
            return mv[0] * nextboard.board_width + mv[1]
        elif dive == 3:
            score = - dive3(nextboard, check_depth - 1, time.time(), tfract)

        if score == 1:
            return mv[0] * nextboard.board_width + mv[1]
        elif score == 0:
            mehlist.append((score, mv))
        elif score > -1:
            bahlist.append((score, mv))

    if len(mehlist):
        return mehlist[0][1][0] * board.board_width + mehlist[0][1][1]
    elif len(bahlist):
        return mehlist[-1][1][0] * board.board_width + mehlist[-1][1][1]
    else:
        return atomlist[0][1][0] * board.board_width + atomlist[0][1][1]


from enum import Enum, unique

WINNING = 5


@unique
class State(Enum):
    Blank = 1
    X = 2
    O = 3


class GomokuBoard:

    def __init__(self, board_width):
        self.board_width = board_width
        self.board = [[State.Blank for j in range(self.board_width)] for i in range(self.board_width)]

        self.move_count = 0
        self.game_over = False
        self.players_turn = State.X
        self.winner = State.Blank

        self.moves_available = {}

        for i in range(self.board_width ** 2):
            self.moves_available[i] = i

        self.board_X = []
        self.board_O = []

        self.bad_diag = []
        self.bad_add_diag = []

        for i in range(self.board_width):
            if i > self.board_width - WINNING:
                self.bad_add_diag.append([i, self.board_width - 1])
                self.bad_diag.append([i, 0])
                self.bad_diag.append([0, i])
            else:
                self.bad_add_diag.append([0, i])

    def reset(self):
        self.move_count = 0
        self.game_over = False
        self.players_turn = State.X
        self.winner = State.Blank
        self.initialize()

    def initialize(self):
        self.board = [[State.Blank for j in range(self.board_width)] for i in range(self.board_width)]

        self.moves_available = {}

        for i in range(self.board_width ** 2):
            self.moves_available[i] = i

    def move(self, index):
        return self.mov(index % self.board_width, index // self.board_width)

    def mov(self, x, y):
        assert not self.game_over, "TicTacToe is over. No moves can be played."

        if self.board[y][x] == State.Blank:
            self.board[y][x] = self.players_turn
        else:
            return False

        self.move_count += 1
        del self.moves_available[y * self.board_width + x]

        if self.players_turn == State.X:
            self.board_X.append([y, x])
        else:
            self.board_O.append([y, x])

        if self.move_count == self.board_width ** 2:
            self.winner = State.Blank
            self.game_over = True

        self.check_row(y)
        self.check_column(x)
        self.check_diagonal_from_top_left(y, x)
        self.check_diagonal_from_top_right(y, x)

        self.players_turn = State.O if self.players_turn == State.X else State.X
        return True

    def get_turn(self):
        return self.players_turn

    def get_winner(self):
        assert self.game_over, "TicTacToe is not over yet"
        return self.winner

    def get_available_moves(self):
        return self.moves_available

    def set_victory(self):
        self.winner = self.players_turn
        self.game_over = True

    def check_row(self, row):
        r = 0

        for i in range(1, self.board_width):

            if self.board[row][i] != self.board[row][i-1]:
                r = 0
            elif self.board[row][i] == self.board[row][i-1] and self.board[row][i] != State.Blank:
                r += 1

            if r == WINNING - 1:
                self.set_victory()
                break

    def check_column(self, col):
        column = 0

        for i in range(1, self.board_width):

            if self.board[i][col] != self.board[i-1][col]:
                column = 0
            elif self.board[i][col] == self.board[i-1][col] and self.board[i][col] != State.Blank:
                column += 1

            if column == WINNING - 1:
                self.set_victory()
                break

    def check_diagonal_from_top_left(self, y, x):
        diag_score = 0
        start_point = [y - min(x, y), x - min(x, y)]

        if start_point not in self.bad_diag:

            i = start_point[0] + 1
            j = start_point[1] + 1

            while i < self.board_width - start_point[1] and j < self.board_width - start_point[0]:

                if self.board[i][j] != self.board[i-1][j-1]:
                    diag_score = 0
                elif self.board[i][j] == self.board[i-1][j-1] and self.board[i][j] != State.Blank:
                    diag_score += 1

                if diag_score == WINNING - 1:
                    self.set_victory()
                    break

                i += 1
                j += 1

    def check_diagonal_from_top_right(self, y, x):
        diag_score = 0
        start_point = [max(0, x + y - self.board_width + 1), min(self.board_width - 1, x + y)]

        if start_point not in self.bad_add_diag:

            i = start_point[0] + 1
            j = start_point[1] - 1

            while i < start_point[1] + 1 and j > start_point[0] - 1:

                if self.board[i][j] != self.board[i-1][j+1]:
                    diag_score = 0
                elif self.board[i][j] == self.board[i-1][j+1] and self.board[i][j] != State.Blank:
                    diag_score += 1

                if diag_score == WINNING - 1:
                    self.set_victory()
                    break

                i += 1
                j -= 1

    def in_board(self, y, x):
        if y >= self.board_width or x >= self.board_width:
            return False

        if y < 0 or x < 0:
            return False

        return True

    def __str__(self):
        s = ''

        for i in range(self.board_width):
            for j in range(self.board_width):
                if self.board[i][j] == State.Blank:
                    s += '.'
                else:
                    s += self.board[i][j].name
            if i < self.board_width - 1:
                s += '\n'

        return s

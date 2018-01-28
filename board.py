from enum import Enum, unique


@unique
class State(Enum):
    Blank = 1
    X = 2
    O = 3


class Board:

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

        if self.move_count == self.board_width ** 2:
            self.winner = State.Blank
            self.game_over = True

        self.check_row(y)
        self.check_column(x)
        if x == y:
            self.check_diagonal_from_top_left()
        if x == self.board_width - 1 - y:
            self.check_diagonal_from_top_right()

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
        for i in range(1, self.board_width):
            if self.board[row][i] != self.board[row][i-1]:
                break
            if i == self.board_width - 1:
                self.set_victory()

    def check_column(self, col):
        for i in range(1, self.board_width):
            if self.board[i][col] != self.board[i-1][col]:
                break
            if i == self.board_width - 1:
                self.set_victory()

    def check_diagonal_from_top_left(self):
        for i in range(1, self.board_width):
            if self.board[i][i] != self.board[i-1][i-1]:
                break
            if i == self.board_width - 1:
                self.set_victory()

    def check_diagonal_from_top_right(self):
        for i in range(1, self.board_width):
            if self.board[self.board_width - 1 - i][i] != self.board[self.board_width - i][i - 1]:
                break
            if i == self.board_width - 1:
                self.set_victory()

    def to_string(self):
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

from tictactoe import board, alphabeta


class Console:
    def __init__(self, width):
        self.board = board.Board(width)
        self.human = board.State.X
        self.ai = board.State.O

    def play(self):

        print("Starting a new game.")

        while True:

            self.set_sides()

            print("You are playing for " + self.human.name)

            while True:

                self.print_game_status()
                self.play_move()

                if self.board.game_over:
                    self.print_winner()
                    break

            if not self.try_again():
                break

    def play_move(self):
        if self.board.get_turn() == self.human:
            self.get_player_move()
        else:
            abp = alphabeta.AlphaBetaPruning(self.board.board_width ** 2 - 1)
            if self.board.board_width > 3:
                m_p = 5
            else:
                m_p = self.board.board_width ** 2 - 1
            abp.run(player=self.board.get_turn(), board=self.board, max_ply=m_p)

    def print_game_status(self):
        print("\n" + self.board.to_string() + "\n")
        print(self.board.get_turn().name + "'s turn")

    def get_player_move(self):

        while True:
            try:
                move = int(input("Index of move: "))
                if move < 0 or move > self.board.board_width ** 2 - 1:
                    raise ValueError
                if not self.board.move(move):
                    raise ZeroDivisionError
                break
            except ValueError:
                print("Index should be a number between 0 and " + str(self.board.board_width ** 2 - 1))
            except ZeroDivisionError:
                print("Invalid move. Selected index must be blank")

    def print_winner(self):
        winner = self.board.get_winner()

        print("\n" + self.board.to_string() + "\n")

        if winner == board.State.Blank:
            print("The TicTacToe is a Draw.")
        else:
            print("Player " + str(winner.name) + " wins!")

    def try_again(self):
        if self.prompt_try_again():
            self.board.reset()
            print("Started new game")
            return True

        return False

    def prompt_try_again(self):
        while True:
            try:
                ans = input("Would you like to start a new game? (Y/N): ").upper()
                if ans == 'Y':
                    return True
                elif ans == 'N':
                    return False
                else:
                    raise ValueError
            except ValueError:
                print("Enter 'y' or 'n' in any case")

    def set_sides(self):

        while True:
            try:
                ans = input("Choose your side: (X/O): ").upper()
                if ans == 'X':
                    self.human = board.State.X
                    self.ai = board.State.O
                    return
                elif ans in ['O', '0']:
                    self.human = board.State.O
                    self.ai = board.State.X
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Enter 'x' or  'o'.")


def game(n):
    Console(n).play()


if __name__ == '__main__':
    game(3)

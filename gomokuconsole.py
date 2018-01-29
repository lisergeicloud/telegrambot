import alphabeta
import gomokuboard
import evaluation


class Console:

    def __init__(self, width):
        self.board = gomokuboard.GomokuBoard(width)
        self.human = gomokuboard.State.X
        self.ai = gomokuboard.State.O

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
            if self.board.move_count == 0:
                pl_mv = evaluation.firstmove(self.board)
            elif self.board.move_count == 1:
                pl_mv = evaluation.secondmove(self.board)
            else:
                pl_mv = evaluation.nextMove(self.board, 2, 3)
            self.board.move(pl_mv)

    def print_game_status(self):
        print("\n" + str(self.board) + "\n")
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

        print("\n" + str(self.board) + "\n")

        if winner == gomokuboard.State.Blank:
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
                    self.human = gomokuboard.State.X
                    self.ai = gomokuboard.State.O
                    return
                elif ans in ['O', '0']:
                    self.human = gomokuboard.State.O
                    self.ai = gomokuboard.State.X
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Enter 'x' or  'o'.")


def game(n):
    Console(n).play()


if __name__ == '__main__':
    game(8)

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class Square(Button):
    """
    A blueprint for a single position of the Tic-Tac-Toe board where a token can be placed.
    """

    def __init__(self, index, **kwargs):
        super(Square, self).__init__(**kwargs)
        self.id = str(index)

    def get_id(self):
        return self.id

    def update_square(self, player):
        self.text = player


class Board(GridLayout):
    """
    A blueprint for the Tic-Tac-Toe playing board.
    """

    b = None

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.cols = 3

    def reset(self):
        self.b = [i for i in range(9)]

    def update_board(self, index, player):
        self.b[int(index)] = player


class TicTacToeGame(BoxLayout):
    """
    A classic game of Tic-Tac-Toe also known as Noughts and Crosses.
    """

    human = "O"
    computer = "X"
    squares = []
    winningMoves = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                    [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]

    def __init__(self, **kwargs):
        super(TicTacToeGame, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 20

        self.board = Board()
        self.board.reset()
        # Going through cells
        for index in range(9):
            self.button = Square(index)
            self.squares.append(self.button)
            self.board.add_widget(self.button)
        # Adding the board to the layout
        self.add_widget(self.board)

    def startGame(self):
        print("The game now starts.")
        self.gameState()

    def gameState(self):
        for index in range(9):
            self.squares[index].bind(
                on_press=self.turn_click)

    def turn_click(self, square):
        if square.text == "":
            self.turn(square.get_id(), self.human)
            # The computer takes its turn
            # Before the computer takes a turn check for a win
            if not (self.check_win(self.board.b, self.human) or self.check_win(self.board.b, self.computer)):
                # Before the computer takes a turn, check for a draw
                if not self.check_draw():
                    self.turn(self.best_spot(), self.computer)
                    # Check if computer won
                    if self.check_win(self.board.b, self.computer):
                        # The game is over
                        self.game_over(self.computer)
                else:
                    self.game_over("DRAW!")
            else:
                # The game is over
                self.game_over(self.human)
        else:
            print("This sqaure is occupied")
            # Nothing to do.

    def turn(self, button_id, player):
        # This can be called with the human or the computer player
        # update the sqaure
        self.squares[int(button_id)].update_square(player)
        # then update the internal representation of the board
        self.board.update_board(button_id, player)

    def check_win(self, board, player):
        self.plays = []
        for i, j in enumerate(board):
            if j == player:
                self.plays.append(i)
        for i, j in enumerate(self.winningMoves):
            if all(elem in self.plays for elem in self.winningMoves[i]):
                return True
        return False

    def check_draw(self):
        if len(self.empty_squares(self.board.b)) == 0:
            return True
        return False

    def empty_squares(self, board):
        """
        Return a list of the indexes of empty squares on the board.
        """
        return [self.board.b.index(x) for x in board if x != "O" and x != "X"]

    def best_spot(self):
        # The line below uses a basic AI
        return self.empty_squares(self.board.b)[0]

    def game_over(self, game_winner):
        if game_winner == self.human:
            self.declare_winner("Human Won.")
        elif game_winner == self.computer:
            self.declare_winner("Computer Won.")
        else:
            self.declare_winner("DRAW!")

        # Disable further placement of tokens on the board
        for index in range(9):
            self.squares[index].unbind(on_press=self.turn_click)

    def declare_winner(self, winner):
        print(winner)


class TicTacToeApp(App):
    def build(self):
        self.game = TicTacToeGame()
        return self.game

    def on_start(self):
        self.game.startGame()


if __name__ == "__main__":
    TicTacToeApp().run()

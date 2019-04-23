"""
Created on Dec 2018

@author: Emmanuel MOLEFI
@version: 0.1
"""

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup

import kivy
kivy.require('1.10.1')


class Square(Button):
    """
    A blueprint for a single position of the Tic-Tac-Toe game board where a token can be placed.
    """

    def __init__(self, index, **kwargs):
        super(Square, self).__init__(**kwargs)
        self.id = str(index)

    def get_id(self):
        """ Return the id that uniquely identifies a sqaure on the Tic-Tac-Toe game board. """
        return self.id

    def update_square(self, player):
        """ Update the square with the token that indicates a player who just took a turn. """
        self.text = player


class Board(GridLayout):
    """
    A blueprint for the Tic-Tac-Toe playing board.
    """

    tictactoeBoard = None

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.cols = 3

    def reset(self):
        """
        Initialise the Tic-Tac-Toe board with values from 0 through to 8.
        Invoke this function at start of a particular game.
        """
        self.tictactoeBoard = [None] * 9

    def update_board(self, index, player):
        """ Update the internal representation of the board according to a player who just took a turn. """
        self.tictactoeBoard[int(index)] = player


class TicTacToeGame(BoxLayout):
    """
    A classic game of Tic-Tac-Toe also known as Noughts and Crosses.
    There are two players, "X" and "O" .
    This class presents player "X" as the Computer , and player "O" as the Human.
    """

    human = "O"
    computer = "X"
    currentPlayer = "O"
    squares = []
    who = ""
    winningMoves = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                    [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]

    def __init__(self, **kwargs):
        super(TicTacToeGame, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 20

        self.setup()

    def setup(self):
        """
        Setup a board for playing a tic-tac-toe game.
        """
        self.board = Board()
        # Going through cells
        for index in range(9):
            self.button = Square(index)
            self.squares.append(self.button)
            self.board.add_widget(self.button)
        # Adding the board to the layout
        self.add_widget(self.board)

    def start_game(self):
        """
        Begin playing the game of tic-tac-toe.
        """
        print("The game now starts.")
        self.board.reset()
        # Adding event listeners to the buttons
        for index in range(9):
            self.squares[index].bind(
                on_press=self.turn_click)

    def turn_click(self, square):
        """
        Allow the human to take the first turn, then let the computer play second.
        """
        if "O" != self.board.tictactoeBoard[int(square.get_id())]:
            if "X" != self.board.tictactoeBoard[int(square.get_id())]:
                self.turn(square.get_id(), self.currentPlayer)
                # The computer takes its turn
                # Before the computer takes a turn check for a win
                if not self.check_winner(self.board.tictactoeBoard):
                    # Furthermore before the computer takes a turn, check for a draw
                    if not self.check_draw():
                        self.next_turn()
                        # functionality for AI (computer) player
                        if self.currentPlayer == self.computer:
                            self.best_pos = self.best_spot()
                            # This makes use of the basic AI implementation, ie. play on the next available spot.
                            # self.turn(self.best_pos, self.computer)
                            # This makes use of the minimax function.
                            self.turn(self.best_pos["position"], self.computer)
                        self.next_turn()
        else:
            print("This sqaure is occupied")
            # Nothing to do.

    def turn(self, button_id, player):
        """ Functionality for when a turn is taken by a specific player on a particular position. """
        # update the sqaure
        self.squares[int(button_id)].update_square(player)
        # then update the internal representation of the board
        self.board.update_board(button_id, player)

        # check for a Win by the player who just took a turn
        if self.check_winner(self.board.tictactoeBoard):
            # The game is over
            self.game_over(player)

    def next_turn(self):
        """ Functionality for turn-taking between the Player "X" and Player "O" """
        self.currentPlayer = "X" if self.currentPlayer == "O" else "O"

    def check_winner(self, board):
        """ Functionality to check for a winner for the current game. """
        for i in range(len(self.winningMoves)):
            win = self.winningMoves[i]
            if (board[win[0]] == board[win[1]] and board[win[1]] == board[win[2]] and board[win[0]] != None):
                return board[win[0]]
                # return True
        return False

    def check_draw(self):
        """
        Return True for a DRAW , otherwise return False for NOT a Draw
        A DRAW is when there is no more available places on the board to play
        and there is no winner.
        """
        if not self.check_winner(self.board.tictactoeBoard):
            if not self.check_winner(self.board.tictactoeBoard):
                if len(self.empty_squares(self.board.tictactoeBoard)) == 0:
                    self.game_over("DRAW")
                    return True
        return False

    def empty_squares(self, board):
        """ Return a list of the indexes of empty squares on the board. """
        emptySpaces = []
        for i in range(len(board)):
            if board[i] == None:
                emptySpaces.append(i)
        return emptySpaces

    def best_spot(self):
        """ Functionality to find the best position for the computer to place its token. """
        # The line below uses an unbeatable AI , this must return an index
        return self.minimax(self.board.tictactoeBoard, self.computer)

    def game_over(self, game_winner):
        """ Functionality for when the game is over. """
        # Consider highlighting the winning combination depending on who won the game
        if game_winner == self.human:
            print("Human Won.")
            self.who = "O Winnner!"
        elif game_winner == self.computer:
            print("Computer Won.")
            self.who = "X Winner!"
        else:
            print("DRAW!")
            self.who = "DRAW!"

        # Disable further placement of tokens on the board
        for index in range(9):
            self.squares[index].unbind(on_press=self.turn_click)

        self.game_over_settings()

    def declare_winner(self):
        return self.who

    def game_over_settings(self):
        """ Functionality for displaying useful information at the end of the game. """
        # create content and add to the popup
        title = self.declare_winner()
        content = Button(text='REPLAY!')
        popup = Popup(title=title,
                      content=content,
                      size_hint=(None, None), size=(350, 200), auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)

        popup.bind(on_dismiss=self.display_winner)

        # open the popup
        popup.open()

    def display_winner(self, instance):
        """ End of match/game details. """
        self.replay_game()
        print('Popup', instance, 'is being dismissed but is prevented!')
        # return True

    def replay_game(self):
        """ Allow for a rematch of the classic game of Tic-Tac-Toe. """
        # Reset the sqaures
        for i in range(9):
            self.squares[i].update_square("")
        self.start_game()

    def swap(self, player):
        """ Functionality to allow swapping of player turns for the purpose of the minimax function. """
        return "X" if player == "O" else "O"

    def minimax(self, board, player):
        """ The minimax function. """

        # Making a copy of the board for use by the minimax function
        boardCopy = board[:]

        # Checking for terminal states
        winner = self.check_winner(boardCopy)
        if winner == self.computer:
            return {"value": 1, "position": -1}

        if winner == self.human:
            return {"value": -1, "position": -1}

        # Find out if the game has ended for a terminal state of zero (0)
        availableMoves = self.empty_squares(boardCopy)
        if len(availableMoves) < 1:
            return {"value": 0, "position": -1}

        moves = []
        for index in range(len(availableMoves)):
            # Make a move into the next available position for the current player
            currentMove = availableMoves[index]
            boardCopy[currentMove] = player

            # Make note of the score and keep a record of the move in the moves list for later evaluation.
            score = self.minimax(boardCopy, self.swap(player))
            moves.append({"value": score["value"], "position": currentMove})

            # Reset the board to its original state
            boardCopy[currentMove] = None

        # Evaluate the scores of the possible valid moves collected from above
        # and return the best move to be played by the computer.
        f = max if player == self.computer else min
        return f(moves, key=lambda x: x["value"])


class TicTacToeApp(App):
    def build(self):
        self.game = TicTacToeGame()
        return self.game

    def on_start(self):
        Window.size = (200, 200)
        self.game.start_game()


if __name__ == "__main__":
    TicTacToeApp().run()

from gui import game_gui as GUI
from model.state import State
from service.move import *


class Game:
    AI = -1
    PLAYER = 0

    def __init__(self, game_board):
        self.current_state = State(0, 0)
        self.turn = self.AI
        self.first = self.turn
        self.board = game_board

    def is_game_over(self):
        if self.has_winning_state():
            """Display who won"""
            print("AI Bot won!") if ~self.turn == self.AI else print("Congratulations, you won!")
            return True
        elif self.draw():
            print("Draw...Thank you...come again")
            return True
        return False

    def draw(self):
        """Check current state to determine if it is in a draw"""
        return State.is_draw(self.current_state.game_position) and not self.has_winning_state()

    def has_winning_state(self):
        return State.is_winning_state(self.current_state.ai_position) or State.is_winning_state(
            self.current_state.player_position)

    def next_turn(self):
        if self.turn == self.AI:
            self.query_AI()
        else:
            self.query_player()
        self.turn = ~self.turn

    def query_player(self):
        """Make a move by querying standard input."""
        print("\nPlayer's Move...")
        column = None
        while column is None:
            try:
                column = GUI.getHumanInteraction(self.board)
                if not 0 <= column <= 6:  # check if move it allow
                    raise ValueError
                if self.current_state.game_position & (1 << (7 * column + 5)):
                    raise IndexError
            except (ValueError, IndexError):
                print("Invalid move. Try again...")
                column = None

        GUI.dropHumanToken(self.board, column)

        new_position, new_game_position = make_move(self.current_state.player_position,
                                                    self.current_state.game_position, column)
        self.current_state = State(self.current_state.ai_position, new_game_position, self.current_state.depth + 1)

    def query_AI(self):
        """ AI Bot chooses next best move from current state """
        print("\nAI's Move...")
        temp_position = self.current_state.ai_position
        self.current_state = alphabeta_search(self.current_state, self.first, d=7)

        # Get column for GUI
        column = temp_position ^ self.current_state.ai_position
        column = (column.bit_length() - 1) // 7
        GUI.animateComputerMoving(self.board, column)
        GUI.makeMove(self.board, GUI.BLACK, column)

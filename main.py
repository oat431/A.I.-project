from gui import game_gui as GUI
from model.game import Game
from service.move import *

if __name__ == '__main__':
    print("Game of connect four is begin")

    GUI.run()
    while True:
        game_board = GUI.getNewBoard()  # reset board when the game is start
        GUI.drawBoard(game_board)
        GUI.updateDisplay()

        game = Game(game_board)  # get the new board ready

        while not game.is_game_over():
            game.next_turn()
            print_board(game.current_state)  # debugging via console
            GUI.drawBoard(game.board)
            GUI.updateDisplay()

        WINNER = '' if game.draw() else GUI.COMPUTER if ~game.turn == -1 else GUI.HUMAN  # show who win
        GUI.processGameOver(WINNER, game.board)

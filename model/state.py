from service.move import *
infinity = float('inf')
"""
    algorithm behind connect four project
    State class
    Each position is a 6x7 board with top row as sentinel row of 0's; so a 7x7 bitboard
    Bit positions corresponding to the board are as follows...
    -  -   -   -   -   -   -
    5  12  19  26  33  40  47
    4  11  18  25  32  39  46
    3  10  17  24  31  38  45
    2  9   16  23  30  37  44
    1  8   15  22  29  36  43
    0  7   14  21  28  35  42
"""


class State:

    status = 3

    def __init__(self, ai_position, game_position, depth=0):
        self.ai_position = ai_position
        self.game_position = game_position
        self.depth = depth

    @property
    def player_position(self):
        return self.ai_position ^ self.game_position

    @staticmethod
    def is_winning_state(position):
        m = position & (position >> 7)  # check for horizontal pattern
        if m & (m >> 14):
            return True

        m = position & (position >> 6)  # check for downer diagonal
        if m & (m >> 12):
            return True

        m = position & (position >> 8)  # check for upper diagonal
        if m & (m >> 16):
            return True

        m = position & (position >> 1)  # check for vertical
        if m & (m >> 2):
            return True

        return False  # tie

    @staticmethod
    def is_draw(position):
        return all(position & (1 << (7 * column + 5)) for column in range(0, 7))

    def terminal_node_test(self):
        if self.is_winning_state(self.ai_position):  # AI Won
            self.status = -1
            return True
        elif self.is_winning_state(self.player_position):  # Player Won
            self.status = 1
            return True
        elif self.is_draw(self.game_position):  # Tie
            self.status = 0
            return True
        else:
            return False

    def calculate_heuristic(self):
        if self.status == -1:  # AI won
            return 22 - (self.depth // 2)
        elif self.status == 1:  # Player won
            return -1 * (22 - (self.depth // 2))
        elif self.status == 0:  # Tie
            return 0
        elif self.depth % 2 == 0:  # Max node
            return infinity
        else:  # Min Node
            return -infinity

    def generate_children(self, who_went_first):
        for i in range(0, 7):
            column = 3 + (1 - 2 * (i % 2)) * (i + 1) // 2
            if not self.game_position & (1 << (7 * column + 5)):
                if (who_went_first == -1 and self.depth % 2 == 0) or (who_went_first == 0 and self.depth % 2 == 1):
                    new_ai_position, new_game_position = make_move(self.ai_position, self.game_position, column)
                else:
                    new_ai_position, new_game_position = make_move_opponent(self.ai_position, self.game_position,
                                                                            column)
                yield State(new_ai_position, new_game_position, self.depth + 1)

    def __str__(self):
        return '{0:049b}'.format(self.ai_position) + ' ; ' + '{0:049b}'.format(self.game_position)

    def __hash__(self):
        return hash((self.ai_position, self.game_position, self.depth % 2))

    def __eq__(self, other):
        return (self.ai_position, self.game_position, self.depth % 2) == (
            other.ai_position, other.game_position, other.depth % 2)

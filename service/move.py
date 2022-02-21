infinity = float('inf')

"""Search game state to determine best action; use alpha-beta pruning. """


def alphabeta_search(state, turn=-1, d=7):

    # Functions used by alpha beta
    def max_value(state, alpha, beta, depth):
        if cutoff_search(state, depth):
            return state.calculate_heuristic()

        v = -infinity
        for child in state.generate_children(turn):
            if child in seen:
                continue
            v = max(v, min_value(child, alpha, beta, depth + 1))
            seen[child] = alpha
            if v >= beta:
                return v
            alpha = max(alpha, v)
        if v == -infinity:
            return infinity
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_search(state, depth):
            return state.calculate_heuristic()

        v = infinity
        for child in state.generate_children(turn):
            if child in seen:
                continue
            v = min(v, max_value(child, alpha, beta, depth + 1))
            seen[child] = alpha
            if v <= alpha:
                return v
            beta = min(beta, v)
        if v == infinity:
            return -infinity
        return v
    seen = {}

    cutoff_search = (lambda state, depth: depth > d or state.terminal_node_test())
    best_score = -infinity
    beta = infinity
    best_action = None
    for child in state.generate_children(turn):
        v = min_value(child, best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = child
    return best_action


def make_move(position, mask, col):
    """ Helper method to make a move and return new position along with new board position """
    opponent_position = position ^ mask
    new_mask = mask | (mask + (1 << (col * 7)))
    return opponent_position ^ new_mask, new_mask


def make_move_opponent(position, mask, col):
    """ Helper method to only return new board position """
    new_mask = mask | (mask + (1 << (col * 7)))
    return position, new_mask


def print_board(state):
    """
    Helper method to pretty print binary board (6x7 board with top sentinel row of 0's)
    """
    ai_board, total_board = state.ai_position, state.game_position
    for row in range(5, -1, -1):
        print("")
        for column in range(0, 7):
            if ai_board & (1 << (7 * column + row)):
                print("1", end='')
            elif total_board & (1 << (7 * column + row)):
                print("2", end='')
            else:
                print("0", end='')
    print("")

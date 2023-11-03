"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

# 1D indexes for winning sets (3 horizontals, 3 verticals, 2 diag
# they are used on a flattened board. Could be used with // and % to revert back to row and col
winning_sets = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # flatten the 2D array with a nested comprehension and filter on non-empty positions
    non_empty_positions = [ pos for one_row in board for pos in one_row if pos != EMPTY]

    # the player will X if there is an even number of occupied positions, O otherwise
    return X if (len(non_empty_positions) % 2 == 0) else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    legal_moves = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                legal_moves.add( (row,col) )

    return legal_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    brd = copy.deepcopy(board)

    # Unclear whether we want to handle action=None as a problem, or just return the same board.
    #   (for the game's logic, accepting None should be fine
    if action == None:
    #    return brd
        raise RuntimeError("Board's change requested without providing an action")

    row , col = action

    if row<0 or row>2 or col<0 or col>2 or board[row][col] != EMPTY :
        raise RuntimeError("Tried to assign an invalid position")

    brd[row][col] = player(board)

    return brd


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # choice : we need to test horizontal, vertical and diagonal wins. Could be 3 different functions or
    #   three loops in this functions
    #   Let's rather flatten the array, and have a static reference to the 8 possible win configuration
    #   This has the advantage of being one single loop iso 3, and using 1 index instead of pairs

    flat_board = [ pos for one_row in board for pos in one_row ]

    for win_test in range(len(winning_sets)):
        win_set = winning_sets[win_test]

    #   if we have three matching positions (not empty) then we have a winner
        if (flat_board[win_set[0]] == flat_board[win_set[1]] == flat_board[win_set[2]]) and  \
            flat_board[win_set[0]] != EMPTY :
            return flat_board[win_set[0]]

    # if we reach this point, no winner was found
    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Attention : "game over" and "there is a winner" are not equivalent (case of ties)
    #   So, this is incorrect :       return winner(board) != EMPTY
    # We need to test for a winner OR the 9 positions are exhausted
    full_board = len([pos for one_row in board for pos in one_row if pos != EMPTY]) == 9

    return full_board or winner(board) != EMPTY


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    if res == X:
        return 1
    elif res == O:
        return -1
    else:
        return 0

    # should never reach this statement
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

#    Comment out the first version - minimax without pruning - works fine but slow
#    if player(board) == X:
#        v , move = maxValue(board)
#    else:
#        v , move = minValue(board)

#    Let's test the speed improvement of pruning
    v , move = alphaBeta( board , -10 , +10 , player(board) == X )

    return move

# Max Value adapted to return both the maximum value and the corresponding action.
# Simplifies the main loop, as we need the value in the recursion here, and the action for the caller
def maxValue(board):
    if terminal(board):
        return ( utility(board) , None )

    best_action = None
    max_v = -10

    # this loop should always be executed (if empty actions, the previous check on "terminal" should have been triggered
    for action in actions(board):
        v , _ = minValue(result(board,action))
        if v > max_v:
            max_v = v
            best_action = action

    return (max_v , best_action)


# Min Value adapted to return both the minimum value and the corresponding action. Simplifies the main loop
def minValue(board):
    if terminal(board):
        return ( utility(board) , None )

    best_action = None
    min_v = +10

    for action in actions(board):
        v , _ = maxValue(result(board, action))
        if v < min_v:
            min_v = v
            best_action = action

    return (min_v, best_action)

# Version with alpha beta pruning
#    Adding a parameter for speed up : we know whose turn it is, as we always starts with X and then alternate
#    So, we can save some time avoiding to parse the board every time to deduce it
# For the loop structure, remember that alpha is the best we can do so far, and beta is the worst we can do so far
def alphaBeta( board, alpha , beta , maxPlayer = True):

    if terminal(board):
        return (utility(board), None)

    best_action = None

    if maxPlayer:
        value = -10

        for action in actions(board):
            v, _ = alphaBeta( result(board, action) , alpha , beta , False)
            if v > value:
                value = v
                best_action = action
                # If the branch value is higher than beta, no need to go further : the min player will not pick this branch
                if value > beta:
                    break
                # Keep a proper tracking of the best score
                alpha = max( alpha , value )
    else:
        value = +10

        for action in actions(board):
            v, _ = alphaBeta( result(board, action) , alpha , beta , True)
            if v < value:
                value = v
                best_action = action
                # If the branch value is lower than alpha, no need to go further : the max player will not pick this branch
                if value < alpha:
                    break
                # Keep a proper tracking of the best score (from min's perspective)
                beta = min( beta , value )

    return ( value , best_action)

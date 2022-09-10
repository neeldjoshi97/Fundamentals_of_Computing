"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import user302_JXaeiHeMJ1mihQO as poc_ttt_gui
import user302_QIuDpxfj9yeF8cS as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.

NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. It does not
    return anything.
    """
    not_empty = board.get_empty_squares()
    if len(not_empty) > 0:
        random.shuffle(not_empty)
        random_square = not_empty[0] # (row, column) tuple
        board.move(random_square[0], random_square[1], player) # move played
        # change the player
        player = provided.switch_player(player)
        # recursion
        mc_trial(board, player)
    else:
        return # Game simulation done

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same
    dimensions as the Tic-Tac-Toe board, a board from a completed game, and
    which player the machine player is.
    """

    opponent = provided.switch_player(player)
    who_won = board.check_win()
    dim = board.get_dim()
    won_dic = {player: 0, opponent: 1}
    n_power = {player: 0, opponent: 1, provided.EMPTY: -1}
    score_const = {player: SCORE_CURRENT, opponent: SCORE_OTHER, provided.EMPTY: 0}

    n = won_dic[who_won]

    if who_won == provided.DRAW:
        for ind_i in range(dim):
            for ind_j in range(dim):
                scores[ind_i][ind_j] += 0
    else:
        for ind_i in range(dim):
            for ind_j in range(dim):
                select_square = board.square(ind_i, ind_j)
                scores[ind_i][ind_j] += ((-1) ** (n + n_power[select_square])) * score_const[select_square]



def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    """

    not_empty = board.get_empty_squares() # list of (row, column) tuples
    leng = len(not_empty)
    max_score_tups = []
    if leng > 0:
        empty_scores = []
        for ind_l in range(leng):
            dim = not_empty[ind_l]
            score = scores[dim[0]][dim[1]]
            empty_scores.append(score)
        maxi_score = max(empty_scores)
        for ind_i in range(len(empty_scores)):
            if empty_scores[ind_i] == maxi_score:
                max_score_tups.append(not_empty[ind_i])
        random.shuffle(max_score_tups)
        return max_score_tups[0]
    else:
        return None

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is,
    and the number of trials to run."""

    scores_matrix = list()
    dim = board.get_dim()
    for ind_i in range(dim):
        dummy = list()
        for ind_j in range(dim):
            dummy.append(0)
        scores_matrix.append(dummy)
    while trials > 0:
        trials -= 1
        mc_trial(board, player)
        mc_update_scores(scores_matrix, board, player)
    best_move = get_best_move(board, scores_matrix)
    if best_move == None:
        return (0, 0)
    return best_move


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

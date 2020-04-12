import random
from TicTacToe_AI import *
# if AI turn isMax = True


def random_cell(TTT):
    rndm_num = random.randint(0, len(empty_cells(TTT))-1)
    cells = empty_cells(TTT)
    rndm_cell = cells[rndm_num]
    return rndm_cell


def minimax(TTT, isMax):
    if isMax:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if len(empty_cells(TTT)) == 0 or is_winner(TTT):
        score = eval(TTT)
        return [-1, -1, score]

    for cell in empty_cells(TTT):
        x, y = cell[0], cell[1]
        if isMax:
            TTT[x][y] = 'o'
        else:
            TTT[x][y] = 'x'
        score = minimax(TTT, not isMax)
        TTT[x][y] = None
        score[0], score[1] = x, y

        if isMax:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def alpha_beta(TTT, alpha, beta, isMax):
    if isMax:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if len(empty_cells(TTT)) == 0 or is_winner(TTT):
        score = eval(TTT)
        return [-1, -1, score]

    for cell in empty_cells(TTT):
        x, y = cell[0], cell[1]
        if isMax:
            TTT[x][y] = 'o'
        else:
            TTT[x][y] = 'x'
        score = alpha_beta(TTT, alpha, beta, not isMax)
        TTT[x][y] = None
        score[0], score[1] = x, y

        if isMax:
            if score[2] > best[2]:
                best = score
            alpha = max(alpha, best[2])
            if beta <= alpha:
                break
        else:
            if score[2] < best[2]:
                best = score
            beta = min(beta, best[2])
            if beta <= alpha:
                break

    return best


def minimax_depth_limit(TTT, depth, isMax):
    if isMax:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if len(empty_cells(TTT)) == 0 or is_winner(TTT):
        score = eval(TTT)
        return [-1, -1, score]

    # cutoff at depth of 3 and evaluate TTT state
    if depth == 3:
        result = eval_heuristic(TTT)
        return [-1, -1, result]

    for cell in empty_cells(TTT):
        x, y = cell[0], cell[1]
        if isMax:
            TTT[x][y] = 'o'
        else:
            TTT[x][y] = 'x'
        score = minimax_depth_limit(TTT, depth+1, not isMax)
        TTT[x][y] = None
        score[0], score[1] = x, y

        if isMax:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def depth_alphabeta(TTT, depth, alpha, beta, isMax):
    if isMax:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if len(empty_cells(TTT)) == 0 or is_winner(TTT):
        score = eval(TTT)
        return [-1, -1, score]

    # cutoff at depth of 3 and evaluate TTT state
    if depth == 3:
        result = eval_heuristic(TTT)
        return [-1, -1, result]

    for cell in empty_cells(TTT):
        x, y = cell[0], cell[1]
        if isMax:
            TTT[x][y] = 'o'
        else:
            TTT[x][y] = 'x'
        score = depth_alphabeta(TTT, depth+1, alpha, beta, not isMax)
        TTT[x][y] = None
        score[0], score[1] = x, y

        if isMax:
            if score[2] > best[2]:
                best = score
            alpha = max(alpha, best[2])
            if beta <= alpha:
                break
        else:
            if score[2] < best[2]:
                best = score
            beta = min(beta, best[2])
            if beta <= alpha:
                break

    return best


def minimax_exper(TTT, depth, alpha, beta, isMax):
    if isMax:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if len(empty_cells(TTT)) == 0 or is_winner(TTT):
        score = eval(TTT)
        return [-1, -1, score]

    # cutoff at depth of 3 and evaluate TTT state
    if depth == 8:
        result = eval_heuristic(TTT)
        return [-1, -1, result]

    for cell in empty_cells(TTT):
        x, y = cell[0], cell[1]
        if isMax:
            TTT[x][y] = 'o'
        else:
            TTT[x][y] = 'x'
        score = minimax_exper(TTT, depth+1, alpha, beta, not isMax)
        TTT[x][y] = None
        score[0], score[1] = x, y

        if isMax:
            if score[2] > best[2]:
                best = score
            alpha = max(alpha, best[2])
            if beta <= alpha:
                break
        else:
            if score[2] < best[2]:
                best = score
            beta = min(beta, best[2])
            if beta <= alpha:
                break

    return best


def eval_heuristic(TTT):

    # no of possible wins in next 2 moves of AI
    score_AI = 0
    for cell_i in empty_cells(TTT):
        x_i, y_i = cell_i[0], cell_i[1]
        TTT[x_i][y_i] = 'o'
        for cell_j in empty_cells(TTT):
            x_j, y_j = cell_j[0], cell_j[1]
            TTT[x_j][y_j] = 'o'
            if is_winner(TTT) == 'o':
                score_AI = score_AI + 1
            TTT[x_j][y_j] = None
        TTT[x_i][y_i] = None

    # no of possible wins in next 2 moves of User
    score_User = 0
    for cell_i in empty_cells(TTT):
        x_i, y_i = cell_i[0], cell_i[1]
        TTT[x_i][y_i] = 'x'
        for cell_j in empty_cells(TTT):
            x_j, y_j = cell_j[0], cell_j[1]
            TTT[x_j][y_j] = 'x'
            if is_winner(TTT) == 'x':
                score_User = score_User + 1
            TTT[x_j][y_j] = None
        TTT[x_i][y_i] = None

    if score_AI > score_User:
        score = 10
    elif score_AI < score_User:
        score = -10
    else:
        score = 0

    return score

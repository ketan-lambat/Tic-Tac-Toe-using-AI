import pygame
import time
import random
import platform
import sys
from math import inf
from os import system

TTT = [[None]*6, [None]*6, [None]*6, [None]*6, [None]*6, [None]*6]


def is_winner(TTT):
    for row in range(0, 6):
        for j in range(0, 3):
            if ((TTT[row][j] is not None) and (TTT[row][j]
                                               == TTT[row][j+1]
                                               == TTT[row][j+2]
                                               == TTT[row][j+3])):
                return TTT[row][j]

    for col in range(0, 6):
        for i in range(0, 3):
            if((TTT[i][col] is not None) and (TTT[i][col]
                                              == TTT[i+1][col]
                                              == TTT[i+2][col]
                                              == TTT[i+3][col])):
                return TTT[i][col]

    # forward diagonals
    for i in range(0, 3):
        for j in range(0, 3):
            if((TTT[i][j] is not None) and (TTT[i][j]
                                            == TTT[i+1][j+1]
                                            == TTT[i+2][j+2]
                                            == TTT[i+3][j+3])):
                return TTT[i][j]

    # reverse diagonals
    for i in range(5, 2, -1):
        for j in range(5, 2, -1):
            if ((TTT[i][j] is not None) and (TTT[i][j]
                                             == TTT[i-1][j-1]
                                             == TTT[i-2][j-2]
                                             == TTT[i-3][j-3])):
                return TTT[i][j]

    return None


def eval(TTT):
    if is_winner(TTT) == 'x':
        score = -1
    elif is_winner(TTT) == 'o':
        score = 1
    else:
        score = 0
    return score


def empty_cells(TTT):
    cells = []
    for x, row in enumerate(TTT):
        for y, cell in enumerate(row):
            if cell is None:
                cells.append([x, y])
    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(TTT):
        return True
    else:
        return False


# def set_move(x, y, OX, screen):
def set_move(x, y, OX):
    if valid_move(x, y):
        TTT[x][y] = OX
        # draw_OX(x+1, y+1, OX, screen)
        return True
    else:
        return False


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


def depth_alphabeta(TTT, depth, alpha, beta, isMax):
    if isMax:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if len(empty_cells(TTT)) == 0 or is_winner(TTT):
        score = eval(TTT)
        return [-1, -1, score]

    # cutoff at depth of 3 and evaluate TTT state
    if depth == 1:
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


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def print_board(TTT):
    line = '------------------------------'
    print("\n" + line)

    for x, row in enumerate(TTT):
        for y, cell in enumerate(row):
            if cell is None:
                symb = '_'
            else:
                symb = TTT[x][y]
            print(f'| {symb} |', end='')
        print("\n" + line)


# def ai_turn(TTT, screen, ai_algo):
def ai_turn(TTT):
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    clean()
    print("AI TURN")

    # print_status('o', False, False, screen)

    # if depth == 9:
    #     x = choice([0, 1, 2])
    #     y = choice([0, 1, 2])
    # else:
    #     if ai_algo == 1:
    # move = minimax(TTT, True)
    # move = alpha_beta(TTT, -inf, inf, True)
    move = depth_alphabeta(TTT, 0, -inf, inf, True)
    # if ai_algo == 2:
    #     move = alpha_beta(TTT, -inf, inf, True)
    # if ai_algo == 3:
    #     move = minimax_depth_limit(TTT, 0, True)
    # if ai_algo == 4:
    #     move = depth_alphabeta(TTT, 0, -inf, inf, True)
    # if ai_algo == 5:
    #     move = minimax_exper(TTT, 0, -inf, inf, True)
    x, y = move[0], move[1]

    # set_move(x, y, 'o', screen)
    set_move(x, y, 'o')
    print_board(TTT)
    time.sleep(1)
    # print_status('x', False, False, screen)


# def user_turn(TTT, screen):
def user_turn(TTT):
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    clean()
    print("USER TURN")
    print_board(TTT)

    # print_status('x', False, False, screen)

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [0, 4], 6: [0, 5],
        7: [1, 0], 8: [1, 1], 9: [1, 2], 10: [1, 3], 11: [1, 4], 12: [1, 5],
        13: [2, 0], 14: [2, 1], 15: [2, 2], 16: [2, 3], 17: [2, 4], 18: [2, 5],
        19: [3, 0], 20: [3, 1], 21: [3, 2], 22: [3, 3], 23: [3, 4], 24: [3, 5],
        25: [4, 0], 26: [4, 1], 27: [4, 2], 28: [4, 3], 29: [4, 4], 30: [4, 5],
        31: [5, 0], 32: [5, 1], 33: [5, 2], 34: [5, 3], 35: [5, 4], 36: [5, 5]
    }

    while move < 1 or move > 36:
        try:
            move = int(input("Enter ip move position (1...36):"))
            coord = moves[move]
            # move_possib = set_move(coord[0], coord[1], 'x', screen)
            move_possib = set_move(coord[0], coord[1], 'x')

            if not move_possib:
                print("Incorrect Move")
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad Input')


# def is_game_over(TTT, screen):
def is_game_over(TTT):
    # game over conditions
    if is_winner(TTT) == 'x':
        clean()
        print("USER TURN")
        print_board(TTT)
        print("YOU WIN !!")
        # draw_win_line(TTT, screen)
        # print_status(False, True, 'x', screen)
        return True

    elif is_winner(TTT) == 'o':
        clean()
        print("AI TURN")
        print_board(TTT)
        print("AI WINS !!")
        # draw_win_line(TTT, screen)
        # print_status(False, True, 'o', screen)
        return True
    elif len(empty_cells(TTT)) == 0 or is_winner(TTT):
        clean()
        print_board(TTT)
        print("DRAW -_-")
        # print_status(False, True, False, screen)
        return True
    else:
        return False


def main():
    clean()

    while len(empty_cells(TTT)) > 0 and not is_winner(TTT):
        # if first == 'N':
        #     ai_turn(c_choice, h_choice)
        #     first = ''

        user_turn(TTT)
        ai_turn(TTT)
    is_game_over(TTT)
    exit()


if __name__ == "__main__":
    main()

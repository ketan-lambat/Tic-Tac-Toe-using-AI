import pygame
import time
import random
import platform
from math import floor
import sys
from math import inf
from os import system
from pygame.locals import *
from AI_algo import *

# global variables
WIDTH = 100
HEIGHT = 100
# size of the tic tac toe grid (default 3x3)
SIZE = 3
TTT = [[None]*3, [None]*3, [None]*3]

# colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LINE_COLOUR = (10, 10, 10)
# BG_COLOR = (33, 47, 60)
BG_COLOR = (163, 0, 204)


# initialize pygame window
pygame.init()
FPS = 30
CLOCK = pygame.time.Clock()


# load the images/sprites
x_img = pygame.image.load("X.png")
o_img = pygame.image.load("O.png")

# resize to proper scale
x_img = pygame.transform.scale(
    x_img, (floor(WIDTH/(SIZE)), floor(WIDTH/(SIZE))))
o_img = pygame.transform.scale(
    o_img, (floor(WIDTH/(SIZE)), floor(WIDTH/(SIZE))))


def open_window():
    screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
    pygame.display.set_caption("Open Field Tic Tac Toe with AI")
    return screen


def game_start(screen):

    screen.fill(BG_COLOR)

    # line(surface, color, start_pos, end_pos, width)

    # vertical lines
    for i in range(1, SIZE):
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH/SIZE*i, 0),
                         (WIDTH/SIZE*i, HEIGHT), 7)

    # horizontal lines
    for i in range(1, SIZE):
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/SIZE*i),
                         (WIDTH, HEIGHT/SIZE*i), 7)

    pygame.display.update()


def draw_OX(row, col, OX, screen):
    for i in range(1, SIZE+1):
        if row == i:
            posX = 20 + WIDTH/SIZE * (i-1)

    for i in range(1, SIZE+1):
        if col == i:
            posY = 20 + HEIGHT/SIZE * (i-1)

    if(OX == 'x'):
        screen.blit(x_img, (posY, posX))
    else:
        screen.blit(o_img, (posY, posX))

    pygame.display.update()


def draw_win_line(TTT, screen):
    # winning rows
    for row in range(0, SIZE):
        for j in range(0, SIZE-3):
            if ((TTT[row][j] is not None) and (TTT[row][j]
                                               == TTT[row][j+1]
                                               == TTT[row][j+2]
                                               == TTT[row][j+3])):
                pygame.draw.line(screen, RED,
                                 ((j+1)*WIDTH/SIZE-WIDTH/(SIZE*2),
                                  (row+1)*HEIGHT/SIZE-HEIGHT/(SIZE*2)),
                                 ((j+4)*WIDTH/SIZE-WIDTH/(SIZE*2), (row+1)*HEIGHT/SIZE-HEIGHT/(SIZE*2)), 4)
            break

    # winning columns
    for col in range(0, SIZE):
        for i in range(0, SIZE-3):
            if((TTT[i][col] is not None) and (TTT[i][col]
                                              == TTT[i+1][col]
                                              == TTT[i+2][col]
                                              == TTT[i+3][col])):
                pygame.draw.line(screen, RED,
                                 ((col+1)*WIDTH/SIZE-WIDTH/(SIZE*2),
                                  (i+1)*HEIGHT/SIZE-HEIGHT/(SIZE*2)),
                                 ((col+1)*WIDTH/SIZE-WIDTH/(SIZE*2), (i+4)*HEIGHT/SIZE-HEIGHT/(SIZE*2)), 4)
            break

    # diagonal winners
    for i in range(0, SIZE-3):
        for j in range(0, SIZE-3):
            if((TTT[i][j] is not None) and (TTT[i][j]
                                            == TTT[i+1][j+1]
                                            == TTT[i+2][j+2]
                                            == TTT[i+3][j+3])):
                pygame.draw.line(screen, RED,
                                 ((j+1)*WIDTH/SIZE-WIDTH/(SIZE*2),
                                  (i+1)*HEIGHT/SIZE-HEIGHT/(SIZE*2)),
                                 ((j+4)*WIDTH/SIZE-WIDTH/(SIZE*2), (i+4)*HEIGHT/SIZE-HEIGHT/(SIZE*2)), 4)

    for i in range(0, SIZE-3):
        for j in range(SIZE-1, 2, -1):
            if ((TTT[i][j] is not None) and (TTT[i][j]
                                             == TTT[i+1][j-1]
                                             == TTT[i+2][j-2]
                                             == TTT[i+3][j-3])):
                pygame.draw.line(screen, RED,
                                 ((j+1)*WIDTH/SIZE-WIDTH/(SIZE*2),
                                  (i+1)*HEIGHT/SIZE-HEIGHT/(SIZE*2)),
                                 ((j-2)*WIDTH/SIZE-WIDTH/(SIZE*2), (i+4)*HEIGHT/SIZE-HEIGHT/(SIZE*2)), 4)


def print_status(playerTurn, isOver, winner, screen):

    if not isOver:
        if playerTurn == 'x':
            msg = " User(X)'s Turn"
        elif playerTurn == 'o':
            msg = " AI(O)'s Turn"
    elif isOver:
        if winner == 'x':
            msg = "YOU WIN !!"
        elif winner == 'o':
            msg = "AI WINs !! You Lose"
        else:
            msg = "Game Tied"

    # render(text, antialias, color, background=None) -> Surface
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text = font.render(msg, True, (255, 255, 255))

    # rendered msg on the screen
    # fill (colour, position(x, y),size(len, wid) )
    screen.fill((0, 0, 0,), (0, HEIGHT, WIDTH, 100))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT+50))
    screen.blit(text, text_rect)
    pygame.display.update()


def print_board(TTT):
    line = '-----'
    print("\n" + line*SIZE)

    for x, row in enumerate(TTT):
        for y, cell in enumerate(row):
            if cell is None:
                symb = '_'
            else:
                symb = TTT[x][y]
            print(f'| {symb} |', end='')
        print("\n" + line*SIZE)


def is_winner(TTT):
    for row in range(0, SIZE):
        for j in range(0, SIZE-3):
            if ((TTT[row][j] is not None) and (TTT[row][j]
                                               == TTT[row][j+1]
                                               == TTT[row][j+2]
                                               == TTT[row][j+3])):
                return TTT[row][j]

    for col in range(0, SIZE):
        for i in range(0, SIZE-3):
            if((TTT[i][col] is not None) and (TTT[i][col]
                                              == TTT[i+1][col]
                                              == TTT[i+2][col]
                                              == TTT[i+3][col])):
                return TTT[i][col]

    # forward diagonals
    for i in range(0, SIZE-3):
        for j in range(0, SIZE-3):
            if((TTT[i][j] is not None) and (TTT[i][j]
                                            == TTT[i+1][j+1]
                                            == TTT[i+2][j+2]
                                            == TTT[i+3][j+3])):
                return TTT[i][j]

    # reverse diagonals
    for i in range(0, SIZE-3):
        for j in range(SIZE-1, 2, -1):
            if ((TTT[i][j] is not None) and (TTT[i][j]
                                             == TTT[i+1][j-1]
                                             == TTT[i+2][j-2]
                                             == TTT[i+3][j-3])):
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


def set_move(x, y, OX, screen):
    if valid_move(x, y):
        TTT[x][y] = OX
        draw_OX(x+1, y+1, OX, screen)
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


def reset_game(TTT, screen):
    time.sleep(2)
    game_start(screen)


def ai_turn(TTT, screen, ai_algo):
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    clean()
    print("AI TURN")

    print_status('o', False, False, screen)

    if depth == SIZE*SIZE:
        x = choice([i for i in range(SIZE)])
        y = choice([i for i in range(SIZE)])
    else:
        if ai_algo == 1:
            move = minimax(TTT, True)
        if ai_algo == 2:
            move = alpha_beta(TTT, -inf, inf, True)
        if ai_algo == 3:
            move = minimax_depth_limit(TTT, 0, True)
        if ai_algo == 4:
            move = depth_alphabeta(TTT, 0, -inf, inf, True)
        if ai_algo == 5:
            move = minimax_exper(TTT, 0, -inf, inf, True)
    x, y = move[0], move[1]

    set_move(x, y, 'o', screen)
    print_board(TTT)
    # time.sleep(1)
    print_status('x', False, False, screen)


# fun to take the user input from cmd line for 6x6 grid
# def user_turn(TTT, screen):
#     depth = len(empty_cells(TTT))
#     if depth == 0 or is_winner(TTT):
#         return

#     clean()
#     print("USER TURN")
#     print_board(TTT)

#     print_status('x', False, False, screen)

#     move = -1
#     moves = {
#         1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [0, 4], 6: [0, 5],
#         7: [1, 0], 8: [1, 1], 9: [1, 2], 10: [1, 3], 11: [1, 4], 12: [1, 5],
#         13: [2, 0], 14: [2, 1], 15: [2, 2], 16: [2, 3], 17: [2, 4], 18: [2, 5],
#         19: [3, 0], 20: [3, 1], 21: [3, 2], 22: [3, 3], 23: [3, 4], 24: [3, 5],
#         25: [4, 0], 26: [4, 1], 27: [4, 2], 28: [4, 3], 29: [4, 4], 30: [4, 5],
#         31: [5, 0], 32: [5, 1], 33: [5, 2], 34: [5, 3], 35: [5, 4], 36: [5, 5]
#     }

#     while move < 1 or move > 36:
#         try:
#             move = int(input("Enter ip move position (1...36):"))
#             coord = moves[move]
#             # move_possib = set_move(coord[0], coord[1], 'x', screen)
#             move_possib = set_move(coord[0], coord[1], 'x')

#             if not move_possib:
#                 print("Incorrect Move")
#                 move = -1
#         except (EOFError, KeyboardInterrupt):
#             print('Bye')
#             exit()
#         except (KeyError, ValueError):
#             print('Bad Input')


def userClick(TTT, screen):
    # print_status('x', False, False, screen)
    x, y = pygame.mouse.get_pos()
    col = 0
    row = 0

    # col clicked
    for i in range(1, SIZE+1):
        if(x < floor(WIDTH/SIZE*i)):
            col = i
            break

    # row clicked
    for i in range(1, SIZE+1):
        if (y < floor(HEIGHT/SIZE*i)):
            row = i
            break


    if (row and col and TTT[row-1][col-1] is None):
        # print("row : ", row, "col: ", col)
        set_move(row-1, col-1, 'x', screen)


def is_game_over(TTT, screen):
    # game over conditions
    if is_winner(TTT) == 'x':
        clean()
        print("USER TURN")
        print_board(TTT)
        print("YOU WIN !!")
        draw_win_line(TTT, screen)
        print_status(False, True, 'x', screen)
        return True

    elif is_winner(TTT) == 'o':
        clean()
        print("AI TURN")
        print_board(TTT)
        print("AI WINS !!")
        draw_win_line(TTT, screen)
        print_status(False, True, 'o', screen)
        return True
    elif len(empty_cells(TTT)) == 0 or is_winner(TTT):
        clean()
        print_board(TTT)
        print("DRAW -_-")
        print_status(False, True, False, screen)
        return True
    else:
        return False


def get_grid_size():
    grid_size = -1
    while grid_size < 4 or grid_size > 10:
        print("Enter the required size of the Tic Tac Toe grid (X*X):")
        try:
            grid_size = int(input())
            return grid_size
        except(KeyError, ValueError):
            print("Enter a value between 4 and 10")


def choose_algo():
    while True:
        print("Choose AI Algo. [1/2/3/4]")
        print("1: minimax (Don't use this)")
        print("2: minimax-AlphaBeta (You don't wanna use this too)")
        print("3: depth limited Minimax")
        print("4: depth limited AlphaBeta Minimax (Take this one)")
        print("5: Experimental Minimax")
        try:
            choice = int(input())
            return choice
        except(KeyError, ValueError):
            print("Bad Input")


def main():
    clean()
    time_taken = []
    running = True
    global WIDTH, HEIGHT, SIZE, TTT
    while running:
        SIZE = get_grid_size()
        ai_algo = choose_algo()

        TTT = [[None for i in range(SIZE)] for j in range(SIZE)]
        WIDTH = 70*SIZE
        HEIGHT = 70*SIZE

        screen = open_window()
        game_start(screen)
        print_status('x', False, False, screen)

        terminal_state = False

        while not terminal_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # while len(empty_cells(TTT)) > 0 and not is_winner(TTT):
                        # if first == 'N':
                        #     ai_turn(c_choice, h_choice)
                        #     first = ''
                    userClick(TTT, screen)
                    game_over = is_game_over(TTT, screen)

                    if game_over:
                        print("Avg time taken : ", sum(time_taken)/len(time_taken), "sec")
                        reset_game(TTT, screen)
                        pygame.quit()
                        terminal_state = True
                        running = False

                    if len(empty_cells(TTT)) != 0:
                        s_time = time.time()
                        ai_turn(TTT, screen, ai_algo)
                        e_time = time.time()
                        del_time = e_time-s_time
                        time_taken.append(del_time)
                        print("Time Taken : ", del_time, "sec")
                        game_over = is_game_over(TTT, screen)

                        if game_over:
                            print("Avg time taken : ", sum(time_taken)/len(time_taken))
                            reset_game(TTT, screen)
                            pygame.quit()
                            terminal_state = True
                            running = False
    pygame.quit()
    # exit()


if __name__ == "__main__":
    main()

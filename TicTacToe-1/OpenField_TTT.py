import pygame
import time
import random
import platform
import sys
from math import inf
from os import system
from pygame.locals import *

# global variables
WIDTH = 600
HEIGHT = 600

# colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LINE_COLOUR = (10, 10, 10)
BG_COLOR = (33, 47, 60)

TTT = [[None]*6, [None]*6, [None]*6, [None]*6, [None]*6, [None]*6]

# initialize pygame window
pygame.init()
FPS = 30
CLOCK = pygame.time.Clock()


# load the images/sprites
x_img = pygame.image.load("X.png")
o_img = pygame.image.load("O.png")

# resize to proper scale
x_img = pygame.transform.scale(x_img, (50, 50))
o_img = pygame.transform.scale(o_img, (50, 50))


def open_window():
    screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
    pygame.display.set_caption("Open Field Tic Tac Toe with AI")
    return screen


def game_start(screen):

    screen.fill(BG_COLOR)

    # line(surface, color, start_pos, end_pos, width)

    # vertical lines
    pygame.draw.line(screen, LINE_COLOUR, (WIDTH/6, 0),
                     (WIDTH/6, HEIGHT), 7)
    pygame.draw.line(screen, LINE_COLOUR, (WIDTH/6*2, 0),
                     (WIDTH/6*2, HEIGHT), 7)
    pygame.draw.line(screen, LINE_COLOUR, (WIDTH/6*3, 0),
                     (WIDTH/6*3, HEIGHT), 7)
    pygame.draw.line(screen, LINE_COLOUR, (WIDTH/6*4, 0),
                     (WIDTH/6*4, HEIGHT), 7)
    pygame.draw.line(screen, LINE_COLOUR, (WIDTH/6*5, 0),
                     (WIDTH/6*5, HEIGHT), 7)

    # horizontal lines
    pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/6),
                     (WIDTH, HEIGHT/6), 7)
    pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/6*2),
                     (WIDTH, HEIGHT/6*2), 7)
    pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/6*3),
                     (WIDTH, HEIGHT/6*3), 7)
    pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/6*4),
                     (WIDTH, HEIGHT/6*4), 7)
    pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/6*5),
                     (WIDTH, HEIGHT/6*5), 7)

    pygame.display.update()
    # print_status()


def draw_OX(row, col, OX, screen):
    if row == 1:
        posX = 30
    if row == 2:
        posX = WIDTH/6 + 30
    if row == 3:
        posX = WIDTH/6*2 + 30
    if row == 4:
        posX = WIDTH/6*3 + 30
    if row == 5:
        posX = WIDTH/6*4 + 30
    if row == 6:
        posX = WIDTH/6*5 + 30

    if col == 1:
        posY = 30
    if col == 2:
        posY = HEIGHT/6 + 30
    if col == 3:
        posY = HEIGHT/6*2 + 30
    if col == 4:
        posY = HEIGHT/6*3 + 30
    if col == 5:
        posY = HEIGHT/6*4 + 30
    if col == 6:
        posY = HEIGHT/6*5 + 30

    if(OX == 'x'):
        screen.blit(x_img, (posY, posX))
    else:
        screen.blit(o_img, (posY, posX))

    pygame.display.update()


def draw_win_line(TTT, screen):
    # winning rows
    for row in range(0, 6):
        for j in range(0, 3):
            if ((TTT[row][j] is not None) and (TTT[row][j]
                                               == TTT[row][j+1]
                                               == TTT[row][j+2]
                                               == TTT[row][j+3])):
                pygame.draw.line(screen, RED,
                                 ((j+1)*WIDTH/6-WIDTH/12,
                                  (row+1)*HEIGHT/6-HEIGHT/12),
                                 ((j+4)*WIDTH/6-WIDTH/12, (row+1)*HEIGHT/6-HEIGHT/12), 4)
            break

    # winning columns
    for col in range(0, 6):
        for i in range(0, 3):
            if((TTT[i][col] is not None) and (TTT[i][col]
                                              == TTT[i+1][col]
                                              == TTT[i+2][col]
                                              == TTT[i+3][col])):
                pygame.draw.line(screen, RED,
                                 ((col+1)*WIDTH/6-WIDTH/12,
                                  (i+1)*HEIGHT/6-HEIGHT/12),
                                 ((col+1)*WIDTH/6-WIDTH/12, (i+4)*HEIGHT/6-HEIGHT/12), 4)
            break

    # diagonal winners
    for i in range(0, 3):
        for j in range(0, 3):
            if((TTT[i][j] is not None) and (TTT[i][j]
                                            == TTT[i+1][j+1]
                                            == TTT[i+2][j+2]
                                            == TTT[i+3][j+3])):
                pygame.draw.line(screen, RED,
                                 ((j+1)*WIDTH/6-WIDTH/12,
                                  (i+1)*HEIGHT/6-HEIGHT/12),
                                 ((j+4)*WIDTH/6-WIDTH/12, (i+4)*HEIGHT/6-HEIGHT/12), 4)

    for i in range(0, 3):
        for j in range(5, 2, -1):
            if ((TTT[i][j] is not None) and (TTT[i][j]
                                             == TTT[i+1][j-1]
                                             == TTT[i+2][j-2]
                                             == TTT[i+3][j-3])):
                pygame.draw.line(screen, RED,
                                 ((j+1)*WIDTH/6-WIDTH/12,
                                  (i+1)*HEIGHT/6-HEIGHT/12),
                                 ((j-2)*WIDTH/6-WIDTH/12, (i+4)*HEIGHT/6-HEIGHT/12), 4)


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
    screen.fill((0, 0, 0,), (0, 600, 600, 100))
    text_rect = text.get_rect(center=(WIDTH/2, 700-50))
    screen.blit(text, text_rect)
    pygame.display.update()


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
    for i in range(0, 3):
        for j in range(5, 2, -1):
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
    TTT = [[None]*3, [None]*3, [None]*3]


# def ai_turn(TTT, screen, ai_algo):
def ai_turn(TTT, screen):
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    clean()
    print("AI TURN")

    print_status('o', False, False, screen)

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

    set_move(x, y, 'o', screen)
    print_board(TTT)
    # time.sleep(1)
    print_status('x', False, False, screen)


def user_turn(TTT, screen):
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    clean()
    print("USER TURN")
    print_board(TTT)

    print_status('x', False, False, screen)

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


def userClick(TTT, screen):
    # print_status('x', False, False, screen)
    x, y = pygame.mouse.get_pos()

    # col clicked
    if(x < WIDTH/6):
        col = 1
    elif(x < WIDTH/6*2):
        col = 2
    elif(x < WIDTH/6*3):
        col = 3
    elif(x < WIDTH/6*4):
        col = 4
    elif(x < WIDTH/6*5):
        col = 5
    elif(x < WIDTH):
        col = 6
    else:
        col = None

    # row clicked
    if(y < HEIGHT/6):
        row = 1
    elif(y < HEIGHT/6*2):
        row = 2
    elif(y < HEIGHT/6*3):
        row = 3
    elif(y < HEIGHT/6*4):
        row = 4
    elif(y < HEIGHT/6*5):
        row = 5
    elif(y < HEIGHT):
        row = 6
    else:
        row = None

    if(row and col and TTT[row-1][col-1] is None):
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


def main():
    clean()

    running = True
    while running:
        screen = open_window()
        game_start(screen)
        # ai_algo = choose_algo()
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
                        reset_game(TTT, screen)
                        pygame.quit()
                        terminal_state = True
                        running = False

                    if len(empty_cells(TTT)) != 0:
                        ai_turn(TTT, screen)

                        game_over = is_game_over(TTT, screen)

                        if game_over:
                            reset_game(TTT, screen)
                            pygame.quit()
                            terminal_state = True
                            running = False
    pygame.quit()
    # exit()


if __name__ == "__main__":
    main()

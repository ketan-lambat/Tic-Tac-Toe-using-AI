import pygame
import time
from random import choice
import platform
import sys
from math import floor, inf
from os import system
from pygame.locals import *
from AI_algo_custom import *

# global variables

WIDTH = 400
HEIGHT = 400

# size of the tic tac toe grid (default 3x3)
SIZE = 3
TTT = [[None]*3, [None]*3, [None]*3]

# initialize pygame window
pygame.init()
FPS = 30
CLOCK = pygame.time.Clock()

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = pygame.Color('indianred1')
# RED = (255, 0, 0)
LINE_COLOUR = (10, 10, 10)
TEXT_COLOR = pygame.Color('ivory')
# BG_COLOR = (33, 47, 60)
BG_COLOR = (163, 0, 204)
BG_COLOR_2 = pygame.Color('darkslategrey')
BG_COLOR_3 = pygame.Color('slateblue4')
NORMAL_COLOR = pygame.Color('tan2')
HOVER_COLOR = pygame.Color('tan3')
ACTIVE_COLOR = pygame.Color('forestgreen')

FONT_TITLE = pygame.font.Font("ZealotOutline-rnMy.ttf", 20)
FONT_SCORE = pygame.font.Font("Gallant-2O1r3.ttf", 40)
FONT_TEXT = pygame.font.Font("TicTacToe.ttf", 40)
FONT_BTN = pygame.font.Font("FrostbiteBossFight-dL0Z.ttf", 30)
# FONT_TITLE = pygame.font.Font("../static/ZealotOutline-rnMy.ttf", 20)
# FONT_SCORE = pygame.font.Font("../static/Gallant-2O1r3.ttf", 40)
# FONT_TEXT = pygame.font.Font("../static/TicTacToe.ttf", 40)
# FONT_BTN = pygame.font.Font("../static/FrostbiteBossFight-dL0Z.ttf", 30)
# FONT_TITLE.set_bold(True)
FONT = pygame.font.SysFont('Comic Sans MS', 20)

# load the images/sprites
x_img = pygame.image.load("X.png")
o_img = pygame.image.load("O.png")
# x_img = pygame.image.load("../static/X.png")
# o_img = pygame.image.load("../static/O.png")

# resize to proper scale
x_img = pygame.transform.scale(
    x_img, (40, 40))
o_img = pygame.transform.scale(
    o_img, (40, 40))


def open_window():
    screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
    pygame.display.set_caption("Open Field Tic Tac Toe with AI")
    return screen


def draw_button(button, screen):
    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback):
    """A button is a dictionary that contains the relevant data.

    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf = FONT_BTN.render(text, True, BLACK)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': NORMAL_COLOR,
        'callback': callback,
    }
    return button


def create_title_rect(x, y, w, h, text):

    text_surf = FONT_TITLE.render(text, True, TEXT_COLOR)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': BG_COLOR_3,
    }
    return button


def create_text_rect(x, y, w, h, text):

    text_surf = FONT_TEXT.render(text, True, BLACK)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': BG_COLOR,
    }
    return button


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
    # font = pygame.font.SysFont("Comic Sans MS", 30)
    text = FONT_SCORE.render(msg, True, (255, 255, 255))

    # rendered msg on the screen
    # fill (colour, position(x, y),size(wid, ht) )
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
        if ai_algo == 6:
            move = random_cell(TTT)
    x, y = move[0], move[1]

    set_move(x, y, 'o', screen)
    print_board(TTT)
    print_status('x', False, False, screen)


""" fun to take the user input from cmd line for 6x6 grid """
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


"""
function to choose the AI algo from terminal
"""


# def choose_algo():
#     while True:
#         print("Choose AI Algo. [1/2/3/4]")
#         print("1: minimax (Don't use this)")
#         print("2: minimax-AlphaBeta (You don't wanna use this too)")
#         print("3: depth limited Minimax")
#         print("4: depth limited AlphaBeta Minimax (Take this one)")
#         print("5: Experimental Minimax")
#         print("6: Random")
#         try:
#             choice = int(input())
#             return choice
#         except(KeyError, ValueError):
#             print("Bad Input")


def main():
    clean()
    time_taken = []
    running = True
    terminal_state = False
    global WIDTH, HEIGHT, SIZE, TTT

    # buttons to be used in the opening screen
    title = create_title_rect(20, 15, 370, 70, 'Open-Field Tic Tac Toe')
    title_size = create_text_rect(30, 80, 350, 70, 'Choose Grid Size')
    title_algo = create_text_rect(35, 80, 350, 70, 'Choose Algorithm')

    # (x, y, w, h, text, fun)
    grid_btn_4 = create_button(30, 150, 150, 40, "4x4", grid_size_4)
    grid_btn_5 = create_button(230, 150, 150, 40, "5x5", grid_size_5)
    grid_btn_6 = create_button(30, 230, 150, 40, "6x6", grid_size_6)
    grid_btn_7 = create_button(230, 230, 150, 40, "7x7", grid_size_7)
    grid_btn_8 = create_button(30, 310, 150, 40, "8x8", grid_size_8)
    grid_btn_9 = create_button(230, 310, 150, 40, "9x9", grid_size_9)
    grid_btn_10 = create_button(130, 390, 150, 40, "10x10", grid_size_10)
    grid_btn_list = [grid_btn_4, grid_btn_5, grid_btn_6,
                     grid_btn_7, grid_btn_8, grid_btn_9, grid_btn_10]

    ai_btn_1 = create_button(30, 150, 350, 40, "Minimax (Don't if size > 4)", get_algo_1)
    ai_btn_2 = create_button(
        30, 200, 350, 40, "AlphaBeta (Don't if size > 4)", get_algo_2)
    ai_btn_3 = create_button(
        30, 250, 350, 40, "DepthLimit (Use This)", get_algo_3)
    ai_btn_4 = create_button(
        30, 300, 350, 40, "Depth_AB (Use This)", get_algo_4)
    ai_btn_5 = create_button(
        30, 350, 350, 40, "Experiment(Use This)", get_algo_5)
    ai_btn_6 = create_button(
        30, 400, 350, 40, "Random (Use This)", get_algo_6)

    button_list = [ai_btn_1, ai_btn_2,
                   ai_btn_3, ai_btn_4, ai_btn_5, ai_btn_6]

    screen = open_window()
    clock = pygame.time.Clock()
    ai_algo = 0
    grid_size = 0

    while running:
        pygame.display.update()
        clock.tick(30)

        if grid_size == 0 and ai_algo == 0:
            screen.fill(BG_COLOR)
            draw_button(title, screen)
            draw_button(title_size, screen)
            for btn in grid_btn_list:
                draw_button(btn, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # 1 is the left mouse button, 2 is middle, 3 is right.
                    if event.button == 1:
                        for btn in grid_btn_list:
                            if btn['rect'].collidepoint(event.pos):
                                btn['color'] = ACTIVE_COLOR
                                SIZE = btn['callback']()
                                grid_size = SIZE
                                print("grid size : ", SIZE)
                                WIDTH = 70*SIZE
                                HEIGHT = 70*SIZE

                elif event.type == pygame.MOUSEMOTION:
                    for btn in grid_btn_list:
                        if btn['rect'].collidepoint(event.pos):
                            btn['color'] = HOVER_COLOR
                        else:
                            btn['color'] = NORMAL_COLOR

        elif grid_size is not 0 and ai_algo == 0:
            pygame.display.flip()
            screen.fill(BG_COLOR)
            draw_button(title, screen)
            draw_button(title_algo, screen)
            for button in button_list:
                draw_button(button, screen)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        for button in button_list:
                            if button['rect'].collidepoint(event.pos):
                                button['color'] = ACTIVE_COLOR
                                ai_algo = button['callback']()
                                print("AI_algo : ", ai_algo)

                elif event.type == pygame.MOUSEMOTION:
                    for button in button_list:
                        if button['rect'].collidepoint(event.pos):
                            button['color'] = HOVER_COLOR
                        else:
                            button['color'] = NORMAL_COLOR

        elif grid_size is not 0 and ai_algo is not 0:
            screen = open_window()
            pygame.display.update()
            game_start(screen)
            print_status('x', False, False, screen)
            TTT = [[None for i in range(SIZE)] for j in range(SIZE)]
            while not terminal_state:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit(0)

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        userClick(TTT, screen)
                        game_over = is_game_over(TTT, screen)

                        if game_over:
                            print("Avg time taken : ", sum(
                                time_taken)/len(time_taken), "sec")
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
                                print("Avg time taken : ", sum(
                                    time_taken)/len(time_taken))
                                reset_game(TTT, screen)
                                pygame.quit()
                                terminal_state = True
                                running = False


if __name__ == "__main__":
    main()



"""
Written By:
Ketan Lambat
https://github.com/ketan-lambat/
"""
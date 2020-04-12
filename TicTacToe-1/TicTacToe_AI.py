import pygame
import time
import platform
import sys
from math import inf
from os import system
from random import choice
from pygame.locals import *
from AI_algo import *

pygame.init()
# global variables

WIDTH = 400
HEIGHT = 400

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LINE_COLOUR = (10, 10, 10)
BG_COLOR = (80, 80, 80)
BG_COLOR_2 = pygame.Color('darkslategrey')
BG_COLOR_3 = pygame.Color('purple4')
NORMAL_COLOR = pygame.Color('tan2')
HOVER_COLOR = pygame.Color('tan3')
ACTIVE_COLOR = pygame.Color('forestgreen')

FONT = pygame.font.SysFont('Comic Sans MS', 20)
TTT = [[None]*3, [None]*3, [None]*3]


# initialize pygame window
FPS = 30
CLOCK = pygame.time.Clock()


# load the images/sprites
x_img = pygame.image.load("X.png")
o_img = pygame.image.load("O.png")

# resize to proper scale
x_img = pygame.transform.scale(x_img, (80, 80))
o_img = pygame.transform.scale(o_img, (80, 80))


def open_window():
    screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
    pygame.display.set_caption("Tic Tac Toe with AI")
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
    text_surf = FONT.render(text, True, BLACK)
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

def create_text_button(x, y, w, h, text):

    text_surf = FONT.render(text, True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': BG_COLOR_3,
    }
    return button

def game_start(screen):

    screen.fill(BG_COLOR)

    # line(surface, color, start_pos, end_pos, width)

    # vertical lines
    pygame.draw.line(screen, LINE_COLOUR, (WIDTH/3, 0),
                     (WIDTH/3, HEIGHT), 7)
    pygame.draw.line(screen, LINE_COLOUR, (WIDTH/3*2, 0),
                     (WIDTH/3*2, HEIGHT), 7)

    # horizontal lines
    pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/3),
                     (WIDTH, HEIGHT/3), 7)
    pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT/3*2),
                     (WIDTH, HEIGHT/3*2), 7)

    pygame.display.update()


def draw_OX(row, col, OX, screen):
    if row == 1:
        posX = 30
    if row == 2:
        posX = WIDTH/3 + 30
    if row == 3:
        posX = WIDTH/3*2 + 30

    if col == 1:
        posY = 30
    if col == 2:
        posY = HEIGHT/3 + 30
    if col == 3:
        posY = HEIGHT/3*2 + 30

    if(OX == 'x'):
        screen.blit(x_img, (posY, posX))
    else:
        screen.blit(o_img, (posY, posX))

    pygame.display.update()


def draw_win_line(TTT, screen):
    # winning rows
    for row in range(0, 3):
        if ((TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None)):
            pygame.draw.line(screen, RED,
                             (0, (row+1)*HEIGHT/3-HEIGHT/6),
                             (WIDTH, (row+1)*HEIGHT/3-HEIGHT/6), 4)
            break

    # winning columns
    for col in range(0, 3):
        if((TTT[0][col] == TTT[1][col] == TTT[2][col])and(TTT[0][col] is not None)):
            pygame.draw.line(screen, RED,
                             ((col+1)*WIDTH/3-WIDTH/6, 0),
                             ((col+1)*WIDTH/3-WIDTH/6), HEIGHT, 4)
            break

    # diagonal winners
    if((TTT[0][0] is not None) and (TTT[0][0] == TTT[1][1] == TTT[2][2])):
        pygame.draw.line(screen, RED, (50, 50), (350, 350), 4)

    if((TTT[0][2] is not None) and (TTT[0][2] == TTT[1][1] == TTT[2][0])):
        pygame.draw.line(screen, RED, (350, 50), (50, 350), 4)


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
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(msg, 1, (255, 255, 255))

    # rendered msg on the screen
    screen.fill((0, 0, 0,), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(WIDTH/2, 500-50))
    screen.blit(text, text_rect)
    pygame.display.update()


def print_board(TTT):
    line = '---------------'
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
    for row in range(0, 3):
        if ((TTT[row][0] is not None) and (TTT[row][0] == TTT[row][1] == TTT[row][2])):
            return TTT[row][0]

    for col in range(0, 3):
        if((TTT[0][col] is not None) and (TTT[0][col] == TTT[1][col] == TTT[2][col])):
            return TTT[0][col]

    if((TTT[0][0] is not None) and (TTT[0][0] == TTT[1][1] == TTT[2][2])):
        return TTT[0][0]

    if((TTT[0][2] is not None) and (TTT[0][2] == TTT[1][1] == TTT[2][0])):
        return TTT[0][2]

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
    TTT = [[None]*3, [None]*3, [None]*3]


def ai_turn(TTT, screen, ai_algo):
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    clean()
    print("AI TURN")

    print_status('o', False, False, screen)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
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
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    while move < 1 or move > 9:
        try:
            move = int(input("Enter ip move position (1...9):"))
            coord = moves[move]
            move_possib = set_move(coord[0], coord[1], 'x', screen)

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
    if(x < WIDTH/3):
        col = 1
    elif(x < WIDTH/3*2):
        col = 2
    elif(x < WIDTH):
        col = 3
    else:
        col = None

    # row clicked
    if(y < HEIGHT/3):
        row = 1
    elif(y < HEIGHT/3*2):
        row = 2
    elif(y < HEIGHT):
        row = 3
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


def get_algo_1():
    return 1


def get_algo_2():
    return 2


def get_algo_3():
    return 3


def get_algo_4():
    return 4


def get_algo_5():
    return 5
def get_algo_6():
    return 6


def play_again(TTT, screen):
    while True:
        pygame.display.update()
        sys.stdout.write("Play again? [Y/N] : \n  ")
        answer = input().lower()
        if (answer == "y"):
            reset_game(TTT, screen)
            return True
        elif (answer == "n"):
            sys.exit(0)
        else:
            print("Please respond with 'Y' or 'N'.\n")


def get_first_player():
    first_move = ''
    while first_move != 'y' and first_move != 'n':
        try:
            first_move = input(
                'Want to start first?[Y/N]: ').lower()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad Input')
    if first_move == 'y':
        return 'x'
    else:
        return 'o'


def choose_algo():
    while True:
        print("Choose AI Algo. [1/2/3/4]")
        print("1: minimax")
        print("2: minimax-AlphaBeta")
        print("3: depth limited Minimax")
        print("4: depth limited AlphaBeta Minimax")
        print("5: Experimental Minimax")
        print("6: Random")
        try:
            choice = int(input())
            return choice
        except(KeyError, ValueError):
            print("Bad Input")


def main():
    clean()
    time_taken = []
    running = True
    terminal_state = False

    title = create_text_button(30, 50, 350, 70, 'Choose Algorithm')
    ai_butn_1 = create_button(30, 150, 150, 80, 'Minimax', get_algo_1)
    ai_butn_2 = create_button(230, 150, 150, 80, 'AlphaBeta', get_algo_2)
    ai_butn_3 = create_button(30, 250, 150, 80, 'DepthLimit', get_algo_3)
    ai_butn_4 = create_button(230, 250, 150, 80, 'Depth_AB', get_algo_4)
    ai_butn_5 = create_button(30, 350, 150, 80, 'Experiment', get_algo_5)
    ai_butn_6 = create_button(230, 350, 150, 80, 'Random', get_algo_6)

    button_list = [ai_butn_1, ai_butn_2, ai_butn_3, ai_butn_4, ai_butn_5, ai_butn_6]

    # while running:
    screen = open_window()
    clock = pygame.time.Clock()
    ai_algo = 0
    # ai_algo = get_algo_1(screen)
    # ai_algo = choose_algo()

    # player = get_first_player()
    # if player == 'o':
    #     ai_turn(screen)
    #     # first_move = ''

    while running:
        pygame.display.update()
        clock.tick(30)
        if ai_algo == 0:
            screen.fill(BG_COLOR_2)
            draw_button(title, screen)
            for button in button_list:
                draw_button(button, screen)
            

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    # pygame.quit()
                    # sys.exit(0)

                # else:

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # 1 is the left mouse button, 2 is middle, 3 is right.
                    if event.button == 1:
                        for button in button_list:
                            if button['rect'].collidepoint(event.pos):
                                button['color'] = ACTIVE_COLOR
                                ai_algo = button['callback']()
                                print(ai_algo)
                                # running = False
                                # break

                elif event.type == pygame.MOUSEMOTION:
                    for button in button_list:
                        if button['rect'].collidepoint(event.pos):
                            button['color'] = HOVER_COLOR
                        else:
                            button['color'] = NORMAL_COLOR

        elif ai_algo is not 0:

            pygame.display.update()
            game_start(screen)
            print_status('x', False, False, screen)
            while not terminal_state:

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # while len(empty_cells(TTT)) > 0 and not is_winner(TTT):

                        # if event.type == pygame.MOUSEBUTTONDOWN:
                        userClick(TTT, screen)
                        # user_turn(TTT, screen)
                        game_over = is_game_over(TTT, screen)

                        if game_over:
                            print("Avg time taken : ", sum(
                                time_taken)/len(time_taken))
                            reset_game(TTT, screen)
                            pygame.quit()
                            terminal_state = True
                            running = False
                            # pygame.event.get()
                            # terminal_state = play_again(TTT, screen)

                        # else:
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
                                # pygame.event.get()
                                # terminal_state = play_again(TTT, screen)

    # exit()


if __name__ == '__main__':
    main()

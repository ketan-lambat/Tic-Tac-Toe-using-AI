import pygame
import time
import platform
import sys
from math import inf
from os import system
from random import choice
from pygame.locals import *

# global variables
WIDTH = 400
HEIGHT = 400

# colours
WHITE = (255, 255, 255)
LINE_COLOUR = (10, 10, 10)
BG_COLOR = (80, 80, 80)

TTT = [[None]*3, [None]*3, [None]*3]
# USER = -1
# AI = 1

# initialize pygame window
pygame.init()
FPS = 30
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
pygame.display.set_caption("Tic Tac Toe with AI")

# load the images/sprites
x_img = pygame.image.load("X.png")
o_img = pygame.image.load("O.png")

# resize to proper scale
x_img = pygame.transform.scale(x_img, (80, 80))
o_img = pygame.transform.scale(o_img, (80, 80))


def reset_game(TTT):
    time.sleep(2)
    game_start()
    TTT = [[None]*3, [None]*3, [None]*3]


# def play_again():
#     while True:
#         pygame.display.update()
#         sys.stdout.write("Play again? [Y/N] : \n  ")
#         answer = input().lower()
#         if (answer == "y"):
#             return True
#         elif (answer == "n"):
#             sys.exit(0)
#         else:
#             print("Please respond with 'Y' or 'N'.\n")


def game_start():
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

    # print_status()


def print_status(playerTurn, isOver, winner):

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
    font = pygame.font.Font(None, 30)
    text = font.render(msg, 1, (255, 255, 255))

    # rendered msg on the screen
    screen.fill((0, 0, 0,), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(WIDTH/2, 500-50))
    screen.blit(text, text_rect)
    pygame.display.update()


def draw_OX(row, col, OX):
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


def draw_win_line(TTT):
    # winning rows
    for row in range(0, 3):
        if ((TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None)):
            # WINNER = TTT[row][0]
            pygame.draw.line(screen, (250, 0, 0),
                             (0, (row+1)*HEIGHT/3-HEIGHT/6),
                             (WIDTH, (row+1)*HEIGHT/3-HEIGHT/6), 4)
            break

    # winning columns
    for col in range(0, 3):
        if((TTT[0][col] == TTT[1][col] == TTT[2][col])and(TTT[0][col] is not None)):
            # WINNER = TTT[0][col]
            pygame.draw.line(screen, (250, 0, 0),
                             ((col+1)*WIDTH/3-WIDTH/6, 0),
                             ((col+1)*WIDTH/3-WIDTH/6), HEIGHT, 4)
            break

    # diagonal winners
    if((TTT[0][0] is not None) and (TTT[0][0] == TTT[1][1] == TTT[2][2])):
        # WINNER = TTT[0][0]
        pygame.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if((TTT[0][2] is not None) and (TTT[0][2] == TTT[1][1] == TTT[2][0])):
        # WINNER = TTT[0][2]
        pygame.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    # if(all([all(row) for row in TTT]) and WINNER is None):
    #     TIE = True
    # draw_status()

def eval(TTT):
    if is_winner(TTT) == 'x':
        score = -1
    elif is_winner(TTT) == 'o':
        score = 1
    else:
        score = 0
    return score


def is_winner(TTT):
    for row in range(0, 3):
        if ((TTT[row][0] is not None) and (TTT[row][0] == TTT[row][1] == TTT[row][2])):
            return TTT[row][0]
            # return True

    for col in range(0, 3):
        if((TTT[0][col] is not None) and (TTT[0][col] == TTT[1][col] == TTT[2][col])):
            return TTT[0][col]
            # return True

    if((TTT[0][0] is not None) and (TTT[0][0] == TTT[1][1] == TTT[2][2])):
        return TTT[0][0]
        # return True

    if((TTT[0][2] is not None) and (TTT[0][2] == TTT[1][1] == TTT[2][0])):
        return TTT[0][2]
        # return True

    return None
    # return False


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


def set_move(x, y, OX):
    if valid_move(x, y):
        TTT[x][y] = OX
        draw_OX(x+1, y+1, OX)
        return True
    else:
        return False


# if AI turn isMax = True
def minimax(TTT, depth, isMax):
    if isMax:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if depth == 0 or is_winner(TTT):
        score = eval(TTT)
        return [-1, -1, score]

    for cell in empty_cells(TTT):
        x, y = cell[0], cell[1]
        if isMax:
            TTT[x][y] = 'o'
        else:
            TTT[x][y] = 'x'
        score = minimax(TTT, depth-1, not isMax)
        TTT[x][y] = None
        score[0], score[1] = x, y

        if isMax:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

# clear the console


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def print_board(TTT):
    line = '---------------'
    print("\n" + line)
    # print(TTT)

    for x, row in enumerate(TTT):
        for y, cell in enumerate(row):
            if cell is None:
                symb = '_'
            else:
                symb = TTT[x][y]
            print(f'| {symb} |', end='')
        print("\n" + line)


def ai_turn():
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    clean()
    print("AI TURN")
    print_board(TTT)

    print_status('o', False, False)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(TTT, depth, True)
        x, y = move[0], move[1]

    set_move(x, y, 'o')
    time.sleep(1)


def user_turn():
    depth = len(empty_cells(TTT))
    if depth == 0 or is_winner(TTT):
        return

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print("USER TURN")
    print_board(TTT)

    print_status('x', False, False)

    while move < 1 or move > 9:
        try:
            move = int(input("Enter ip move position (1...9):"))
            coord = moves[move]
            move_possib = set_move(coord[0], coord[1], 'x')

            if not move_possib:
                print("Incorrect Move")
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad Input')


def main():
    clean()

    game_start()
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

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
            else:

                while len(empty_cells(TTT)) > 0 and not is_winner(TTT):
                    if first_move == 'n':
                        ai_turn()
                        first_move = ''

                    user_turn()
                    ai_turn()
                    pygame.event.pump()

                # game over conditions
                if is_winner(TTT) == 'x':
                    clean()
                    print("USER TURN")
                    print_board(TTT)
                    print("YOU WIN !!")
                    draw_win_line(TTT)
                    print_status(False, True, 'x')
                    # pygame.event.get()
                    # running = play_again()
                    reset_game(TTT)

                elif is_winner(TTT) == 'o':
                    clean()
                    print("AI TURN")
                    print_board(TTT)
                    print("AI WINS !!")
                    draw_win_line(TTT)
                    print_status(False, True, 'o')
                    # pygame.event.get()
                    # running = play_again()
                    reset_game(TTT)
                else:
                    clean()
                    print_board(TTT)
                    print("DRAW -_-")
                    print_status(False, True, False)
                    # pygame.event.get()
                    # running = play_again()
                    reset_game(TTT)

                exit()

            pygame.event.pump()
            CLOCK.tick(FPS)


if __name__ == '__main__':
    main()

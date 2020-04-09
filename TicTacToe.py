import pygame
import sys
import random
import time
from math import inf
from pygame.locals import *


# global variables
OX = 'x'
WINNER = None
TIE = False
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# colours
WHITE = (255, 255, 255)
LINE_COLOUR = (10, 10, 10)
BG_COLOR = (80, 80, 80)

TTT = [[None]*3, [None]*3, [None]*3]


# initialize pygame window
pygame.init()
FPS = 30
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+100))
pygame.display.set_caption("Tic Tac Toe with AI")


# load the images/sprites
x_img = pygame.image.load("X.png")
o_img = pygame.image.load("O.png")

# resize to proper scale
x_img = pygame.transform.scale(x_img, (80, 80))
o_img = pygame.transform.scale(o_img, (80, 80))


def game_start():
    screen.fill(BG_COLOR)

    # line(surface, color, start_pos, end_pos, width)

    # vertical lines
    pygame.draw.line(screen, LINE_COLOUR, (SCREEN_WIDTH/3, 0),
                     (SCREEN_WIDTH/3, SCREEN_HEIGHT), 7)
    pygame.draw.line(screen, LINE_COLOUR, (SCREEN_WIDTH/3*2, 0),
                     (SCREEN_WIDTH/3*2, SCREEN_HEIGHT), 7)

    # horizontal lines
    pygame.draw.line(screen, LINE_COLOUR, (0, SCREEN_HEIGHT/3),
                     (SCREEN_WIDTH, SCREEN_HEIGHT/3), 7)
    pygame.draw.line(screen, LINE_COLOUR, (0, SCREEN_HEIGHT/3*2),
                     (SCREEN_WIDTH, SCREEN_HEIGHT/3*2), 7)

    print_status()


def print_status():
    global TIE

    if WINNER is None:
        msg = OX.upper() + "'s Turn"
    else:
        msg = WINNER.upper() + " Won !"
    if TIE:
        msg = "Game Tied"

    # render(text, antialias, color, background=None) -> Surface
    font = pygame.font.Font(None, 30)
    text = font.render(msg, 1, (255, 255, 255))

    # rendered msg on the screen
    screen.fill((0, 0, 0,), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, 500-50))
    screen.blit(text, text_rect)
    pygame.display.update()


def is_winner(TTT):
    global WINNER
    for row in range(0, 3):
        if ((TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None)):
            # WINNER = TTT[row][0]
            # break
            return TTT[row][0]

    for col in range(0, 3):
        if((TTT[0][col] == TTT[1][col] == TTT[2][col])and(TTT[0][col] is not None)):
            # WINNER = TTT[0][col]
            # break
            return TTT[0][col]

    if((TTT[0][0] is not None) and (TTT[0][0] == TTT[1][1] == TTT[2][2])):
        # WINNER = TTT[0][0]
        return TTT[0][0]

    if((TTT[0][2] is not None) and (TTT[0][2] == TTT[1][1] == TTT[2][0])):
        # WINNER = TTT[0][2]
        return TTT[0][2]

    # return WINNER
    return None


def check_win():
    global TTT, WINNER, TIE

    # winning rows
    for row in range(0, 3):
        if ((TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None)):
            WINNER = TTT[row][0]
            pygame.draw.line(screen, (250, 0, 0),
                             (0, (row+1)*SCREEN_HEIGHT/3-SCREEN_HEIGHT/6),
                             (SCREEN_WIDTH, (row+1)*SCREEN_HEIGHT/3-SCREEN_HEIGHT/6), 4)
            break

    # winning columns
    for col in range(0, 3):
        if((TTT[0][col] == TTT[1][col] == TTT[2][col])and(TTT[0][col] is not None)):
            WINNER = TTT[0][col]
            pygame.draw.line(screen, (250, 0, 0),
                             ((col+1)*SCREEN_WIDTH/3-SCREEN_WIDTH/6, 0),
                             ((col+1)*SCREEN_WIDTH/3-SCREEN_WIDTH/6), SCREEN_HEIGHT, 4)
            break

    # diagonal winners
    if((TTT[0][0] is not None) and (TTT[0][0] == TTT[1][1] == TTT[2][2])):
        WINNER = TTT[0][0]
        pygame.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if((TTT[0][2] is not None) and (TTT[0][2] == TTT[1][1] == TTT[2][0])):
        WINNER = TTT[0][2]
        pygame.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if(all([all(row) for row in TTT]) and WINNER is None):
        TIE = True
    print_status()


def draw_OX(row, col):
    global TTT, OX
    print("drawing", OX, " : ",  row, col)
    if row == 1:
        posX = 30
    if row == 2:
        posX = SCREEN_WIDTH/3 + 30
    if row == 3:
        posX = SCREEN_WIDTH/3*2 + 30

    if col == 1:
        posY = 30
    if col == 2:
        posY = SCREEN_HEIGHT/3 + 30
    if col == 3:
        posY = SCREEN_HEIGHT/3*2 + 30

    TTT[row-1][col-1] = OX
    if(OX == 'x'):
        screen.blit(x_img, (posY, posX))
        OX = 'o'
    else:
        screen.blit(o_img, (posY, posX))
        OX = 'x'
    pygame.display.update()


def userClick():
    # global TTT
    x, y = pygame.mouse.get_pos()

    # col clicked
    if(x < SCREEN_WIDTH/3):
        col = 1
    elif(x < SCREEN_WIDTH/3*2):
        col = 2
    elif(x < SCREEN_WIDTH):
        col = 3
    else:
        col = None

    # row clicked
    if(y < SCREEN_HEIGHT/3):
        row = 1
    elif(y < SCREEN_HEIGHT/3*2):
        row = 2
    elif(y < SCREEN_HEIGHT):
        row = 3
    else:
        row = None

    if(row and col and TTT[row-1][col-1] is None):
        global OX
        draw_OX(row, col)
        # check_win()


def reset_game():
    global TTT, WINNER, OX, TIE
    time.sleep(2)
    OX = 'x'
    TIE = False
    game_start()
    WINNER = None
    TTT = [[None]*3, [None]*3, [None]*3]


def empty_cells(TTT):
    # global TTT
    cells = []

    for x, row in enumerate(TTT):
        for y, cell in enumerate(row):
            # print(x, row, y, cell)
            if cell is None:
                cells.append([x, y])
    print(cells)
    return cells


def evalFunc(WINNER):
    # global WINNER
    # AI wins
    if WINNER == 'o':
        return 1
    # user wins
    elif WINNER == 'x':
        return -1
    else:
        return 0


def minimax(TTT, depth, isMax):
    print("minimax \t depth", depth, "\t isMax:",  isMax)
    # global TTT,
    # global TIE, WINNER

    if isMax == True:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]

    if depth == 0 or is_winner(TTT):
        # score = evalFunc(WINNER)
        if is_winner(TTT) == 'x':
            score = -1
        elif is_winner(TTT) == 'o':
            score = 1
        else:
            score = 0
        print("is_winner() : ", score)
        return [-1, -1, score]

    for cell in empty_cells(TTT):
        x, y = cell[0], cell[1]
        if isMax:
            TTT[x][y] = 'o'
        else:
            TTT[x][y] = 'x'

        score = minimax(TTT, depth - 1, not isMax)
        print("score : ", score)
        TTT[x][y] = None
        # WINNER = None
        score[0], score[1] = x, y

        if isMax:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
        print("best", best)

    print("best_op", best)
    return best

    # if score == 1:
    #     return score
    # if score == -1:
    #     return score
    # if TIE:
    #     return 0

    # if is_winner(TTT) or depth == 0:
    #     # WINNER = None
    #     return result

    # if isMax:
    #     best = -10000

    #     for cell in empty_cells(TTT):
    #         x, y = cell[0], cell[1]
    #         TTT[x][y] = 'o'
    #         score = minimax(depth-1, False)
    #         TTT[x][y] = None
    #         best = max(best, score)

    #     return best
    # else:
    #     best = 10000

    #     for cell in empty_cells(TTT):
    #         x, y = cell[0], cell[1]
    #         TTT[x][y] = 'x'
    #         score = minimax(depth-1, True)
    #         TTT[x][y] = None
    #         best = min(best, score)

    #     return best


def ai_move(TTT):
    # global TTT, WINNER
    depth = len(empty_cells(TTT))
    print("depth:", depth)

    if depth == 0 or is_winner(TTT):
        # WINNER = None
        return
    move = minimax(TTT, depth, True)
    print("move : ", move)
    row = move[0]
    col = move[1]
    # global OX
    # OX = 'o'
    # TTT[row][col] = OX
    draw_OX(row+1, col+1)
    # draw_OX(col+1, row+1)
    # check_win()

    # best = -inf

    # for cell in empty_cells(TTT):
    #     x, y = cell[0], cell[1]
    #     TTT[x][y] = 'o'
    #     score = minimax(depth, True)
    #     print("(x, y):", x, y, "score: ", score)
    #     TTT[x][y] = None
    #     if score > best:
    #         best = score
    #         row = x
    #         col = y

    # print("(row, col):", row+1, col+1, "best: ", best)
    # draw_OX(row+1, col+1)


game_start()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN:
            while len(empty_cells(TTT)) > 0 and not (WINNER or TIE):
                userClick()
                check_win()
                time.sleep(1)
                ai_move(TTT)
                check_win()
                print(TTT)
            if (WINNER or TIE):
                reset_game()

    pygame.display.update()
    CLOCK.tick(FPS)

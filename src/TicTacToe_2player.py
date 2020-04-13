import pygame
import sys
import random
import time
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
# BG_COLOR = (170, 30, 200)
# BG_COLOR = (220, 140, 20)
BG_COLOR = (80, 80, 80)
# BG_COLOR = (200, 70, 230)

TTT = [[None]*3, [None]*3, [None]*3]


# initialize pygame window
pygame.init()
FPS = 60
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

    draw_status()


def draw_status():
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
    draw_status()


def draw_OX(row, col):
    global TTT, OX
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
        check_win()


def reset_game():
    global TTT, WINNER, OX, TIE
    time.sleep(2)
    OX = 'x'
    TIE = False
    game_start()
    WINNER = None
    TTT = [[None]*3, [None]*3, [None]*3]


game_start()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN:
            userClick()
            if (WINNER or TIE):
                reset_game()

    pygame.display.update()
    CLOCK.tick(FPS)
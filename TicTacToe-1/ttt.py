from math import inf
from random import choice
import platform
import time
from os import system


TTT = [[None]*3, [None]*3, [None]*3]
USER = -1
AI = 1


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

    while move < 1 or move > 9:
        try:
            move = int(input("Enter ip move position (1...9):"))
            coord = moves[move]
            move_possib = set_move(coord[0], coord[1], 'x')

            if not move_possib:
                print("Incorrect ip")
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    clean()

    while len(empty_cells(TTT)) > 0 and not is_winner(TTT):
        user_turn()
        ai_turn()

    if is_winner(TTT) == 'x':
        clean()
        print("USER TURN")
        print_board(TTT)
        print("YOU WIN !!")
    elif is_winner(TTT) == 'o':
        clean()
        print("AI TURN")
        print_board(TTT)
        print("AI WINS !!")
    else:
        clean()
        print_board(TTT)
        print("DRAW -_-")


if __name__ == '__main__':
    main()

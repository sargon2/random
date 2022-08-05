#!/usr/bin/env python3

from itertools import chain

# "Hard" puzzle from sudoku.com
puzzle = [[0, 4, 9, 0, 0, 0, 0, 0, 5],
          [0, 0, 0, 8, 3, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 8],
          [0, 0, 0, 0, 9, 0, 8, 1, 0],
          [0, 0, 0, 0, 0, 7, 6, 0, 0],
          [0, 0, 1, 0, 0, 0, 3, 0, 0],
          [7, 8, 0, 4, 1, 0, 0, 0, 9],
          [2, 9, 4, 7, 0, 0, 0, 0, 0],
          [6, 0, 0, 9, 0, 0, 0, 0, 0]]

def print_board(board):
    print()
    for i in range(0, 9):
        print("%d %d %d | %d %d %d | %d %d %d" % tuple(board[i]))
        if i % 3 == 2:
            print("------+-------+------")

def print_possible(possible):
    for i in range(0, 9):
        for j in range(0, 9):
            print(i, j, ": ", end=" ")
            for k in range(0, 9):
                if possible[i][j][k]:
                    print(k+1, end=" ")
            print()

def square_iter(row, col):
    upper_left_row = row - (row % 3)
    upper_left_col = col - (col % 3)
    for x in range(upper_left_row, upper_left_row+3):
        for y in range(upper_left_col, upper_left_col+3):
            yield (x, y)

print("Puzzle:")
print_board(puzzle)

possible = [[[True for i in range(0, 9)] for j in range(0, 9)] for k in range(0, 9)]

# For each known square, set possible to that answer only
for row in range(0, 9):
    for column in range(0, 9):
        answer = puzzle[row][column]
        if answer != 0:
            possible[row][column] = [i==answer-1 for i in range(0, 9)]

while True:
    mutated = False
    # Remove conflicting possible numbers
    for row in range(0, 9):
        for column in range(0, 9):
            answer = puzzle[row][column]
            if answer != 0:
                # Rows
                for i in chain(range(0, column), range(column+1, 9)):
                    if possible[row][i][answer-1]:
                        mutated = True
                        possible[row][i][answer-1] = False

                # Columns
                for i in chain(range(0, row), range(row+1, 9)):
                    if possible[i][column][answer-1]:
                        mutated = True
                        possible[i][column][answer-1] = False

                # Squares
                for x, y in square_iter(row, column):
                    if x != row and y != column:
                        if possible[x][y][answer-1]:
                            mutated = True
                            possible[x][y][answer-1] = False
    # TODO other strategies -- there are lots. See https://www.sudokuwiki.org/sudoku.htm

    # Scan for squares where there's only a single possible number and fill it in
    for row in range(0, 9):
        for column in range(0, 9):
            possibles = possible[row][column]
            count = 0
            val = -1
            for i in range(0, 9):
                if possible[row][column][i] == True:
                    count += 1
                    if count > 1:
                        break
                    val = i+1
            if count == 0:
                print("Error, no possible answers!", row, column)
                exit(1)
            if count == 1:
                if puzzle[row][column] == 0:
                    print("Setting", row, column, val)
                    mutated = True
                    puzzle[row][column] = val

    if not mutated:
        print("No mutations")
        exit(0)

    print_board(puzzle)
    print_possible(possible)

board = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
         [6, 0, 0, 0, 7, 5, 0, 0, 9],
         [0, 0, 0, 6, 0, 1, 0, 7, 8],
         [0, 0, 7, 0, 4, 0, 2, 6, 0],
         [0, 0, 1, 0, 5, 0, 9, 3, 0],
         [9, 0, 4, 0, 6, 0, 0, 0, 5],
         [0, 7, 0, 3, 0, 0, 0, 1, 2],
         [1, 2, 0, 0, 0, 7, 4, 0, 0],
         [0, 4, 9, 2, 0, 6, 0, 0, 7]]


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def find_empty(board):
    for i, row in enumerate(board):
        for j, num in enumerate(row):
            if num == 0:
                return i, j
    return -1


def valid_move(board, num, position):
    # Check for duplicates in row:
    if board[position[0]].count(num) > 1:
        return False

    # Check for duplicates in column:
    for i in range(len(board)):
        if board[i][position[1]] == num and i != position[0]:
            return False

    # Check for duplicates in 3x3 box:
    x_box = position[0] // 3
    y_box = position[1] // 3

    for i in range(x_box * 3, x_box * 3 + 3):
        for j in range(y_box * 3, y_box * 3 + 3):
            if board[i][j] == num and (i, j) != position:
                return False
    return True


def solve(board):
    if find_empty(board) == -1:
        return True
    else:
        row, col = find_empty(board)
        for i in range(1, 10):
            if valid_move(board, i, (row, col)):
                board[row][col] = i

                if solve(board):
                    return True

                board[row][col] = 0
        return False


print_board(board)
solve(board)
print('Solved:')
print_board(board)

import pyautogui as pyg
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



board1 = [[6, 9, 0, 4, 0, 5, 0, 7, 0],
         [0, 0, 4, 9, 0, 0, 0, 0, 1],
         [8, 0, 5, 7, 6, 0, 4, 2, 9],
         [0, 4, 6, 1, 0, 0, 0, 3, 2],
         [0, 0, 0, 0, 9, 0, 0, 0, 5],
         [5, 0, 3, 2, 8, 4, 0, 0, 6],
         [3, 5, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 8, 3, 0, 2, 5, 0],
         [2, 8, 0, 0, 0, 0, 6, 0, 0]]


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
    for i in range(len(board[0])):
        if board[position[0]][i] == num and i != position[1]:
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


def input_values(board):
    str_vals = [str(num) for row in board for num in row]
    print(str_vals)
    # for i, str_val in enumerate(str_vals):
    #     if (i + 1) % 9 == 0:
    #         pyg.press(str_val)
    #         pyg.press('down')
    #         pyg.press('left')
    #         pyg.press('left')
    #         pyg.press('left')
    #         pyg.press('left')
    #         pyg.press('left')
    #         pyg.press('left')
    #         pyg.press('left')
    #         pyg.press('left')
    #     else:
    #         pyg.press(str_val)
    #         pyg.press('right')

def main():
    # Read sudoku board
    sudoku_matrix = np.zeros((9, 9)).astype(int)
    chrome_path = r'/Users/tariqkharseh/Desktop/chromedriver'
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://nine.websudoku.com/?level=4')
    time.sleep(3)

    board = []
    blank_idxs = []
    for row_idx in range(9):
        row = []
        for col_idx in range(9):
            element = driver.find_element(By.XPATH, '//*[@id="f{}{}"]'.format(col_idx, row_idx)).get_attribute('value')
            if element == '':
                row.append(0)
                blank_idx = str(col_idx) + str(row_idx)
                blank_idxs.append(blank_idx)
            else:
                row.append(int(element))
        board.append(row)

    solve(board)

    for idx in blank_idxs:
        col, row = idx[0], idx[1]
        blank_box = driver.find_element(By.XPATH, '//*[@id="f{}{}"]'.format(col, row))
        blank_box.send_keys(board[int(row)][int(col)])
    time.sleep(2)
    button = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/p[4]/input[1]')
    button.click()
    time.sleep(15)

main()
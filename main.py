import time
from selenium import webdriver
from selenium.webdriver.common.by import By


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


def main():
    # Open website
    chrome_path = r'/Users/tariqkharseh/Desktop/chromedriver'
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://nine.websudoku.com/?level=4')
    time.sleep(3)

    # Make board and read values from website
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

    # Solve board
    solve(board)

    # Fill in solved values on website
    for idx in blank_idxs:
        col, row = idx[0], idx[1]
        blank_box = driver.find_element(By.XPATH, '//*[@id="f{}{}"]'.format(col, row))
        blank_box.send_keys(board[int(row)][int(col)])
    time.sleep(2)

    # Submit solution
    button = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/p[4]/input[1]')
    button.click()
    time.sleep(15)


if __name__ == '__main__':
    main()
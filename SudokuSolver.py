# function to check if certain num at board location is valid
def is_valid(board, row, col, num):
    # check if num is in the current row
    for i in range(9):
        if board[row][i] == num:
            return False
    # check if num is in the current col
    for i in range(9):
        if board[i][col] == num:
            return False
        
    # check if num in 3x3 subgrid
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    # num is not in row, col, or 3x3 subgrid so it can be placed
    return True

# backtracking function to sovle board
def solve_sudoku(board):
    # loop through each cell in the board
    for row in range(9):
        for col in range(9):
            # check if current cell is empty
            if board[row][col] == '.':
                # test all numbers from 1-9
                for num in map(str, range(1, 10)):
                    # check if num is valid and can be placed
                    if is_valid(board, row, col, num):
                        board[row][col] = num       # set cell to num
                        if solve_sudoku(board):     # recursively try to solve the rest of the board
                            return True
                        board[row][col] = '.'   # if no solution is found, backtrack by resetting the cell
                # return false because no number can be placed in the cell
                return False
    # board is filled and all cells are valid            
    return True

# function to print board
def print_board(board):
    for row in board:
        print(" ". join(row))

# example board given (solvable)
board_1 = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

# test board (unsolvable)
board_2 = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
           ["6", ".", ".", "1", "9", "5", ".", ".", "."],
           [".", "9", "8", ".", ".", ".", ".", "6", "."],
           ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
           ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
           ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
           [".", "6", ".", ".", ".", ".", "2", "8", "."],
           [".", ".", ".", "4", "1", "9", ".", ".", "5"],
           [".", ".", ".", ".", "8", ".", ".", "7", "8"]]  # The last row has two '8's, making it unsolvable

# edit this variable to test other boards
board = board_2

if solve_sudoku(board):
    print("Sudoku solved:")
    print_board(board)
else:
    print("Sudoku board is unsolvable.")
    print_board(board)
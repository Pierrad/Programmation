# TODO create the random sudoku
import random as rd
# Create a board (lenght*lenght)
def createBoard(lenght):
    board = [[0 for i in range(lenght)] for j in range(lenght)]
    return board

# Print the board
def printBoard(board, lenght):
    for i in range(lenght):
        print(board[i])
    print("\n")

# Check if the number is already in the square
def checkIfInSquare(board, x, y, num):
    # Replace the coords into the first upper left square
    boardX = y // 3
    boardY = x // 3
    # Double for that loop in [x*3,x*3+3], multiplication *3 to return in the original range of coords and +3 beacause square of 3
    # This double loop pass in every element of the square
    for i in range(boardY*3, boardY*3 + 3):
        for j in range(boardX*3, boardX*3 + 3):
            # If the number is equal to the number in the case and if the position (i,j) is not the new position (we can rewrite by the same number)
            if board[i][j] == num and (i,j) != (x,y):
                return False
    return True

# Check if the number is already in the row
def checkIfInRow(board, x, y, num):
    # If the number is in the row and if the position is not the new position (we can rewrite by the same number)
    if num in board[x] and (x,y) != (x, board[x].index(num)):
        return False
    return True

# Check if the number is already in the column
def checkIfInColumn(board, x, y, num):
    # For loop on the size of the board
    for i in range(len(board)):
        # If tbe number is in the column and if the position is not the new position (we can rewrite by the same number)
        if num == board[i][y] and x != i:
            return False
    return True

# Create a random board
def randomBoard(board, alreadyPlaced, lenght):
    # Choose a random position in the board and place a number in it until alreadyPlaced > 0
    while(alreadyPlaced > 0):
        x = rd.randint(0,lenght-1)
        y = rd.randint(0,lenght-1)
        num = rd.choice(range(1,10))
        # Check if the num can be at this position
        if checkIfInRow(board, x, y, num) == True and checkIfInColumn(board, x, y, num) == True and checkIfInSquare(board, x, y, num) == True:
            board[x][y] = num
            alreadyPlaced -= 1
    return board

# Check if the 2 boards are the same after the solve
def checkIfValid(board, board2):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != board2[i][j]:
                return False
    return True

# Check if Empty space (0) in the board and return the position (x,y) of this empty space if it exist
def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return i, j
    return None

# Solve the board with Backtracking algorithm (recursive programming)
def solve(board):
    # Get the empty space and if no empty space then return true because it's solve
    find = findEmpty(board)
    if find == None:
        return True
    else:
        x, y = find
    for i in range(1,10):
        if checkIfInRow(board, x, y, i) == True and checkIfInColumn(board, x, y, i) == True and checkIfInSquare(board, x, y, i) == True:
            board[x][y] = i
            # This is recursive programming, this will continue until it falls on False or until there is no more 0 then its solve
            if solve(board):
                return True
            # If the last if falls on False then the number at the beginning was not the good one, then we reput 0 and try again with another numer (for loop)
            board[x][y] = 0
    # There is no solution
    return False


# Taille du board
lenght = 9
# Number of digits already places in the board
alreadyPlaced = 20
# Creat a Board by 9*9
board = createBoard(lenght)
# Create a random Sudoku board
board = randomBoard(board, alreadyPlaced, lenght)
printBoard(board, lenght)
# Solve the new Random Board
value = solve(board)
print(value)
printBoard(board, lenght)



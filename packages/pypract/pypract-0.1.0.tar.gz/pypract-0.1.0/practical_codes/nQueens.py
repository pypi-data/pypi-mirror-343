def isValid(board, row, col, N):
    # Check the row to the left of current column
    for i in range(col):
        if board[row][i] == 1:
            return False
    
    # Check the upper diagonal to the left
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    
    # Check the lower diagonal to the left
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    
    return True

def solveNQueen(board, col, N):
    if col >= N:
        return True
    

    for i in range(N):
        if isValid(board, i, col, N):
            board[i][col] = 1
            if solveNQueen(board, col + 1, N):
                return True
            # Backtrack
            board[i][col] = 0
    
    return False

def printBoard(board, N):
    for i in range(N):
        for j in range(N):
            print("Q" if board[i][j] == 1 else "_", end=" ")
        print()

def nQueens(N):
    board = [[0] * N for _ in range(N)] 
    if not solveNQueen(board, 0, N):
        print("No solution exists")
    else:
        printBoard(board, N)

N = 8  
nQueens(N)

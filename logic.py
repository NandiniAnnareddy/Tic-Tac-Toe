
# Tic Tac Toe backend logic
# 3x3 Board
board = [["" for i in range(3)] for i in range(3)]

def reset_board():
    global board
    board = [["" for i in range(3)] for i in range(3)]

def check_winner(player):
    # Rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def check_draw():
    return all(board[r][c] != "" for r in range(3) for c in range(3))

def computer_move(symbol="O", player_symbol="X"):
    # 1. Here computer will check if it can win
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = symbol
                if check_winner(symbol):
                    return r, c
                board[r][c] = ""

    # 2. Here computer will try to block the opponent
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = player_symbol
                if check_winner(player_symbol):
                    board[r][c] = symbol
                    return r, c
                board[r][c] = ""

    # 3. If center is empty first it will choose center
    if board[1][1] == "":
        board[1][1] = symbol
        return 1, 1

    # 4. If center is not empty it chooses corners
    for r, c in [(0,0),(0,2),(2,0),(2,2)]:
        if board[r][c] == "":
            board[r][c] = symbol
            return r, c

    # 5. If corners are not empty it chooses edges
    for r, c in [(0,1),(1,0),(1,2),(2,1)]:
        if board[r][c] == "":
            board[r][c] = symbol
            return r, c

    # 6. If edges are not empty it chooses random
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = symbol
                return r, c

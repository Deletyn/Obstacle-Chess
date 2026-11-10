import sys

white_king = 'K'
white_queen = 'Q'
white_rook = 'R'
white_knight = 'N'
white_bishop = 'B'
white_pawn = 'P' 

black_king = 'k'
black_queen = 'q'
black_rook = 'r'
black_knight = 'n'
black_bishop = 'b'
black_pawn = 'p' 

hidden_trap_door = 'D'
open_trap_door = 'O'
mine = 'M'
mine_hidden_trap_door = 'X'
west_wall = '|'
south_wall = '_'
empty_squre = '.'

file = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

def is_valid_square(board, x, y):
    return 0 <= y < len(board) and 0 <= x < len(board[y])

def is_blocked(board, start_pos, target_pos):
    x1, y1 = start_pos
    x2, y2 = target_pos

    dx = 1 if x1 < x2 else -1 if x1 > x2 else 0
    dy = 1 if y1 < y2 else -1 if y1 > y2 else 0

    x, y = x1 + dx, y1 + dy
    while (x, y) != (x2, y2):
        if board[y][x] != '.':
            return True
        x += dx
        y += dy

    return False 

def can_move(board, start_pos, target_pos):
    x1, y1 = start_pos
    x2, y2 = target_pos

    piece = board[y1][x1]

    if piece == white_king or piece == black_king:
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

    if piece == white_queen or piece == black_queen:
        return (x1 == x2 or y1 == y2 or abs(x1 - x2) == abs(y1 - y2)) and not is_blocked(board, start_pos, target_pos)

    if piece == white_rook or piece == black_rook:
        return (x1 == x2 or y1 == y2) and not is_blocked(board, start_pos, target_pos)

    if piece == white_bishop or piece == black_bishop:
        return abs(x1 - x2) == abs(y1 - y2) and not is_blocked(board, start_pos, target_pos)

    if piece == white_knight or piece == black_knight:
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    if piece == white_pawn or piece == black_pawn:
        if (piece == white_pawn and y2 == y1 - 1 and x1 == x2) or (piece == black_pawn and y2 == y1 + 1 and x1 == x2):
            return board[y2][x2] == '.'
        if (piece == white_pawn and y2 == y1 - 1 and abs(x1 - x2) == 1 and board[y2][x2].islower()) or (piece == black_pawn and y2 == y1 + 1 and abs(x1 - x2) == 1 and board[y2][x2].isupper()):
            return True

    return False   

def black_rook_check(board, target_pos):
    right = len(board[target_pos[1]])
    left = target_pos[0]
    top = target_pos[1]

    blocked = False
    # Vertically up
    for i in range(top-1, -1, -1):
        if board[i][target_pos[0]] != '.' and board[i][target_pos[0]] != white_king:
            blocked = True
        if  board[i][target_pos[0]] == white_king and blocked == False:
            checkmate = b_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True
        
    blocked = False    
    # Vertically down    
    for i in range(target_pos[1] + 1, 8):
        if board[i][target_pos[0]] != '.' and board[i][target_pos[0]] != white_king:
            blocked = True
        if board[i][target_pos[0]] == white_king and blocked == False:
            checkmate = b_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True

    blocked = False
    # Horizontally to the left
    for i in range(left - 1, -1, -1):
        if board[target_pos[1]][i] != '.' and board[target_pos[1]][i] != white_king:
            blocked = True
        if board[target_pos[1]][i] == white_king and blocked == False:
            checkmate = b_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True  

    blocked = False
    # Horizontally to the right
    for i in range(target_pos[0] + 1, right):
        if board[target_pos[1]][i] != '.' and board[target_pos[1]][i] != white_king:
            blocked = True
        if board[target_pos[1]][i] == white_king and blocked == False:
            checkmate = b_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True    
    return False

def white_rook_check(board, target_pos):
    right = len(board[target_pos[1]]) - target_pos[0]
    left = target_pos[0]
    top = target_pos[1]

    blocked = False
    # Vertically up
    for i in range(top-1, -1, -1):
        if board[i][target_pos[0]] != '.' and board[i][target_pos[0]] != black_king:
            blocked = True
        if  board[i][target_pos[0]] == black_king and blocked == False:
            checkmate = w_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True
        
    blocked = False
    # Vertically down    
    for i in range(target_pos[1] + 1, 8):
        if board[i][target_pos[0]] != '.' and board[i][target_pos[0]] != black_king:
            blocked = True
        if board[i][target_pos[0]] == black_king and blocked == False:
            checkmate = w_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True            


    blocked = False
    # Horizontally to the left
    for i in range(left - 1, -1, -1):
        if board[target_pos[1]][i] != '.' and board[target_pos[1]][i] != black_king:
            blocked = True
        if board[target_pos[1]][i] == black_king and blocked == False:
            checkmate = w_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True       

    blocked = False
    # Horizontally to the right
    for i in range(target_pos[0] + 1, right):
        if board[target_pos[1]][i] != '.' and board[target_pos[1]][i] != black_king:
            blocked = True
        if board[target_pos[1]][i] == black_king and blocked == False:
            checkmate = w_checkmate(board, [i, target_pos[0]])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True
            
    return False

def white_knight_check(board, target_pos):
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    for dx, dy in knight_moves:
        new_x, new_y = target_pos[0] + dx, target_pos[1] + dy

        if is_valid_square(board, new_x, new_y) and board[new_y][new_x] == black_king:
            checkmate = w_checkmate(board, [new_x, new_y])
            if checkmate:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True

    return False

def black_knight_check(board, target_pos):
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    for dx, dy in knight_moves:
        new_x, new_y = target_pos[0] + dx, target_pos[1] + dy

        if is_valid_square(board, new_x, new_y) and board[new_y][new_x] == white_king:
            checkmate = b_checkmate(board, [new_x, new_y])
            if checkmate:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True

    return False

def white_bishop_check(board, target_pos):
    blocked = False
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for direction in directions:
        i = target_pos[1]
        j = target_pos[0]

        while (i >= 0 and i < 8 and j >= 0 and j < len(board[i])):
            i += direction[0]
            j += direction[1]

            if (i >= 0 and i < 8 and j >= 0 and j < len(board[i])):
                if board[i][j] == black_king:
                    k = target_pos[1]
                    p = target_pos[0]
                    while (k >= 0 and k < 8 and p >= 0 and p < len(board[k])):
                        k += direction[0]
                        p += direction[1]
                        if (k >= 0 and k < 8 and p >= 0 and p < len(board[k])):
                            if board[k][p] != '.' and board[k][p] != black_king:
                                blocked = True
                            if board[k][p] == black_king and blocked == False:
                                return True
                            
    return False

def black_bishop_check(board, target_pos):
    blocked = False
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for direction in directions:
        i = target_pos[1]
        j = target_pos[0]

        while (i >= 0 and i < 8 and j >= 0 and j < len(board[i])):
            i += direction[0]
            j += direction[1]

            if (i >= 0 and i < 8 and j >= 0 and j < len(board[i])):
                if board[i][j] == white_king:
                    k = target_pos[1]
                    p = target_pos[0]
                    while (k >= 0 and k < 8 and p >= 0 and p < len(board[k])):
                        k += direction[0]
                        p += direction[1]
                        if (k >= 0 and k < 8 and p >= 0 and p < len(board[k])):
                            if board[k][p] != '.' and board[k][p] != white_king:
                                blocked = True
                            if board[k][p] == white_king and blocked == False:
                                return True
                               
    return False

def white_queen_check(board, target_pos):    
    if white_rook_check(board, target_pos) or white_bishop_check(board, target_pos):
        return True
    return False

def black_queen_check(board, target_pos):
    if black_rook_check(board, target_pos) or black_bishop_check(board, target_pos):
        return True
    return False

def white_pawn_check(board, target_pos):
    if target_pos[1] - 1 >= 0 and target_pos[0] - 1 >= 0 and target_pos[0] + 1 < len(board[target_pos[1]]):
        if board[target_pos[1]-1][target_pos[0]+1] == black_king:
            checkmate = w_checkmate(board, [target_pos[1]-1, target_pos[0]+1])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True  
        if board[target_pos[1]-1][target_pos[0]-1] == black_king:
            checkmate = w_checkmate(board, [target_pos[1]-1, target_pos[0]-1])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True 
    return False

def black_pawn_check(board, target_pos):
    if target_pos[1] + 1 <= 7 and target_pos[0] - 1 >= 0 and target_pos[0] + 1 < len(board[target_pos[1]]):
        if board[target_pos[1]+1][target_pos[0]+1] == white_king:
            checkmate = b_checkmate(board, [target_pos[1]+1, target_pos[0]+1])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True 
        if board[target_pos[1]+1][target_pos[0]-1] == white_king:
            checkmate = b_checkmate(board, [target_pos[1]+1, target_pos[0]-1])
            if checkmate == True:
                print("INFO: checkmate", file=sys.stdout)
            else:
                return True 
    return False
        
def b_checkmate(board, w_king_pos):
    white_moves = []

    for y in range(8):
        for x in range(len(board[y])):
            if board[y][x] in (black_king, black_queen, black_rook, black_knight, black_bishop, black_pawn):
                if can_move(board, (x, y), w_king_pos):
                    white_moves.append((x, y))

    return len(white_moves) == 0

def w_checkmate(board, b_king_pos):
    black_moves = []

    for y in range(8):
        for x in range(len(board[y])):
            if board[y][x] in (white_king, white_queen, white_rook, white_knight, white_bishop, white_pawn):
                if can_move(board, (x, y), b_king_pos):
                    black_moves.append((x, y))

    return len(black_moves) == 0                                            
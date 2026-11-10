import sys
import piece_check

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

def move(half_move, board, side_move):
    half_m = half_move.split('-')
    
    status = board[8].split(" ")

    next_to_move = status[0]
    w_walls = int(status[1])
    b_walls = int(status[2])
    w_kingside = status[3]
    w_queenside = status[4]
    b_kingside = status[5]
    b_queenside = status[6]
    en_passant = status[7]
    halfmove_clock = int(status[8])

    halfmove_clock += 1  

    if len(half_m) == 1:
        if half_m[0] == '':
            print_move_error(half_move)
        end = half_m[0]
        piece = end[0]
        target_pos = [file.index(end[1]), 8-int(end[2])]
        if piece == hidden_trap_door:
            check_initial(board, half_move, side_move, halfmove_clock)
            halfmove_clock = 0
            if not (2 <= target_pos[1] <= 5):
                print_move_error(half_move)
            if board[target_pos[1]][target_pos[0]] == mine:
                board[target_pos[1]][target_pos[0]] = mine_hidden_trap_door
            elif board[target_pos[1]][target_pos[0]] == mine_hidden_trap_door:
                board[target_pos[1]][target_pos[0]] = mine_hidden_trap_door
            else:
                board[target_pos[1]][target_pos[0]] = hidden_trap_door
        if piece == mine:
            check_initial(board, half_move, side_move, halfmove_clock)
            halfmove_clock = 0
            if not (3 <= target_pos[1] <= 4):
                print_move_error(half_move)
            if board[target_pos[1]][target_pos[0]] == hidden_trap_door:
                board[target_pos[1]][target_pos[0]] = mine_hidden_trap_door
            elif board[target_pos[1]][target_pos[0]] == mine_hidden_trap_door:
                board[target_pos[1]][target_pos[0]] = mine_hidden_trap_door    
            else:
                board[target_pos[1]][target_pos[0]] = mine 
        if piece == west_wall:
            halfmove_clock = 0
            if side_move == 0:
                if w_walls > 0:
                    w_walls -= 1
                else:
                    print_move_error(half_move)    
            elif side_move == 1:
                if b_walls > 0:
                    b_walls -= 1
                else:
                    print_move_error(half_move)      
            if target_pos[0] == 0:
                print_move_error(half_move)        
            board[target_pos[1]].insert(target_pos[0], west_wall)  
        if piece == south_wall:
            halfmove_clock = 0
            if side_move == 0:
                if w_walls > 0:
                    w_walls -= 1
                else:
                    print_move_error(half_move)
            elif side_move == 1:
                if b_walls > 0:
                    b_walls -= 1
                else:
                    print_move_error(half_move)       
            if target_pos[1] == 0 or target_pos[1] == 7:
                print_move_error(half_move)      
            if board[target_pos[1]][target_pos[0]] == west_wall:
                board[target_pos[1]].insert(target_pos[0]+1, south_wall) 
            else:
                board[target_pos[1]].insert(target_pos[0], south_wall)    

    if len(half_m) == 2:
        start = half_m[0]
        end = half_m[1]

        if start[0] != '0':
            start_pos = [file.index(start[0]), 8-int(start[1])]
            target_pos = [file.index(end[0]), 8-int(end[1])]
            piece = ''

            start_walls = 0
            for v in board[start_pos[1]]:
                if v == '|' or v == '_':
                    start_walls += 1
            start_pos[0] += start_walls   

            piece = board[start_pos[1]][start_pos[0]]
            board[start_pos[1]][start_pos[0]] = '.'

            # Pawn promotion
            if start_pos[1] == 1 and target_pos[1] == 0 and piece == white_pawn:
                piece = end[-1:]
                if piece != white_queen and piece != white_rook and piece != white_bishop \
                    and piece != white_knight:
                    print_move_error(half_move)
            if start_pos[1] == 6 and target_pos[1] == 7 and piece == black_pawn:
                piece = end[-1:]
                if piece != black_queen and piece != black_rook and piece != black_bishop \
                    and piece != black_knight:
                    print_move_error(half_move)                                

            wall_block = 0

            for i in range(target_pos[0]+2):
                if target_pos[0]+2 <= len(board[target_pos[1]]):
                    if board[target_pos[1]][i] == west_wall or board[target_pos[1]][i] == south_wall:
                        wall_block += 1

            captured = board[target_pos[1]][target_pos[0]+wall_block]
            target_pos = [target_pos[0] + wall_block, target_pos[1]]

            # En passant update for status
            if start_pos[1] == 6 and piece == white_pawn:
                if start_pos[1] - 2 == target_pos[1]:
                    if target_pos[0] - 1 >= 0 and target_pos[0] + 1 <= 7:
                        if board[target_pos[1]][target_pos[0]-1] == black_pawn:
                            en_passant = file[target_pos[0]] + str(7-target_pos[1])
                        if board[target_pos[1]][target_pos[0]+1] == black_pawn:
                            en_passant = file[target_pos[0]] + str(7-target_pos[1])  
            if start_pos[1] == 1 and piece == black_pawn:
                if start_pos[1] + 2 == target_pos[1]:
                    if target_pos[0] - 1 >= 0 and target_pos[0] + 1 <= 7:
                        if board[target_pos[1]][target_pos[0]-1] == white_pawn:
                            en_passant = file[target_pos[0]] + str(9-target_pos[1])
                        if board[target_pos[1]][target_pos[0]+1] == white_pawn:
                            en_passant = file[target_pos[0]] + str(9-target_pos[1]) 

            if side_move == 0:
                if captured != '.' and captured != black_rook and captured != black_knight \
                    and captured != black_bishop and captured != black_queen and captured != black_pawn:
                    if captured == mine:
                        piece = '.'
                        if 0 <= target_pos[0] < len(board[target_pos[1]]) and 0 <= target_pos[1] < 8:
                            for y in [-1, 0, 1]:
                                for x in [-1, 0, 1]:
                                    new_x = target_pos[0] + x
                                    new_y = target_pos[1] + y
                                    if 0 <= new_x < len(board[new_y]) and 0 <= new_y < 8:
                                        if y == 0:
                                            if x == -1 and board[new_y][new_x] == '_':
                                                if board[new_y][new_x-1] != '|':
                                                    board[new_y][new_x-1] = '.'                    
                                        if board[new_y][new_x] != '|' and board[new_y][new_x] != '_':
                                            if board[new_y][new_x] != '.':
                                                if board[new_y][new_x-1] != '_' and board[new_y][new_x-1] != '|':
                                                    board[new_y][new_x] = '.'
                    elif captured == mine_hidden_trap_door:
                        piece = open_trap_door
                        if 0 <= target_pos[0] < len(board[target_pos[1]]) and 0 <= target_pos[1] < 8:
                            for y in [-1, 0, 1]:
                                for x in [-1, 0, 1]:
                                    new_x = target_pos[0] + x
                                    new_y = target_pos[1] + y
                                    if 0 <= new_x < len(board[new_y]) and 0 <= new_y < 8:
                                        if board[new_y][new_x] != '|' and board[new_y][new_x] != '_':
                                            if board[new_y][new_x] != '.':
                                                if board[new_y][new_x-1] != '_' and board[new_y][new_x-1] != '|':
                                                    board[new_y][new_x] = '.'
                    elif captured == hidden_trap_door:
                        piece = open_trap_door                            
                    elif captured == open_trap_door:
                        piece = '.'    
                    else:    
                        print_move_error(half_move)
                    halfmove_clock = 0                
                else:
                    if captured != '.':
                        halfmove_clock = 0        
            if side_move == 1:
                if captured != '.' and captured != white_rook and captured != white_knight \
                    and captured != white_bishop and captured != white_queen and captured != white_pawn:
                    if captured == mine:
                        piece = '.'
                        if 0 <= target_pos[0] < len(board[target_pos[1]]) and 0 <= target_pos[1] < 8:
                            for y in [-1, 0, 1]:
                                for x in [-1, 0, 1]:
                                    new_x = target_pos[0] + x
                                    new_y = target_pos[1] + y
                                    if 0 <= new_x < len(board[new_y]) and 0 <= new_y < 8:
                                        if y == 0:
                                            if x == -1 and board[new_y][new_x] == '_':
                                                if board[new_y][new_x-1] != '|':
                                                    board[new_y][new_x-1] = '.'                    
                                        if board[new_y][new_x] != '|' and board[new_y][new_x] != '_':
                                            if board[new_y][new_x] != '.':
                                                if board[new_y][new_x-1] != '_' and board[new_y][new_x-1] != '|':
                                                    board[new_y][new_x] = '.'
                    elif captured == mine_hidden_trap_door:
                        piece = open_trap_door
                        if 0 <= target_pos[0] < len(board[target_pos[1]]) and 0 <= target_pos[1] < 8:
                            for y in [-1, 0, 1]:
                                for x in [-1, 0, 1]:
                                    new_x = target_pos[0] + x
                                    new_y = target_pos[1] + y
                                    if 0 <= new_x < len(board[new_y]) and 0 <= new_y < 8:
                                        if board[new_y][new_x] != '|' and board[new_y][new_x] != '_':
                                            if board[new_y][new_x] != '.':
                                                if board[new_y][new_x-1] != '_' and board[new_y][new_x-1] != '|':
                                                    board[new_y][new_x] = '.'
                    elif captured == hidden_trap_door:
                        piece = open_trap_door   
                    elif captured == open_trap_door:
                        piece = '.' 
                    else:    
                        print_move_error(half_move) 
                    halfmove_clock = 0       
                else:
                    if captured != '.':
                        halfmove_clock = 0  

            # Place piece
            target_pos = [target_pos[0] - wall_block, target_pos[1]]
            board[target_pos[1]][target_pos[0]+wall_block] = piece    

            # En passant
            if half_move[-2:len(half_move)] == en_passant:
                if side_move == 1:
                    if board[target_pos[1]-1][target_pos[0]+wall_block] != '.':
                        print_move_error(half_move)
                    else:
                        board[target_pos[1]-1][target_pos[0]+wall_block] = '.'
                else:
                    if board[target_pos[1]+1][target_pos[0]+wall_block] != '.':
                        print_move_error(half_move)
                    else:    
                        board[target_pos[1]+1][target_pos[0]+wall_block] = '.'  

            if piece == white_rook:
                if piece_check.white_rook_check(board, target_pos):
                    print("INFO: check", file=sys.stdout)
            if piece == black_rook:
                if piece_check.black_rook_check(board, target_pos):
                    print("INFO: check", file=sys.stdout)
            if piece == white_knight:
                if piece_check.white_knight_check(board, target_pos):
                    print("INFO: check", file=sys.stdout)  
            if piece == black_knight:
                if piece_check.black_knight_check(board, target_pos):
                    print("INFO: check", file=sys.stdout)     
            if piece == white_bishop:
                if piece_check.white_bishop_check(board, target_pos):
                    print("INFO: check", file=sys.stdout) 
            if piece == black_bishop:
                if piece_check.black_bishop_check(board, target_pos):
                    print("INFO: check", file=sys.stdout)
            if piece == white_queen:
                if piece_check.white_queen_check(board, target_pos):
                    print("INFO: check", file=sys.stdout) 
            if piece == black_queen:
                if piece_check.black_queen_check(board, target_pos):
                    print("INFO: check", file=sys.stdout)
            if piece == white_pawn:
                if piece_check.white_pawn_check(board, target_pos):
                    print("INFO: check", file=sys.stdout) 
            if piece == black_pawn:
                if piece_check.black_pawn_check(board, target_pos):
                    print("INFO: check", file=sys.stdout)                                                      

            # remove en passant from status if it was played
            if len(en_passant) > 1:
                if target_pos[1] == 8 - int(en_passant[1]) and file[target_pos[0]] == en_passant[0]:
                    en_passant = '-' 

            if piece == white_pawn or piece == black_pawn:
                halfmove_clock = 0         

        else:
            if side_move == 0: # white kingside castling
                if w_kingside != '+':
                    print_move_error(half_move)
                for i in range(4, 8):
                    if board[7][i] != '.' and board[7][i] != 'K' and board[7][i] != 'R':
                        print_move_error(half_move)
                board[7][5] = 'R'
                board[7][6] = 'K'
                board[7][4] = '.'
                board[7][7] = '.'
            if side_move == 1: # black kingside castling
                if b_kingside != '+':
                    print_move_error(half_move)
                for i in range(4, 8):
                    if board[0][i] != '.' and board[0][i] != 'k' and board[0][i] != 'r':
                        print_move_error(half_move)
                board[0][5] = 'r'
                board[0][6] = 'k'
                board[0][4] = '.'
                board[0][7] = '.'

    if len(half_m) == 3:
        if side_move == 0: # white queenside castling
                if w_queenside != '+':
                    print_move_error(half_move)
                for i in range(0, 5):
                    if board[7][i] != '.' and board[7][i] != 'K' and board[7][i] != 'R':
                        print_move_error(half_move)
                board[7][3] = 'R'
                board[7][2] = 'K'
                board[7][0] = '.'
                board[7][4] = '.'
        if side_move == 1: # black queenside castling
                if b_queenside != '+':
                    print_move_error(half_move)
                for i in range(0, 5):
                    if board[0][i] != '.' and board[0][i] != 'k' and board[0][i] != 'r':
                        print_move_error(half_move)
                board[0][3] = 'r'
                board[0][2] = 'k'
                board[0][0] = '.'
                board[0][4] = '.' 

    # Update castling status 
    if board[7][4] != white_king:
        w_kingside = w_queenside = '-'
    if board[7][0] != white_rook:
        w_queenside = '-'
    if board[7][7] != white_rook:
        w_kingside = '-'
    if board[0][4] != black_king:
        b_kingside = b_queenside = '-'                              
    if board[0][0] != black_rook:
        b_queenside = '-'
    if board[0][7] != black_rook:
        b_kingside = '-'

    # Set which color to move next
    if side_move == 0:
        next_to_move = 'b'
    if side_move == 1:
        next_to_move = 'w'                   

    new_status = next_to_move + " " + str(w_walls) + " " + str(b_walls) + " " + w_kingside \
                    + " " + w_queenside + " " + b_kingside + " " + b_queenside + " " + \
                    en_passant + " " + str(halfmove_clock)
    board[8] = new_status  

    # Stalemate
    if only_kings(board):
        print("INFO: stalemate", file=sys.stdout)

    # Draw to fifty move rule
    if halfmove_clock > 50:
        print("INFO: draw due to fifty moves", file=sys.stdout)       

def print_move_error(move):
    print("ERROR: illegal move " + move, file=sys.stderr, end="")
    quit()    

def only_kings(board):
    only_k = True

    for i in range(8):
        for j in range(len(board[i])):
            if board[i][j] != '.' and board[i][j] != '_' and board[i][j] != '|' and \
                board[i][j] != white_king and board[i][j] != black_king:    
                    only_k = False

    return only_k

def check_initial(board, half_move, side_move, halfmove_clock):
    w_k_count = w_q_count = w_r_count = w_n_count = w_b_count = w_p_count = 0 
    b_k_count = b_q_count = b_r_count = b_n_count = b_b_count = b_p_count = 0 

    status = board[8].split(" ") 

    if status[3] != '+' or status[4] != '+' or status[5] != '+' or status[6] != '+':
        print_move_error(half_move)

    if status[7] != '-':
        print_move_error(half_move)    

    if side_move != 0 and halfmove_clock != 1:
        print_move_error(half_move)

    for i in range(2, 6):
        for j in range(len(board[i])):
            if board[i][j] != '.' and board[i][j] != 'D' and board[i][j] != 'M' \
                and board[i][j] != 'X' and board[i][j] != 'O':
                print_move_error(half_move)    
            
            if board[i][j] == 'D' and int(halfmove_clock) < 2:
                print_move_error(half_move)

    for i in range(len(board[0])):
        if board[0][i] == black_king:
            b_k_count += 1
        if board[0][i] == black_queen:
            b_q_count += 1
        if board[0][i] == black_rook:
            b_r_count += 1
        if board[0][i] == black_knight:
            b_n_count += 1
        if board[0][i] == black_bishop:
            b_b_count += 1   

    if b_k_count != 1 or b_q_count != 1 or b_r_count != 2 or b_n_count != 2 or b_b_count != 2:
        print_move_error(half_move)

    for i in range(len(board[1])):
        if board[1][i] == black_pawn:
            b_p_count += 1        

    if b_p_count != 8:
        print_move_error(half_move) 

    for i in range(len(board[7])):
        if board[7][i] == white_king:
            w_k_count += 1
        if board[7][i] == white_queen:
            w_q_count += 1
        if board[7][i] == white_rook:
            w_r_count += 1
        if board[7][i] == white_knight:
            w_n_count += 1
        if board[7][i] == white_bishop:
            w_b_count += 1 

    if w_k_count != 1 or w_q_count != 1 or w_r_count != 2 or w_n_count != 2 or w_b_count != 2:
        print_move_error(half_move) 

    for i in range(len(board[6])):
        if board[6][i] == white_pawn:
            w_p_count += 1                                          

    if w_p_count != 8:
        print_move_error(half_move) 
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
empty_square = '.'

file = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

def validate(board):
    mines_count = 0
    trapdoors_count = 0
    wall_count = 0
    bk_count = wk_count = 0
    status = []
    
    if len(board) != 9:
        print_status_error()
    else:    
        status = board[8].split(" ")

    if status[0] != 'w' and status[0] != 'b':
        print_status_error()
    
    if (not status[1].isnumeric()) or (not status[2].isnumeric()): 
        print_status_error()
    
    for i in range(3, 7):
        if status[i] != '+' and status[i] != '-':
            print_status_error()
    
    if not status[8].isnumeric():
        print_status_error()        

    if not(0 <= int(status[1]) <= 3):
        print_status_error()
    if not(0 <= int(status[2]) <= 3):
        print_status_error()

    check_rank(board)

    for i in range(8):
        if board[i] == []:
            print_error(i, 0, board)
        for j in range(len(board[i])):
            check_invalid_piece(i, j, board)

            # Count kings
            if board[i][j] == white_king:
                wk_count += 1
            if board[i][j] == black_king:
                bk_count += 1    

            # Count walls
            if board[i][j] == west_wall or board[i][j] == south_wall: 
                if board[i][j] == west_wall and (j == 0 or j == len(board[i]) - 1):
                    print_error(i, j, board)
                wall_count += 1   

            # Count mines and trapdoors
            if board[i][j] == mine:
                mines_count += 1
            if board[i][j] == hidden_trap_door or board[i][j] == open_trap_door:
                trapdoors_count += 1
            if board[i][j] == mine_hidden_trap_door:
                mines_count += 1
                trapdoors_count += 1 
            
            if mines_count > 2:
                print_error(i, j, board)

            if trapdoors_count > 2:
                print_error(i, j, board)    

            if wall_count > 6 or (wall_count + int(status[1]) + int(status[2])) > 6:
                print_error(i, j, board)

            # Mines are not in rank 4 or 5
            if i != 3 and i != 4:
                if board[i][j] == mine:
                    print_error(i, j, board) 

            # Trapdoors are not in rank 3 to 6  
            if not(2 <= i <= 5):
                if board[i][j] == open_trap_door or board[i][j] == hidden_trap_door:
                    print_error(i, j, board) 

            if i == 0 or i == 7:
                if board[i][j] == white_pawn or board[i][j] == black_pawn:
                    print_error(i, j, board)

            if wk_count > 1 or bk_count > 1:
                print_error(i, j, board)

    # Missing king
    if wk_count == 0 or bk_count == 0:
        print_error(7, 7, board) 

    if 0 <= int(status[1]) + int(status[2]) <= 6:
        k = 6 - wall_count
        if k != int(status[1]) + int(status[2]):
            print_status_error()     

    pawn_validation(board)    

    return True

def pawn_validation(board): 
    white_total = 0
    black_total = 0
    w_k_count = w_q_count = w_r_count = w_n_count = w_b_count = w_p_count = 0 
    b_k_count = b_q_count = b_r_count = b_n_count = b_b_count = b_p_count = 0
    w_promotions_list = {'r': 0, 'n': 0, 'b': 0, 'q': 0}
    b_promotions_list = {'r': 0, 'n': 0, 'b': 0, 'q': 0}   

    for i in range(8):
        for j in range(len(board[i])):
            # Count all white pieces
            if board[i][j] == white_king:
                w_k_count += 1
            if board[i][j] == white_queen:
                w_q_count += 1
            if board[i][j] == white_rook:
                w_r_count += 1
            if board[i][j] == white_knight:
                w_n_count += 1 
            if board[i][j] == white_bishop:
                w_b_count += 1
            if board[i][j] == white_pawn:
                w_p_count += 1
            
            # Count all black pieces
            if board[i][j] == black_king:
                b_k_count += 1
            if board[i][j] == black_queen:
                b_q_count += 1
            if board[i][j] == black_rook:
                b_r_count += 1
            if board[i][j] == black_knight:
                b_n_count += 1
            if board[i][j] == black_bishop:
                b_b_count += 1
            if board[i][j] == black_pawn:
                b_p_count += 1         
            
            white_total = w_k_count + w_q_count + w_r_count + w_n_count + w_b_count + w_p_count
            black_total = b_k_count + b_q_count + b_r_count + b_n_count + b_b_count + b_p_count 

            # Check if either side has more than 8 pawns
            if w_p_count > 8:
                print_error(i, j, board)
            elif b_p_count > 8:
                print_error(i, j, board)   

            # Check if pawn = 8 and rooks<=2 or knights<=2 or bishops<=2 or queen<=1
            if w_p_count == 8:
                if w_r_count > 2:
                    print_error(i, j, board)  
                if w_n_count > 2:
                    print_error(i, j, board)
                if w_b_count > 2:
                    print_error(i, j, board)
                if w_q_count > 1:
                    print_error(i, j, board)  
            if b_p_count == 8:
                if b_r_count > 2:
                    print_error(i, j, board)  
                if b_n_count > 2:
                    print_error(i, j, board)
                if b_b_count > 2:
                    print_error(i, j, board)
                if b_q_count > 1:
                    print_error(i, j, board) 

            if w_q_count > 9:
                print_error(i, j, board)   
            if w_r_count > 10:
                print_error(i, j, board)
            if w_n_count > 10:
                print_error(i, j, board)
            if w_b_count > 10:
                print_error(i, j, board) 
                
            if b_q_count > 9:
                print_error(i, j, board)   
            if b_r_count > 10:
                print_error(i, j, board)
            if b_n_count > 10:
                print_error(i, j, board)
            if b_b_count > 10:
                print_error(i, j, board)

            # Extra piece(s) and missing pawns
            if board[i][j] == white_rook and w_r_count > 2:
                missing_p = 8 - w_p_count
                w_promotions_list['r'] = w_r_count - 2
                available = missing_p - (w_promotions_list['r'] + w_promotions_list['n'] \
                            + w_promotions_list['b'] + w_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board) 

            if board[i][j] == white_knight and w_n_count > 2:
                missing_p = 8 - w_p_count
                w_promotions_list['n'] = w_n_count - 2
                available = missing_p - (w_promotions_list['r'] + w_promotions_list['n'] \
                            + w_promotions_list['b'] + w_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board)         

            if board[i][j] == white_bishop and w_b_count > 2:
                missing_p  = 8 - w_p_count
                w_promotions_list['b'] = w_b_count - 2
                available = missing_p - (w_promotions_list['r'] + w_promotions_list['n'] \
                            + w_promotions_list['b'] + w_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board)   

            if board[i][j] == white_queen and w_q_count > 1:
                missing_p = 8 - w_p_count
                w_promotions_list['q'] = w_q_count - 1
                available = missing_p - (w_promotions_list['r'] + w_promotions_list['n'] \
                            + w_promotions_list['b'] + w_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board)

            if board[i][j] == black_rook and b_r_count > 2:
                missing_p = 8 - b_p_count
                b_promotions_list['r'] = b_r_count - 2
                available = missing_p - (b_promotions_list['r'] + b_promotions_list['n'] \
                            + b_promotions_list['b'] + b_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board) 

            if board[i][j] == black_knight and b_n_count > 2:
                missing_p = 8 - b_p_count
                b_promotions_list['n'] = b_n_count - 2
                available = missing_p - (b_promotions_list['r'] + b_promotions_list['n'] \
                            + b_promotions_list['b'] + b_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board)         

            if board[i][j] == black_bishop and b_b_count > 2:
                missing_p = 8 - b_p_count
                b_promotions_list['b'] = b_b_count - 2
                available = missing_p - (b_promotions_list['r'] + b_promotions_list['n'] \
                            + b_promotions_list['b'] + b_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board)   

            if board[i][j] == black_queen and b_q_count > 1:
                missing_p = 8 - b_p_count
                b_promotions_list['q'] = b_q_count - 2
                available = missing_p - (b_promotions_list['r'] + b_promotions_list['n'] \
                            + b_promotions_list['b'] + b_promotions_list['q']) 
                
                if available < 0:
                    print_error(i, j, board)              

            if white_total > 16:
                print_error(i, j, board)
            elif black_total > 16:
                print_error(i, j, board)  

    return True           

def count_pawns(board):
    white_pawns = 0
    black_pawns = 0
    
    for i in range(8):
        for j in range(len(board[i])):
            if board[i][j] == white_pawn:
                white_pawns += 1
            if board[i][j] == black_pawn:
                black_pawns += 1

    return [white_pawns, black_pawns]

def check_rank(board):
    for i in range(8):
        count = 0
        for j in range(len(board[i])):
            if board[i][j] != '|' and board[i][j] != '_':
                count += 1
    if count != 8:
        print_error(i, j, board)  

def check_invalid_piece(i, j, board):
    if board[i][j] != white_king and board[i][j] != white_queen and board[i][j] != white_rook\
        and board[i][j] != white_bishop and board[i][j] != white_knight and board[i][j] != white_pawn\
        and board[i][j] != black_king and board[i][j] != black_queen and board[i][j] != black_rook\
        and board[i][j] != black_bishop and board[i][j] != black_knight and board[i][j] != black_pawn\
        and board[i][j] != hidden_trap_door and board[i][j] != open_trap_door and \
        board[i][j] != mine and board[i][j] != mine_hidden_trap_door and board[i][j] != west_wall \
        and board[i][j] != south_wall and board[i][j] != empty_square:
            print_error(i, j, board)

def print_error(i, j, board):
    f_correct = 0

    for p in range(0, j):
        if p < len(board[i]):
            if board[i][p] == '_' or board[i][p] == '|':
                f_correct += 1

    if f_correct > 0:
        j = j - f_correct

    i = 8 - i

    print("ERROR: illegal board at " + file[7 if j > 7 else j] + str(i), file=sys.stderr, end="")
    quit()

def print_status_error():
    print("ERROR: illegal board at status line", file=sys.stderr, end="")
    quit()
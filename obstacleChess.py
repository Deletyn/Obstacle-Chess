import sys
import move_piece
import validate

def main():
    board = read_board()

    if len(board) == 0: # Check for the correct number of arguments
        print("ERROR: incorrect number of arguments", file=sys.stderr)
        quit()
    else:
        if len(sys.argv) == 3: # Run only board validation if 2 arguments are provided
            is_valid = validate.validate(board)

            if is_valid:
                try:
                    outboard_filename = sys.argv[2]
                    write_board(board, outboard_filename)
                except:
                    print("ERROR: outboard file not found", file=sys.stderr)
                    quit()
            else:
                quit()
        else: # Play moves if there is more than 2 arguments provided
            moves = read_moves()

            is_valid = validate.validate(board)
            side_move = to_move(board)

            for move in moves:
                # Which side to move, 0 = White and 1 = Black
                if move == '...': 
                    side_move = 1 if side_move == 0 else 0
                    continue

                move_piece.move(move, board, side_move)
                is_valid = validate.validate(board)
                side_move = 1 if side_move == 0 else 0

            if is_valid:
                try:
                    outboard_filename = sys.argv[2]
                    write_board(board, outboard_filename)
                except:
                    print("ERROR: outboard file not found", file=sys.stderr)
                    quit()
            else:
                quit()

def read_board():
    board = []
    
    try:
        board_filename = sys.argv[1]
        board_file = open(board_filename, "r")
        lines = board_file.readlines()
        
        i = 0
        for line in lines:
            if not ("%" in line): # Skip lines that start with %
                if (i < 8):
                    board.append(list(line)[0:-1])
                else:
                    if line[-1] == '\n':
                        board.append(line[0:-1])
                    else:    
                        board.append(line)    
                i = i + 1

        board_file.close()

        return board
    except:
        return board

def read_moves():
    moves = []

    try:
        ingame_filename = sys.argv[3]
        ingame_file = open(ingame_filename, "r")
        lines = ingame_file.readlines()
        
        i = 0
        for line in lines:
            if line[0] != "%": # Skip lines that start with %
                if line[-1] == '\n':
                    moves.append(line[0:-1])
                else:    
                    moves.append(line)  

        ingame_file.close()

        return moves
    except:
        # Return empty moves if there is an exception
        return moves

def to_move(board):
    status = board[8].split(" ")
    return 0 if status[0] == 'w' else 1

def write_board(board, filename):
    with open(filename, "w") as outboard_file:
        for i in range(9):
            if i == 8:
                outboard_file.write(''.join(board[i]))
            else:
                outboard_file.write(''.join(board[i]) + '\n')

if __name__ == "__main__":
    main() 
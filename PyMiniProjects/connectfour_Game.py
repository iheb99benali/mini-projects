import copy


def create_board():
    board = []
    width = 7
    for i in range(width-1):
        j = 1
        board.append([' '])
        while j < width-1:
            board[i].append(" ")
            j+=1

        board[i].append(" ")
    return board

def create_visual_board(vboard):
    for i in vboard:
        j = 0
        while j <= len(vboard[0]):
            i.insert(j,"|")
            j+=2

    return  vboard

def add_char(pos,board,char="X",rep=False):
    if rep:
        pos = int(input(f"input a position for {char}: "))

    for i in range(len(board)):
        if pos > len(board[0]) or pos < 1:
            print("\n**out of bound!\nTry again**")
            add_char(pos, board, char,True)
            break
        elif board[0][pos-1]!= " ":
            print("\n**no more space here!**")
            add_char(pos, board, char,True)
            break
        elif board[i][pos-1] == board[-1]:
            continue
        elif board[i][pos-1] == " " and i == len(board)-1:
            board[i][pos-1] = f"{char}"
            break
        elif board[i][pos-1] != " ":
            board[i-1][pos-1]=f"{char}"
            break
    return board

def detect_four_diagonal(board):
    rows = len(board)
    cols = len(board[0])
    for i in range(3,rows):
        for j in range(cols-3):
            char = board[i][j]
            if ((char != " " or not char)
                    and board[i -1][j+1] == char
                    and board[i-2][j+2] == char
                    and board[i-3][j+3] == char

            ):
                return char

    for i in range(rows-3):
        for j in range(cols-3):
            char = board[i][j]
            if ((char != " " or not char)
                    and board[i+1][j+1] == char
                    and board[i+2][j+2] == char
                    and board[i+3][j+3] == char

            ):
                return char

    return None


def detect_four(board):
    rows = len(board)
    cols = len(board[0])
    current = ""
    count = 0

    diagonal_char = detect_four_diagonal(board)

    if diagonal_char:
        return f"**CONNECT FOUR**\n congrats {diagonal_char}"

    for i in range(cols):
        for j in range(rows):
            char = board[j][i]
            if  char== " " or not char:
                continue
            elif char == current:
                count += 1
                if count == 4:
                    return f"**CONNECT FOUR**\n congrats {current}"
            elif char != current:
                current = char
                count = 1
        count = 0

    for i in range(rows):
        for j in range(cols):
            char = board[i][j]
            if  char== " ":
                count = 0
                continue
            elif char == current:
                count += 1
                if count == 4:
                    return f"**CONNECT FOUR**\n congrats {current}"
            elif char != current:
                current = char
                count = 1
        count = 0


    return None




def main(rep = False):
    board = create_board()
    game = True
    char = "X"
    while game:
        visual_board = create_visual_board(copy.deepcopy(board))
        ended = detect_four(board)
        if ended:
            for i in visual_board:
                print("".join(i))
            print(ended)
            break

        for i in visual_board: #print view board
            print("".join(i))

        while True:
            try:
                pos = int(input(f"input a position for {char}: "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")

        board = add_char(pos, board, char)


        if char == "X":
            char = "O"
        else:
            char = "X"




if __name__ == '__main__':
    main()

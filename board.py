# Colors
_WHITE = "W"
_BLACK = "B"

# Pieces
_KING = "k",
_QUEEN = "q"
_KNIGHT = "n"
_ROOK = "r"
_BISHOP = "b"
_PAWN = ""

# Syntax
_TAKES = "x"

# helper functions
def clamp(n, lo, hi):
    return max(lo, min(n, hi))

class Board:
    def __init__(self, board_str):
        self.board = [board_str.split(",")[i:i+8] for i in range(8)]

    @staticmethod
    def notation_to_coords(space_notation):
        return "87654321".index(space_notation[1]), "abcdefgh".index(space_notation[0])

    @staticmethod
    def coords_to_notation(coords):
        return "".join(("abcdefgh"[coords[1]], "87654321"[coords[0]]))

    def in_check(self, who, board=self.board):
        # First, get the coords of the king.
        king_coords = None
        for i in range(8):
            for j in range(8):
                if board[i][j] == who + "k"
                    king_coords = (i, j)

        if not king_coords:
            print(f"Cound not find {who}k in board")
            return False

        for i in range(8):
            for j in range(8):
                whose, piece = board[i][j]
                if whose != who and king_coords in self.valid_next_spaces(whose, piece, (i, j)):
                    return True
        else:
            return False


    def valid_next_spaces(self, who, piece, coords):
        row, col = coords

        res = []

        # TODO need to handle the fact that pieces...block you.
        match piece:
            case _KING:
                # Cardinals and diags
                res = [
                    (row - 1, col - 1),
                    (row + 1, col + 1),
                    (row - 1, col + 1),
                    (row + 1, col - 1),
                    (row - 1, col),
                    (row + 1, col),
                    (row, col - 1), 
                    (row, col + 1),    
                ]

            case _QUEEN:
                res = []
                flags = [True, True, True, True, True, True, True, True]
                for i in range(8):
                    if flags[0]:
                        res.append((row - i, col - i))
                    if self.board[row - i][col - i] != "x":
                        flags[0] = False

                    if flags[1]:
                        res.append((row + i, col + i))
                    if self.board[row + i][col + i] != "x":
                        flags[1] = False

                    if flags[2]:
                        res.append((row - i, col + i))
                    if self.board[row - i][col + i] != "x":
                        flags[2] = False

                    if flags[3]:
                        res.append((row + i, col - i))
                    if self.board[row + i][col - i] != "x":
                        flags[3] = False

                    if flags[4]:
                        res.append((row + i, col))
                    if self.board[row + i][col] != "x":
                        flags[4] = False

                    if flags[5]:
                        res.append((row - i, col))
                    if self.board[row - i][col] != "x":
                        flags[5] = False

                    if flags[6]:
                        res.append((row, col + i))
                    if self.board[row][col + i] != "x":
                        flags[6] = False

                    if flags[7]:
                        res.append((row, col - i))
                    if self.board[row][col - i] != "x":
                        flags[7] = False

            case _KNIGHT:
                res = [
                    (row - 2, col - 1),
                    (row - 2, col + 1),
                    (row + 2, col - 1),
                    (row + 2, col + 1),
                    (row - 1, col - 2),
                    (row + 1, col - 2),
                    (row - 1, col + 2), 
                    (row + 1, col + 2),    
                ]

            case _BISHOP:
                res = []
                flags = [True, True, True, True]
                for i in range(8):
                    if flags[0]:
                        res.append((row + i, col + i))
                    if self.board[row + i][col + i] != "x":
                        flags[0] = False

                    if flags[1]:
                        res.append((row + i, col - i))
                    if self.board[row + i][col - i] != "x":
                        flags[1] = False
                    
                    if flags[2]:
                        res.append((row - i, col - i))
                    if self.board[row - i][col - i] != "x":
                        flags[2] = False

                    if flags[3]:
                        res.append((row - i, col + i))
                    if self.board[row - i][col + i] != "x":
                        flags[3] = False

            case _ROOK:
                res = []

                flags = [True, True, True, True]
                for i in range(8):
                    if flags[0]:
                        res.append((row - i, col))
                    if self.board[row - i][col] != "x":
                        flags[0] = False

                    if flags[1]:
                        res.append((row + i, col))
                    if self.board[row + i][col] != "x":
                        flags[1] = False

                    if flags[2]:
                        res.append((row, col + i))
                    if self.board[row][col + i] != "x":
                        flags[2] = False

                    if flags[3]:
                        res.append((row, col - i))
                    if self.board[row][col - i] != "x":
                        flags[3] = False

            case _PAWN:
                # Lots of cases to handle here.
                res = []

                # Check forward.
                row_direction = 1 if who == _BLACK else -1

                if self.board[row + row_direction][col] == "x":
                    res.append((row + row_direction, col))

                # Pawn start condition, allow 2 moves
                if (who == _WHITE and coords_to_notation(coords)[1] == "2") or (who == _BLACK and coords_to_notation(coords)[1] == "7"):
                    res.append((row + 2 * row_direction, col))

                # Attacking
                if self.board[row + row_direction][col - 1] !== "x":
                    res.append((row + row_direction, col - 1))
                if self.board[row + row_direction][col + 1] !== "x":
                    res.append((row + row_direction, col + 1))

                # TODO I'll deal with en passant later.
                # TODO I'll also deal with promoting later.

            case _:
                print("idk lol")

        return filter(lambda x: 0 <= x[0] < 8 and 0 <= x[1] < 8, res)

    def move(self, who, move_str):
        # First, convert the move string to a valid piece and coordinate.

        # Move str: <space_notation> to <space_notation>
        # TODO eventually make this accept chess notation

        

import ruamel.yaml
import numpy as np


class Chess(object):
    """Chess"""

    def __init__(self):
        super(Chess, self).__init__()
        self.yaml = ruamel.yaml.YAML()
        self.build_board()

    def build_board(self):
        data = self.yaml.load(open(r'data/key.yml', 'r'))
        self.piece_key = data['pieces']
        self.value_key = data['values']

        self.board = []
        for i in range(8):
            self.board.append([self.piece_key["unoccupied"] for j in range(8)])

        self.populate_board()

    def populate_board(self):
        # row 0 is white, row len(self.board)-1 is black
        # 0 is white 1 is black

        start_id = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        start_white = [Square(self, 0, self.piece_key[i], i) for i in start_id]
        pawn_white = [Square(self, 0, self.piece_key["pawn"], "pawn") for i in range(8)]
        start_black = [Square(self, 1, self.piece_key[i], i) for i in start_id]
        pawn_black = [Square(self, 1, self.piece_key["pawn"], "pawn") for i in range(8)]

        self.board[0] = start_white
        self.board[1] = pawn_white

        for i in range(2, len(self.board) - 2):
            self.board[i] = [Square(self, -1, self.piece_key["unoccupied"], "unoccupied") for j in range(8)]

        self.board[len(self.board) - 1] = start_black
        self.board[len(self.board) - 2] = pawn_black

    def reset(self):
        self.build_board()

    def checkmate(self, color):     # is this color checkmated
        for move in self.possible_moves(color):
            board = self.step(move)

            can_kill_king = False
            for opp_move in self.possible_moves((color + 1) % 2, board):
                new_board = self.step(opp_move, board)
                king_present = False  # Is color's king still on the board

                for r in range(len(new_board)):
                    for c in range(len(new_board[r])):
                        if new_board[r][c].index == 6 and new_board[r][c].color == color:
                            king_present = True

                if not king_present:     # We found a move that if color makes it opponent can take king
                    can_kill_king = True
                    break

            if not can_kill_king:
                return False
        return True

    def possible_moves(self, color, board=None):
        if board is None:
            board = self.board

        moves = []

        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c].color == color:
                    moves += self.moves_at_pos(r, c, board)

        return moves

    def moves_at_pos(self, r, c, board=None):

        if board is None:
            board = self.board

        p = board[r][c]

        use = {
            0: lambda x, y, z: [],
            1: self.pawn_possible_moves,
            2: self.rook_possible_moves,
            3: self.bishop_possible_moves,
            4: self.knight_possible_moves,
            5: lambda x, y, z: self.rook_possible_moves(x, y, z) + self.bishop_possible_moves(x, y, z),
            6: self.king_possible_moves
        }

        return use[p.index](r, c, board)

    def real_step(self, action):
        """Actually take a move in the game"""
        if action.type == 0:
            a_init = action.new[0]
            a_final = action.new[1]

            if action in self.moves_at_pos(a_init[0], a_init[1]):
                self.board[a_final[0]][a_final[1]] = self.board[a_init[0]][a_init[1]]
                self.board[a_init[0]][a_init[1]] = Square(self, -1, self.piece_key["unoccupied"], "unoccupied")
            else:
                return False
        return True

    def step(self, action, board=None):
        """For planning purposes; what would the board look like if this move happened"""

        if board is None:
            board = self.board

        # Make a copy of board
        new_board = []
        for row in board:
            new_board.append([Square(self, s.color, s.index, s.name) for s in row])

        if action.type == 0:
            a_init = action.new[0]
            a_final = action.new[1]
            new_board[a_final[0]][a_final[1]] = new_board[a_init[0]][a_init[1]]
            new_board[a_init[0]][a_init[1]] = Square(self, -1, self.piece_key["unoccupied"], "unoccupied")

        return new_board

    def evaluate(self, my_col, board=None):
        """Simple evaluation of board that returns sum of your pts - sum of opponents"""

        if board is None:
            board = self.board

        total = 0

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j].color == 1:
                    total += self.value_key[board[i][j].name]
                else:
                    total -= self.value_key[board[i][j].name]

        if my_col == 1:
            return total
        return -1*total

    def king_possible_moves(self, r, c, board):
        p = board[r][c]
        moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (([i, j] != [0, 0]) and (0 <= r + i < len(board)) and (0 <= c + j < len(board[0]))
                        and (board[r + i][c + j].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + i, c + j]]))

        return moves

    def knight_possible_moves(self, r, c, board):
        p = board[r][c]
        moves = []

        for i in range(-2, 3):
            for j in [-3 + abs(i), 3 - abs(i)]:
                if ((i != 0 and j != 0) and (0 <= r + i < len(board)) and (0 <= c + j < len(board[0]))
                        and (board[r + i][c + j].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + i, c + j]]))

        return moves

    def bishop_possible_moves(self, r, c, board):
        p = board[r][c]
        moves = []

        if p.color == 0:
            complement = 1
        else:
            complement = 0

        offset = 1
        rpcp = False
        rpcm = False
        rmcp = False
        rmcm = False

        while True:
            if not rpcp:
                if (r + offset < len(board) and (c + offset) < len(board[0])
                        and (board[r + offset][c + offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + offset, c + offset]]))
                    if board[r + offset][c + offset].color == complement:
                        rpcp = True
                else:
                    rpcp = True
            if not rpcm:
                if (r + offset < len(board) and (c - offset) >= 0
                        and (board[r + offset][c - offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + offset, c - offset]]))
                    if board[r + offset][c - offset].color == complement:
                        rpcm = True
                else:
                    rpcm = True
            if not rmcp:
                if (r - offset >= 0 and (c + offset) < len(board[0])
                        and (board[r - offset][c + offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r - offset, c + offset]]))
                    if board[r - offset][c + offset].color == complement:
                        rmcp = True
                else:
                    rmcp = True
            if not rmcm:
                if (r - offset >= 0 and (c - offset) >= 0
                        and (board[r - offset][c - offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r - offset, c - offset]]))
                    if board[r - offset][c - offset].color == complement:
                        rmcm = True
                else:
                    rmcm = True
            if rpcp and rpcm and rmcp and rmcm:
                break
            else:
                offset += 1

        return moves

    def rook_possible_moves(self, r, c, board):
        p = board[r][c]
        moves = []

        if p.color == 0:
            complement = 1
        else:
            complement = 0

        for i in range(c + 1, 8):
            if board[r][i].color != p.color:
                moves.append(Action(0, [[r, c], [r, i]]))
                if board[r][i].color == complement:
                    break
            else:
                break

        for i in range(c - 1, -1, -1):
            if board[r][i].color != p.color:
                moves.append(Action(0, [[r, c], [r, i]]))
                if board[r][i].color == complement:
                    break
            else:
                break

        for i in range(r + 1, 8):
            if board[i][c].color != p.color:
                moves.append(Action(0, [[r, c], [i, c]]))
                if board[i][c].color == complement:
                    break
            else:
                break

        for i in range(r - 1, -1, -1):
            if board[i][c].color != p.color:
                moves.append(Action(0, [[r, c], [i, c]]))
                if board[i][c].color == complement:
                    break
            else:
                break

        return moves

    def pawn_possible_moves(self, r, c, board):
        p = board[r][c]
        moves = []

        if p.color == 0:
            complement = 1
        else:
            complement = 0

        i = 1
        if p.color == 0:
            if (r == 1) and (board[r + 1][c].index == 0) and (board[r + 2][c].index == 0):
                moves.append(Action(0, [[r, c], [r + 2, c]]))
        elif p.color == 1:
            i = -1
            if (r == len(board) - 2) and (board[r - 1][c].index == 0) and (board[r - 2][c].index == 0):
                moves.append(Action(0, [[r, c], [r - 2, c]]))

        if (0 <= r + i < len(board)) and (board[r + i][c].index == 0):
            moves.append(Action(0, [[r, c], [r + i, c]]))

        for j in [-1, 1]:
            if (0 <= r + i < len(board)) and (0 <= c + j < len(board[0])) and (board[r + i][c + j].color == complement):
                moves.append(Action(0, [[r, c], [r + i, c + j]]))

        return moves

    def print_board(self):
        print(np.array(self.board))

    def to_array(self):
        arr = [[self.board[i][j].__repr__() for j in range(8)] for i in range(8)]
        return arr


class Action(object):
    """Action."""

    def __init__(self, type, new):
        super(Action, self).__init__()
        self.type = type  # 0 is movement, 1 is switch
        self.new = new  # if movement, a list of coords [[xi, yi], [xf, yf]]; if switch, new Square

    def __str__(self):
        if self.type == 0:
            return "go_to(" + str(self.new) + ")"
        return "change_to(" + str(self.new) + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, obj):
        return isinstance(obj, Action) and str(obj) == str(self)


class Square(object):
    """Piece."""

    def __init__(self, game, color, index, name):
        super(Square, self).__init__()
        self.game = game
        self.color = color
        self.index = index
        self.name = name

    def alternate_string_rep(self):
        return "\"" + self.__repr__() + "\""

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.color) + " " + str(self.name)

    def __eq__(self, obj):
        return isinstance(obj, Square) and obj.__repr__() == self.__repr__()


def main():
    game = Chess()
    game.print_board()
    game.real_step(game.moves_at_pos(0, 1)[0])
    print()
    game.print_board()


if __name__ == '__main__':
    main()

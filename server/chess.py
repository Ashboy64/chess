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

    def possible_moves(self, r, c):
        p = self.board[r][c]

        use = {
            0: lambda x, y: [],
            1: self.pawn_possible_moves,
            2: self.rook_possible_moves,
            3: self.bishop_possible_moves,
            4: self.knight_possible_moves,
            5: lambda x, y: self.rook_possible_moves(x, y) + self.bishop_possible_moves(x, y),
            6: self.king_possible_moves
        }

        return use[p.index](r, c)

    def real_step(self, action):
        """Actually take a move in the game"""
        if action.type == 0:
            a_init = action.new[0]
            a_final = action.new[1]

            if action in self.possible_moves(a_init[0], a_init[1]):
                self.board[a_final[0]][a_final[1]] = self.board[a_init[0]][a_init[1]]
                self.board[a_init[0]][a_init[1]] = Square(self, -1, self.piece_key["unoccupied"], "unoccupied")
        return self.board

    def step(self, action):
        """For planning purposes; what would the board look like if this move happened"""
        board = self.board.copy()
        if action.type == 0:
            a_init = action.new[0]
            a_final = action.new[1]
            board[a_final[0]][a_final[1]] = board[a_init[0]][a_init[1]]
            board[a_init[0]][a_init[1]] = Square(self, -1, self.piece_key["unoccupied"], "unoccupied")
        return board

    def evaluate(self, my_col):
        """Simple evaluation of board that returns sum of your pts - sum of opponents"""
        total = 0

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].color == 1:
                    total += self.value_key[self.board[i][j].name]
                else:
                    total -= self.value_key[self.board[i][j].name]

        if my_col == 1:
            return total
        return -1*total

    def king_possible_moves(self, r, c):
        p = self.board[r][c]
        moves = []

        for i in range(-1, 1):
            for j in range(-1, 1):
                if ((i != 0 or j != 0) and (0 <= r + i < len(self.board)) and (0 <= c + j < len(self.board[0]))
                        and (self.board[r + i][c + j].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + i, c + j]]))

        return moves

    def knight_possible_moves(self, r, c):
        p = self.board[r][c]
        moves = []

        for i in range(-2, 3):
            for j in [-3 + abs(i), 3 - abs(i)]:
                if ((i != 0 and j != 0) and (0 <= r + i < len(self.board)) and (0 <= c + j < len(self.board[0]))
                        and (self.board[r + i][c + j].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + i, c + j]]))

        return moves

    def bishop_possible_moves(self, r, c):
        p = self.board[r][c]
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
                if (r + offset < len(self.board) and (c + offset) < len(self.board[0])
                        and (self.board[r + offset][c + offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + offset, c + offset]]))
                    if self.board[r + offset][c + offset].color == complement:
                        rpcp = True
                else:
                    rpcp = True
            if not rpcm:
                if (r + offset < len(self.board) and (c - offset) >= 0
                        and (self.board[r + offset][c - offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r + offset, c - offset]]))
                    if self.board[r + offset][c - offset].color == complement:
                        rpcm = True
                else:
                    rpcm = True
            if not rmcp:
                if (r - offset >= 0 and (c + offset) < len(self.board[0])
                        and (self.board[r - offset][c + offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r - offset, c + offset]]))
                    if self.board[r - offset][c + offset].color == complement:
                        rmcp = True
                else:
                    rmcp = True
            if not rmcm:
                if (r - offset >= 0 and (c - offset) >= 0
                        and (self.board[r - offset][c - offset].color != p.color)):
                    moves.append(Action(0, [[r, c], [r - offset, c - offset]]))
                    if self.board[r - offset][c - offset].color == complement:
                        rmcm = True
                else:
                    rmcm = True
            if rpcp and rpcm and rmcp and rmcm:
                break
            else:
                offset += 1

        return moves

    def rook_possible_moves(self, r, c):
        p = self.board[r][c]
        moves = []

        if p.color == 0:
            complement = 1
        else:
            complement = 0

        for i in range(c + 1, 8):
            if self.board[r][i].color != p.color:
                moves.append(Action([r, c], [r, i]))
                if self.board[r][i].color == complement:
                    break
            else:
                break

        for i in range(c - 1, -1, -1):
            if self.board[r][i].color != p.color:
                moves.append(Action([r, c], [r, i]))
                if self.board[r][i].color == complement:
                    break
            else:
                break

        for i in range(r + 1, 8):
            if self.board[i][c].color != p.color:
                moves.append(Action([r, c], [i, c]))
                if self.board[i][c].color == complement:
                    break
            else:
                break

        for i in range(r - 1, -1, -1):
            if self.board[i][c].color != p.color:
                moves.append(Action([r, c], [i, c]))
                if self.board[i][c].color == complement:
                    break
            else:
                break

        return moves

    def pawn_possible_moves(self, r, c):
        p = self.board[r][c]
        moves = []

        if p.color == 0:
            complement = 1
        else:
            complement = 0

        if p.color == 0:
            i = 1
            if (r == 1) and (self.board[r + 2][c].index == 0):
                moves.append(Action(0, [[r, c], [r + 2, c]]))

        elif p.color == 1:
            i = -1
            if (r == len(self.board) - 2) and (self.board[r - 2][c].index == 0):
                moves.append(Action(0, [[r, c], [r - 2, c]]))

        for j in [-1, 0, 1]:
            if (i != 0) or (j != 0):
                p2 = self.board[r + i][c + j]
                if p2.color == complement:
                    moves.append(Action(0, [[r, c], [r + i, c + j]]))

        if self.board[r + i][c].index == 0:
            moves.append(Action(0, [[r, c], [r + i, c]]))

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


def main():
    game = Chess()
    game.print_board()
    game.real_step(game.possible_moves(0, 1)[0])
    print()
    game.print_board()


if __name__ == '__main__':
    main()
from Helpers import debug


def on_grid(number):
    return 0 <= number <= 7


class Token:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.direction = -1 if symbol == 'x' else 1
        self.king = False
        self.in_killing_spree = False

    def get_legal_moves_from(self, x, y):
        moves = list()
        moves.append((-1, (-1) * self.direction))
        moves.append((1, (-1) * self.direction))

        if self.king:
            moves.append((-1, 1 * self.direction))
            moves.append((1, 1 * self.direction))

        legal_moves = list()

        for x_move, y_move in moves:
            if on_grid(x + x_move) and on_grid(y + y_move):
                legal_moves.append((x + x_move, y + y_move))

        return legal_moves

    def get_legal_moves(self):
        # return the landing spots without checking if they can actually be done or not
        return self.get_legal_moves_from(self.x, self.y)

    def get_legal_regular_moves(self, board):
        possible_moves = list()

        for x, y in self.get_legal_moves():
            if board[x][y] == ' ':
                possible_moves.append((x, y))

        return possible_moves

    def get_legal_kills(self, board):
        # return the landing spots without checking if they can actually be done or not
        possible_kill = list()

        for x, y in self.get_legal_moves():
            if not board[x][y] == ' ' and not board[x][y].lower() == self.symbol.lower():
                possible_kill.append((x, y))

        kills = list()

        for (x_kill, y_kill) in possible_kill:
            for (x, y) in self.get_legal_moves_from(x_kill, y_kill):
                if board[x][y] == ' ':
                    if x + self.x == x_kill * 2 and y + self.y == y_kill * 2:
                        kills.append((x, y))

        return kills

    def get_possible_moves(self, board, allow_only_kills):
        kills = self.get_legal_kills(board)

        if len(kills) > 0 or allow_only_kills:
            # debug(f'Token[{(self.x,self.y)}]')
            if len(kills) > 0:
                self.in_killing_spree = True
            return kills
        self.in_killing_spree = False
        # debug(f'Token[{(self.x,self.y)}]')
        return self.get_legal_regular_moves(board)

    def stop_killing_spree(self):
        self.in_killing_spree = False

    def move_token(self, x, y):
        self.x = x
        self.y = y

        if self.direction == -1 and y == 7:
            self.king = True
            self.symbol = self.symbol.capitalize()
        elif self.direction == 1 and y == 0:
            self.king = True
            self.symbol = self.symbol.capitalize()

    def is_king(self):
        return self.symbol == self.symbol.capitalize()
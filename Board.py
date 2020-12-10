from Player import Player
from Helpers import debug


class Board:
    def __init__(self, level_player_1: int = 0, level_player_2: int = 0):
        debug('Create Board')
        self.player1 = Player(0, 0, 'x', level_player_1)
        self.player2 = Player(5, 1, 'o', level_player_2)
        rows, cols = (8, 8)
        self.board = [[' ' for i in range(rows)] for j in range(cols)]
        self.turn = 0
        self.winner = None
        self.update_board()
        self.next_move = (-1, -1)
        self.player_moved = False

    def game_over(self):

        if len(self.player1.possible_moves(self.board)[0]) == 0:
            self.winner = self.player2
            return True

        if len(self.player2.possible_moves(self.board)[0]) == 0:
            self.winner = self.player1
            return True

        return False

    def next_turn(self):
        playing_player = self.player1 if self.turn % 2 == 0 else self.player2
        opponent = self.player1 if not self.turn % 2 == 0 else self.player2

        dead_token = playing_player.play(self.board, opponent)

        self.clear(opponent, dead_token)

        # if playing_player.turn_finished:
        #     self.turn += 1
        debug(f'dead: {dead_token}')
        if dead_token == (-1, -1):
            self.turn += 1
        self.update_board()

    def verify_move(self, next_move):
        if next_move == (-1, -1):
            return False

        playing_player = self.player1 if self.turn % 2 == 0 else self.player2

        return playing_player.verify_move(self.board, next_move)

    def set_next_move(self, next_move):
        self.next_move = next_move

    def get_playing_player(self):
        return self.player1 if self.turn % 2 == 0 else self.player2

    def clear(self, opponent, dead_token):
        rows, cols = (8, 8)
        self.board = [[' ' for i in range(rows)] for j in range(cols)]
        opponent.kill_token(dead_token)

    def update_board(self):
        rows, cols = (8, 8)
        self.board = [[' ' for i in range(rows)] for j in range(cols)]

        for token in self.player1.tokens + self.player2.tokens:
            self.board[token.x][token.y] = token.symbol

        print('\n\n\n\n\n\n')

        for x in self.board:
            print(x)

    def get_all_tokens(self):
        return self.player1.tokens + self.player2.tokens

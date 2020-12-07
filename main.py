from Board import Board
from collections import defaultdict


def game_loop():
    wins = defaultdict(lambda: 0)

    for i in range(100):
        board = Board()

        while not board.game_over():
            board.next_turn()

        if board.winner:
            print(f'{board.winner.symbol} Won!')
            wins[board.winner.symbol] += 1
        else:
            wins['-'] += 1

    # board = Board()
    #
    # print(board.player1.possible_moves(board.board)[0])

    print(wins)

    if wins['x'] > wins['o']:
        print('X won overall')
    else:
        print('O won overall')


if __name__ == '__main__':
    game_loop()


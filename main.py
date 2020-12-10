from Board import Board
from collections import defaultdict
import pygame
import pygame.gfxdraw
from pygame_test import UIToken

TILE_SIZE = 60
TOKEN_SIZE = 50

def game_loop():
    wins = defaultdict(lambda: 0)

    for i in range(100):
        board = Board(1, 2)

        while not board.game_over():
            board.next_turn()

        if board.winner:
            print(f'{board.winner.symbol} Won!')
            wins[board.winner.symbol] += 1
        else:
            wins['-'] += 1

    board = Board(1, 2)

    print(board.player1.possible_moves(board.board)[0])

    print(wins)

    if wins['x'] > wins['o']:
        print('X won overall')
    else:
        print('O won overall')


def intro_screen():
    pygame.init()
    screen = pygame.display.set_mode((8 * TILE_SIZE, 8 * TILE_SIZE))

    pygame.display.set_caption('Checkers')

    running = True

    board = Board()

    token_list = pygame.sprite.Group()
    token_last_moved = None

    while running:
        screen.fill((0, 0, 0))

        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, (76, 63, 119), (TILE_SIZE * i, TILE_SIZE * j, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, (164, 188, 188), (TILE_SIZE * i, TILE_SIZE * j, TILE_SIZE, TILE_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()

                if event.button == pygame.BUTTON_RIGHT:
                    x = int(x / TILE_SIZE)
                    y = int(y / TILE_SIZE)

                    token_list.add(UIToken(x, y, 'purpleToken.png'))
                if event.button == pygame.BUTTON_LEFT:
                    x = int(x / TILE_SIZE)
                    y = int(y / TILE_SIZE)

                    token_list.add(UIToken(x, y, 'blackToken.png'))
                elif event.button == pygame.BUTTON_MIDDLE:
                    for key in token_list:
                        if key.rect.collidepoint((x, y)):
                            print('asdf')
                            key.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                for key in token_list:
                    key.clicked = False
                if token_last_moved:
                    token_last_moved.locate_token()

        for key in token_list:
            if key.clicked:
                (x, y) = pygame.mouse.get_pos()
                key.move_token(x, y)
                token_last_moved = key

        token_list.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    intro_screen()


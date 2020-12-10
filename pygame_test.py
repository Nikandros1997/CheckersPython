import pygame
from enum import Enum
from pygame.sprite import RenderUpdates
import time
from UI import UIToken, UIElement, TILE_SIZE, TOKEN_SIZE
from Board import Board

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME_0 = 1
    NEWGAME_1 = 4
    NEWGAME_2 = 5
    NEWGAME_3 = 6
    GAME_OVER = 2
    SELECT_LEVEL = 3


def main():
    pygame.init()

    screen = pygame.display.set_mode((8 * TILE_SIZE, 8 * TILE_SIZE + 100))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME_0:
            board = Board()
            game_state = play_level(screen, board)

        if game_state == GameState.NEWGAME_1:
            board = Board(0, 1)
            game_state = play_level(screen, board)

        if game_state == GameState.NEWGAME_2:
            board = Board(0, 2)
            game_state = play_level(screen, board)

        if game_state == GameState.NEWGAME_3:
            board = Board(0, 3)
            game_state = play_level(screen, board)

        if game_state == GameState.GAME_OVER:
            game_state = game_over(screen)

        if game_state == GameState.SELECT_LEVEL:
            game_state = select_level(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def game_over(screen):
    game_over_text = UIElement(
        center_position=(240, 250),
        font_size=60,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Game Over!'
    )

    main_menu = UIElement(
        center_position=(240, 330),
        font_size=15,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Go Back To Main Menu',
        action=GameState.TITLE
    )

    buttons = RenderUpdates(
        game_over_text,
        main_menu
    )

    return game_loop(screen, buttons)


def title_screen(screen):
    start_button = UIElement(
        center_position=(240, 250),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Start',
        action=GameState.SELECT_LEVEL
    )

    quit_button = UIElement(
        center_position=(240, 310),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Quit',
        action=GameState.QUIT
    )

    buttons = RenderUpdates(
        start_button,
        quit_button
    )

    return game_loop(screen, buttons)


def play_level(screen, board):

    return_button = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Return to main menu',
        action=GameState.TITLE
    )

    buttons = RenderUpdates(return_button)

    return game_loop(screen, buttons, board)


def select_level(screen):
    against_human_button = UIElement(
        center_position=(240, 200),
        font_size=25,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Against Human',
        action=GameState.NEWGAME_0
    )

    against_computer_l1_button = UIElement(
        center_position=(240, 260),
        font_size=25,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Against Computer (Level 1)',
        action=GameState.NEWGAME_1
    )

    against_computer_l2_button = UIElement(
        center_position=(240, 320),
        font_size=25,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Against Computer (Level 2)',
        action=GameState.NEWGAME_2
    )

    against_computer_l3_button = UIElement(
        center_position=(240, 380),
        font_size=25,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Against Computer (Level 3)',
        action=GameState.NEWGAME_3
    )

    buttons = RenderUpdates(
        against_human_button,
        against_computer_l1_button,
        against_computer_l2_button,
        against_computer_l3_button
    )

    return game_loop(screen, buttons)


def tokens(board):

    token_list = pygame.sprite.Group()

    if board is not None:
        for token in board.get_all_tokens():
            x = token.x
            y = token.y

            if token.symbol == 'x':
                token_list.add(UIToken(x, 7 - y, 'blackToken.png', token))
            if token.symbol == 'X':
                token_list.add(UIToken(x, 7 - y, 'blackToken_king.png', token))
            if token.symbol == 'o':
                token_list.add(UIToken(x, 7 - y, 'purpleToken.png', token))
            if token.symbol == 'O':
                token_list.add(UIToken(x, 7 - y, 'purpleToken_king.png', token))

    return token_list


def game_loop(screen, buttons, board=None):

    token_last_moved = None
    token_list = tokens(board)

    while True:
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()

                if event.button == pygame.BUTTON_LEFT:
                    for key in token_list:
                        if key.rect.collidepoint((x, y)):
                            key.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True
                for key in token_list:
                    key.clicked = False
                # if token_last_moved:
                #     next_move = token_last_moved.locate_token()

        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)

            if ui_action is not None:
                print(ui_action)
                return ui_action

        for key in token_list:
            if key.clicked:
                (x, y) = pygame.mouse.get_pos()
                key.move_token(x, y)
                # token_last_moved = key

        buttons.draw(screen)

        if board is not None:
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 1:
                        pygame.draw.rect(screen, (76, 63, 119), (TILE_SIZE * i, TILE_SIZE * j, TILE_SIZE, TILE_SIZE))
                    else:
                        pygame.draw.rect(screen, (164, 188, 188), (TILE_SIZE * i, TILE_SIZE * j, TILE_SIZE, TILE_SIZE))

        token_list.draw(screen)

        pygame.display.update()

        if board is not None:
            if board.game_over():
                pygame.display.flip()
                time.sleep(1)
                return GameState.GAME_OVER

            board.next_turn()
            token_list = tokens(board)

            if board.get_playing_player().is_ai():
                time.sleep(.5)



main()









from Token import Token
from Helpers import debug
import random
import copy


def get_player_input(tokens_that_can_move, all_moves):

    print('Give me your input:')

    print('Your options are:')
    for x, y in tokens_that_can_move:
        print(f'{(x, y)} => {all_moves[x][y]}')

    result = list(input())

    return int(result[0]) - 1, 0 if len(result) < 2 else result[1]


class Player:
    def __init__(self, x, y, symbol, difficulty_level=0, dev=False):
        debug('Create Player')
        self.tokens = list()
        self.turn_finished = True
        self.last_kill = (-1, -1)
        self.symbol = symbol
        # when difficulty_level = 0, a human player can take over
        # when difficulty_level >= 1, the AI is taking over
        self.difficulty_level = difficulty_level

        self.setup_tokens_the_right_way(symbol)

    # kill two in a row and game is over
    def test_multikill_case_1(self, symbol):
        if symbol == 'x':
            self.tokens.append(Token(1, 2, symbol))
            self.tokens.append(Token(4, 1, symbol))
        else:
            self.tokens.append(Token(0, 3, symbol))
            self.tokens.append(Token(1, 4, symbol))

    # token kills one, becomes king and kills another one on the way back and game is over
    def test_multikill_case_2(self, symbol):
        if symbol == 'x':
            self.tokens.append(Token(2, 1, symbol))
            self.tokens.append(Token(4, 1, symbol))
            self.tokens.append(Token(6, 1, symbol))
        else:
            self.tokens.append(Token(1, 2, symbol))

    # token kills one, becomes king and kills another one on the way back and wait for another player move
    def test_multikill_case_3(self, symbol):
        if symbol == 'x':
            self.tokens.append(Token(2, 1, symbol))
            self.tokens.append(Token(4, 1, symbol))
            self.tokens.append(Token(6, 1, symbol))
            self.tokens.append(Token(7, 6, symbol))
        else:
            self.tokens.append(Token(1, 2, symbol))

    def setup_tokens_the_right_way(self, symbol):
        if symbol == 'x':
            for x_token in range(8):
                if x_token % 2 == 0:
                    self.tokens.append(Token(x_token, 0, symbol))
                    self.tokens.append(Token(x_token, 2, symbol))

            for x_token in range(8):
                if x_token % 2 == 1:
                    self.tokens.append(Token(x_token, 1, symbol))
        else:
            for x_token in range(8):
                if x_token % 2 == 1:
                    self.tokens.append(Token(x_token, 5, symbol))
                    self.tokens.append(Token(x_token, 7, symbol))

            for x_token in range(8):
                if x_token % 2 == 0:
                    self.tokens.append(Token(x_token, 6, symbol))

    def play(self, board, opponent):
        self.turn_finished = False

        agents = {
            0: self.human_player,
            1: self.level_1_difficulty_agent,
            2: self.level_2_difficulty_agent,
            3: self.level_3_difficulty_agent,
        }

        selected_agent = agents[self.difficulty_level]

        return selected_agent(board, opponent)

    def human_player(self, board, opponent):

        tokens_that_can_move, all_moves, forced_kill = self.possible_moves(board, self.last_kill)

        if len(tokens_that_can_move) == 0:
            self.turn_finished = True
            self.last_kill = -1, -1
            return -1, -1

        user_input = get_player_input(tokens_that_can_move, all_moves)

        token, target_tile = self.get_move(user_input, tokens_that_can_move, all_moves)

        killed_token_coordinates = self.move_token(token, target_tile)

        debug(f'killing spree {token.in_killing_spree}')

        self.is_in_killing_spree(token)

        self.turn_finished = not forced_kill

        return killed_token_coordinates

    def level_1_difficulty_agent(self, board, _):
        debug('I will do it by myself randomly.')

        tokens_that_can_move, all_moves, forced_kill = self.possible_moves(board, self.last_kill)

        if len(tokens_that_can_move) == 0:
            self.turn_finished = True
            self.last_kill = -1, -1
            return -1, -1

        (x, y) = random.choice(tokens_that_can_move)
        token = self.get_token(x, y)
        killed_token_coordinates = self.move_token(token, random.choice(all_moves[x][y]))
        # debug(f'AI: {new_x}{new_y}')
        self.turn_finished = not forced_kill

        debug(f'killing spree {token.in_killing_spree}')

        self.is_in_killing_spree(token)

        return killed_token_coordinates

    def level_2_difficulty_agent(self, board, opponent):
        debug(f'\n\n\n\nAI START => \'{self.symbol}\'')

        # successor -> all possible moves
        tokens_that_can_move, all_moves, forced_kill = self.possible_moves(board, self.last_kill)

        if len(tokens_that_can_move) == 0:
            self.turn_finished = True
            self.last_kill = -1, -1
            return -1, -1

        best_score = float('-inf')
        best_move = (-1, -1)
        token_coordindates = (-1, -1)

        debug(f'tokens_that_can_move: {tokens_that_can_move}')

        for x, y in tokens_that_can_move:
            for current_move in all_moves[x][y]:
                debug(f'Rate Moves of Token[{x}][{y}]')

                temp_self = copy.deepcopy(self)
                temp_opponent = copy.deepcopy(opponent)
                temp_board = copy.deepcopy(board)

                token = temp_self.get_token(x, y)

                killed_token_coordinates = temp_self.move_token(token, current_move)
                current_move_x, current_move_y = current_move

                temp_board[current_move_x][current_move_y] = temp_self.symbol
                temp_board[x][y] = ' '

                if not killed_token_coordinates == (-1, -1):
                    opponent.kill_token(killed_token_coordinates)

                    killed_x, killed_y = killed_token_coordinates

                    temp_board[killed_x][killed_y] = ' '

                current_score = temp_opponent.minimax(temp_board, 2, True, temp_self)

                if current_score > best_score:
                    best_score = current_score
                    best_move = current_move
                    token_coordindates = (x, y)
                    print(f'best_score: {best_score} => token_coordinate: {token_coordindates}')
                print(best_move)
                print(f'current_score: {current_score} => best_score: {best_score}')

        (x, y) = token_coordindates
        final_token = self.get_token(x, y)
        killed_token_coordinates = self.move_token(final_token, best_move)

        self.is_in_killing_spree(final_token)

        debug(f'Chosen Move: Token[{x}][{y}] => Tile[{best_move[0]}][{best_move[1]}]')

        return killed_token_coordinates

    def fitness(self, board, opponent):
        debug('FITNESS')
        # score = 1

        score = 0

        # score += 5 * (len(self.tokens) - len(opponent.tokens))

        # score += sum([5 for token in self.tokens if token.is_king()])
        # score -= sum([5 for token in opponent.tokens if token.is_king()])

        # if score < 1:
        #     score = 1

        # for column in range(8):
        #     for row in range(8):
        #         token = self.get_token(row, column)
        #         if token and token.symbol == self.symbol and (column == 0 or column == 7):
        #             score += 20

        for y in range(8):
            for x in range(8):
                if board[x][y] == 'O':
                    score += 10

                if board[x][y] == 'X':
                    score -= 10

                if board[x][y] == 'x' or board[x][y] == 'X':
                    if x == 0 or x == 7:
                        score += 5

                if board[x][y] == 'o' or board[x][y] == 'O':
                    if x == 0 or x == 7:
                        score -= 5

        if score <= 0:
            score += 1

        debug(f'fitness: {score}')

        return score

    def is_in_killing_spree(self, token):
        if token.in_killing_spree:
            self.last_kill = token
        else:
            self.last_kill = -1, -1

    def minimax(self, board, depth, maximizing_player, opponent):
        debug('\n\n\n\n\n\n')
        debug('===========BEFORE===========')
        for x in board:
            debug(x)
        debug('===========BEFORE===========')

        tokens_that_can_move, all_moves, forced_kill = self.possible_moves(board, self.last_kill)

        if depth == 0 or len(tokens_that_can_move) == 0:
            debug(f'MINIMAX(FITNESS) - Depth: {depth} - maximazing={maximizing_player}')

            return self.fitness(board, opponent)  # heuristic function to evaluate the state

        if maximizing_player:
            value = -1000
            counter = 1
            for x, y in tokens_that_can_move:
                for current_move in all_moves[x][y]:
                    self.print_statements('UP', all_moves, x, y, counter, depth, maximizing_player)
                    counter += 1

                    temp_self = copy.deepcopy(self)
                    temp_opponent = copy.deepcopy(opponent)
                    temp_board = copy.deepcopy(board)

                    token = temp_self.get_token(x, y)
                    # make move and get dead token
                    killed_token_coordinates = temp_self.move_token(token, current_move)
                    current_move_x, current_move_y = current_move

                    temp_board[current_move_x][current_move_y] = temp_self.symbol
                    temp_board[x][y] = ' '

                    if not killed_token_coordinates == (-1, -1):
                        opponent.kill_token(killed_token_coordinates)

                        killed_x, killed_y = killed_token_coordinates

                        temp_board[killed_x][killed_y] = ' '

                    debug('UP===========AFTER===========')
                    for asdf in temp_board:
                        debug(asdf)
                    debug('===========AFTER===========')

                    # this does not take into account the multi-kill (use if statement and pass the same variables in the minimax when there is a kill)
                    value = max(value, temp_opponent.minimax(temp_board, depth - 1, False, temp_self))

            return value
        else:
            value = 1000

            counter = 1
            for x, y in tokens_that_can_move:
                debug(f'[x, y]=[{x, y}]')
                for current_move in all_moves[x][y]:
                    debug(tokens_that_can_move)
                    self.print_statements('DOWN', all_moves, x, y, counter, depth, maximizing_player)
                    counter += 1
                    temp_self = copy.deepcopy(self)
                    temp_opponent = copy.deepcopy(opponent)
                    temp_board = copy.deepcopy(board)

                    token = temp_self.get_token(x, y)

                    killed_token_coordinates = temp_self.move_token(token, current_move)
                    current_move_x, current_move_y = current_move

                    temp_board[current_move_x][current_move_y] = temp_self.symbol
                    temp_board[x][y] = ' '

                    if not killed_token_coordinates == (-1, -1):
                        opponent.kill_token(killed_token_coordinates)

                        killed_x, killed_y = killed_token_coordinates

                        temp_board[killed_x][killed_y] = ' '

                    debug('DOWN===========AFTER===========')
                    for asdf in temp_board:
                        debug(asdf)
                    debug('===========AFTER===========')

                    value = min(value, temp_opponent.minimax(temp_board, depth - 1, True, temp_self))

            return value

    def print_statements(self, position, all_moves, x, y, counter, depth, maximizing_player):
        debug(f'MINIMAX({position}:{counter}) - Depth: {depth} - maximazing={maximizing_player}')
        debug(f'all_moves for Token[{x}][{y}] => {all_moves[x][y]}')

    def goal_state(self, opponent):
        return len(self.tokens) > 0 and opponent.tokens == 0

    def level_3_difficulty_agent(self, board):

        tokens_that_can_move, all_moves, forced_kill = self.possible_moves(board, self.last_kill)

        if len(tokens_that_can_move) == 0:
            self.turn_finished = True
            self.last_kill = -1, -1
            return -1, -1

        return self

    def get_move(self, user_input, tokens_that_can_move, all_moves):
        for token in self.tokens:
            (x, y) = tokens_that_can_move[user_input[0]]

            if token.x == x and token.y == y:
                return token, all_moves[x][y][user_input[1]]

    def move_token(self, token, move):

        if not token:
            return (-1, -1)

        debug(token)
        (new_x, new_y) = move
        asdf_x = (new_x + token.x) / 2
        asdf_y = (new_y + token.y) / 2
        dead_token = (-1, -1)
        if asdf_x % 1 == 0 and asdf_y % 1 == 0:
            dead_token = (int(asdf_x), int(asdf_y)) if asdf_x.is_integer() and asdf_y.is_integer() else (-1, -1)
        token.move_token(new_x, new_y)
        return dead_token

    def kill_token(self, dead_token):
        (x, y) = dead_token

        for token in self.tokens:
            if token.x == x and token.y == y:
                debug('job done')
                self.tokens.remove(token)
                break

    def possible_moves(self, board, follow_up_kill=(-1, -1)):

        if not follow_up_kill == (-1, -1):
            debug('stop killing, don\'t play next')
            follow_up_kill.stop_killing_spree()

        tokens_to_parse = self.tokens if follow_up_kill == (-1, -1) else [follow_up_kill]

        debug(f'{self.symbol} : follow_up_kill: {follow_up_kill}')

        all_moves = [[() for i in range(8)] for j in range(8)]
        tokens_that_can_move = list()
        at_least_one_kill = not follow_up_kill == (-1, -1)

        for token in tokens_to_parse:
            possible_moves = token.get_possible_moves(board, at_least_one_kill)
            all_moves[token.x][token.y] = possible_moves

            if token.in_killing_spree and not at_least_one_kill:
                at_least_one_kill = True
                tokens_that_can_move = list()
                # token.stop_killing_spree()

            if len(possible_moves) > 0:
                tokens_that_can_move.append((token.x, token.y))


        return tokens_that_can_move, all_moves, at_least_one_kill

    def get_token(self, x, y):
        for token in self.tokens:
            if token.x == x and token.y == y:
                # debug(f'Target Token[{x}][{y}] from {[(token.x, token.y) for token in self.tokens]}')
                return token

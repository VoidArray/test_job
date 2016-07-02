import random


class Game:

    GAME_TURN_1P, GAME_TURN_2P, DISCONNECT, PLAYER1_WIN, PLAYER2_WIN = range(5)
    COLORS = ['Indigo', 'DarkRed', 'Coral', 'DarkBlue', 'SteelBlue', 'DarkSalmon',
              'Maroon', 'magenta', 'navy', 'cyan', 'lime', 'tan', 'LightSteelBlue']

    def __init__(self, player1, player2):
        self._players = [player1, player2]
        self._colors = random.sample(self.COLORS, 2)
        self._desk = {}
        self._state = self.GAME_TURN_1P
        self._move_history = []

    def set_desk(self, new_desk, color1, color2, turn):
        '''DEBUG'''
        self._desk = new_desk
        self._colors = (color1, color2)
        self._set_game_state(turn)

    def get_players(self):
        return self._players

    def get_player_number(self, player_id):
        if player_id in self._players:
            return self._players.index(player_id)
        else:
            return -1

    def get_color(self, player_id):
        number = self.get_player_number(player_id)
        return self._colors[number]

    def get_desk_state(self):
        return self._desk

    def get_game_state(self):
        return self._state

    def get_status_string(self):
        if self._state == 0:
            return 'Player 1 turn'
        if self._state == 1:
            return 'Player 2 turn'
        if self._state == 2:
            return 'Disconnect'
        if self._state == 3:
            return 'Player 1 win'
        if self._state == 4:
            return 'Player 2 win'

    def _set_game_state(self, state):
        self._state = state

    def _change_turn(self):
        if self._state == self.GAME_TURN_1P:
            self._set_game_state(self.GAME_TURN_2P)
        else:
            self._set_game_state(self.GAME_TURN_1P)

    def is_game_continued(self):
        return True if (self.get_game_state() < 2) else False

    def get_status_after_move(self, col, row, player_id):
        '''
        :return: status as string
        '''

        if not self.is_game_continued():
            return 'game overed!'

        if self.get_game_state() != self.get_player_number(player_id):
            return 'Cheater! :D'

        col = int(col)
        row = int(row)

        player_color = self.get_color(player_id)
        if not col in self._desk:
            self._desk[col] = {}

        if not row in self._desk[col]:
            order = self.add_move_to_history(col, row)
            self._desk[col][row] = {}
            self._desk[col][row]['color'] = player_color
            self._desk[col][row]['order'] = order
        else:
            return 'Impossible move, exist'

        winner = self._is_some_color_win(col, row)
        if winner:
            if winner == self.get_color(self._players[0]):
                self._set_game_state(self.PLAYER1_WIN)
            else:
                self._set_game_state(self.PLAYER2_WIN)
        else:
            self._change_turn()
        result = self.get_status_string()
        return result

    def _is_some_color_win(self, col, row):
        def check_winner(col_numbers, row_numbers):
            player_color = ''
            current_series = 1
            for pair in zip(col_numbers, row_numbers):
                col_number, row_number = pair
                if (col_number in self._desk) and (row_number in self._desk[col_number]):
                    if player_color == self._desk[col_number][row_number]['color']:
                        current_series += 1
                        if current_series == win_series:
                            return player_color
                    else:
                        player_color = self._desk[col_number][row_number]['color']
                        current_series = 1
                else:
                    player_color = ''
            return None
        # check only 5 * 5 field after move
        col = int(col)
        row = int(row)
        win_series = 5
        col_begin = col - win_series + 1
        col_end = col + win_series
        row_begin = row - win_series + 1
        row_end = row + win_series

        col_range = list(range(col_begin, col_end))
        row_range = list(range(row_begin, row_end))
        const_col_range = [col, ] * len(row_range)
        const_row_range = [row, ] * len(col_range)

        # check vertical, col - const
        color_of_winner = check_winner(const_col_range, row_range)
        if (color_of_winner):
            return color_of_winner

        # check horizontal, row - const
        color_of_winner = check_winner(col_range, const_row_range)
        if (color_of_winner):
            return color_of_winner

        # check main diagonal
        color_of_winner = check_winner(col_range, row_range)
        if (color_of_winner):
            return color_of_winner

        # check reverse diagonal
        color_of_winner = check_winner(col_range[::-1], row_range)
        if (color_of_winner):
            return color_of_winner

    def take_surrender(self, player_id):
        surrended_player_number = self.get_player_number(player_id)
        if surrended_player_number >= 0:
            game_state = self.get_game_state()
            self._set_game_state(self.PLAYER2_WIN - surrended_player_number)
            return True
        else:
            return False

    def add_move_to_history(self, col, row):
        self._move_history.append( (col, row) )
        return len(self._move_history)

    def get_move_from_history(self, number):
        return self._move_history[number]

    def get_move_count(self):
        return len(self._move_history)

class GameList:

    def __init__(self):
        self._games = {}

    def get_count(self):
        return len(self._games)

    def get_game_id_by_player_or_none(self, searched_player):
        for game_id in self._games:
            game = self._games[game_id]
            players = game.get_players()
            if game.is_game_continued() and (searched_player in players):
                return game_id

    def get_game_by_id(self, game_id):
        if game_id in self._games:
            return self._games[game_id]

    def add(self, game_id, game):
        self._games[game_id] = game


if __name__ == '__main__':

    def check_horizontal_line():
        g = Game('123', '456')
        new_desk = {}
        new_desk[1] = {}
        new_desk[2] = {}
        new_desk[3] = {}
        new_desk[4] = {}
        new_desk[5] = {}
        new_desk[1][1] = {'color': 'red', 'order': 1} 
        new_desk[2][1] = {'color': 'red', 'order': 1} 
        new_desk[3][1] = {'color': 'red', 'order': 1} 
        new_desk[4][1] = {'color': 'red', 'order': 1} 
        g.set_desk(new_desk, 'blue', 'red', Game.GAME_TURN_2P)
        return g.get_status_after_move(5, 1, '456')


    def check_vertical_line():
        g = Game('123', '456')
        new_desk = {}
        new_desk[1] = {}
        new_desk[1][1] = {'color': 'red', 'order': 1} 
        new_desk[1][2] = {'color': 'red', 'order': 1} 
        new_desk[1][3] = {'color': 'red', 'order': 1} 
        new_desk[1][4] = {'color': 'red', 'order': 1} 
        g.set_desk(new_desk, 'blue', 'red', Game.GAME_TURN_2P)
        return g.get_status_after_move(1, 5, '456')


    def check_diagonal_line():
        g = Game('123', '456')
        new_desk = {}
        new_desk[1] = {}
        new_desk[2] = {}
        new_desk[3] = {}
        new_desk[4] = {}
        new_desk[5] = {}
        new_desk[1][1] = {'color': 'red', 'order': 1} 
        new_desk[2][2] = {'color': 'red', 'order': 1} 
        new_desk[3][3] = {'color': 'red', 'order': 1} 
        new_desk[4][4] = {'color': 'red', 'order': 1} 
        g.set_desk(new_desk, 'blue', 'red', Game.GAME_TURN_2P)
        return g.get_status_after_move(5, 5, '456')

    def check_diagonal_line2():
        g = Game('123', '456')
        new_desk = {}
        new_desk[1] = {}
        new_desk[2] = {}
        new_desk[3] = {}
        new_desk[4] = {}
        new_desk[5] = {}
        new_desk[4][1] = {'color': 'red', 'order': 1} 
        new_desk[3][2] = {'color': 'red', 'order': 1} 
        new_desk[2][3] = {'color': 'red', 'order': 1} 
        new_desk[1][4] = {'color': 'red', 'order': 1} 
        g.set_desk(new_desk, 'blue', 'red', Game.GAME_TURN_2P)
        return g.get_status_after_move(5, 0, '456')

    assert check_vertical_line() == 'Player 2 win'
    assert check_horizontal_line() == 'Player 2 win'
    assert check_diagonal_line() == 'Player 2 win'
    assert check_diagonal_line2() == 'Player 2 win'



import random
import logging

import jinja2
import aiohttp_jinja2
from aiohttp import web

from classes.game_classes import Game, GameList

players_queue = []
game_list = GameList()


def _gen_new_id(size=16):
    char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    new_id = ''.join(random.sample(char_set * size, size))
    return new_id


@aiohttp_jinja2.template('index.html')
async def index(request):
    user_id = _gen_new_id()
    return {'user_id': user_id}


@aiohttp_jinja2.template('game.html')
async def get_page_with_canvas(request):
    game_id = request.match_info['game_id']
    user_id = request.match_info['user_id']
    print(game_id, user_id)
    if user_id == '0':
        user_id = _gen_new_id()
        add_player_to_queue(user_id)
    elif game_id == '0':
        add_player_to_queue(user_id)

    try_create_new_game()
    return {'user_id': user_id, 'game_id': game_id}


def add_player_to_queue(player_id):
    if not player_id in players_queue:
        players_queue.append(player_id)


def try_create_new_game():
    while len(players_queue) > 1:
        player1 = players_queue.pop()
        player2 = players_queue.pop()
        game = Game(player1, player2)
        game_id = _gen_new_id()
        game_list.add(game_id, game)
        logger.info('Added new game {} {}'.format(player1, player2))
        

async def ajax_move(request):
    game_id = request.match_info['game_id']
    if game_id == '0':
        json_dict = {'status': 'No game id'}
    else:
        user_id = request.match_info['user_id']
        col = request.match_info['col']
        row = request.match_info['row']
        logger.debug('move: {} {} {} {}'.format(game_id, user_id, col, row))
        game = game_list.get_game_by_id(game_id)
        if game:
            move_result = game.get_status_after_move(col, row, user_id)
            logger.debug('move result: {}, game state: {}'.format(move_result, game.get_game_state()))
            json_dict = {'status': move_result}
        else:
            json_dict = {'status': 'Wrong game id'}
    result = web.json_response(json_dict)
    return result


async def get_full_state(request):
    game_id = request.match_info['game_id']
    user_id = request.match_info['user_id']
    if game_id == '0':
        # Try restore game_id from game list
        game_id = game_list.get_game_id_by_player_or_none(user_id)

    if game_id:
        game = game_list.get_game_by_id(game_id)
        if game:
            json_dict = {'desk': game.get_desk_state(),
                         'game_id': game_id,
                         'status': game.get_status_string(),
                         'color': game.get_color(user_id),
                         'game_state': game.get_game_state(),
                         'player_number': game.get_player_number(user_id),
                         'game_continued': game.is_game_continued(),
                         'move_count': game.get_move_count()
            }
        else:
            json_dict = {
                'status': 'Game not found on server.'
            }
    else:
        json_dict = {
            'status': 'wait for begin.'
        }
    result = web.json_response(json_dict)
    return result


async def surrender(request):
    game_id = request.match_info['game_id']
    user_id = request.match_info['user_id']
    game = game_list.get_game_by_id(game_id)
    if game:
        if game.take_surrender(user_id):
            status = 'Game over. You surrender.'
        else:
            status = 'Wrong id'
    else:
        status = 'Game not found on server.'
    json_dict = {
        'status': status
    }
    logger.info('surrender {}, status: {}'.format(user_id, status))
    result = web.json_response(json_dict)
    return result


# Logging file
logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('server.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# Log to console
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.INFO)
logger.addHandler(log_to_console)

# Web server
app = web.Application()
app.router.add_route('GET', '/', index)
app.router.add_route('GET', '/game/{game_id}/{user_id:\S+}', get_page_with_canvas)
app.router.add_route('GET', '/move/{game_id}/{user_id:\S+}/{col:-*\d+}/{row:-*\d+}', ajax_move)
app.router.add_route('GET', '/getstate/{game_id}/{user_id:\S+}', get_full_state)
app.router.add_route('GET', '/surrender/{game_id}/{user_id:\S+}', surrender)

# special dirs
app.router.add_static('/static/', 'static')
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

logger.info('Server started.')
web.run_app(app)
logger.info('Server stoped.')

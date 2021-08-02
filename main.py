import json

from flask import Flask, make_response, render_template, request

from board import ConnectFour
from config import Config

app = Flask(__name__)


def get_board(request):
    cookie = request.cookies.get('connect_four_board')
    return json.loads(cookie) if cookie else None


def get_player(request):
    return False if request.cookies.get('current_player') == Config.player_two_name else True


def set_board(request, board):
    request.set_cookie('connect_four_board', json.dumps(board))


def set_player(request, player):
    request.set_cookie('current_player', Config.player_one_name if player else Config.player_two_name)


@app.route("/", methods=["GET"])
def connect_four_get():
    connect_four = ConnectFour(get_board(request))
    player = get_player(request)
    response = make_response(
        render_template('connect_four.html', board=connect_four.board, player=player,
                        width=Config.width))
    set_board(response, connect_four.board)
    set_player(response, player)
    return response


@app.route("/", methods=["POST"])
def connect_four_set():
    connect_four = ConnectFour(get_board(request))
    player = get_player(request)
    position = int(request.form['position'])
    winner = connect_four.check_winner()
    if not winner:
        connect_four.add_element(position, player)
        winner = connect_four.check_winner()
        player = not player
    response = make_response(
        render_template('connect_four.html', board=connect_four.board, player=player,
                        width=Config.width, winner=winner))
    set_board(response, connect_four.board)
    set_player(response, player)
    return response

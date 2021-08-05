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


def create_response(connect_four, player, winner=""):
    response = make_response(
        render_template('connect_four.html', board=connect_four.board, player=player, player_one=Config.player_one,
                        player_one_name=Config.player_one_name,
                        player_two=Config.player_two, player_two_name=Config.player_two_name,
                        width=Config.width, winner=winner))
    set_board(response, connect_four.board)
    set_player(response, player)
    return response


@app.route("/", methods=["GET"])
def connect_four_get():
    connect_four = ConnectFour(get_board(request))
    player = get_player(request)
    return create_response(connect_four, player)


def add_element(request, argument):
    assert len(argument) == 1
    connect_four = ConnectFour(get_board(request))
    player = get_player(request)
    winner = connect_four.check_winner()
    if not winner:
        connect_four.add_element(int(argument[0]), player)
        winner = connect_four.check_winner()
        player = not player
    response = create_response(connect_four, player, winner)
    return response


def reset_board(request, argument):
    connect_four = ConnectFour(get_board(request))
    connect_four.reset_board()
    player = get_player(request)
    response = create_response(connect_four, player)
    return response


@app.route("/", methods=["POST"])
def connect_four_post():
    command_dictionary = {"add": add_element,
                          "reset": reset_board}
    command = request.form['command'].split(":")
    command, argument = command[0], command[1:]
    return command_dictionary[command](request, argument)

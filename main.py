import json

from flask import Flask, make_response, render_template, request
from flask_socketio import SocketIO, emit

from board import ConnectFour, generate_board
from config import Config

app = Flask(__name__)
socketio = SocketIO(app)


def get_user_data(request):
    try:
        with open(f"games/{request.cookies.get('userid')}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"board": generate_board(), "player": True}


def set_user_data(request, board, player):
    data_dictionary = {"board": board, "player": player}
    with open(f"games/{request.cookies.get('userid')}.json", "w") as file:
        json.dump(data_dictionary, file)


def create_response(connect_four, player, winner=""):
    response = make_response(
        render_template('connect_four.html', board=connect_four.board, player=player, player_one=Config.player_one,
                        player_one_name=Config.player_one_name,
                        player_two=Config.player_two, player_two_name=Config.player_two_name,
                        width=Config.width, winner=winner))
    return response


@app.route("/", methods=["GET"])
def connect_four_get():
    user_data = get_user_data(request)
    connect_four = ConnectFour(user_data["board"])
    player = user_data["player"]
    winner = connect_four.check_winner()
    return create_response(connect_four, player, winner)


def add_element(request, argument):
    assert len(argument) == 1
    user_data = get_user_data(request)
    connect_four = ConnectFour(user_data["board"])
    player = user_data["player"]
    winner = connect_four.check_winner()
    if not winner:
        if connect_four.add_element(int(argument[0]), player):
            winner = connect_four.check_winner()
            player = not player
    return connect_four, player, winner


def reset_board(request, argument):
    connect_four = ConnectFour(request)
    connect_four.reset_board()
    user_data = get_user_data(request)
    player = user_data["player"]
    winner = None
    return connect_four, player, winner


@socketio.on("connect_four_update")
def connect_four_post_socket(message):
    command_dictionary = {"add": add_element,
                          "reset": reset_board}
    command = message.split(":")
    command, argument = command[0], command[1:]
    connect_four, player, winner = command_dictionary[command](request, argument)
    user_data = get_user_data(request)
    player_board = ConnectFour(user_data["board"])
    set_user_data(request, connect_four.board, player)
    user_id = request.cookies.get("userid")
    emit("connect_four_board"+user_id, connect_four-player_board)
    emit("connect_four_player"+user_id, Config.player_one_name if player else Config.player_two_name)
    if not winner:
        winner = "None"
    emit("connect_four_winner"+user_id, winner)


@app.route("/", methods=["POST"])
def connect_four_post():
    command_dictionary = {"add": add_element,
                          "reset": reset_board}
    command = request.form['command'].split(":")
    command, argument = command[0], command[1:]
    return command_dictionary[command](request, argument)


if __name__ == '__main__':
    socketio.run(app)
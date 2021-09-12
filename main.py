import json
import os

from flask import Flask, make_response, render_template, request, redirect
from flask_socketio import SocketIO, emit, ConnectionRefusedError

from board import ConnectFour, generate_board
from config import Config

app = Flask(__name__)
socketio = SocketIO(app)
current_players = []


def get_user_data(username=None):
    if username and os.path.exists(f"games/{username}.json"):
        with open(f"games/{username}.json", "r") as file:
            return json.load(file)
    return {"board": generate_board(), "player": True}


def set_user_data(username, board, player):
    data_dictionary = {"board": board, "player": player}
    with open(f"games/{username}.json", "w") as file:
        json.dump(data_dictionary, file)


def single_player():
    user_data = get_user_data()
    connect_four = ConnectFour(user_data["board"])
    player = user_data["player"]
    winner = connect_four.check_winner()
    return connect_four.board, player, winner


@app.route("/", methods=["GET"])
def main():
    board, player, winner = single_player()
    response = make_response(
        render_template('connect_four.html', board=board, player=player, player_one=Config.player_one,
                        player_one_name=Config.player_one_name,
                        player_two=Config.player_two, player_two_name=Config.player_two_name,
                        width=Config.width, winner=winner))
    return response


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


@socketio.on("connect", namespace="/")
def on_connect(auth):
    username = auth.get('username')
    if username:
        current_players.append(username)
        emit("players", len(current_players))
    else:
        raise ConnectionRefusedError('You must provide username!')

    @socketio.on("disconnect")
    def on_disconnect():
        current_players.remove(username)

    @socketio.on("singleplayer")
    def single_player_board():
        user_data = get_user_data(username)
        board = ConnectFour(user_data["board"])
        player = user_data["player"]
        winner = board.check_winner()
        emit("connect_four_board" + username, board - ConnectFour())
        emit("connect_four_player" + username, Config.player_one_name if player else Config.player_two_name)
        if not winner:
            winner = "None"
        emit("connect_four_winner" + username, winner)

    @socketio.on("connect_four_update")
    def single_player_update(message):
        command_dictionary = {"add": add_element,
                              "reset": reset_board}
        command = message.split(":")
        command, argument = command[0], command[1:]
        connect_four, player, winner = command_dictionary[command](username, argument)
        user_data = get_user_data(username)
        player_board = ConnectFour(user_data["board"])
        set_user_data(username, connect_four.board, player)
        emit("connect_four_board"+username, connect_four-player_board)
        emit("connect_four_player"+username, Config.player_one_name if player else Config.player_two_name)
        if not winner:
            winner = "None"
        emit("connect_four_winner"+username, winner)








if __name__ == '__main__':
    socketio.run(app)


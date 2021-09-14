import json
import os

from flask import Flask, make_response, render_template, request, redirect
from flask_socketio import SocketIO, emit, ConnectionRefusedError

from board import ConnectFour, generate_board
from config import Config

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
current_players = {}


class User:
    def __init__(self, session_id, username):
        self.session_id = session_id
        self.username = username

    def __eq__(self, other):
        return self.username == other

    def get_user_data(self):
        if self.username and os.path.exists(f"games/{self.username}.json"):
            with open(f"games/{self.username}.json", "r") as file:
                data_file = json.load(file)
                return ConnectFour(data_file["board"]), data_file["player"]
        return ConnectFour(generate_board()), True

    def set_user_data(self, board, player):
        data_dictionary = {"board": board, "player": player}
        with open(f"games/{self.username}.json", "w") as file:
            json.dump(data_dictionary, file)


@app.route("/", methods=["GET"])
def main():
    board = generate_board()
    player = Config.player_one_name
    winner = ""
    response = make_response(
        render_template('connect_four.html', board=board, player=player, player_one=Config.player_one,
                        player_one_name=Config.player_one_name,
                        player_two=Config.player_two, player_two_name=Config.player_two_name,
                        width=Config.width, winner=winner))
    return response


def add_element(user, argument):
    connect_four, player = user.get_user_data()
    winner = connect_four.check_winner()
    if not winner:
        if connect_four.add_element(int(argument[0]), player):
            winner = connect_four.check_winner()
            player = not player
    return connect_four, player, winner


def reset_board(user, argument):
    connect_four, player = user.get_user_data()
    connect_four.reset_board()
    winner = ""
    return connect_four, player, winner


@socketio.on("connect")
def on_connect(auth):
    username = auth.get("username")
    if username and username not in current_players:
        current_players[request.sid] = (User(request.sid, username))
        emit("players", len(current_players), broadcast=True)
    else:
        raise ConnectionRefusedError('You must provide a unique username!')


@socketio.on("disconnect")
def on_disconnect():
    del current_players[request.sid]


@socketio.on("singleplayer")
def single_player_board():
    user = current_players[request.sid]
    connect_four, player = user.get_user_data()
    player = Config.player_one_name if player else Config.player_two_name
    winner = connect_four.check_winner()
    winner = winner if winner else "None"
    emit("connect_four_board", {"connect_four": connect_four - ConnectFour(), "player": player, "winner": winner},
         room=user.session_id)


@socketio.on("connect_four_update")
def single_player_update(message):
    command_dictionary = {"add": add_element,
                          "reset": reset_board}
    command = message.split(":")
    command, argument = command[0], command[1:]
    user = current_players[request.sid]
    player_board, player = user.get_user_data()

    connect_four, player, winner = command_dictionary[command](user, argument)
    user.set_user_data(connect_four.board, player)

    connect_four = connect_four - player_board
    player = Config.player_one_name if player else Config.player_two_name
    winner = winner if winner else "None"

    emit("connect_four_board", {"connect_four": connect_four, "player": player, "winner": winner}, room=user.session_id)


if __name__ == '__main__':
    socketio.run(app)

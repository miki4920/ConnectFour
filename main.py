import json
import os
import random

from flask import Flask, make_response, render_template, request
from flask_socketio import SocketIO, emit, ConnectionRefusedError, join_room, leave_room

from board import ConnectFour, generate_board
from config import Config

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
current_players = {}
looking_for_multiplayer = []


class User:
    def __init__(self, session_id, username):
        self.session_id = session_id
        self.username = username
        self.room = None

    def __eq__(self, other):
        return self.username == other

    def get_user_data(self):
        path = self.room if self.room else self.username
        if path and os.path.exists(f"games/{path}.json"):
            with open(f"games/{path}.json", "r") as file:
                data_file = json.load(file)
                return ConnectFour(data_file["board"]), data_file["player"]
        return ConnectFour(generate_board()), True

    def set_user_data(self, board, player):
        path = self.room if self.room else self.username
        data_dictionary = {"board": board, "player": player}
        with open(f"games/{path}.json", "w") as file:
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


@socketio.on("connect")
def on_connect(auth):
    username = auth.get("username")
    if username and username not in [player.username for player in current_players.values()]:
        current_players[request.sid] = (User(request.sid, username))
        emit("players", len(current_players), broadcast=True)
    else:
        raise ConnectionRefusedError('You must provide a unique username!')


def remove_looking_for_multiplayer(sid):
    for i, user in enumerate(looking_for_multiplayer):
        if user.session_id == sid:
            del looking_for_multiplayer[i]


@socketio.on("disconnect")
def on_disconnect():
    player = current_players[request.sid]
    del current_players[request.sid]
    remove_looking_for_multiplayer(request.sid)
    leave_room(player.room, player.session_id)


@socketio.on("multiplayer")
def multi_player_board():
    user = current_players[request.sid]
    if len(looking_for_multiplayer) > 0:
        opponent = random.choice(list(looking_for_multiplayer))
        room = user.session_id + opponent.session_id
        join_room(room, user.session_id)
        join_room(room, opponent.session_id)
        user.room = room
        opponent.room = room
        remove_looking_for_multiplayer(user.session_id)
        remove_looking_for_multiplayer(opponent.session_id)
        emit("multiplayer", {"connect_four": {}, "player": Config.player_one_name, "winner": "None"},
             to=room, include_self=True)
    else:
        looking_for_multiplayer.append(user)


def add_element(user, user_board, position):
    connect_four, player = user.get_user_data()
    winner = connect_four.check_winner()
    if not winner:
        if connect_four.add_element(int(position), player):
            winner = connect_four.check_winner()
            player = not player
    return connect_four, connect_four-user_board, player, winner


def reset_board(user, user_board, argument=None):
    connect_four, player = user.get_user_data()
    connect_four.reset_board()
    winner = "None"
    return connect_four, connect_four-user_board, player, winner


def get_board(user, user_board, argument=None):
    connect_four, player = user.get_user_data()
    winner = connect_four.check_winner()
    return connect_four, connect_four-ConnectFour(), player, winner


@socketio.on("command")
def update(message):
    command_dictionary = {"add": add_element,
                          "reset": reset_board,
                          "get": get_board}
    command, argument = message.get("command"), message.get("argument")
    user = current_players[request.sid]
    user_board, player = user.get_user_data()

    connect_four, instructions, player, winner = command_dictionary[command](user, user_board, argument)
    user.set_user_data(connect_four.board, player)
    player = Config.player_one_name if player else Config.player_two_name
    winner = winner if winner else "None"
    if user.room:
        emit("update", {"instructions": instructions, "player": player, "winner": winner}, room=user.room)
    else:
        emit("update", {"instructions": instructions, "player": player, "winner": winner})


if __name__ == '__main__':
    socketio.run(app)

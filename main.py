import json
import os
import random

from flask import Flask, make_response, render_template, request
from flask_socketio import SocketIO, emit, ConnectionRefusedError, join_room, leave_room, rooms

from board import ConnectFour, generate_board
from config import Config

app = Flask(__name__)
socketio = SocketIO(app)
current_players = {}
looking_for_multiplayer = []


class User:
    def __init__(self, session_id, username):
        self.session_id = session_id
        self.username = username
        self.room = None
        self.player = False
        self.reset = False

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
def index():
    board = ConnectFour().board
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
        emit("update_html", {"type": "show", "id": "username_form", "value": "none"})
        emit("update_html", {"type": "show", "id": "mode_form", "value": "flex"})
        emit("update_html", {"type": "update", "id": "display_username", "value": username})
        emit("update_html", {"type": "update", "id": "players", "value": len(current_players)}, broadcast=True)
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


def multiplayer_player(user, opponent, room):
    join_room(room, user.session_id)
    user.room = room
    remove_looking_for_multiplayer(user.session_id)
    player = Config.player_one_name if user.player else Config.player_two_name
    values_dictionary = {"username": user.username, "opponent": opponent.username, "colour": player}
    for key in values_dictionary:
        emit("update_html", {"type": "show", "id": key, "value": "block"}, to=user.session_id)
        emit("update_html", {"type": "update", "id": key, "value": values_dictionary[key]}, to=user.session_id)
    emit("update_html", {"type": "show", "id": "entry_form", "value": "none"}, to=user.session_id)


@socketio.on("multiplayer")
def multiplayer_index():
    user = current_players[request.sid]
    if len(looking_for_multiplayer) > 0:
        opponent = random.choice(list(looking_for_multiplayer))
        room = user.session_id + opponent.session_id
        random.choice([user, opponent]).player = True
        multiplayer_player(user, opponent, room)
        multiplayer_player(opponent, user, room)
    else:
        looking_for_multiplayer.append(user)


def add_element(user, user_board, position):
    connect_four, player = user.get_user_data()
    winner = connect_four.check_winner()
    if not winner and (not user.room or user.player == player):
        if connect_four.add_element(int(position), player):
            winner = connect_four.check_winner()
            player = not player
    return connect_four, connect_four-user_board, player, winner


def reset_board(user, user_board, argument=None):
    if user.room and not user.reset:
        emit("reset_request", to=user.room, include_self=False)
        return None, None, None, None
    elif user.room and user.reset:
        user.reset = False
    connect_four, player = user.get_user_data()
    connect_four.reset_board()
    winner = ""
    return connect_four, connect_four-user_board, player, winner


@socketio.on("reset")
def reset_request():
    current_players[request.sid].reset = True


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
    if connect_four is None:
        return
    user.set_user_data(connect_four.board, player)
    player = Config.player_one_name if player else Config.player_two_name
    winner = winner if winner else "None"
    emit("update", {"instructions": instructions, "player": player, "winner": winner}, room=user.room if user.room else user.session_id)


if __name__ == '__main__':
    socketio.run(app)

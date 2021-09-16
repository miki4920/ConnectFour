function incorrect_username() {
    let button = document.getElementById("submit_username")
    button.style.background = "rgba(255, 0, 0, 0.45)";
}

function correct_username(username) {
    socket.auth = {"username": username}
    socket.connect()
}

function set_username() {
    let username = document.getElementById("username").value
    let username_regex = /^[a-zA-Z0-9]+$/
    if (!username_regex.test(username)) {
        incorrect_username()
    } else {
        correct_username(username)
    }
}

function singleplayer() {
    document.getElementById("entry_form").style.display = "none";
    socket.emit("command", {"command": "get"})
}

function multiplayer() {
    document.getElementById("mode_form").style.display = "none";
    document.getElementById("looking_form").style.display = "flex";
    socket.emit("multiplayer")
}


function send_command(command, argument = "") {
    let message = {"command":command,
            "argument": + argument};
    socket.emit("command", message);
}

socket = io.connect(window.location.host, {autoConnect: false});

function update_players(players) {
    let player_number = document.getElementById("current_players")
    player_number.innerText = "Current Players: " + players;
}

socket.on("connected", (message) => {
    let username_form = document.getElementById("username_form")
    username_form.style.display = "none"
    let mode_form = document.getElementById("mode_form")
    mode_form.style.display = "flex"
})

socket.on("players", (message) => {
    update_players(message);
})

function update_board(message) {
    let instructions = message["instructions"]
    let player = message["player"]
    let winner = message["winner"]
    for (let [key, value] of Object.entries(instructions)) {
        let element = document.getElementById(key);
        element.classList.remove(...element.classList);
        if (value) {
            element.classList.add("connect_four_element_" + value)
        } else {
            element.classList.add("connect_four_element")
        }
    }
    document.getElementById("player").innerHTML = "Player: " + player;
    document.getElementById("winner").innerHTML = "Winner: " + winner;
}

socket.on('update', (message) => {
    update_board(message)
});

socket.on('multiplayer', (message) => {
    document.getElementById("entry_form").style.display = "none";
    update_board(message)
});

socket.on("connect_error", (err) => {
    let button = document.getElementById("submit_username")
    button.style.background = "rgba(255, 0, 0, 0.45)";
});



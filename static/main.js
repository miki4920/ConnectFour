function incorrect_username() {
    let button = document.getElementById("submit_username")
    button.style.background = "rgba(255, 0, 0, 0.45)";
}

function correct_username(username) {
    document.cookie = "username=" + username;
    let username_form = document.getElementById("username_form")
    username_form.style.display = "none"

    let mode_form = document.getElementById("mode_form")
    mode_form.style.display = "flex"

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

function update_players(players) {
    let player_number = document.getElementById("current_players")
    player_number.innerText = "Current Players: " + players;
}

function mode() {
    document.getElementById("entry_form").style.display = "none";
    socket.emit("singleplayer")
}

function send_command(command, argument = "") {
    let message = command + ":" + argument;
    socket.emit("connect_four_update", message);
}

socket = io.connect(window.location.host, {autoConnect: false});

socket.on("players", (message) => {
    update_players(message);
})

socket.on('connect_four_board', (message) => {
    let board = message["connect_four"]
    let player = message["player"]
    let winner = message["winner"]
    for (let [key, value] of Object.entries(board)) {
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
});




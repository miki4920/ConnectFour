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

function mode(button) {
    if(parseInt(button.value) === 0) {
        document.getElementById("entry_form").style.display = "none";
        socket.emit("command", {"command": "get"})
    }
    else if (parseInt(button.value) === 1) {
        document.getElementById("mode_form").style.display = "none";
        document.getElementById("looking_for").style.display = "flex";
        socket.emit("multiplayer")
    }
}

function send_command(command, argument = "") {
    let message = {"command":command,
            "argument": + argument};
    socket.emit("command", message);
}

socket = io.connect(window.location.host, {autoConnect: false});

socket.on("connected", (message) => {
    let username_form = document.getElementById("username_form")
    username_form.style.display = "none"
    let mode_form = document.getElementById("mode_form")
    mode_form.style.display = "flex"
    for (let [key, value] of Object.entries(message)) {
        document.getElementById(key).innerText = "Username: " + value;
    }
})

socket.on("players", (message) => {
    let player_number = document.getElementById("current_players")
    player_number.innerText = "Current Players: " + message;
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
    document.getElementById("player").innerHTML = "Current Player: " + player;
    document.getElementById("winner").innerHTML = "Winner: " + winner;
}

socket.on('update', (message) => {
    let button = document.getElementById("reset")
    button.className = ''
    update_board(message)
});

function show_buttons(message) {
    document.getElementById("entry_form").style.display = "none";
    let paragraphs = document.getElementsByClassName("multiplayer");
    for(let paragraph of paragraphs) {
        paragraph.innerText = paragraph.innerText + message[paragraph.id];
        paragraph.style.display = "block";
    }
}


socket.on('multiplayer_data', (message) => {
    show_buttons(message)
})

socket.on("connect_error", (err) => {
    let button = document.getElementById("submit_username")
    button.style.background = "rgba(255, 0, 0, 0.45)";
});


socket.on("reset_request", (message) => {
    let button = document.getElementById("reset")
    button.classList.add("reset_request")
    socket.emit("reset")
})





function set_username() {
    let username = document.getElementById("username").value
    let username_regex = /^[a-zA-Z0-9]+$/
    if (!username_regex.test(username)) {
        add_class("submit_username", "error")
    } else {
        socket.auth = {"username": username}
        socket.connect()
    }
}

function mode(button) {
    if(parseInt(button.value) === 0) {
        show_element("entry_form", "none")
        socket.emit("command", {"command": "get"})
    }
    else if (parseInt(button.value) === 1) {
        show_element("mode_form", "none")
        show_element("looking_for", "flex")
        socket.emit("multiplayer")
    }
}

function send_command(command, argument = "") {
    let message = {"command":command,
            "argument": + argument};
    socket.emit("command", message);
}

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
    update_text("player", player)
    update_text("winner", winner)
}

function show_element(id, method) {
    document.getElementById(id).style.display = method;
}

function hide_element(id) {
    document.getElementById(id).style.display = "none";
}

function update_text(id, text) {
    let paragraph = document.getElementById(id)
    paragraph.innerText = paragraph.innerText.split(": ")[0] + ": " + text;
}

function add_class(id, class_name) {
    document.getElementById(id).classList.add(class_name)
}

function remove_class(id, class_name) {
    document.getElementById(id).classList.remove(class_name)
}

socket = io.connect(window.location.host, {autoConnect: false});

socket.on("connect_error", (err) => {
    add_class("submit_username", "error")
});

socket.on('update', (message) => {
    let button = document.getElementById("reset")
    button.className = ''
    update_board(message)
});

socket.on("reset_request", (message) => {
    let button = document.getElementById("reset")
    button.classList.add("reset_request")
    socket.emit("reset")
})

socket.on("update_html", (message) => {
    let type = message["type"]
    let id = message["id"]
    let value = message["value"]
    if(type === "show") {
        show_element(id, value)
    }
    else if(type === "hide") {
        hide_element(id)
    }
    else if(type === "update") {
        update_text(id, value)
    }
    else if(type === "add_class") {
        add_class(id, value)
    }
    else if(type === "remove_class") {
        remove_class(id, value)
    }
})
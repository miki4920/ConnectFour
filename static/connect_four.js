function back()  {
    window.location.href = "http://127.0.0.1:5000/";
}


function send_command(command, argument="") {
    let message = command + ":" + argument;
    socket.emit("connect_four_update", message);
}

let socket = io.connect("http://127.0.0.1:5000/")
let cookie = document.cookie
if(!cookie) {
    document.cookie = "userid=" + Math.floor(Math.random()*100000)
}
let id = document.cookie.split("=")[1]

socket.on('connect_four_board' + id, (message) => {
    for (let [key, value] of Object.entries(message)) {
        let element = document.getElementById(key);
        element.classList.remove(...element.classList);
        if(value) {
            element.classList.add("connect_four_element_" + value)
        }
        else {
            element.classList.add("connect_four_element")
        }
    }
});

socket.on('connect_four_player' + id, (message) => {
    document.getElementById("player").innerHTML = "Player: " + message;
})

socket.on('connect_four_winner' + id, (message) => {
    document.getElementById("winner").innerHTML = "Winner: " + message;
})




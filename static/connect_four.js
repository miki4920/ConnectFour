function send_command(command, argument="") {
    let message = command + ":" + argument;
    socket.emit("connect_four_update", message);
}


let socket = io.connect("http://127.0.0.1:5000/")

socket.on('connect_four_board', (msg) => {
    document.querySelector('html').innerHTML = msg;
});




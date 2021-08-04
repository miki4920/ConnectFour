function send_command(command, argument="") {
    document.getElementById("command").value = command + ":" + argument;
    document.getElementById("command_form").submit();
}
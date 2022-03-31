import select
import socket


host = 'localhost'                  #the ip and port
port = 5555


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

socket_list = [server_socket]
active_clients = {}
names = []

expected_message_count = 0
message_count = 0


suggestions = ["Why don't we sing", "Let's take a walk",
               "Let's yell!", "I feel like fighting right now",
               "Maybe we could try some bickering?",
               "What do you say about we start hugging?",
               "Let's start working"]



def add_client():                                           #a function to add new clinets
    c, addr = server_socket.accept()
    socket_list.append(c)
    name = c.recv(1024).decode()
    names.append(name)
    print(f"{name} has joined the chat!")


def Delete_Client(sock):                                      #a function tp delete clients
    print(f"{active_clients[sock]} disconnected.")
    socket_list.remove(sock)
    del active_clients[sock]

def Control_Client_MSG(sock):                               #
    global message_count, expected_message_count
    try:
        msg = sock.recv(1024)
    except ConnectionAbortedError:
        Delete_Client(sock)
        expected_message_count -= 1
        return
    if not len(msg):
        Delete_Client(sock)
        return
    print(f"{msg.decode()}")
    message_count += 1
    for client in active_clients:
        if client == sock: continue
        client.send(msg)


def send_suggestion():
    global message_count, expected_message_count
    print('\n', str(suggestions))
    inpt = input(f"Select a suggestion by index (1-{len(suggestions)}): ")
    if not inpt.isnumeric(): return False
    suggestion = "Host: " + suggestions[int(inpt)-1]

    print('\n', suggestion, sep="")
    for client in active_clients:
        try:
            client.send(suggestion.encode())
            expected_message_count += 1
        except:
            socket_list.remove(client)
    return True


print(f'Listening for connections on {host}:{port}...')
while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], socket_list)

    for sock in read_sockets:
        if sock == server_socket:
            add_client()
        else:
            Control_Client_MSG(sock)

    for sock in error_sockets:                # removing the errors
        Delete_Client(sock)

    if message_count == expected_message_count:
        for index, name in enumerate(names):
            active_clients[socket_list[-len(names) + index]] = name
        names.clear()

        message_count = 0
        expected_message_count = 0

        if not send_suggestion(): break
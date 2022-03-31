import socket
import sys, os, threading
from Bots import *          #importing the bots from Bots.py

actions = ["work", "play", "eat", "cry", "sleep",
           "fight", "sing", "kill", "hug", "bicker", "speak",          #Random actions
           "complain", "shit"]


bots = {"bob": Bob, "alice": Alice, "dora": Dora, "chuck": Chuck, "user": User}
host, port, bot = sys.argv[1], int(sys.argv[2]), sys.argv[3]
if (bot not in bots): bots[bot] = User

print(f"Welcome, you have selected {bot.capitalize()}!")
print(f"You are connecting to the server at {host}:{port}...")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #connects u the ip and port u choose
client_socket.connect((host, port))

client_socket.setblocking(False)
client_socket.send((bot.capitalize()).encode())

print("Connected! Waiting for messages from server...")

def Receive_MSG():
    server_action, client_action = "", None
    msg = client_socket.recv(1024)
    if not len(msg):                                                     #if the message is empty the server will assume that you are disconnatction
        print('Connection has been closed by server')
        os._exit(0)

    if (msg.decode().find("Host") != -1):
        print(f"\nSuggestion from server!")
        print(f"{msg.decode()}")
        server_action = [action for action in actions if msg.decode().find(action) != -1][0]
        return (server_action, client_action)
    else:
        client_action = [action for action in actions if msg.decode().find(action) != -1][0]
        print(f"{msg.decode()}\n(I don't have any response to that :((((()\n")
        return (server_action, client_action)

def Send_MSG(server_action, client_action):
    if client_action == server_action: client_action = None
    msg = (f"{bot.capitalize()}: " + bots[bot](server_action, client_action)).encode()
    print(f"{msg.decode()}\n")
    client_socket.send(msg)

def Input_thread():
    while True:
        inpt = input()
        if inpt == 'q' or inpt == 'quit':
            client_socket.close()
            os._exit(0)

threading.Thread(target=Input_thread).start()

action_server, action_client = "", None
while True:
    if action_server:
        Send_MSG(action_server, action_client)
    action_server, action_client = "", None

    try:
        while True:
            action_server, action_client = Receive_MSG()
    except Exception as e:
        if e is SystemExit:
            break
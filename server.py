import pygame
from settings import WIN_RES, FPS
from cr import Map, Tour, Game
from troupes import Archer, Knight
from player import Player, Carte
from consts import COORDS_CARTE, DIM_CARTE
import socket
import threading
import json
import time

HOST = "127.0.0.1"
PORT = 5555

def send_message():
    game_state = 1# {"game": game.state, "running": running, "scores": scores}
    message = json.dumps(game_state) + "\n"
    for client_socket in clients:
        client_socket.sendall(message.encode())

def handle_client(client_socket, player_id):
    global inputs
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Joueur {player_id} dit : {data}")
            inputs[player_id] = data
        except:
            break
    print(f"Joueur {player_id} déconnecté.")
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen(2)

clients = []

while len(clients) < 2:
    print(f"En attente de {2-len(clients)} joueur(s)...")
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Joueur {len(clients)} connecté depuis {client_address}")

print("Les deux joueurs sont connectés.")

threads = []

for i, client_socket in enumerate(clients):
    thread = threading.Thread(target=handle_client, args=(client_socket, i+1))
    thread.start()
    threads.append(thread)

running = True
while running:
    send_message()
    time.sleep(0.1)

print("Partie terminée")  

for client_socket in clients:
    client_socket.close()

server_socket.close()

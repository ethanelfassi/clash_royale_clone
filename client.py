import socket
import json
import pygame
import argparse
from settings import WIN_RES, FPS
from cr import Map, Tour, Game
from troupes import Archer, Knight
from player import Player, Carte
from consts import COORDS_CARTE, DIM_CARTE, WIN_SIZE

HOST = "127.0.0.1"
PORT = 5555

parser = argparse.ArgumentParser(description="")

parser.add_argument("-i", "--ip", type=str, help="l'ip de l'hote")

args = parser.parse_args()

if args.ip:
    HOST = args.ip
else:
    HOST = '127.0.0.1'

PORT = 5555
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connecté au serveur !")

pygame.init((WIN_SIZE[0]*720, WIN_SIZE[1]*1280))

screen = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("CR")
font = pygame.font.SysFont(None, 370) 
running = True
buffer = ""

def receive_server_data(buffer):
    buffer += client_socket.recv(4096).decode()

    while "\n" in buffer:
        raw, buffer = buffer.split('\n', 1)
        try:
            game_state = json.loads(raw)
        except json.JSONDecodeError:
            continue
    return buffer, game_state

def update_display(game_state):
    for val in game_state:
        screen.blit(*val)
    pygame.display.flip()

def send_inputs():
    click_coords = (0, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_coords = pygame.mouse.get_pos()

    message =  click_coords.encode()
    client_socket.sendall(message)

while running:
    buffer, game_state = receive_server_data(buffer)
    update_display(game_state)
    send_inputs()    



client_socket.close()

import socket
import time
import UDP
import threading
import pygame
import Main
import Player
# Examples of headers

HEADER_USERNAME = "[0]type=username<>Flockland"
HEADER_WORLD = "[1]type=world, -counter-5-counter-<>123456789"
HEADER_PLAYERUPDATE= "[2]type=playerUpdate<> <x>0<x> <y>1<y> <dx>1<dx> <dy>1<dy> <name>Flockland<name>"



class Globals:
    username = ""
    world = []
    receivedPackets = []
    players = []
    def __init__(self) -> None:
        pass

for i in range(50):
    Globals.world.append([])

def parse_received(recv):
    recv = recv.decode()
    header = recv.split("<>")[0]
    data = recv.split("<>")[1]
    if "type=username" in header:
        Globals.username = recv.split("<>")[1]
    
    if "type=playerUpdate" in header:
        xPos = int(float(data.split("<x>")[1]))
        yPos = int(float(data.split("<y>")[1]))
        dx = int(float(data.split("<dx>")[1]))
        dy = int(float(data.split("<dy>")[1]))
        playerName = data.split("<name>")[1]
        
        for player in Globals.players:
            if player.name == playerName:
                player.x = xPos
                player.y = yPos
                player.dx = dx
                player.dy = dy
    
    elif "type=player" in header:
        xPos = int(data.split("<x>")[1])
        yPos = int(data.split("<y>")[1])
        name = data.split("<name>")[1]
        playerObj = Player.Player(xPos,yPos)
        playerObj.name = name
        Globals.players.append(playerObj)
        

        
        
    if "type=world" in header:
        counter = int(header.split("-counter-")[1])
        for i in range(len(data)):
            Globals.world[counter].append(int(data[i]))





client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def udp_recv(client_socket):
    print("Server is waiting for a connection...")

    # Receiving data from the server
    data, addr = client_socket.recvfrom(1024) # Using recvfrom method
    
    # Send an acknowledgment back to the server
    client_socket.sendto(b'ACK', addr) # Using sendto method
    return data

our_port = 12344
UDP.udp_send(HEADER_USERNAME + f"<port>{our_port}<port>", 9999)

client_socket.bind(('localhost', our_port))

def listenToServer():
    while True:
        data = udp_recv(client_socket)
        parse_received(data)


listenerThread = threading.Thread(target=listenToServer)
listenerThread.start()
username = "Flockland"
window = pygame.display.set_mode((800,800))

CameraX = 0
CameraY = 0

game = True

def checkIfWorldComplete(world):
    for i in world:
        if len(i) != 500:
            return False
    return True

while game:
    if checkIfWorldComplete(Globals.world):
        while game:
            window.fill("Cyan")
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    game = False
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            mouseCords = pygame.mouse.get_pos()
            for player in Globals.players:
                if player.name == "Flockland":
                    Main.applyGrassLayer(Globals.world, player)
                    Main.draw_world(window,Globals.world, CameraX, CameraY, player)
                    CameraX, CameraY = player.update(keys, Globals.world, CameraX, CameraY)
                    UDP.udp_send(f"type=playerUpdate<> <x>{player.x}<x> <y>{player.y}<y> <dx>{player.dx}<dx> <dy>{player.dy}<dy> <name>{username}<name>", 9999)
                player.draw(window, CameraX, CameraY)
            
            pygame.display.update()
            
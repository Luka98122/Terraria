import socket
import time
from Player import *
import threading
import json


AIR = 0
DIRT = 1
GRASS = 2
STONE = 3
WOOD_PLATFORM = 4
import UDP

HEADER_USERNAME = "[0]type=username<>Flockland"
HEADER_WORLD = "[1]type=world, -counter-5-counter-<>123456789"


class Globals:
    players = []
    counter = 0


def generate_world(w,h): # Generate flat world split into layers 
    world = []
    for i in range(h):
        world.append([])
        for j in range(w):
            block = None
            if i > 0 and i < 30:
                block = AIR
            elif i >=30 and i < 40:
                block = DIRT
            elif i >= 40 and i < 45:
                block = DIRT
            else:
                block = STONE
            world[i].append(block) 
    return world


def parse_received(recv,addr):
    recv = recv.decode()
    header = recv.split("<>")[0]
    data = recv.split("<>")[1]
    if "type=username" in header:
        playa = Player(20,5)
        Globals.players.append([playa,int(data.split("<port>")[1])])
        playa.name = data.split("<port>")[0]
        send_world(world)
        playerData = ""
        playerData += "type=player" + "<>" + "<x>20<x>" + "<y>5<y>" + "<name>"+data.split("<port>")[0]+"<name>"
        UDP.udp_send(playerData, Globals.players[-1][1])
    
    
    if "type=playerUpdate" in header:
        xPos = int(float(data.split("<x>")[1]))
        yPos = int(float(data.split("<y>")[1]))
        dx = int(float(data.split("<dx>")[1]))
        dy = int(float(data.split("<dy>")[1]))
        playerName = data.split("<name>")[1]
        
        for player in Globals.players:
            player = player[0]
            if player.name == playerName:
                player.x = xPos
                player.y = yPos
                player.dx = dx
                player.dy = dy
        
        for player in Globals.players:
            msg = f"type=playerUpdate<> <x>{player[0].x}<x> <y>{player[0].y}<y> <dx>{player[0].dx}<dx> <dy>{player[0].dy}<dy> <name>{player[0].name}<name>"
            UDP.udp_send(msg, player[1])
    
    if "type=player_2_Update" in header:
        name = data.split("<name>")[0]
        playerInput = data.split("<name>")[1]
        playerInput = json.loads(playerInput)
        keys = playerInput["keys"]
        mouseState = playerInput["mouse"]
        mouseCoords = playerInput["mouseCoords"]
        cameraX = playerInput["cameraX"]
        cameraY = playerInput["cameraY"]
        
        realKeys = []
        
        for key in keys:
            if key == 0:
                realKeys.append(False)
            else:
                realKeys.append(True)
        
        keys = realKeys
                
        playerInQuestion = None
        for player in Globals.players:
            if player[0].name == name:
                playerInQuestion = player[0]
                break
        
        cameraX, cameraY = playerInQuestion.update(keys,Globals.world, cameraX, cameraY)
        msg = f"type=playerUpdate<> <x>{playerInQuestion.x}<x> <y>{playerInQuestion.y}<y> <dx>{playerInQuestion.dx}<dx> <dy>{playerInQuestion.dy}<dy> <cameraX>{cameraX}<cameraX> <cameraY>{cameraY}<cameraY> <name>{playerInQuestion.name}<name>"
        for player in Globals.players:
            UDP.udp_send(msg, player[1])






world = generate_world(500,50)
Globals.world = world
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a public host and a port
server_socket.bind(('localhost', 9999))

def listenToServer():
    while True:
        data,addr = UDP.udp_recv(server_socket)
        parse_received(data,addr)

listenerThread = threading.Thread(target=listenToServer)
listenerThread.start()




def send_world(world):
    time.sleep(0.2)
    for i in range(len(world)):
        myStr = ""
        for j in range(len(world[i])):
            myStr += str(world[i][j])
        UDP.udp_send(f"[{Globals.counter}]type=world, -counter-{i}-counter-<>{myStr}", 12344)
        Globals.counter+=1


while True:
    pass


import socket
import threading
from threading import Thread
import subprocess as sp
import pygame
from pygame import mixer
from pygame.locals import *

mixer.init()

HEADER = 64
PORT = 8000
SERVER = "192.168.0.131"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DC"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

network_connected = True

def networking_start():
    server.listen()
    global network_connected
    print(f"LISTENING Server is listening on {SERVER}")
    while network_connected:
        if network_connected == True:
            conn, addr = server.accept()
            thread = Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"ACTIVE CONNECTIONS {threading.activeCount() - 1}")

def handle_client(conn, addr):
    global network_connected
    print(f"NEW CONNECTION {addr} connected")
    connected = True

    while connected and network_connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == "Get_Files":
            connected = False
            files_folder = sp.getoutput("ls | grep .wav").splitlines()
            sending_msg = ''.join([n+"@" for n in files_folder])
            conn.send(bytes(sending_msg,'utf-8'))
        elif msg == "!DC":
            network_connected = False
            connected = False
        elif msg == "":
            connected = False
        else:
            received_msg = msg.split('@')
            f = open('stored_songs.txt',"r")
            songs = []
            for x in f:
                songs.append(x.replace('\n',''))
            f = open('stored_songs.txt', "w")
            songs[int(received_msg[0])-1] = received_msg[1]
            for x in songs:
                f.write(x+'\n')
            
            f.close()
            tmp_sound = mixer.Sound(received_msg[1])
            tmp_sound.play()
            connected = False
            
        print(f"{addr}: {msg}")

    conn.close()
    
networking_start()
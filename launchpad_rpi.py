import time
import keyboard
import pygame
from enum import Enum
from pygame import mixer
from pygame.locals import *
import socket

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess as sp

import RPi.GPIO as GPIO

import sounddevice as sd
from scipy.io.wavfile import write


class States(Enum):
    PLAYER = 1
    PROGRAMMING = 2
    BLUETOOTH = 3


mixer.init()

start = 0
end = 0
loop = [0,0,0]
looper_recorder = 0
print('Loop mode')
record_loop = 0
loop_recording = False
music_recording = False
    
state = States.PLAYER
    
fs = 44100  # Sample rate
seconds = 4  # Duration of recording

seconds_rec = 30  # Duration of recording
    
display = pygame.display.set_mode((10,10))

stored_songs = []
f = open("stored_songs.txt","r")
for x in f:
    stored_songs.append(x.replace('\n',''))

Key1_sound = mixer.Sound(stored_songs[0])
Key2_sound = mixer.Sound(stored_songs[1])
Key3_sound = mixer.Sound(stored_songs[2])

Key4_sound = mixer.Sound(stored_songs[3])
Key5_sound = mixer.Sound(stored_songs[4])
Key6_sound = mixer.Sound(stored_songs[5])

Key7_sound = mixer.Sound(stored_songs[6])
Key8_sound = mixer.Sound(stored_songs[7])
Key9_sound = mixer.Sound(stored_songs[8])

loop_sound = mixer.Sound('output1e.wav')
loop_sound2 = mixer.Sound('output2e.wav')
loop_sound3 = mixer.Sound('output3e.wav')

looper_seconds1 = [0,0]
looper_seconds2 = [0,0]
looper_seconds3 = [0,0]
loop_length = 3.2

pygame.init()

def  button_sound1(channel):
    global state
    if GPIO.input(7) == GPIO.HIGH:
        if state == States.PLAYER:
            Key1_sound.play()

def  button_sound2(channel):
    global state
    if GPIO.input(11) == GPIO.HIGH:
        if state == States.PLAYER:
            Key2_sound.play()
        
def  button_sound3(channel):
    global state
    if GPIO.input(12) == GPIO.HIGH:
        if state == States.PLAYER:
            Key3_sound.play()
        
def  button_sound4(channel):
    global state
    if GPIO.input(13) == GPIO.HIGH:
        if state == States.PLAYER:
            Key4_sound.play()
        
def  button_sound5(channel):
    global state
    if GPIO.input(15) == GPIO.HIGH:
        if state == States.PLAYER:
            Key5_sound.play()
        
def  button_sound6(channel):
    global state
    if GPIO.input(16) == GPIO.HIGH:
        if state == States.PLAYER:
            Key6_sound.play()
        
def  button_sound7(channel):
    global state
    if GPIO.input(18) == GPIO.HIGH:
        if state == States.PLAYER:
            Key7_sound.play()
        
def  button_sound8(channel):
    global state
    if GPIO.input(22) == GPIO.HIGH:
        if state == States.PLAYER:
            Key8_sound.play()
        
def  button_sound9(channel):
    global state
    if GPIO.input(29) == GPIO.HIGH:
        if state == States.PLAYER:
            Key9_sound.play()
        
def  button_looper1(channel):
    global state
    if GPIO.input(31) == GPIO.HIGH and state == States.PLAYER:
        global loop
        global looper_recorder
        global loop_recording
        global record_loop
        global start
        global myrecording
        global loop_sound
        global looper_seconds1
        global loop_length
        
        if looper_recorder == 0:
            if loop[0] == 0:
                loop[0] = -1
                loop_sound = mixer.Sound('output1.wav')
                loop_sound.play(loop[0])
                GPIO.output(8, GPIO.HIGH)
            elif loop[0] == -1:
                loop[0] = 0
                loop_sound.stop()
                GPIO.output(8, GPIO.LOW)
        elif looper_recorder == 1 and loop_recording == False:
            loop_recording = True
            record_loop = 1
            looper_seconds1[1] = 0
            start = time.time()
            looper_seconds1[0] = time.time()
            print('Recording Looper 1')
            GPIO.output(8, GPIO.HIGH)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
        elif loop_recording == True and record_loop == 1:
            print('Loop1 cut')
            GPIO.output(8, GPIO.LOW)
            loop_length = looper_seconds1[1] - looper_seconds1[0]
            
                    
        
def  button_looper2(channel):
    global state
    if GPIO.input(32) == GPIO.HIGH and state == States.PLAYER:
        global loop
        global looper_recorder
        global loop_recording
        global record_loop
        global start
        global myrecording
        global loop_sound2
        global looper_seconds2
        global loop_length
        
        if looper_recorder == 0:
            if loop[1] == 0:
                loop[1] = -1
                loop_sound2 = mixer.Sound('output2.wav')
                loop_sound2.play(loop[1])
                GPIO.output(10, GPIO.HIGH)
            elif loop[1] == -1:
                loop[1] = 0
                loop_sound2.stop()
                GPIO.output(10, GPIO.LOW)
        elif looper_recorder == 1 and loop_recording == False:
            loop_recording = True
            record_loop = 2
            looper_seconds2[1] = 0
            start = time.time()
            looper_seconds2[0] = time.time()
            print('Recording Looper 2')
            GPIO.output(10, GPIO.HIGH)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
        elif loop_recording == True and record_loop == 2:
            print('Loop2 cut')
            GPIO.output(10, GPIO.LOW)
            loop_length = looper_seconds2[1] - looper_seconds2[0]
                            
                
def  button_looper3(channel):
    global state
    if GPIO.input(33) == GPIO.HIGH and state == States.PLAYER:
        global loop
        global looper_recorder
        global loop_recording
        global record_loop
        global start
        global myrecording
        global loop_sound3
        global looper_seconds3
        global loop_length
        
        if looper_recorder == 0:
            if loop[2] == 0:
                loop[2] = -1
                loop_sound3 = mixer.Sound('output3.wav')
                loop_sound3.play(loop[2])
                GPIO.output(24, GPIO.HIGH)
            elif loop[2] == -1:
                loop[2] = 0
                loop_sound3.stop()
                GPIO.output(24, GPIO.LOW)
        elif looper_recorder == 1 and loop_recording == False:
            loop_recording = True
            record_loop = 3
            looper_seconds3[1] = 0
            start = time.time()
            looper_seconds3[0] = time.time()
            print('Recording Looper 3')
            GPIO.output(24, GPIO.HIGH)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
        elif loop_recording == True and record_loop == 3:
            print('Loop3 cut')
            GPIO.output(24, GPIO.LOW)
            loop_length = looper_seconds3[1] - looper_seconds3[0]
                            
        
def  button_record(channel):
    global state
    global music_recording
    global seconds_rec
    global myrecording
    global start
    global record_loop
    global loop_sound
    global loop_sound2
    global loop_sound3
    global loop
    
    if GPIO.input(35) == GPIO.HIGH and state == States.PLAYER and not music_recording:
        loop[0] = 0
        loop_sound.stop()
        loop[1] = 0
        loop_sound2.stop()
        loop[2] = 0
        loop_sound3.stop()
        GPIO.output(8, GPIO.LOW)
        GPIO.output(10, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        music_recording = True
        record_loop = 4
        start = time.time()
        print('Recording Music')
        GPIO.output(40, GPIO.HIGH)
        myrecording = sd.rec(int(seconds_rec * fs), samplerate=fs, channels=2, dtype='int16')
        
subprocess_name_file = 0

def  button_programming(channel):
    if GPIO.input(36) == GPIO.HIGH:
        global state
        global loop_sound
        global loop_sound2
        global loop_sound3
        global loop
        global stored_songs
        global Key1_sound,Key2_sound,Key3_sound,Key4_sound,Key5_sound,Key6_sound,Key7_sound,Key8_sound,Key9_sound
        global network_connected
        global subprocess_name_file
        
        if state == States.PLAYER:
            state = States.PROGRAMMING
            
            
            loop[0] = 0
            loop_sound.stop()
            loop[1] = 0
            loop_sound2.stop()
            loop[2] = 0
            loop_sound3.stop()
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(8, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)
            print('Programming')
            subprocess_name_file = sp.call(['python3','network_server.py'])
        elif state == States.PROGRAMMING:
            f = open("stored_songs.txt","r")
            stored_songs = []
            for x in f:
                stored_songs.append(x.replace('\n',''))
            Key1_sound = mixer.Sound(stored_songs[0])
            Key2_sound = mixer.Sound(stored_songs[1])
            Key3_sound = mixer.Sound(stored_songs[2])

            Key4_sound = mixer.Sound(stored_songs[3])
            Key5_sound = mixer.Sound(stored_songs[4])
            Key6_sound = mixer.Sound(stored_songs[5])

            Key7_sound = mixer.Sound(stored_songs[6])
            Key8_sound = mixer.Sound(stored_songs[7])
            Key9_sound = mixer.Sound(stored_songs[8])
            state = States.PLAYER
            GPIO.output(26, GPIO.LOW)
            print('Player')
            network_connected = False
            if subprocess_name_file != 0:
                subprocess_name_file.terminate()
                subprocess_name_file = 0
        
def  button_switch(channel):
    if GPIO.input(37) == GPIO.HIGH:
        global looper_recorder
        if looper_recorder == 0 and not music_recording:
            looper_recorder = 1
            GPIO.output(38, GPIO.HIGH)
            print('Record mode')
        elif looper_recorder == 1:
            looper_recorder = 0
            GPIO.output(38, GPIO.LOW)
            print('Loop mode')

def game1():
    running = True
    
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(29,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(31,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(33,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(35,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(36,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setup(40, GPIO.OUT)
    
    GPIO.output(8, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)
    
    
    global state
    global start
    global end
    global seconds
    global seconds_rec
    global myrecording
    global loop_recording
    global music_recording
    global record_loop
    global looper_recorder
    global looper_seconds1
    global looper_seconds2
    global looper_seconds3
    global loop_length
    
    
    GPIO.add_event_detect(7, GPIO.BOTH, callback=button_sound1,bouncetime=50)
    GPIO.add_event_detect(11, GPIO.BOTH, callback=button_sound2,bouncetime=50)
    GPIO.add_event_detect(12, GPIO.BOTH, callback=button_sound3,bouncetime=50)
    GPIO.add_event_detect(13, GPIO.BOTH, callback=button_sound4,bouncetime=50)
    GPIO.add_event_detect(15, GPIO.BOTH, callback=button_sound5,bouncetime=50)
    GPIO.add_event_detect(16, GPIO.BOTH, callback=button_sound6,bouncetime=50)
    GPIO.add_event_detect(18, GPIO.BOTH, callback=button_sound7,bouncetime=50)
    GPIO.add_event_detect(22, GPIO.BOTH, callback=button_sound8,bouncetime=50)
    GPIO.add_event_detect(29, GPIO.BOTH, callback=button_sound9,bouncetime=50)
    GPIO.add_event_detect(31, GPIO.BOTH, callback=button_looper1,bouncetime=50)
    GPIO.add_event_detect(32, GPIO.BOTH, callback=button_looper2,bouncetime=50)
    GPIO.add_event_detect(33, GPIO.BOTH, callback=button_looper3,bouncetime=50)
    GPIO.add_event_detect(35, GPIO.BOTH, callback=button_record,bouncetime=50)
    GPIO.add_event_detect(36, GPIO.BOTH, callback=button_programming,bouncetime=50)
    GPIO.add_event_detect(37, GPIO.BOTH, callback=button_switch,bouncetime=50)

    while running:
        
        if start != 0:
            end = time.time()
        if looper_seconds1[0] != 0:
            looper_seconds1[1] = time.time()
        if looper_seconds2[0] != 0:
            looper_seconds2[1] = time.time()
        if looper_seconds3[0] != 0:
            looper_seconds3[1] = time.time()
        
        if (not music_recording and end-start >= seconds) or (music_recording and end-start >= seconds_rec):
            print(f'Loop {record_loop} Saved')
            write(f'output{record_loop}e.wav', fs, myrecording)  # Save as WAV file
            time.sleep(2)
            ffmpeg_extract_subclip(f'output{record_loop}e.wav', 0, loop_length, targetname=f'output{record_loop}.wav')
            print(f'output{record_loop}.wav written')
            start = 0
            end = 0
            loop_recording = False
            record_loop = 0
            looper_seconds1 = [0,0]
            looper_seconds2 = [0,0]
            looper_seconds3 = [0,0]
            GPIO.output(8, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)
            GPIO.output(40, GPIO.LOW)
            music_recording = False
            loop_length = 3.2
            
    GPIO.cleanup()
       
game1()
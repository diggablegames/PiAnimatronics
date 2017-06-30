#!/usr/bin/env python
#
# Command Line usage:
#   xmas.py <input sequence> <audio file>

import RPi.GPIO as GPIO, time
import sys
import time
import pygame
import random

#This is the array that stores the SPI sequence
set = bytearray(25 * 3)

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = RED
# 7 = GREEN
# 8 = BLUE
logical_map = [0 for i in range(9)]

# Defines the mapping of the GPIO1-8 to the pin on the Pi
pin_map = [0,11,12,13,15,16,18,22,7]

#####################################################################
#####################################################################


# Setup the board
GPIO.setmode(GPIO.BOARD)
for i in range(1,9):
  GPIO.setup(pin_map[i], GPIO.OUT)
time.sleep(2.0);
dev    = "/dev/spidev0.0"
spidev = file(dev,"wb")


# Calculate gamma correction
gamma = bytearray(256)
for i in range(256):
  gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)

# starinit(1)

# Open the setup config file and parse it to determine 
# how GPIO1-8 are mapped to logical 1-8
with open("setup.txt",'r') as f:
  data = f.readlines()
  for i in range(8):
    logical_map[i+1] = int(data[i])

# Open the input sequnce file and read/parse it
with open(sys.argv[1],'r') as f:
  seq_data = f.readlines()
  for i in range(len(seq_data)):
    seq_data[i] = seq_data[i].rstrip()

# Current light states
lights = [False for i in range(8)]

# Load and play the music
pygame.mixer.init()
pygame.mixer.music.load(sys.argv[2])
pygame.mixer.music.play()

# Start sequencing
start_time = int(round(time.time()*1000))
step       = 1 #ignore the header line 

while True :
  next_step = seq_data[step].split(",");
  next_step[1] = next_step[1].rstrip()
  cur_time = int(round(time.time()*1000)) - start_time

  # time to run the command
  if int(next_step[0]) <= cur_time:

    print "Next Step %s" % next_step
    # if the command is Relay 1-8 
    if next_step[1] >= "1" and next_step[1] <= "8":

      # change the pin state
      if next_step[2] == "1":
        GPIO.output(pin_map[logical_map[int(next_step[1])]],True)
      else:
        GPIO.output(pin_map[logical_map[int(next_step[1])]],False)

    # if the END command
    if next_step[1].rstrip() == "END":
      for i in range(1,9):
        GPIO.output(pin_map[logical_map[i]],False)
      break
    step += 1


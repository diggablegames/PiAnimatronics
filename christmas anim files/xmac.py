#!/usr/bin/env python
#
# Command Line usage:
#   sudo python2.7-32 xmac.py
import sys
import time
import pygame

#####################################################################

# time.sleep(2.0);

# Open the input sequnce file and read/parse it
with open("Frosty.TXT") as f:
  seq_data = f.readlines()
  for i in range(len(seq_data)):
    seq_data[i] = seq_data[i].rstrip()

# Start sequencing
start_time = int(round(time.time()*1000))
step = 1 #ignore the header line 

# Load and play the music
pygame.mixer.init()
pygame.mixer.music.load("./Frosty.mp3")
pygame.mixer.music.play()
pygame.mixer.music.pause()

musicstarted = 0

while True :
  next_step = seq_data[step].split(",");
  next_step[1] = next_step[1].rstrip()
  cur_time = int(round(time.time()*1000)) - start_time
  #give the music 5 seconds to start up
  if cur_time >= (5*60) and musicstarted == 0:
    pygame.mixer.music.unpause()
    musicstarted = 1
  	
  # time to run the command
  if int(next_step[0]) <= cur_time:
#     print "Next Step %s" % next_step
    # if the END command
    if next_step[1] == "END":
      break
    elif int(next_step[1]) >= 1 and int(next_step[1])<= 8:
      # change the pin state
      if int(next_step[2]) == 1:
      	print "Closed"
      else:
        print "Open"
    step += 1


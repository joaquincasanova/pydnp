import math
import sys
import numpy as np
import time
import RPi.GPIO as GPIO
import synthesizer
import attenuator

GPIO.setmode(GPIO.BOARD)

global digatt_l
digatt_l=12
global digatt_c
digatt_c=16
global digatt_r
digatt_r=18
global digatt_s
digatt_s=22

global yig_l
yig_l=7
global yig_d
yig_d=11
global yig_e
yig_e=13
global yig_c
yig_c=15

# digital attenuator pins
GPIO.setup(digatt_l, GPIO.OUT)
GPIO.setup(digatt_c, GPIO.OUT)
GPIO.setup(digatt_r, GPIO.OUT)
GPIO.setup(digatt_s, GPIO.OUT)

# yig synthesizer pins
GPIO.setup(yig_l, GPIO.IN)
GPIO.setup(yig_d, GPIO.OUT)
GPIO.setup(yig_e, GPIO.OUT)
GPIO.setup(yig_c, GPIO.OUT)

freq = sys.argv[1] #MHz
attn = sys.argv[2]
resolution = 0.5  

synthesizer.yig_set_freq(freq, resolution)
print " I just set the yig."
attenuator.digatt_set(attn)
print " I just set the digatt."

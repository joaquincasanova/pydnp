import math
import sys
import numpy as np
import time
import RPi.GPIO as GPIO
import synthesizer
import attenuator

freq = float(sys.argv[1]) #MHz
attn = float(sys.argv[2])
resolution = 500000  

synthesizer.yig_set_freq(freq, resolution)
print " I just set the yig."
attenuator.digatt_set(attn)
print " I just set the digatt."

import math
import sys
import numpy as np
import time
import synthesizer
import attenuator
import RPi.GPIO as GPIO

freq = float(sys.argv[1])
attn = float(sys.argv[2])
resolution = 500000  

try:
	synthesizer.yig_set_lock(1)
	print " I just set the yig."
	while  ~synthesizer.yig_check_lock():
		#attenuator.digatt_set(attn)
		#print " I just set the digatt."
		synthesizer.yig_set_freq(freq, resolution)
		print " I just set the yig."

except KeyboardInterrupt:
	print "STOP"

finally:
	GPIO.cleanup()

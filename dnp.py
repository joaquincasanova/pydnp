import math
import sys
import numpy as np
import time
import synthesizer
import attenuator

freq = float(sys.argv[1])
attn = float(sys.argv[2])
resolution = 500000  
for i in range(0, 2000):
	attenuator.digatt_set(attn)
	print " I just set the digatt."
#
#	synthesizer.yig_set_freq(freq, resolution)
#	print " I just set the yig."

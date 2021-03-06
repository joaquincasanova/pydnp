import math
import sys
import numpy as np
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#latch board 18, pin 12, grey
global digatt_l
digatt_l=12
#clock board 23, pin 16, white
global digatt_c
digatt_c=16
#reset board 24, pin 18, purple
global digatt_r
digatt_r=18
#serial(data) board 25, pin 22, yellow
global digatt_s
digatt_s=22
#gnd black
#-5 orange

# digital attenuator pins
GPIO.setup(digatt_l, GPIO.OUT)
GPIO.setup(digatt_c, GPIO.OUT)
GPIO.setup(digatt_r, GPIO.OUT)
GPIO.setup(digatt_s, GPIO.OUT)

def digatt_write(data):
	small_wait=25e-6
	#set everything on the digatt to zero, except reset and serial
	GPIO.output(digatt_l, 0)
	GPIO.output(digatt_c, 0)	
	GPIO.output(digatt_r, 1)
	GPIO.output(digatt_s, 1)
	time.sleep(small_wait)
	#turn on the clock 1
	GPIO.output(digatt_c, 1)
	time.sleep(small_wait)
	#turn off the clock
	#turn off reset
	GPIO.output(digatt_c, 0)
	GPIO.output(digatt_r, 0)
	time.sleep(small_wait)
	#turn on the clock 2
	GPIO.output(digatt_c, 1)
	time.sleep(small_wait)
	#turn off the clock
	#turn on reset
	#two clock cycles
	GPIO.output(digatt_r, 1)
	GPIO.output(digatt_c, 0)
	time.sleep(small_wait)
	#turn on the clock 3
	GPIO.output(digatt_c, 1)	
	time.sleep(small_wait)
	#turn off the clock
	GPIO.output(digatt_c, 0)    
	time.sleep(small_wait)
	#turn on the clock 4
	GPIO.output(digatt_c, 1)	
	time.sleep(small_wait)
	for j in range(0,6): #there are always 6
		#turn off the clock
		#set the data bit
		GPIO.output(digatt_s, data[j])
		GPIO.output(digatt_c, 0)		
		time.sleep(small_wait)
		#turn on the clock 5 6 7 8 9 10
		GPIO.output(digatt_c, 1)
		time.sleep(small_wait)
	#turn off the clock
	#set serial to one
	#latch on	
	GPIO.output(digatt_l, 1)
	GPIO.output(digatt_s, 1)
	GPIO.output(digatt_c, 0)
	time.sleep(small_wait)
	#turn on the clock 11
	GPIO.output(digatt_c, 1)
	time.sleep(small_wait)
	#turn off the clock
	#latch off
	GPIO.output(digatt_l, 0)	
	GPIO.output(digatt_c, 0)
		
def attnround(number): # this will round us to the attenuation "bins"
	#initialize setting to all ones and store the values of the attenuators
	thisatten = np.array([0.5,1,2,4,8,16])
	setting = np.array([1,1,1,1,1,1])
	for j in range(5, -1, -1):
		if number>=thisatten[j]:
			setting[j]=0
			number -= thisatten[j]
			print "Setting the ", thisatten[j], " attenuator to ",setting[j] #low means that attenuator is set
	return setting	

def digatt_set(number):
	setting = attnround(number)
	digatt_write(setting)


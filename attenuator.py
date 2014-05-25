import math
import sys
import numpy as np
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

global digatt_l
digatt_l=12
global digatt_c
digatt_c=16
global digatt_r
digatt_r=18
global digatt_s
digatt_s=22

# digital attenuator pins
GPIO.setup(digatt_l, GPIO.OUT)
GPIO.setup(digatt_c, GPIO.OUT)
GPIO.setup(digatt_r, GPIO.OUT)
GPIO.setup(digatt_s, GPIO.OUT)

def digatt_write(data):
	small_wait=2e-8#1000e-6
	long_wait=2e-8#1000e-6
	# set everything on the digatt to zero, except reset and serial
	GPIO.output(digatt_l, 0)
	GPIO.output(digatt_c, 0)	
	GPIO.output(digatt_r, 1)
	GPIO.output(digatt_s, 1)
	time.sleep(small_wait)
	#	turn on the clock
	GPIO.output(digatt_c, 1)
	time.sleep(small_wait)
	#turn off the clock
	GPIO.output(digatt_c, 0)
	time.sleep(small_wait)
	#turn off reset
	GPIO.output(digatt_r, 0)
	time.sleep(small_wait)
	#turn on the clock
	GPIO.output(digatt_c, 1)
	time.sleep(small_wait)
	#turn on reset
	GPIO.output(digatt_r, 1)
	time.sleep(small_wait)
	#turn off the clock
	GPIO.output(digatt_c, 0)
	time.sleep(small_wait)
	#turn on the clock
	GPIO.output(digatt_c, 1)	
	time.sleep(small_wait)
	#turn off the clock
	GPIO.output(digatt_c, 0)    
	time.sleep(small_wait)
	#turn on the clock
	GPIO.output(digatt_c, 1)	
	time.sleep(small_wait)
	for j in range(0,5): #there are always 6
		#turn off the clock
		GPIO.output(digatt_c, 0)		
		time.sleep(small_wait)
		#set the data bit
		GPIO.output(digatt_s, data[j])
		time.sleep(small_wait)
		#turn on the clock
		GPIO.output(digatt_c, 1)
		time.sleep(small_wait)
	#set serial to zero
	GPIO.output(digatt_s, 0)
	time.sleep(small_wait)
	#latch on
	GPIO.output(digatt_l, 1)
	time.sleep(small_wait)
	#turn on the clock
	GPIO.output(digatt_c, 1)
	time.sleep(small_wait)
	#turn off the clock
	GPIO.output(digatt_c, 0)
	time.sleep(small_wait)
	
def attnround(number): # this will round us to the .5 MHz
    #initialize setting to all ones and store the values of the attenuators
	thisatten[5]=16
	thisatten[4]=8
	thisatten[3]=4
	thisatten[2]=2
	thisatten[1]=1
	thisatten[0]=0.5
	setting[0]=1
	setting[1]=1
	setting[2]=1
	setting[3]=1
	setting[4]=1
	setting[5]=1
	for j in range(5, 0, -1):
		if number>=thisatten[j]:
			setting[j]=0
			number -= thisatten[j]
			print "Setting the ", thisatten[j], " attenuator to ",setting[j] #low means that attenuator is set
	return setting	

def digatt_set(number):
	setting = attnround(number)
	digatt_write(setting)


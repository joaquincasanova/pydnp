import math
import binascii
import sys
import numpy as np
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

global yig_l
yig_l=7
global yig_d
yig_d=15
global yig_e
yig_e=13
global yig_c
yig_c=11

# yig synthesizer pins
GPIO.setup(yig_l, GPIO.IN)
GPIO.setup(yig_d, GPIO.OUT,initial=0)
GPIO.setup(yig_e, GPIO.OUT,initial=1)
GPIO.setup(yig_c, GPIO.OUT,initial=0)

def yig_check_lock():
	time.sleep(500e-3)
        retval = GPIO.input(yig_l)
        return retval

def freqround(number): # this will round us to the .5 MHz
	number /= 1e6
        remainder = number - math.floor(number)
        print "I've determined the remainder to be: ", remainder
        if remainder < .25:
        	remainder = 0.0
        elif (remainder >= .25 and remainder <= .75):
        	remainder = .50
        elif remainder > .75:
        	remainder = 1
        number = round(number,0)    
        print "I just rounded the number to: ", number
        number += remainder    
        number *= 1e6
        print "calculated remainder is ", remainder, "new frequency is: ", number
        return number

def yig_set_lock(lock):
        GPIO.output(yig_c, 0) #clock low
        GPIO.output(yig_d, 0) #clock low
	
	string = 'L'+ str(lock)
	
	print "setting lock ", string
	small_wait = 25e-6
	long_wait = 20e-3+10e-3

        GPIO.output(yig_e, 0) #select low
        GPIO.output(yig_c, 0) #clock low
        GPIO.output(yig_d, 0) #clock low
        time.sleep(small_wait)
        
        for j in range(0,len(string)):
		x = bin(int(binascii.hexlify(string[j]),16))
		x = x[2:10]
		while len(x)<8:
			x = '0' + x
		for whichbit in range(0,8):
			GPIO.output(yig_d,int(x[whichbit]))
			GPIO.output(yig_c, 0)
			time.sleep(small_wait)
			GPIO.output(yig_c, 1)
			time.sleep(small_wait)
			
        GPIO.output(yig_c, 0)
	GPIO.output(yig_d, 0)
	time.sleep(small_wait)
	GPIO.output(yig_e, 1)
	time.sleep(long_wait)
	
def yig_set_freq(frequency, resolution):
        GPIO.output(yig_c, 0) #clock low
        GPIO.output(yig_d, 0) #clock low

        #frequency = freqround(frequency)
	y = str(frequency/1e6)
	while len(y)<8:
		y += '0'
	string = 'F'+ y[0:8]
	
	print "setting frequency ", frequency," yields string ", string
	small_wait = 1e-3#25e-6
	long_wait = 120e-3+frequency*1e-9*10e-3+10e-3

        GPIO.output(yig_e, 0) #select low
        GPIO.output(yig_c, 0) #clock low
        GPIO.output(yig_d, 0) #clock low
        time.sleep(small_wait)
        
        for j in range(0,len(string)):
		x = bin(int(binascii.hexlify(string[j]),16))
		x = x[2:10]
		while len(x)<8:
			x = '0' + x
		for whichbit in range(0,8):
			GPIO.output(yig_d,int(x[whichbit]))
			#print j  ," " , whichbit, " " , x[whichbit]
			GPIO.output(yig_c, 0)
			time.sleep(small_wait)
			GPIO.output(yig_c, 1)
			time.sleep(small_wait)
			
        GPIO.output(yig_c, 0)
	GPIO.output(yig_d, 0)
	time.sleep(small_wait)
	GPIO.output(yig_e, 1)
	time.sleep(long_wait)
	
def yig_set_chan(frequency, resolution):
        frequency = freqround(frequency)
        channel = int(frequency/resolution)
	x = (bin(int(channel)))
	x = x[2:len(x)]
	string = bin(int(binascii.hexlify('C'),16))+x
	string = '0'+string[2:len(string)]
	print "setting frequency ", frequency," yields string ", string," at resolution ", resolution," with channel ", channel
	small_wait = 25e-6
	long_wait = 100e-3+frequency*1e-9*10e-3+10e-3

        GPIO.output(yig_e, 0) #select low
        GPIO.output(yig_c, 0) #clock low
        GPIO.output(yig_d, 0) #clock low
        time.sleep(small_wait)
        
        for j in range(0,len(string)):
		GPIO.output(yig_d,int(string[j]))
		GPIO.output(yig_c, 0)
		time.sleep(small_wait)
		GPIO.output(yig_c, 1)
		time.sleep(small_wait)
			
        GPIO.output(yig_c, 0)
	GPIO.output(yig_d, 0)
	time.sleep(small_wait)
	GPIO.output(yig_e, 1)
	time.sleep(long_wait)

import math
import sys
import numpy as np
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

global yig_l
yig_l=7
global yig_d
yig_d=11
global yig_e
yig_e=13
global yig_c
yig_c=15

# yig synthesizer pins
GPIO.setup(yig_l, GPIO.IN)
GPIO.setup(yig_d, GPIO.OUT)
GPIO.setup(yig_e, GPIO.OUT)
GPIO.setup(yig_c, GPIO.OUT)

def write_yig(string, strlen):
	small_wait = 25e-6
	long_wait = 150e-3
        GPIO.output(yig_e, 1) 
        time.sleep(small_wait)
        GPIO.output(yig_e, 0) #select low
        time.sleep(small_wait)
        
        for j in range(0,strlen):
	        for whichbit in range(7,0,-1):
                	GPIO.output(yig_d,((1<<whichbit) & string[j])>>whichbit)
                        GPIO.output(yig_c, 1)
                        time.sleep(small_wait)
                        GPIO.output(yig_c, 0)
                        time.sleep(small_wait)

        GPIO.output(yig_e, 1) 
        time.sleep(long_wait)
	
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
	
def yig_set_freq(frequency, resolution):
        frequency = freqround(frequency)
        channel = int(frequency/resolution)
	string = 'C'
#	for j in range(0,3):
#		string[4-j] = 0xFF & (channel>>(8*j));
	for j in range(3,0,-1):
		string += str(0xFF & (channel>>(8*j)))
	
	print "setting frequency ", frequency," at resolution ", resolution," with channel ", channel," yields string ", string
	write_yig(string,5)
